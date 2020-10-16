# pyGREAT

https://great-help.atlassian.net/wiki/spaces/GREAT/pages/655447/Programming+Interface


GREAT analysis, http://great.stanford.edu/public/html/, python wrapper

rGREAT is the best if it works for you. But it doesn't work for me.

Motivation
----------

My work here at St. Jude is to develop pipelines and simplify user's effort for NGS analyses.
I don't want users, when finish running my HemTools pipeline, have to upload bed files to GREAT
server themselves.

Summary
-------

This tool uses Dropbox to create a sharable link and then use it for GREAT analysis. It will
print out a GREAT url. You then just need to copypaste the url to a browser to check out the results.


Installation
------------

module load conda3
conda create -n share_url
source activate share_url
conda install -c anaconda dropbox

Please follow the dropbox instruction below, mainly, you need a token.
The dropbox code is taken from: https://gist.github.com/Keshava11/d14db1e22765e8de2670b8976f3c7efb

Usage
-----

python pyGREAT.py test.bed

Return
------

http://great.stanford.edu/public/cgi-bin/greatStart.php?requestURL=https://www.dropbox.com/s/jd9q2489k91m8bj/test.bed?dl=0&requestSpecies=hg19&requestName=ensGene&requestSender=UCSC%20Table%20Browser
