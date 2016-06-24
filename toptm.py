import sys
from collections import defaultdict
import codecs
import unicodedata

def remove_unicode(text_data):
   if text_data == None or text_data == '':
       return text_data
   return unicodedata.normalize('NFKD', text_data).encode('ascii','ignore')

def main():
    tmyearly=defaultdict(list)          #
    tmsum=defaultdict(list)             #
    g = defaultdict(list)               #

    # read google books ngram corpus into dictionary
    # each word is a key, with valued rolling up pairs of [year used, times used]
    with codecs.open(sys.argv[2], encoding='utf-8') as corpus:
        for gram in corpus:
            gram2 = remove_unicode(gram)
            ga = gram2.strip().split("\t")
            g[ga[0]].append([int(ga[1]), int(ga[2])])
    # print g

    # process each trademark n-gram
    # if it exists in books n-gram dict, sum total usages
    with open(sys.argv[1]) as grams:
        for tm in grams:
            tm2 = tm.strip()
            if tm2 in g:
                # print g[tm2]
                tmsum[tm2] = sum(zip(*g[tm2])[1])
    print tmsum

    # sort, save, print ngram usages
    with open(sys.argv[3],'w') as f:
        for k,v in sorted(tmsum.items(), key = lambda (k,v): v):
            # print k, v
            f.write('%s: %s\n' % (k, v))

if ( __name__ == "__main__"):
    if len(sys.argv) != 4:
        sys.exit ("Usage: %s trademarks ngrams output" % str(sys.argv[0]))
    main()
