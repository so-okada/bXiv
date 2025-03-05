# arXiv API rate limits  2020-06-16
# no more than 1 request every 3 seconds, a single connection at a time.
# https://arxiv.org/help/api/tou
arxiv_call_limit = 1
arxiv_call_period = 5

arxiv_max_trial = 2
arxiv_call_sleep = 5 * 60
main_thread_wait = 10

# max post length is 300
# bsky url length is 22
# 2024-12
max_len = 290
url_len = 22

# posts for new submissions:
url_margin = 2
urls_len = (url_len + url_margin) * 3
min_len_authors = 90
min_len_title = 128
newsub_spacer = 1
margin = 10

# abstract tag for a counter and url
abst_tag = 11 + (url_len + url_margin) + 1

# rate limit for each categor
# https://docs.bsky.app/docs/advanced-guides/rate-limits
a_day = 24 * 60 * 60
post_updates = 10000

# limits independent to specific categories
bsky_createaccts_sleep = 3
bsky_sleep = 0.5
overall_bsky_limit_call = 5
overall_bsky_limit_period = 1
