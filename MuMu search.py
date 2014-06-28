import cStringIO as StringIO
import re
import glob
import os
import codecs
#import sys

s = StringIO.StringIO()
files = "./database/*.txt"
textlist = []

def loadkey(filename = 'keywords all.txt' ):
    keydict = []
    with open(filename,'r') as keywordfile:
        for keyword in keywordfile:
            keydict.append(keyword.strip())
    keywordfile.close()
    return keydict


def understand(indexfound):
    out = []
    thissection = []
    span = 4;
    connected = False
    broken = True
    for i,item in enumerate(indexfound):
        if broken:
            thissection = []
            broken = False
        thissection.append(item)
        if i == len(indexfound)-1:
            out.append(thissection)
            break
        if indexfound[i+1]-item > 4:
            broken  = True
            out.append(thissection)
    return out
    
    
def intellesearch(keydict, files, expand = 0):
    reducelb = re.compile(r'\n')
    for keyword in keydict:
        print "==================================="
        print keyword #.strip()
        print "==================================="
        #s.write("###%s\n<ol>\n" % keyword.strip())
        retext = re.compile(keyword.lower())
        #s = StringIO.StringIO()
        for pathname in glob.glob(files):
            #print pathname
            basename= os.path.basename(pathname)
            #print basename
            with open(pathname,'r') as singlefile:
            #with codecs.open(pathname,'r',"utf-8") as singlefile:
                data = "".join(singlefile.readlines())
                data = re.sub(r"(?<=\w)\n", " ", data)
                data = re.sub(r",\n", ", ", data)
                #print data
                #sys.exit()
                wholetext = []
                for line in data.split(r"."):
                    wholetext.append(reducelb.sub(r'', line))
                #print wholetext
                #sys.exit()
                indexfound = []
                for i, target in enumerate(wholetext):
                    #target += '.'
                    found = retext.findall(target.lower())
                    if found:
                        #print target
                        #print "***%s:%d***" % (basename,i)
                        indexfound.append(i)
                        #s.write("<li>%s</li>\n" % target.strip())
                        #s.write("%s:%d" % (basename,i) )
                #s.write("</ol>\n")
                #print indexfound
                if len(indexfound)>0:
                    print basename
                    #print indexfound
                    out = understand(indexfound)
                    #print out
                    for item in out:
                        if len(item) == 1:
                            if extend == 0:
                                block = wholetext[item[0]]+'.'
                            else:
                                start = max(item[0] - extend, 0)
                                end = min(item[len(item)-1] + extend, len(wholetext)-1)
                                block = ". ".join(wholetext[start : end+1])+'.'
                        else:
                            start = max(item[0] - extend, 0)
                            end = min(item[len(item)-1] + extend, len(wholetext)-1)
                            block = (". ".join(wholetext[start : end + 1 ]) )+'.'
                        print block
                        print
    return


while True:
    typein = raw_input("enter key dict:")
    extend = 0
    if os.path.isfile(typein):
        keydict = loadkey(typein)
    elif len(typein)> 0:
        extend = typein.count('+')
        #print extend
        typein = typein.rstrip('+').strip(' ')
        keydict = [typein]
    else:
        keydict = loadkey("keywords all.txt")

    intellesearch(keydict, files, extend)
