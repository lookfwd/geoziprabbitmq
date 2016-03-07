#!/usr/bin/env python

import random
import pika
import sys
import json

found = {}
with open('test.txt', 'r') as f:
    for line in f:
        ll = json.loads(line.strip())

        assert len(ll.keys()) == 1

        postcode = ll.keys()[0]
        viewport = ll[postcode]

        if viewport:
            found[postcode] = viewport

lost = set()
with open('sources.json', 'r') as f:
    postcodes = map(lambda l: ("%s\t%s" % (l[0], l[1])), json.loads(f.read()))

    for i in postcodes:
        if i not in found:
            lost.add(i)


with open("sources2.json", "w") as myfile:
    myfile.write(json.dumps(list(broken)))
