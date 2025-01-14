#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a part of bXiv for posting to bsky and stdout
# https://github.com/so-okada/bXiv/

import re
import os
import time
import traceback
from atproto import Client
import pandas as pd
from threading import Thread
from datetime import datetime, timedelta
from ratelimit import limits, sleep_and_retry, rate_limited

from variables import *
import bXiv_format as bXf
import bXiv_daily_feed as bXd


def main(switches, logfiles, captions, aliases, pt_mode):
    starting_time = datetime.utcnow().replace(microsecond=0)
    print("**process started at " + str(starting_time) + " (UTC)")

    client_dict = {}
    update_dict = {}
    entries_dict = {}
    webreplacements_dict = {}
    caption_dict = {}

    newsubmission_mode = {}
    abstract_mode = {}
    crosslist_mode = {}
    quote_replacement_mode = {}
    repost_replacement_mode = {}

    for cat in switches:
        client_dict[cat] = atproto_client(switches[cat])
        update_dict[cat] = sleep_and_retry(rate_limited(post_updates, a_day)(update))
        newsubmission_mode[cat] = int(switches[cat]["newsubmissions"])
        abstract_mode[cat] = int(switches[cat]["abstracts"])
        crosslist_mode[cat] = int(switches[cat]["crosslists"])
        quote_replacement_mode[cat] = int(switches[cat]["quote_replacements"])
        repost_replacement_mode[cat] = int(switches[cat]["repost_replacements"])
        if cat in captions:
            caption_dict[cat] = captions[cat]
        else:
            caption_dict[cat] = ""

    # retrieval/new submissions/abstracts
    threads = []
    for i, cat in enumerate(switches):
        th = Thread(
            name=cat,
            target=newentries,
            args=(
                logfiles,
                aliases,
                cat,
                caption_dict[cat],
                client_dict[cat],
                update_dict[cat],
                entries_dict,
                newsubmission_mode[cat],
                abstract_mode[cat],
                pt_mode,
            ),
        )
        threads.append(th)
        ptext = (
            "starting a thread of "
            + "retrieval/new submissions/abstracts for "
            + th.name
        )
        print(ptext)
        th.start()
        if i != len(switches) - 1:
            ptext = (
                "waiting for a next thread of " + "retrieval/new submissions/abstracts"
            )
            print(ptext)
            time.sleep(main_thread_wait)

    print("joining threads of retrieval/new submissions/abstracts")
    [th.join() for th in threads]

    if not logfiles:
        ending_time = datetime.utcnow().replace(microsecond=0)
        if crosslist_mode[cat]:
            ptext = (
                "No logfiles found. "
                + "bXiv needs logfiles for cross-lists and replacements "
                + "by reposts and unreposts."
            )
            print(ptext)
            ptext = (
                "\n**process ended at "
                + str(ending_time)
                + " (UTC)"
                + "\n**elapsed time from the start: "
                + str(ending_time - starting_time)
            )
            print(ptext)
            return None

    # cross lists
    crosslist_time = datetime.utcnow().replace(microsecond=0)
    ptext = (
        "\n**cross-list process started at "
        + str(crosslist_time)
        + " (UTC)"
        + " \n**elapsed time from the start: "
        + str(crosslist_time - starting_time)
    )
    print(ptext)

    threads = []
    for i, cat in enumerate(switches):
        if entries_dict[cat] and crosslist_mode[cat]:
            crosslist_entries = entries_dict[cat].crosslists
            th = Thread(
                name=cat,
                target=crosslists,
                args=(
                    logfiles,
                    cat,
                    client_dict[cat],
                    update_dict[cat],
                    crosslist_entries,
                    pt_mode,
                ),
            )
            threads.append(th)
            print("start a cross-list thread of " + th.name)
            th.start()
            if i != len(switches) - 1:
                print("waiting for a next cross-list thread")
                time.sleep(main_thread_wait)

    if threads:
        print("joining cross-list threads")
        [th.join() for th in threads]

    # replacements
    replacement_time = datetime.utcnow().replace(microsecond=0)
    ptext = (
        "\n**replacement process started at "
        + str(replacement_time)
        + " (UTC)"
        + "\n**elapsed time from the start: "
        + str(replacement_time - starting_time)
        + "\n**elapsed time from the cross-list start: "
        + str(replacement_time - crosslist_time)
    )
    print(ptext)

    print("\n**quote-replacement starts")
    for i, cat in enumerate(switches):
        if entries_dict[cat]:
            replacement_entries = entries_dict[cat].replacements
            # version check: new sub web pages exclude versions > 5.
            webreplacements_dict[cat] = []
            for each in replacement_entries:
                if not each["version"] == "" and int(each["version"]) > 5:
                    print("version unknown or >5 for " + each["id"])
                    # exclude old arXiv identifiers
                elif not re.match("[a-z|A-Z]", each["id"]):
                    webreplacements_dict[cat].append(each)

    threads = []
    for i, cat in enumerate(switches):
        if webreplacements_dict[cat] and quote_replacement_mode[cat]:
            th = Thread(
                name=cat,
                target=quote_replacement,
                args=(
                    logfiles,
                    cat,
                    client_dict[cat],
                    update_dict[cat],
                    webreplacements_dict[cat],
                    pt_mode,
                ),
            )
            threads.append(th)
            print("start a quote-replacement thread of " + th.name)
            th.start()
            if i != len(switches) - 1:
                print("waiting for a next quote-replacement thread")
                time.sleep(main_thread_wait)

    if threads:
        print("joining quote-replacement threads")
        [th.join() for th in threads]

    print("\n**repost-replacement starts")
    threads = []
    for i, cat in enumerate(switches):
        if webreplacements_dict[cat] and repost_replacement_mode[cat]:
            th = Thread(
                name=cat,
                target=repost_replacement,
                args=(
                    logfiles,
                    cat,
                    client_dict[cat],
                    update_dict[cat],
                    webreplacements_dict[cat],
                    pt_mode,
                ),
            )
            threads.append(th)
            print("start a repost-replacement thread of " + th.name)
            th.start()
            if i != len(switches) - 1:
                print("waiting for a next repost-replacement thread")
                time.sleep(main_thread_wait)

    if threads:
        print("joining repost-replacement threads")
        [th.join() for th in threads]

    ending_time = datetime.utcnow().replace(microsecond=0)
    ptext = (
        "\n**process ended at "
        + str(ending_time)
        + " (UTC)"
        + "\n**elapsed time from the start: "
        + str(ending_time - starting_time)
        + "\n**elapsed time from the cross-list start: "
        + str(ending_time - crosslist_time)
        + "\n**elapsed time from the replacement start: "
        + str(ending_time - replacement_time)
    )
    print(ptext)


# post/repost/unrepost/reply/quote with overall limit
@sleep_and_retry
@limits(calls=overall_bsky_limit_call, period=overall_bsky_limit_period)
def update(
    logfiles,
    cat,
    client,
    total,
    arxiv_id,
    text,
    post_uri,
    post_cid,
    root_uri,
    root_cid,
    parent_uri,
    parent_cid,
    pt_method,
    pt_mode,
):
    result = 0

    if not pt_mode:
        update_print(
            cat,
            arxiv_id,
            text,
            post_uri,
            post_cid,
            root_uri,
            root_cid,
            parent_uri,
            parent_cid,
            pt_method,
            pt_mode,
        )
        return result

    if not client:
        update_print(
            cat,
            arxiv_id,
            "\n**error: client not available:\n\n" + text,
            post_uri,
            post_cid,
            root_uri,
            root_cid,
            parent_uri,
            parent_cid,
            pt_method,
            pt_mode,
        )
        return result

    error_text = (
        "\nthread arXiv category: "
        + cat
        + "\narXiv id: "
        + arxiv_id
        + "\ntext: "
        + text
        + "\nuri: "
        + atproto_uri_to_url(post_uri)
        + "\n"
    )

    if pt_method == "post":
        try:
            result = client.send_post(text=text, facets=generate_facets_for_urls(text))
            update_print(
                cat,
                arxiv_id,
                text,
                result.uri,
                result.cid,
                root_uri,
                root_cid,
                parent_uri,
                parent_cid,
                pt_method,
                pt_mode,
            )
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = "\n**error to post**" + "\nutc: " + str(time_now) + error_text
            print(error_text)
            traceback.print_exc()
    elif pt_method == "repost":
        try:
            result = client.repost(post_uri, post_cid)
            update_print(
                cat,
                arxiv_id,
                text,
                result.uri,
                result.cid,
                "",
                "",
                "",
                "",
                pt_method,
                pt_mode,
            )
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = (
                "\n**error to repost**" + "\nutc: " + str(time_now) + error_text
            )
            print(error_text)
            traceback.print_exc()
    elif pt_method == "unrepost":
        try:
            result = client.delete_repost(result.uri)
            update_print(
                cat,
                arxiv_id,
                text,
                result.uri,
                result.cid,
                "",
                "",
                "",
                "",
                pt_method,
                pt_mode,
            )
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = (
                "\n**error to unrepost**" + "\nutc: " + str(time_now) + error_text
            )
            print(error_text)
            traceback.print_exc()
    elif pt_method == "reply":
        try:
            reply_ref = {
                "root": {"uri": root_uri, "cid": root_cid},
                "parent": {"uri": parent_uri, "cid": parent_cid},
            }
            result = client.send_post(
                text=text, reply_to=reply_ref, facets=generate_facets_for_urls(text)
            )
            update_print(
                cat,
                arxiv_id,
                text,
                result.uri,
                result.cid,
                root_uri,
                root_cid,
                parent_uri,
                parent_cid,
                pt_method,
                pt_mode,
            )
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = "\n**error to reply**" + "\nutc: " + str(time_now) + error_text
            print(error_text)
            traceback.print_exc()
    elif pt_method == "quote":
        try:
            result = client.send_post(
                text=text,
                facets=generate_facets_for_urls(text),
                embed={
                    "$type": "app.bsky.embed.record",
                    "record": {"uri": result.uri, "cid": result.cid},
                },
            )
            update_print(
                cat,
                arxiv_id,
                text,
                result.uri,
                result.cid,
                root_uri,
                root_cid,
                parent_uri,
                parent_cid,
                pt_method,
                pt_mode,
            )
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = "\n**error to quote**" + "\nutc: " + str(time_now) + error_text
            print(error_text)
            traceback.print_exc()

    update_log(logfiles, cat, total, arxiv_id, result, pt_method, pt_mode)
    time.sleep(bsky_sleep)
    return result


# update stdout text format
def update_print(
    cat,
    arxiv_id,
    text,
    result_uri,
    result_cid,
    root_uri,
    root_cid,
    parent_uri,
    parent_cid,
    pt_method,
    pt_mode,
):
    time_now = datetime.utcnow().replace(microsecond=0)
    ptext = (
        "\nutc: "
        + str(time_now)
        + "\nthread arXiv category: "
        + cat
        + "\narXiv id: "
        + arxiv_id
        + "\nurl:"
        + atproto_uri_to_url(root_uri)
        + "\npost method: "
        + pt_method
        + "\npost mode: "
        + str(pt_mode)
        + "\nurl: "
        + atproto_uri_to_url(result_uri)
        + "\ntext: "
        + text
        + "\n"
    )
    print(ptext)


# logging for update
def update_log(logfiles, cat, total, arxiv_id, result, pt_method, pt_mode):
    if not result or not pt_mode or not logfiles:
        return None

    time_now = datetime.utcnow().replace(microsecond=0)

    if not arxiv_id and pt_method == "post":
        filename = logfiles[cat]["post_summary_log"]
        log_text = [
            [time_now, total, logfiles[cat]["username"], result.uri, result.cid]
        ]
        df = pd.DataFrame(log_text, columns=["utc", "total", "username", "uri", "cid"])
    else:
        log_text = [
            [time_now, arxiv_id, logfiles[cat]["username"], result.uri, result.cid]
        ]
        df = pd.DataFrame(
            log_text, columns=["utc", "arxiv_id", "username", "uri", "cid"]
        )
        filename = logfiles[cat][pt_method + "_log"]

    if not filename:
        return None
    if os.path.exists(filename):
        df.to_csv(filename, mode="a", header=None, index=None)
    else:
        df.to_csv(filename, mode="w", index=None)


# retrieval of daily entries, and
# calling a sub process for new submissions and abstracts
def newentries(
    logfiles,
    aliases,
    cat,
    caption,
    client,
    update_limited,
    entries_dict,
    newsubmission_mode,
    abstract_mode,
    pt_mode,
):
    print("getting daily entries for " + cat)
    try:
        entries_dict[cat] = bXd.daily_entries(cat, aliases)
    except Exception:
        entries_dict[cat] = {}
        print("\n**error for retrieval**\nthread arXiv category:" + cat)
        traceback.print_exc()
        if not check_log_dates(cat, "post_log", logfiles) and not check_log_dates(
            cat, "post_summary_log", logfiles
        ):
            # daily entries retrieval failed and
            # no posts for today have been made.
            print("check_log_dates returns False for " + cat)
            time_now = datetime.utcnow().replace(microsecond=0)
            ptext = intro(time_now, 0, cat, caption)
            update_limited(
                logfiles,
                cat,
                client,
                "0",
                "",
                ptext,
                "",
                "",
                "",
                "",
                "",
                "",
                "post",
                pt_mode,
            )

    # new submissions and abstracts
    if newsubmission_mode:
        print("new submissions for " + cat)
        if entries_dict[cat]:
            newsub_entries = bXf.format(entries_dict[cat].newsubmissions)
            if not check_log_dates(cat, "post_log", logfiles) and not check_log_dates(
                cat, "post_summary_log", logfiles
            ):
                newsubmissions(
                    logfiles,
                    cat,
                    caption,
                    client,
                    update_limited,
                    newsub_entries,
                    abstract_mode,
                    pt_mode,
                )
            else:
                print(cat + " already posted for today")


# an introductory text of each category
# an example: [2020-08-01 (UTC),  4 new articles found for mathCV]
def intro(given_time, num, cat, caption):
    ptext = "[" + given_time.strftime("%Y-%m-%d %a") + " (UTC), "
    # On the variable num, arXiv_feed_parser gives new
    # submissions whose primary subjects are the given category.
    if num == 0:
        ptext = ptext + "no new articles found for "
    elif num == 1:
        ptext = ptext + str(num) + " new article found for "
    else:
        ptext = ptext + str(num) + " new articles found for "
    ptext = ptext + re.sub(r"\.", "", cat)

    if caption:
        ptext = ptext + " " + caption

    if num > post_updates - 1:
        ptext = (
            ptext
            + ", but only first "
            + str(post_updates - 1)
            + " articles to post."
            + "]"
        )
    else:
        ptext = ptext + "]"
    return ptext


# new submissions by posts and abstracts by replies
def newsubmissions(
    logfiles, cat, caption, client, update_limited, entries, abstract_mode, pt_mode
):
    time_now = datetime.utcnow().replace(microsecond=0)
    ptext = intro(time_now, len(entries), cat, caption)
    update_limited(
        logfiles,
        cat,
        client,
        str(len(entries)),
        "",
        ptext,
        "",
        "",
        "",
        "",
        "",
        "",
        "post",
        pt_mode,
    )
    post_counter = 1

    for each in entries:
        if post_counter < post_updates:
            arxiv_id = each["id"]
            article_text = (
                each["authors"]
                + ": "
                + each["title"]
                + " "
                + each["abs_url"]
                + " "
                + each["pdf_url"]
                + " "
                + each["html_url"]
            )
            result = update_limited(
                logfiles,
                cat,
                client,
                "",
                arxiv_id,
                article_text,
                "",
                "",
                "",
                "",
                "",
                "",
                "post",
                pt_mode,
            )
            post_counter += 1

            if abstract_mode and result:
                sep_abst = each["separated_abstract"]
                for i, partial_abst in enumerate(sep_abst):
                    if i == 0:
                        print(result.uri, result.cid)
                        abst_result = update_limited(
                            logfiles,
                            cat,
                            client,
                            "",
                            arxiv_id,
                            partial_abst,
                            "",
                            "",
                            result.uri,
                            result.cid,
                            result.uri,
                            result.cid,
                            "reply",
                            pt_mode,
                        )
                    else:
                        abst_result = update_limited(
                            logfiles,
                            cat,
                            client,
                            "",
                            arxiv_id,
                            partial_abst,
                            "",
                            "",
                            result.uri,
                            result.cid,
                            abst_result.uri,
                            abst_result.cid,
                            "reply",
                            pt_mode,
                        )
                    if abst_result == 0:
                        break


# crosslists by reposts
def crosslists(logfiles, cat, client, update_limited, entries, pt_mode):
    # if-clause to avoid duplication errors
    # when bXiv runs twice with cross-lists in a day.

    repost_filename = logfiles[cat]["repost_log"]
    time_now = datetime.utcnow().replace(microsecond=0)
    error_text = "\nutc: " + str(time_now) + "\nrepost_filename: " + repost_filename
    if os.path.exists(repost_filename):
        try:
            drepost_f = pd.read_csv(repost_filename, dtype=object)
        except Exception:
            error_text = "\n**error for pd.read_csv**" + error_text
            print(error_text)
            traceback.print_exc()
            return False
        for repost_index, repost_row in drepost_f.iterrows():
            try:
                log_time = repost_row["utc"]
            except Exception:
                error_text = "\n**error for row['utc']**" + error_text
                print(error_text)
                traceback.print_exc()
            log_time = datetime.fromisoformat(log_time)
            if check_dates(time_now, log_time):
                ptext = "already reposted today for cross-lists: " + cat
                print(ptext)
                return None

    for each in entries:
        arxiv_id = each["id"]
        subject = each["primary_subject"]
        print(cat, " ", arxiv_id, " ", subject)

        if subject == cat:
            # This case is not listed in new submission web pages,
            # but was in rss feeds (2020-06-14).
            ptext = "skip: cross-list of an article in its own category \n"
            print(ptext)
            continue
        if subject not in logfiles.keys():
            print("not in logfiles: " + subject)
            continue

        post_filename = logfiles[subject]["post_log"]
        # skip without post_log
        if not os.path.exists(post_filename):
            print("no post log file for " + subject)
            continue

        # open post_log file
        try:
            post_df = pd.read_csv(post_filename, dtype=object)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = "\nutc: " + str(time_now) + "\npost_filename: " + post_filename
            error_text = "\n**error for pd.read_csv**" + error_text
            print(error_text)
            traceback.print_exc()
            return False

        time_now = datetime.utcnow().replace(microsecond=0)
        for post_index, post_row in post_df.iterrows():
            if arxiv_id == post_row["arxiv_id"]:
                post_uri = post_row["uri"]
                post_cid = post_row["cid"]
                post_time = datetime.fromisoformat(post_row["utc"])
                # if-clause to avoid double reposts
                if not check_dates(time_now, post_time):
                    update_limited(
                        logfiles,
                        cat,
                        client,
                        "",
                        arxiv_id,
                        "",
                        post_uri,
                        post_cid,
                        "",
                        "",
                        "",
                        "",
                        "unrepost",
                        pt_mode,
                    )
                update_limited(
                    logfiles,
                    cat,
                    client,
                    "",
                    arxiv_id,
                    "",
                    post_uri,
                    post_cid,
                    "",
                    "",
                    "",
                    "",
                    "repost",
                    pt_mode,
                )


# replacements by quotes and reposts
def quote_replacement(logfiles, cat, client, update_limited, entries, pt_mode):

    post_filename = logfiles[cat]["post_log"]
    # skip without post_log
    if not os.path.exists(post_filename):
        print("no post log file for " + cat)
        return None

    # open post_log file
    try:
        post_df = pd.read_csv(post_filename, dtype=object)
    except Exception:
        time_now = datetime.utcnow().replace(microsecond=0)
        error_text = "\nutc: " + str(time_now) + "\npost_filename: " + post_filename
        error_text = "\n**error for pd.read_csv**" + error_text
        print(error_text)
        traceback.print_exc()
        return False

    quote_filename = logfiles[cat]["quote_log"]
    # skip without quote_log with posting mode
    if not os.path.exists(post_filename) and pt_mode:
        print("posting mode without quote log file for " + cat)
        return None

    # open quote_log file
    try:
        quote_df = pd.read_csv(quote_filename, dtype=object)
    except Exception:
        time_now = datetime.utcnow().replace(microsecond=0)
        error_text = "\nutc: " + str(time_now) + "\nquote_filename: " + quote_filename
        error_text = "\n**error for pd.read_csv**" + error_text
        print(error_text)
        traceback.print_exc()
        return False

    # if-clause to avoid duplication errors
    time_now = datetime.utcnow().replace(microsecond=0)
    if pt_mode and any(
        check_dates(time_now, datetime.fromisoformat(t)) for t in quote_df.utc.values
    ):
        print("already made quote-replacements today for " + cat)
        return None

    entries_to_quote = []
    for each in entries:
        arxiv_id = each["id"]
        if each["primary_subject"] == cat and not any(
            arxiv_id == post_row["arxiv_id"]
            for post_index, post_row in quote_df.iterrows()
        ):
            entries_to_quote.append(each)

    for each in entries_to_quote:
        arxiv_id = each["id"]
        username = logfiles[cat]["username"]
        for post_index, post_row in post_df.iterrows():
            if arxiv_id == post_row["arxiv_id"]:
                post_uri = post_row["uri"]
                post_cid = post_row["cid"]
                ptext = (
                    "This https://arxiv.org/abs/"
                    + arxiv_id
                    + " has been replaced. "
                    + tools(arxiv_id)
                )
                ptext = ptext + atproto_uri_to_url(post_uri)
                update_limited(
                    logfiles,
                    cat,
                    client,
                    "",
                    arxiv_id,
                    ptext,
                    post_uri,
                    post_cid,
                    "",
                    "",
                    "",
                    "",
                    "quote",
                    pt_mode,
                )


def repost_replacement(logfiles, cat, client, update_limited, entries, pt_mode):
    for each in entries:
        arxiv_id = each["id"]
        subject = each["primary_subject"]

        if subject not in logfiles.keys():
            print("No quote log for " + subject)
            continue
        quote_filename = logfiles[subject]["quote_log"]

        # skip without quote_log
        if not os.path.exists(quote_filename):
            print("no quote log file for " + subject)
            continue

        # open quote_log
        try:
            quote_df = pd.read_csv(quote_filename, dtype=object)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = (
                "\nutc: " + str(time_now) + "\nquote_filename: " + quote_filename
            )
            error_text = "\n**error for pd.read_csv**" + error_text
            print(error_text)
            traceback.print_exc()
            return False

        # unrepost and repost
        for post_index, post_row in quote_df.iterrows():
            # check if arxiv_id is in quote_log.
            if arxiv_id == post_row["arxiv_id"]:
                log_time = post_row["utc"]
                log_time = datetime.fromisoformat(log_time)
                time_now = datetime.utcnow().replace(microsecond=0)
                if cat != subject or not check_dates(time_now, log_time):
                    post_uri = post_row["uri"]
                    post_cid = post_row["cid"]
                    update_limited(
                        logfiles,
                        cat,
                        client,
                        "",
                        arxiv_id,
                        "",
                        post_uri,
                        post_cid,
                        "",
                        "",
                        "",
                        "",
                        "unrepost",
                        pt_mode,
                    )
                    update_limited(
                        logfiles,
                        cat,
                        client,
                        "",
                        arxiv_id,
                        "",
                        post_uri,
                        post_cid,
                        "",
                        "",
                        "",
                        "",
                        "repost",
                        pt_mode,
                    )


# true if this finds a today's post.
def check_log_dates(cat, logname, logfiles):
    if not logfiles:
        print("no log files")
        return False

    filename = logfiles[cat][logname]
    if not os.path.exists(filename):
        print("log file does not exists: " + filename)
        return False

    time_now = datetime.utcnow().replace(microsecond=0)
    try:
        df = pd.read_csv(filename, dtype=object)
    except Exception:
        error_text = "\nutc: " + str(time_now) + "\nfilename: " + filename
        error_text = "\n**error for pd.read_csv**" + error_text
        print(error_text)
        traceback.print_exc()
        return False
    for index, row in df.iterrows():
        log_time = datetime.fromisoformat(row["utc"])
        if (
            check_dates(log_time, time_now)
            and row["username"] == logfiles[cat]["username"]
        ):
            return True
    return False


# true if dates of input times are the same during weekdays
# extended match during weekends
def check_dates(time1, time2):
    time1w = time1.weekday()
    time2w = time2.weekday()
    if time1w >= 5:
        time1 = time1 - timedelta(time1w - 4)
    if time2w >= 5:
        time2 = time2 - timedelta(time2w - 4)
    if time1.date() == time2.date():
        return True
    else:
        return False


def atproto_client(keys):
    client = Client()
    try:
        client.login(keys["username"], keys["password"])
    except Exception:
        print("\n**error: " + keys["username"] + " failed to login.")
        traceback.print_exc()
        return None
    return client


def atproto_uri_to_url(uri):
    if not uri:
        return ""
    path = uri[5:]
    parts = path.split("/", 1)
    did = parts[0]
    resource = parts[1]
    post_id = resource.split("/")[-1]
    return f"https://bsky.app/profile/{did}/post/{post_id}"


def generate_facets_for_urls(text):
    url_pattern = re.compile(r"https?://[^\s\[\]]+")
    facets = []

    for match in url_pattern.finditer(text):
        start, end = match.start(), match.end()
        url = match.group()

        facets.append(
            {
                "index": {
                    "byteStart": start,
                    "byteEnd": end,
                },
                "features": [
                    {
                        "$type": "app.bsky.richtext.facet#link",
                        "uri": url,
                    }
                ],
            }
        )
    return facets


def tools(arxiv_id):
    google_url = "https://scholar.google.com/scholar?q=arXiv%3A" + arxiv_id
    return "Link: " + google_url
