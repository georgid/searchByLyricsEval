'''
Created on Jul 26, 2015

@author: joro
'''
import csv
import sys

def loadPaths(URI_wholeAudio_noExt, SECTION_NUM):

    URI_pathXBegins = URI_wholeAudio_noExt + '_' + str(SECTION_NUM) + '_begins.tsv';
    URI_pathXEnds = URI_wholeAudio_noExt + '_' +  str(SECTION_NUM) + '_ends.tsv';


    with open(URI_pathXBegins, 'rb') as f:
        reader = csv.reader(f)
        XBegins = list(reader)

    with open(URI_pathXEnds, 'rb') as f:
        reader = csv.reader(f)
        XEnds = list(reader)

    pathXs = list(); 
    for pathX in zip(XBegins[0],XEnds[0]):
        pathXs.append( (int(pathX[0]),int(pathX[1])) );


    # sort     
    pathXsSorted = sorted(pathXs,key=lambda x: x[1])
    return pathXsSorted
    
    
def calcCandSegments(URI_wholeAudio_noExt, pathXsSorted, SECTION_NUM):
    # segment
    allSegments = []
    currSegment = [None] * 2

    for i in range(len(pathXsSorted)):
        updateMinMaxSegment(pathXsSorted[i], currSegment)

        # end of path is not overlapping with  start of next path
        if i == len(pathXsSorted)-1:
             allSegments.append(currSegment)
        elif pathXsSorted[i][1] < pathXsSorted[i+1][0]:
            allSegments.append(currSegment)
            currSegment = [None] * 2

    # print segments 
    URI_candidateSegmentsTs = URI_wholeAudio_noExt + '_' + str(SECTION_NUM) + '_candSegmentsTs.csv'
    with open(URI_candidateSegmentsTs , 'w') as f:
        writer = csv.writer(f)    
        for segment in allSegments:
            writer.writerow(segment)
    print "file written " + URI_candidateSegmentsTs

    
def updateMinMaxSegment(currPath, currSegment):
    if currPath[0] < currSegment[0] or currSegment[0] == None:
        currSegment[0]  = currPath[0]
    if currSegment[1] > currSegment[0] or currSegment[1] == None:
        currSegment[1]  = currPath[1]
        

def doit(argv):
    if len(argv) != 3 :
            print ("usage: {}  <URI_wholeAudio_noExt>  <SECTION_NUM>".format(sys.argv[0]) )
            sys.exit();       
    URI_wholeAudio_noExt = argv[1]
    SECTION_NUM = int(argv[2])

    pathXsSorted = loadPaths(URI_wholeAudio_noExt, SECTION_NUM)
    calcCandSegments(URI_wholeAudio_noExt, pathXsSorted, SECTION_NUM)


if __name__ == '__main__':
    
    doit(sys.argv)
#     URI_wholeAudio_noExt= '/Users/joro/Documents/Phd/UPF/ISTANBUL/idil/Sakin--Gec--Kalma';
#     doit(["dummy", URI_wholeAudio_noExt, '2'] )
    
  