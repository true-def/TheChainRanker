#!/usr/bin/env python -W ignore::DeprecationWarning
import sys
sys.path.append('../')

import sys, getopt
from summarizer import summarize
from keywords import keywords

#sys.path.append('../LexChain')
from Boochain import LexicalChain

# Types of summarization
SENTENCE = 0
WORD = 1


def get_arguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:s:r:w:h", ["text=", "summary=", "ratio=", "words=", "help"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    path = '../amazon.txt'
    summarize_by = SENTENCE
    ratio = 0.2
    words = None

    original = 1
    
    for o, a in opts:
        if o in ("-t", "--text"):
            path = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--summary"):
            summarize_by = int(a)
        elif o in ("-w", "--words"):
            words = int(a)
        elif o in ("-r", "--ratio"):
            ratio = float(a)
        else:
            assert False, "unhandled option"

    return path, summarize_by, ratio, original, words


help_text = """Usage: python textrank.py -t FILE
-s UNIT, --summary=UNIT:
\tType of unit to summarize: sentence (0) or word (1). Default value: 0
\t0: Sentence. 1: Word
-t FILE, --text=FILE:
\tPATH to text to summarize
-r RATIO, --ratio=RATIO:
\tFloat number (0,1] that defines the length of the summary. It's a proportion of the original text. Default value: 0.2.
-o ORIGINAL, --original=ORIGINAL:
\tDetermines whether to run with LexChains : 1 - without lexchain, 2 -with lexchain
-w WORDS, --words=WORDS:
\tNumber to limit the length of the summary. The length option is ignored if the word limit is set.
-h, --help:
\tprints this help
"""
def usage():
    print help_text


def textrank(fileName, original='pagerank', summarize_by=SENTENCE, ratio=0.2, words=None):
    
    path = '../Raw_text/'+fileName
    File = open(path) #open file
    text = File.read() #read all lines

    if original=='suraj':
        #print 'with lexchain'
        namscores = LexicalChain(fileName=path)
    else:
        namscores = []
    #print namscores
    if summarize_by == SENTENCE:
        return summarize(text, namscores, original, ratio, words)
    else:
        return keywords(text, ratio, words)


def main():
    path, summarize_by, ratio, original, words = get_arguments()

    with open(path) as file:
        text = file.read()

    print textrank(text, path, original, summarize_by, ratio, words)


if __name__ == "__main__":
    main()
