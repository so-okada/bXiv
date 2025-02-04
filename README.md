# Application Info

bXiv delivers arXiv daily new submissions, abstracts, cross-lists, and
replacements by bluesky posts, repliles, and reposts. We use python3
scripts with atproto. bXiv is not affiliated with arXiv.


## Setup

* Install atproto, pandas, ratelimit, atproto, nameparser, feedparser, and beautifulsoup4. 

	```
	% pip3 install atproto pandas ratelimit atproto nameparser feedparser beautifulsoup4
	```

* Let bXiv.py be executable.
 
	 ```
	 % chmod +x bXiv.py
	 ```

*  Put the following python scripts in the same directory.

	- bXiv.py
	- bXiv_post.py 	
	- bXiv_format.py
	- bXiv_daily_feed.py 	
	- arXiv_feed_parser.py
	- variables.py


* Configure switches.json, logfiles.json, and aliases.json in the
  tests directory for your settings.

	- accesses.json specifies twitter access keys and whether to use
	new submissions/abstracts/cross-lists/replacements by bXiv.

    - logfiles.json indicates log file locations for post summaries,
	posts, reposts, unreposts, and replies.  You can check their
	formats by mathACb_post_summaries.csv, mathACb_posts.csv,
	mathACb_reposts.csv, mathACb_unreposts.csv, mathACb_replies.csv,
	and mathACb_quotes.csv in the tests/logfiles director.  bXiv needs
	a post log file for cross-lists and replacements.  Other log files
	are useful to avoid duplication errors of posts and reposts.
		
	- aliases.json tells bXiv aliases of arXiv category names.  For
    example, math.IT is an alias of cs.IT. Without this file, bXiv of
    rss feeds returns no new submissions, when you take the category
    name math.IT.  If provided, bXiv replaces category names by their
    aliases for new submissions, cross-lists, and replacements.
	
* Configure variables.py for your settings. 

   - variables.py assigns format parameters for bXiv posts 
   and access frequencies for arXiv and twitter.

## Notes

* arXiv_feed_parser.py is a simple arXiv feed parser for bXiv. We
  use this via bXiv_daily_feed.py to regularly obtain data.  
	
* Outputs of bXiv can differ from arXiv new submission web
  pages. First, this can be due to bugs in my scripts or
  connection errors.
  Second, items of arXiv rss feeds are not
  necessarily the same as those of arXiv new submission web
  pages (see
	https://mastoxiv.page/@vela/109829294232368163).  Third,
  arXiv_feed_parser for an arXiv category C gives new
  submissions whose primary subjects are the category C.
  Then, bXiv for the category C counts and posts a new
  paper whose principal subject matches the category C.

	- For example, let us assume that there is no new paper whose
	principal subject matches the category C, but there is a new paper
	P whose non-principal subject matches the category C. Then, the
	arXiv new submission web page of the category C lists the paper P
	as a new submission of the category C, not as a cross-list.
	However, bXiv keeps considering the paper P as a cross-list for
	the category C.  Then, the output of bXiv for the category C
	differs from the arXiv new submission web page of the category C.

	- So, bXiv puts one single post of a new paper across bots in the
	access keys. If configured, bXiv tries to repost and quote for
	cross-lists and replacements from bots in the access keys.


* On the use of metadata of arXiv articles, the web page
   [Terms of Use for arXiv APIs](https://arxiv.org/help/api/tou)
   says that "You are free to use descriptive metadata about
   arXiv e-prints under the terms of the Creative Commons Universal
   (CC0 1.0) Public Domain Declaration." and "Descriptive metadata
   includes information for discovery and identification purposes, and
   includes fields such as title, abstract, authors, identifiers, and
   classification terms."


## Usage

```
% ./bXiv.py -h
usage: bXiv.py [-h] --switches_keys SWITCHES_KEYS
                [--logfiles LOGFILES] [--aliases ALIASES]
                [--captions CAPTIONS] [--mode {0,1}]

arXiv daily new submissions by posts, abstracts by
replies, cross-lists by reposts, and replacements by
quotes and reposts.

optional arguments:
  -h, --help            show this help message and exit
  --switches_keys SWITCHES_KEYS, -s SWITCHES_KEYS
                        output switches and api keys in
                        json
  --logfiles LOGFILES, -l LOGFILES
                        log file names in json
  --aliases ALIASES, -a ALIASES
                        aliases of arXiv categories in
                        json
  --captions CAPTIONS, -c CAPTIONS
                        captions of arXiv categories in
                        json
  --mode {0,1}, -m {0,1}
                        1 for twitter and 0 for stdout
                        only
```

## Sample stdouts


* New submissions for math.AC and math.AG with no log files:

	```
	% ./bXiv.py -s tests/switches.json -m 1
	**process started at xxxx-xx-xx xx:xx:xx (UTC)
	starting a thread of retrieval/new submissions/abstracts for math.AC
	getting daily entries for math.AC
	waiting for a next thread of retrieval/new submissions/abstracts
	new submissions for math.AC
	no log files
	no log files

	utc: xxxx-xx-xx xx:xx:xx 
	thread arXiv category: math.AC
	arXiv id: 
	url: https://bsky.app/profile/
	post method: post
	post mode: 1
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxxxxxx
	text: [xxxx-xx-xx Sun (UTC), 2 new articles found for mathAC]

	starting a thread of retrieval/new submissions/abstracts for math.AG
	getting daily entries for math.AG
	joining threads of retrieval/new submissions/abstracts

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AC
	arXiv id: xxxx.xxxxx
	url: https://bsky.app/profile/
	post method: post
	post mode: 1
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxxxxxx
	text: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	....

	**process ended at xxxx-xx-xx xx:xx:xx (UTC)
	**elapsed time from the start: xx:xx:xx
	```

* New submissions, abstracts, cross-lists and replacements (if any) 
  for math.AC and math.AG:

	```
	% ./bXiv.py -s tests/switches.json -l tests/logfiles.json -a tests/aliases.json -c tests/captions.json -m 1
	**process started at xxxx-xx-xx xx:xx:xx (UTC)
	starting a thread of retrieval/new submissions/abstracts for math.AC
	getting daily entries for math.AC
	waiting for a next thread of retrieval/new submissions/abstracts
	new submissions for math.AC

	utc: xxxx-xx-xx xx:xx:xx 
	thread arXiv category: math.AC
	arXiv id: 
	url: https://bsky.app/profile/
	post method: post
	post mode: 1
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxxxxxxx
	text: [xxxx-xx-xx Sun (UTC), 2 new articles found for mathAC Commutative Algebra]

	starting a thread of retrieval/new submissions/abstracts for math.AG
	getting daily entries for math.AG
	joining threads of retrieval/new submissions/abstracts

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AC
	arXiv id: xx07.xxxxxx
	url: https://bsky.app/profile/
	post method: post
	post mode: 1
	url: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	new submissions for math.AG

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AG
	arXiv id: 
	url: https://bsky.app/profile/
	post method: post
	post mode: 1
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxxxxxxxxxx
	text: [xxxx-xx-xx Sun (UTC), 4 new articles found for mathAG Algebraic Geometry]

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AC
	arXiv id: xx07.xxxxxx
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxx
	post method: reply
	post mode: 1
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxx
	text:  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx [1/4 of https://arxiv.org/abs/xx07.xxxxxv1]

	.....
	
	**crosslist process started at xxxx-xx-xx xx:xx:xx (UTC) 
	**elapsed time from the start: xx:xx:xx
	start a crosslist thread of math.AC
	waiting for a next crosslist thread
	start a crosslist thread of math.AG
	joining crosslist threads

	**replacement process started at xxxx-xx-xx xx:xx:xx (UTC)
	**elapsed time from the start: xx:xx:xx
	**elapsed time from the cross-list start: xx:xx:xx
	quote-replacement starts
	start a quote-replacement thread of math.AC
	waiting for a next quote-replacement thread
	start a quote-replacement thread of math.AG
	
	.....
	
	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AG
	arXiv id: xx10.xxxx
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxx
	post method: quote
	post mode: 0
	url: https://bsky.app/profile/
	text: This https://arxiv.org/abs/xxxx.xxxx has been replaced.....

	.....

	repost-replacement starts
	start a repost-replacement thread of math.AC
	waiting for a next quote-replacement thread
	start a repost-replacement thread of math.AG
	
	utc: xxxx-xx-xx xx:xx:xx 
	thread arXiv category: math.AG
	arXiv id: xx00.xxxxx
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxx
	post method: unrepost
	post mode: 1
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxx
	text: 

	utc: xxxx-xx-xx xx:xx:xx 
	thread arXiv category: math.AG
	arXiv id: xx00.xxxxx
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxx
	post method: repost
	post mode: 1
	url: https://bsky.app/profile/xxxxxxxxxxxxxxxxxxxx
	text: 

	.....

	**process ended at xxxx-xx-xx xx:xx:xx (UTC)
	**elapsed time from the start: xx:xx:xx
	**elapsed time from the cross-list start: xx:xx:xx
	**elapsed time from the replacement start: xx:xx:xx
	```
* Without the option ```-c tests/captions.json```above, you get

	```
	text: [xxxx-xx-xx Sun (UTC), 4 new articles found for mathAG]
	```

	instead of

	```
	text: [xxxx-xx-xx Sun (UTC), 4 new articles found for mathAG Algebraic Geometry]
	```


## Versions

* 0.0.1

  * 2025-01-12, initial release.
  
* 0.0.2

  * 2025-02-04, minor updates.
	
## List of Bots

* [https://bsky.app/profile/mathac-bot.bsky.social](https://bsky.app/profile/mathac-bot.bsky.social): 
  Commutative Algebra
* [https://bsky.app/profile/mathag-bot.bsky.social](https://bsky.app/profile/mathag-bot.bsky.social):
  Algebraic Geometry
* [https://bsky.app/profile/mathap-bot.bsky.social](https://bsky.app/profile/mathap-bot.bsky.social):
  Analysis of PDEs 
* [https://bsky.app/profile/mathat-bot.bsky.social](https://bsky.app/profile/mathat-bot.bsky.social):
Algebraic Topology 
* [https://bsky.app/profile/mathca-bot.bsky.social](https://bsky.app/profile/mathca-bot.bsky.social):
Classical Analysis and ODEs
* [https://bsky.app/profile/mathco-bot.bsky.social](https://bsky.app/profile/mathco-bot.bsky.social):
Combinatorics 
* [https://bsky.app/profile/mathct-bot.bsky.social](https://bsky.app/profile/mathct-bot.bsky.social):
Category Theory 
* [https://bsky.app/profile/mathcv-bot.bsky.social](https://bsky.app/profile/mathcv-bot.bsky.social):
Complex Variables 
* [https://bsky.app/profile/mathdg-bot.bsky.social](https://bsky.app/profile/mathdg-bot.bsky.social):
Differential Geometry 
* [https://bsky.app/profile/mathds-bot.bsky.social](https://bsky.app/profile/mathds-bot.bsky.social):
Dynamical Systems 
* [https://bsky.app/profile/mathfa-bot.bsky.social](https://bsky.app/profile/mathfa-bot.bsky.social):
Functional Analysis 
* [https://bsky.app/profile/mathgm-bot.bsky.social](https://bsky.app/profile/mathgm-bot.bsky.social):
General Mathematics 
* [https://bsky.app/profile/mathgn-bot.bsky.social](https://bsky.app/profile/mathgn-bot.bsky.social):
General Topology 
* [https://bsky.app/profile/mathgr-bot.bsky.social](https://bsky.app/profile/mathgr-bot.bsky.social):
Group Theory 
* [https://bsky.app/profile/mathgt-bot.bsky.social](https://bsky.app/profile/mathgt-bot.bsky.social):
Geometric Topology 
* [https://bsky.app/profile/mathho-bot.bsky.social](https://bsky.app/profile/mathho-bot.bsky.social):
History and Overview 
* [https://bsky.app/profile/mathit-bot.bsky.social](https://bsky.app/profile/mathit-bot.bsky.social):
Information Theory 
* [https://bsky.app/profile/mathkt-bot.bsky.social](https://bsky.app/profile/mathkt-bot.bsky.social):
K-Theory and Homology 
* [https://bsky.app/profile/mathlo-bot.bsky.social](https://bsky.app/profile/mathlo-bot.bsky.social):
Logic 
* [https://bsky.app/profile/mathmg-bot.bsky.social](https://bsky.app/profile/mathmg-bot.bsky.social):
Metric Geometry 
* [https://bsky.app/profile/mathmp-bot.bsky.social](https://bsky.app/profile/mathmp-bot.bsky.social):
Mathematical Physics 
* [https://bsky.app/profile/mathna-bot.bsky.social](https://bsky.app/profile/mathna-bot.bsky.social):
Numerical Analysis 
* [https://bsky.app/profile/mathnt-bot.bsky.social](https://bsky.app/profile/mathnt-bot.bsky.social):
Number Theory 
* [https://bsky.app/profile/mathoa-bot.bsky.social](https://bsky.app/profile/mathoa-bot.bsky.social):
Operator Algebras 
* [https://bsky.app/profile/mathoc-bot.bsky.social](https://bsky.app/profile/mathoc-bot.bsky.social):
Optimization and Control 
* [https://bsky.app/profile/mathpr-bot.bsky.social](https://bsky.app/profile/mathpr-bot.bsky.social):
Probability
* [https://bsky.app/profile/mathqa-bot.bsky.social](https://bsky.app/profile/mathqa-bot.bsky.social):
Quantum Algebra 
* [https://bsky.app/profile/mathra-bot.bsky.social](https://bsky.app/profile/mathra-bot.bsky.social):
Probability 
* [https://bsky.app/profile/mathrt-bot.bsky.social](https://bsky.app/profile/mathrt-bot.bsky.social):
Representation Theory 
* [https://bsky.app/profile/mathsg-bot.bsky.social](https://bsky.app/profile/mathsg-bot.bsky.social):
Symplectic Geometry 
* [https://bsky.app/profile/mathsp-bot.bsky.social](https://bsky.app/profile/mathsp-bot.bsky.social):
Spectral Theory 
* [https://bsky.app/profile/mathst-bot.bsky.social](https://bsky.app/profile/mathst-bot.bsky.social):
 Statistics Theory 

## Author
So Okada, so.okada@gmail.com, https://so-okada.github.io/

## Motivation
This is an open-science practice (see
https://github.com/so-okada/twXiv#motivation).  Since 2013-04, the
author has been running twitter bots for all arXiv math categories. 
Since 2023-01, the author has been running mastodon bots for
all arXiv categories 
with [toXiv](https://github.com/so-okada/toXiv). Since 2025-01, the author has been
running the blusky bots for all arXiv math categories 
with [bXiv](https://github.com/so-okada/bXiv).

## License
[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)


