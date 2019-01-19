__author__ = 'qianchu_liu'

import sys
import time
from nltk.tokenize import sent_tokenize
from copy import deepcopy

word2id = dict()


def extractLocation(context, word):
    line = context.strip().split(' ')
    location = -1
    for j in range(len(line)):
        if line[j] == '<b>':
            location = j
            line = line[:j] + [line[j + 1]] + line[j + 3:]
            break
    if line[location] != word:
        print(line[location], word)
    return location, line


def smooth(context):
    line = context.split(' ')
    i = 0
    while i != len(line):
        #	if line[i] == '(' or line[i] == ')' or line[i] == '"' or line[i] == '[' or line[i] == ']':
        #		line = line[:i]+line[i+1:]
        #		continue
        if line[i] not in word2id:
            if '-' in line[i] and line[i] != '-':
                line[i] = line[i].replace('-', ' - ')
                line = line[:i] + line[i].split(' ') + line[i + 1:]
                continue
            elif '/' in line[i] and line[i] != '</b>' and line[i] != '/':
                line[i] = line[i].replace('/', ' / ')
                line = line[:i] + line[i].split(' ') + line[i + 1:]
                continue
            if line[i] != '<b>' and line[i] != '</b>':
                line = line[:i] + ['_UNK'] + line[i + 1:]
                continue
        i += 1
    return ' '.join(line)


vocab = sys.argv[1]
testInFile = sys.argv[2]
testOutFile = sys.argv[3]
en_fname=sys.argv[4]



en_f=open(en_fname, 'w')

with open(vocab) as fp:
    for line in fp:
        line = line.strip().split(' ')
        word = line[0]
        ID = line[1]
        word2id[word] = ID

start_time = time.time()
wordCount = 0
UNKCount = 0
with open(testInFile) as infp, open(testOutFile, 'w') as outfp:
    for e, line in enumerate(infp):
        line = line.strip().lower()
        line = line.split('\t')
        id = line[0]

        word1 = line[1]
        POS1 = line[2]
        word2 = line[3]
        POS2 = line[4]

        if word1 not in word2id or word2 not in word2id:
            continue

        context1 = sent_tokenize(line[5])
        context2 = sent_tokenize(line[6])
        found = False
        for sentence in context1:
            if '<b>' in sentence and '</b>' in sentence:
                context1 = sentence
                found = True
                break
        if not found:
            print(context1)
        found = False
        for sentence in context2:
            if '<b>' in sentence and '</b>' in sentence:
                context2 = sentence
                found = True
                break
        if not found:
            print(context2)

        aveR = (line[7])
        Rs = map(float, line[8:])

        #general output
        context1_orig=deepcopy(context1)
        context2_orig=deepcopy(context2)

        location1, context1_orig = extractLocation(context1_orig, word1)
        location2, context2_orig = extractLocation(context2_orig, word2)
        # context1_orig=delete_marker(context1_orig)
        # context2_orig=delete_marker(context2_orig)
        en_f.write('{0}\t{1}\t{2}\n'.format(' '.join(context1_orig),str(location1),aveR))
        en_f.write('{0}\t{1}\t{2}\n'.format(' '.join(context2_orig),str(location2),aveR))


        # output for cluse evaluation
        context1 = smooth(context1)
        context2 = smooth(context2)
        location1, context1 = extractLocation(context1, word1)
        location2, context2 = extractLocation(context2, word2)
        outfp.write(aveR + '\n')

        offset = 0
        data = []
        tempData = []
        for i in range(len(context1)):
            if context1[i] in word2id:
                tempData.append(context1[i])
                data.append(word2id[context1[i]])
            else:
                # context1[i] = UNK_ID
                UNKCount += 1
                if i < location1:
                    offset += 1
        wordCount += len(data)
        # print ' '.join(tempData)
        # print word1
        assert (offset == 0)
        assert (data[location1 - offset] == word2id[word1])
        outfp.write(str(location1 - offset) + '\n')
        data = map(str, data)
        outfp.write(' '.join(data) + '\n')

        offset = 0
        data = []
        for i in range(len(context2)):
            if context2[i] in word2id:
                data.append(word2id[context2[i]])
            else:
                # print context2[i]
                # print line[6],'\n'
                # context2[i] = UNK_ID
                UNKCount += 1
                if i < location2:
                    offset += 1

        wordCount += len(data)
        assert (offset == 0)
        assert (data[location2 - offset] == word2id[word2])
        outfp.write(str(location2 - offset) + '\n')
        data = map(str, data)
        outfp.write(' '.join(data) + '\n')

print(wordCount, float(UNKCount) / wordCount)
en_f.close()