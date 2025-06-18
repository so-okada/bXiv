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
	- bXiv_variables.py


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
	
* Configure bXiv_variables.py for your settings. 

   - bXiv_variables.py assigns format parameters for bXiv posts 
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

* 0.0.1, initial release, 2025-01-12.
  
* 0.0.2, minor updates,  2025-02-04.

* 0.0.3, an update for createAccount endpoint ratelimit (100 per 5 min), 2025-02-18. 

* 0.0.4, a fix for unrepost/repost, 2025-03-02.

 
## List of Bots

* [https://bsky.app/profile/csai-bot.bsky.social](https://bsky.app/profile/csai-bot.bsky.social): cs.AI Artificial Intelligence
* [https://bsky.app/profile/csar-bot.bsky.social](https://bsky.app/profile/csar-bot.bsky.social): cs.AR Hardware Architecture
* [https://bsky.app/profile/cscc-bot.bsky.social](https://bsky.app/profile/cscc-bot.bsky.social): cs.CC Computational Complexity
* [https://bsky.app/profile/csce-bot.bsky.social](https://bsky.app/profile/csce-bot.bsky.social): cs.CE Computational Engineering, Finance, and Science
* [https://bsky.app/profile/cscg-bot.bsky.social](https://bsky.app/profile/cscg-bot.bsky.social): cs.CG Computational Geometry
* [https://bsky.app/profile/cscl-bot.bsky.social](https://bsky.app/profile/cscl-bot.bsky.social): cs.CL Computation and Language
* [https://bsky.app/profile/cscr-bot.bsky.social](https://bsky.app/profile/cscr-bot.bsky.social): cs.CR Cryptography and Security
* [https://bsky.app/profile/cscv-bot.bsky.social](https://bsky.app/profile/cscv-bot.bsky.social): cs.CV Computer Vision and Pattern Recognition
* [https://bsky.app/profile/cscy-bot.bsky.social](https://bsky.app/profile/cscy-bot.bsky.social): cs.CY Computers and Society
* [https://bsky.app/profile/csdb-bot.bsky.social](https://bsky.app/profile/csdb-bot.bsky.social): cs.DB Databases
* [https://bsky.app/profile/csdc-bot.bsky.social](https://bsky.app/profile/csdc-bot.bsky.social): cs.DC Distributed, Parallel, and Cluster Computing
* [https://bsky.app/profile/csdl-bot.bsky.social](https://bsky.app/profile/csdl-bot.bsky.social): cs.DL Digital Libraries
* [https://bsky.app/profile/csdm-bot.bsky.social](https://bsky.app/profile/csdm-bot.bsky.social): cs.DM Discrete Mathematics
* [https://bsky.app/profile/csds-bot.bsky.social](https://bsky.app/profile/csds-bot.bsky.social): cs.DS Data Structures and Algorithms
* [https://bsky.app/profile/cset-bot.bsky.social](https://bsky.app/profile/cset-bot.bsky.social): cs.ET Emerging Technologies
* [https://bsky.app/profile/csfl-bot.bsky.social](https://bsky.app/profile/csfl-bot.bsky.social): cs.FL Formal Languages and Automata Theory
* [https://bsky.app/profile/csgl-bot.bsky.social](https://bsky.app/profile/csgl-bot.bsky.social): cs.GL General Literature
* [https://bsky.app/profile/csgr-bot.bsky.social](https://bsky.app/profile/csgr-bot.bsky.social): cs.GR Graphics
* [https://bsky.app/profile/csgt-bot.bsky.social](https://bsky.app/profile/csgt-bot.bsky.social): cs.GT Computer Science and Game Theory
* [https://bsky.app/profile/cshc-bot.bsky.social](https://bsky.app/profile/cshc-bot.bsky.social): cs.HC Human-Computer Interaction
* [https://bsky.app/profile/csir-bot.bsky.social](https://bsky.app/profile/csir-bot.bsky.social): cs.IR Information Retrieval
* [https://bsky.app/profile/csit-bot.bsky.social](https://bsky.app/profile/csit-bot.bsky.social): cs.IT Information Theory
* [https://bsky.app/profile/cslg-bot.bsky.social](https://bsky.app/profile/cslg-bot.bsky.social): cs.LG Machine Learning
* [https://bsky.app/profile/cslo-bot.bsky.social](https://bsky.app/profile/cslo-bot.bsky.social): cs.LO Logic in Computer Science
* [https://bsky.app/profile/csma-bot.bsky.social](https://bsky.app/profile/csma-bot.bsky.social): cs.MA Multiagent Systems
* [https://bsky.app/profile/csmm-bot.bsky.social](https://bsky.app/profile/csmm-bot.bsky.social): cs.MM Multimedia
* [https://bsky.app/profile/csms-bot.bsky.social](https://bsky.app/profile/csms-bot.bsky.social): cs.MS Mathematical Software
* [https://bsky.app/profile/csne-bot.bsky.social](https://bsky.app/profile/csne-bot.bsky.social): cs.NE Neural and Evolutionary Computing
* [https://bsky.app/profile/csna-bot.bsky.social](https://bsky.app/profile/csna-bot.bsky.social): cs.NA Numerical Analysis 
* [https://bsky.app/profile/csni-bot.bsky.social](https://bsky.app/profile/csni-bot.bsky.social): cs.NI Networking and Internet Architecture
* [https://bsky.app/profile/csoh-bot.bsky.social](https://bsky.app/profile/csoh-bot.bsky.social): cs.OH Other Computer Science
* [https://bsky.app/profile/csos-bot.bsky.social](https://bsky.app/profile/csos-bot.bsky.social): cs.OS Operating Systems
* [https://bsky.app/profile/cspf-bot.bsky.social](https://bsky.app/profile/cspf-bot.bsky.social): cs.PF Performance
* [https://bsky.app/profile/cspl-bot.bsky.social](https://bsky.app/profile/cspl-bot.bsky.social): cs.PL Programming Languages
* [https://bsky.app/profile/csro-bot.bsky.social](https://bsky.app/profile/csro-bot.bsky.social): cs.RO Robotics
* [https://bsky.app/profile/cssc-bot.bsky.social](https://bsky.app/profile/cssc-bot.bsky.social): cs.SC Symbolic Computation
* [https://bsky.app/profile/cssd-bot.bsky.social](https://bsky.app/profile/cssd-bot.bsky.social): cs.SD Sound
* [https://bsky.app/profile/csse-bot.bsky.social](https://bsky.app/profile/csse-bot.bsky.social): cs.SE Software Engineering
* [https://bsky.app/profile/cssi-bot.bsky.social](https://bsky.app/profile/cssi-bot.bsky.social): cs.SI Social and Information Networks
* [https://bsky.app/profile/cssy-bot.bsky.social](https://bsky.app/profile/cssy-bot.bsky.social): cs.SY Systems and Control
* [https://bsky.app/profile/econem-bot.bsky.social](https://bsky.app/profile/econem-bot.bsky.social): econ.EM Econometrics
* [https://bsky.app/profile/econgn-bot.bsky.social](https://bsky.app/profile/econgn-bot.bsky.social): econ.GN General Economics
* [https://bsky.app/profile/econth-bot.bsky.social](https://bsky.app/profile/econth-bot.bsky.social): econ.TH Theoretical Economics
* [https://bsky.app/profile/eessas-bot.bsky.social](https://bsky.app/profile/eessas-bot.bsky.social): eess.AS Audio and Speech Processing
* [https://bsky.app/profile/eessiv-bot.bsky.social](https://bsky.app/profile/eessiv-bot.bsky.social): eess.IV Image and Video Processing
* [https://bsky.app/profile/eesssp-bot.bsky.social](https://bsky.app/profile/eesssp-bot.bsky.social): eess.SP Signal Processing
* [https://bsky.app/profile/eesssy-bot.bsky.social](https://bsky.app/profile/eesssy-bot.bsky.social): eess.SY Systems and Control
* [https://bsky.app/profile/mathac-bot.bsky.social](https://bsky.app/profile/mathac-bot.bsky.social): math.AC Commutative Algebra
* [https://bsky.app/profile/mathag-bot.bsky.social](https://bsky.app/profile/mathag-bot.bsky.social): math.AG Algebraic Geometry
* [https://bsky.app/profile/mathap-bot.bsky.social](https://bsky.app/profile/mathap-bot.bsky.social): math.AP Analysis of PDEs
* [https://bsky.app/profile/mathat-bot.bsky.social](https://bsky.app/profile/mathat-bot.bsky.social): math.AT Algebraic Topology
* [https://bsky.app/profile/mathca-bot.bsky.social](https://bsky.app/profile/mathca-bot.bsky.social): math.CA Classical Analysis and ODEs
* [https://bsky.app/profile/mathco-bot.bsky.social](https://bsky.app/profile/mathco-bot.bsky.social): math.CO Combinatorics
* [https://bsky.app/profile/mathct-bot.bsky.social](https://bsky.app/profile/mathct-bot.bsky.social): math.CT Category Theory
* [https://bsky.app/profile/mathcv-bot.bsky.social](https://bsky.app/profile/mathcv-bot.bsky.social): math.CV Complex Variables
* [https://bsky.app/profile/mathdg-bot.bsky.social](https://bsky.app/profile/mathdg-bot.bsky.social): math.DG Differential Geometry
* [https://bsky.app/profile/mathds-bot.bsky.social](https://bsky.app/profile/mathds-bot.bsky.social): math.DS Dynamical Systems
* [https://bsky.app/profile/mathfa-bot.bsky.social](https://bsky.app/profile/mathfa-bot.bsky.social): math.FA Functional Analysis
* [https://bsky.app/profile/mathgm-bot.bsky.social](https://bsky.app/profile/mathgm-bot.bsky.social): math.GM General Mathematics
* [https://bsky.app/profile/mathgn-bot.bsky.social](https://bsky.app/profile/mathgn-bot.bsky.social): math.GN General Topology
* [https://bsky.app/profile/mathgr-bot.bsky.social](https://bsky.app/profile/mathgr-bot.bsky.social): math.GR Group Theory
* [https://bsky.app/profile/mathgt-bot.bsky.social](https://bsky.app/profile/mathgt-bot.bsky.social): math.GT Geometric Topology
* [https://bsky.app/profile/mathho-bot.bsky.social](https://bsky.app/profile/mathho-bot.bsky.social): math.HO History and Overview
* [https://bsky.app/profile/mathit-bot.bsky.social](https://bsky.app/profile/mathit-bot.bsky.social): math.IT Information Theory
* [https://bsky.app/profile/mathkt-bot.bsky.social](https://bsky.app/profile/mathkt-bot.bsky.social): math.KT K-Theory and Homology
* [https://bsky.app/profile/mathlo-bot.bsky.social](https://bsky.app/profile/mathlo-bot.bsky.social): math.LO Logic
* [https://bsky.app/profile/mathmg-bot.bsky.social](https://bsky.app/profile/mathmg-bot.bsky.social): math.MG Metric Geometry
* [https://bsky.app/profile/mathmp-bot.bsky.social](https://bsky.app/profile/mathmp-bot.bsky.social): math.MP Mathematical Physics
* [https://bsky.app/profile/mathna-bot.bsky.social](https://bsky.app/profile/mathna-bot.bsky.social): math.NA Numerical Analysis
* [https://bsky.app/profile/mathnt-bot.bsky.social](https://bsky.app/profile/mathnt-bot.bsky.social): math.NT Number Theory
* [https://bsky.app/profile/mathoa-bot.bsky.social](https://bsky.app/profile/mathoa-bot.bsky.social): math.OA Operator Algebras
* [https://bsky.app/profile/mathoc-bot.bsky.social](https://bsky.app/profile/mathoc-bot.bsky.social): math.OC Optimization and Control
* [https://bsky.app/profile/mathpr-bot.bsky.social](https://bsky.app/profile/mathpr-bot.bsky.social): math.PR Probability
* [https://bsky.app/profile/mathqa-bot.bsky.social](https://bsky.app/profile/mathqa-bot.bsky.social): math.QA Quantum Algebra
* [https://bsky.app/profile/mathra-bot.bsky.social](https://bsky.app/profile/mathra-bot.bsky.social): math.RA Rings and Algebras
* [https://bsky.app/profile/mathrt-bot.bsky.social](https://bsky.app/profile/mathrt-bot.bsky.social): math.RT Representation Theory
* [https://bsky.app/profile/mathsg-bot.bsky.social](https://bsky.app/profile/mathsg-bot.bsky.social): math.SG Symplectic Geometry
* [https://bsky.app/profile/mathsp-bot.bsky.social](https://bsky.app/profile/mathsp-bot.bsky.social): math.SP Spectral Theory
* [https://bsky.app/profile/mathst-bot.bsky.social](https://bsky.app/profile/mathst-bot.bsky.social): math.ST Statistics Theory
* [https://bsky.app/profile/astrophco-bot.bsky.social](https://bsky.app/profile/astrophco-bot.bsky.social): astro-ph.CO Cosmology and Nongalactic Astrophysics
* [https://bsky.app/profile/astrophep-bot.bsky.social](https://bsky.app/profile/astrophep-bot.bsky.social): astro-ph.EP Earth and Planetary Astrophysics
* [https://bsky.app/profile/astrophga-bot.bsky.social](https://bsky.app/profile/astrophga-bot.bsky.social): astro-ph.GA Astrophysics of Galaxies
* [https://bsky.app/profile/astrophhe-bot.bsky.social](https://bsky.app/profile/astrophhe-bot.bsky.social): astro-ph.HE High Energy Astrophysical Phenomena
* [https://bsky.app/profile/astrophim-bot.bsky.social](https://bsky.app/profile/astrophim-bot.bsky.social): astro-ph.IM Instrumentation and Methods for Astrophysics
* [https://bsky.app/profile/astrophsr-bot.bsky.social](https://bsky.app/profile/astrophsr-bot.bsky.social): astro-ph.SR Solar and Stellar Astrophysics
* [https://bsky.app/profile/condmatdisnn-bot.bsky.social](https://bsky.app/profile/condmatdisnn-bot.bsky.social): cond-mat.dis-nn Disordered Systems and Neural Networks
* [https://bsky.app/profile/condmatmeshall-bot.bsky.social](https://bsky.app/profile/condmatmeshall-bot.bsky.social): cond-mat.mes-hall Mesoscale and Nanoscale Physics
* [https://bsky.app/profile/condmatmtrlsci-bot.bsky.social](https://bsky.app/profile/condmatmtrlsci-bot.bsky.social): cond-mat.mtrl-sci Materials Science
* [https://bsky.app/profile/condmatother-bot.bsky.social](https://bsky.app/profile/condmatother-bot.bsky.social): cond-mat.other Other Condensed Matter
* [https://bsky.app/profile/condmatquantgas-bt.bsky.social](https://bsky.app/profile/condmatquantgas-bt.bsky.social): cond-mat.quant-gas Quantum Gases
* [https://bsky.app/profile/condmatsoft-bot.bsky.social](https://bsky.app/profile/condmatsoft-bot.bsky.social): cond-mat.soft Soft Condensed Matter
* [https://bsky.app/profile/condmatstatmech-bt.bsky.social](https://bsky.app/profile/condmatstatmech-bt.bsky.social): cond-mat.stat-mech Statistical Mechanics
* [https://bsky.app/profile/condmatstrel-bot.bsky.social](https://bsky.app/profile/condmatstrel-bot.bsky.social): cond-mat.str-el Strongly Correlated Electrons
* [https://bsky.app/profile/condmatsuprcon-bot.bsky.social](https://bsky.app/profile/condmatsuprcon-bot.bsky.social): cond-mat.supr-con Superconductivity
* [https://bsky.app/profile/grqc-bot.bsky.social](https://bsky.app/profile/grqc-bot.bsky.social): gr-qc General Relativity and Quantum Cosmology
* [https://bsky.app/profile/hepex-bot.bsky.social](https://bsky.app/profile/hepex-bot.bsky.social): hep-ex High Energy Physics - Experiment
* [https://bsky.app/profile/heplat-bot.bsky.social](https://bsky.app/profile/heplat-bot.bsky.social): hep-lat High Energy Physics - Lattice
* [https://bsky.app/profile/hepph-bot.bsky.social](https://bsky.app/profile/hepph-bot.bsky.social): hep-ph High Energy Physics - Phenomenology
* [https://bsky.app/profile/hepth-bot.bsky.social](https://bsky.app/profile/hepth-bot.bsky.social): hep-th High Energy Physics - Theory
* [https://bsky.app/profile/mathph-bot.bsky.social](https://bsky.app/profile/mathph-bot.bsky.social): math-ph Mathematical Physics
* [https://bsky.app/profile/nlinao-bot.bsky.social](https://bsky.app/profile/nlinao-bot.bsky.social): nlin.AO Adaptation and Self-Organizing Systems
* [https://bsky.app/profile/nlincd-bot.bsky.social](https://bsky.app/profile/nlincd-bot.bsky.social): nlin.CD Chaotic Dynamics
* [https://bsky.app/profile/nlincg-bot.bsky.social](https://bsky.app/profile/nlincg-bot.bsky.social): nlin.CG Cellular Automata and Lattice Gases
* [https://bsky.app/profile/nlinps-bot.bsky.social](https://bsky.app/profile/nlinps-bot.bsky.social): nlin.PS Pattern Formation and Solitons
* [https://bsky.app/profile/nlinsi-bot.bsky.social](https://bsky.app/profile/nlinsi-bot.bsky.social): nlin.SI Exactly Solvable and Integrable Systems
* [https://bsky.app/profile/nuclex-bot.bsky.social](https://bsky.app/profile/nuclex-bot.bsky.social): nucl-ex Nuclear Experiment
* [https://bsky.app/profile/nuclth-bot.bsky.social](https://bsky.app/profile/nuclth-bot.bsky.social): nucl-th Nuclear Theory
* [https://bsky.app/profile/physicsaccph-bot.bsky.social](https://bsky.app/profile/physicsaccph-bot.bsky.social): physics.acc-ph Accelerator Physics
* [https://bsky.app/profile/physicsaoph-bot.bsky.social](https://bsky.app/profile/physicsaoph-bot.bsky.social): physics.ao-ph Atmospheric and Oceanic Physics
* [https://bsky.app/profile/physicsappph-bot.bsky.social](https://bsky.app/profile/physicsappph-bot.bsky.social): physics.app-ph Applied Physics
* [https://bsky.app/profile/physicsatmclus-bot.bsky.social](https://bsky.app/profile/physicsatmclus-bot.bsky.social): physics.atm-clus Atomic and Molecular Clusters
* [https://bsky.app/profile/physicsatomph-bot.bsky.social](https://bsky.app/profile/physicsatomph-bot.bsky.social): physics.atom-ph Atomic Physics
* [https://bsky.app/profile/physicsbioph-bot.bsky.social](https://bsky.app/profile/physicsbioph-bot.bsky.social): physics.bio-ph Biological Physics
* [https://bsky.app/profile/physicschemph-bot.bsky.social](https://bsky.app/profile/physicschemph-bot.bsky.social): physics.chem-ph Chemical Physics
* [https://bsky.app/profile/physicsclassph-bot.bsky.social](https://bsky.app/profile/physicsclassph-bot.bsky.social): physics.class-ph Classical Physics
* [https://bsky.app/profile/physicscompph-bot.bsky.social](https://bsky.app/profile/physicscompph-bot.bsky.social): physics.comp-ph Computational Physics
* [https://bsky.app/profile/physicsdataan-bot.bsky.social](https://bsky.app/profile/physicsdataan-bot.bsky.social): physics.data-an Data Analysis, Statistics and Probability
* [https://bsky.app/profile/physicsedph-bot.bsky.social](https://bsky.app/profile/physicsedph-bot.bsky.social): physics.ed-ph Physics Education
* [https://bsky.app/profile/physicsfludyn-bot.bsky.social](https://bsky.app/profile/physicsfludyn-bot.bsky.social): physics.flu-dyn Fluid Dynamics
* [https://bsky.app/profile/physicsgenph-bot.bsky.social](https://bsky.app/profile/physicsgenph-bot.bsky.social): physics.gen-ph General Physics
* [https://bsky.app/profile/physicsgeoph-bot.bsky.social](https://bsky.app/profile/physicsgeoph-bot.bsky.social): physics.geo-ph Geophysics
* [https://bsky.app/profile/physicshistph-bot.bsky.social](https://bsky.app/profile/physicshistph-bot.bsky.social): physics.hist-ph History and Philosophy of Physics
* [https://bsky.app/profile/physicsinsdet-bot.bsky.social](https://bsky.app/profile/physicsinsdet-bot.bsky.social): physics.ins-det Instrumentation and Detectors
* [https://bsky.app/profile/physicsmedph-bot.bsky.social](https://bsky.app/profile/physicsmedph-bot.bsky.social): physics.med-ph Medical Physics
* [https://bsky.app/profile/physicsoptics-bot.bsky.social](https://bsky.app/profile/physicsoptics-bot.bsky.social): physics.optics Optics
* [https://bsky.app/profile/physicsplasmph-bot.bsky.social](https://bsky.app/profile/physicsplasmph-bot.bsky.social): physics.plasm-ph Plasma Physics
* [https://bsky.app/profile/physicspopph-bot.bsky.social](https://bsky.app/profile/physicspopph-bot.bsky.social): physics.pop-ph Popular Physics
* [https://bsky.app/profile/physicssocph-bot.bsky.social](https://bsky.app/profile/physicssocph-bot.bsky.social): physics.soc-ph Physics and Society
* [https://bsky.app/profile/physicsspaceph-bot.bsky.social](https://bsky.app/profile/physicsspaceph-bot.bsky.social): physics.space-ph Space Physics
* [https://bsky.app/profile/quantph-bot.bsky.social](https://bsky.app/profile/quantph-bot.bsky.social): quant-ph Quantum Physics
* [https://bsky.app/profile/qbiobm-bot.bsky.social](https://bsky.app/profile/qbiobm-bot.bsky.social): q-bio.BM Biomolecules
* [https://bsky.app/profile/qbiocb-bot.bsky.social](https://bsky.app/profile/qbiocb-bot.bsky.social): q-bio.CB Cell Behavior
* [https://bsky.app/profile/qbiogn-bot.bsky.social](https://bsky.app/profile/qbiogn-bot.bsky.social): q-bio.GN Genomics
* [https://bsky.app/profile/qbiomn-bot.bsky.social](https://bsky.app/profile/qbiomn-bot.bsky.social): q-bio.MN Molecular Networks
* [https://bsky.app/profile/qbionc-bot.bsky.social](https://bsky.app/profile/qbionc-bot.bsky.social): q-bio.NC Neurons and Cognition
* [https://bsky.app/profile/qbioot-bot.bsky.social](https://bsky.app/profile/qbioot-bot.bsky.social): q-bio.OT Other Quantitative Biology
* [https://bsky.app/profile/qbiope-bot.bsky.social](https://bsky.app/profile/qbiope-bot.bsky.social): q-bio.PE Populations and Evolution
* [https://bsky.app/profile/qbioqm-bot.bsky.social](https://bsky.app/profile/qbioqm-bot.bsky.social): q-bio.QM Quantitative Methods
* [https://bsky.app/profile/qbiosc-bot.bsky.social](https://bsky.app/profile/qbiosc-bot.bsky.social): q-bio.SC Subcellular Processes
* [https://bsky.app/profile/qbioto-bot.bsky.social](https://bsky.app/profile/qbioto-bot.bsky.social): q-bio.TO Tissues and Organs
* [https://bsky.app/profile/qfincp-bot.bsky.social](https://bsky.app/profile/qfincp-bot.bsky.social): q-fin.CP Computational Finance
* [https://bsky.app/profile/qfinec-bot.bsky.social](https://bsky.app/profile/qfinec-bot.bsky.social): q-fin.EC Economics
* [https://bsky.app/profile/qfingn-bot.bsky.social](https://bsky.app/profile/qfingn-bot.bsky.social): q-fin.GN General Finance
* [https://bsky.app/profile/qfinmf-bot.bsky.social](https://bsky.app/profile/qfinmf-bot.bsky.social): q-fin.MF Mathematical Finance
* [https://bsky.app/profile/qfinpm-bot.bsky.social](https://bsky.app/profile/qfinpm-bot.bsky.social): q-fin.PM Portfolio Management
* [https://bsky.app/profile/qfinpr-bot.bsky.social](https://bsky.app/profile/qfinpr-bot.bsky.social): q-fin.PR Pricing of Securities
* [https://bsky.app/profile/qfinrm-bot.bsky.social](https://bsky.app/profile/qfinrm-bot.bsky.social): q-fin.RM Risk Management
* [https://bsky.app/profile/qfinst-bot.bsky.social](https://bsky.app/profile/qfinst-bot.bsky.social): q-fin.ST Statistical Finance
* [https://bsky.app/profile/qfintr-bot.bsky.social](https://bsky.app/profile/qfintr-bot.bsky.social): q-fin.TR Trading and Market Microstructure
* [https://bsky.app/profile/statap-bot.bsky.social](https://bsky.app/profile/statap-bot.bsky.social): stat.AP Applications (from 2025-06)
* [https://bsky.app/profile/statco-bot.bsky.social](https://bsky.app/profile/statco-bot.bsky.social): stat.CO Computation (from 2025-06)
* [https://bsky.app/profile/statme-bot.bsky.social](https://bsky.app/profile/statme-bot.bsky.social): stat.ME Methodology
* [https://bsky.app/profile/statml-bot.bsky.social](https://bsky.app/profile/statml-bot.bsky.social): stat.ML Machine Learning
* [https://bsky.app/profile/statot-bot.bsky.social](https://bsky.app/profile/statot-bot.bsky.social): stat.OT Other Statistics
* [https://bsky.app/profile/statth-bot.bsky.social](https://bsky.app/profile/statth-bot.bsky.social): stat.TH Statistics Theory


## Author
So Okada, so.okada@gmail.com, https://so-okada.github.io/

## Motivation
This is an open-science practice (see
https://github.com/so-okada/twXiv#motivation).  Since 2013-04, the
author has been running twitter bots for all arXiv math categories. 
Since 2023-01, the author has been running mastodon bots for
all arXiv categories 
with [toXiv](https://github.com/so-okada/toXiv). Since 2025-02, the author has been
running the blusky bots for all arXiv categories (except stat.AP and stat.CO from 2025-06)
with [bXiv](https://github.com/so-okada/bXiv).

## License
[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)


