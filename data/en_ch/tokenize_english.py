__author__ = 'qianchu_liu'

if __name__=='__main__':
    import sys
    from nltk.tokenize import word_tokenize
    en_f=sys.argv[1]

    data=[]
    for line in open(en_f):
        data.append(' '.join(word_tokenize(line.strip())))

    with open(en_f,'w') as f:
        f.write('\n'.join(data)+'\n')