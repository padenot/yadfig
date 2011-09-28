#!/usr/bin/python

import codecs
import sys

#print sys.argv[1], sys.argv[2], sys.argv[3]
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
toInsert = codecs.open(sys.argv[1], encoding="utf-8").read()
where = codecs.open(sys.argv[2], encoding="utf-8").read()
where = where.replace(sys.argv[3], toInsert)
print where

