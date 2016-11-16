'''
Created on Jul 25, 2015

@author: joro
'''

import numpy as np
import sys
import numpy

def discoverUniqueLyrics(makamScore):
    '''
    discover section numbers with unique lyrics in a  composition
    '''
    listUnique = []
    # loop in sections 
    lyrics = makamScore.getLyricsForSection(whichSection)
    # store in array uniq ones and combine section numbers. use them as pointers
    
    
    return listUnique

def loadResultsMoreQueries(URI_wholeAudio_noExt, listSections):
    '''
    load results for more than one query together
    '''
    
    resultFragments = list(); 
    for SECTION_NUM in listSections:
        begins_URI = URI_wholeAudio_noExt  + '_'  + str(SECTION_NUM) + '_results_begins.tsv';
        ends_URI = URI_wholeAudio_noExt + '_'  + str(SECTION_NUM) + '_results_ends.tsv';
        weights_URI = URI_wholeAudio_noExt + '_' +  str(SECTION_NUM) + '_results_weights.tsv';
        import csv
    
        with open(begins_URI, 'rb') as f:
                reader = csv.reader(f)
                XBegins = list(reader)
    
        with open(ends_URI, 'rb') as f:
                reader = csv.reader(f)
                XEnds = list(reader)
    
        with open(weights_URI, 'rb') as f:
                reader = csv.reader(f)
                weights = list(reader)        
    
        
        for beginTs, endTs, weight in zip(XBegins[0], XEnds[0], weights[0]):
                print weight
                weight = float(weight)
    #             a = "{.30f}".format(weight)
    #             print a
                resultFragments.append( (float(beginTs),float(endTs), float(weight ) ) );


    # sort  by weights   
    resultFragmentsSorted = sorted(resultFragments,key=lambda x: x[2], reverse=True)
    return resultFragmentsSorted

def loadResults(URI_wholeAudio_noExt, SECTION_NUM):
    '''
    load results for  one query
    '''
    
    resultFragments = list(); 
  
    begins_URI = URI_wholeAudio_noExt  + '_'  + str(SECTION_NUM) + '_results_begins.tsv';
    ends_URI = URI_wholeAudio_noExt + '_'  + str(SECTION_NUM) + '_results_ends.tsv';
    weights_URI = URI_wholeAudio_noExt + '_' +  str(SECTION_NUM) + '_results_weights.tsv';
    import csv

    with open(begins_URI, 'rb') as f:
            reader = csv.reader(f)
            XBegins = list(reader)

    with open(ends_URI, 'rb') as f:
            reader = csv.reader(f)
            XEnds = list(reader)

    with open(weights_URI, 'rb') as f:
            reader = csv.reader(f)
            weights = list(reader)        

    
    for beginTs, endTs, weight in zip(XBegins[0], XEnds[0], weights[0]):
            print weight
            weight = float(weight)
#             a = "{.30f}".format(weight)
#             print a
            resultFragments.append( (float(beginTs),float(endTs), float(weight ) ) );


    # sort  by weights   
    resultFragmentsSorted = sorted(resultFragments,key=lambda x: x[2], reverse=True)
    return resultFragmentsSorted


def getGrTruthSegmentsForSection(URI_scorePath, URI_wholeAudio_noExt, URI_AudioSectionAnno, SECTION_NUM):
    
    import sys  
    
    # there are two classes MakamScore. To make sure the right one is discovered   
    URIAlignStep = '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/AlignmentStep/'
    while URIAlignStep in sys.path:
        sys.path.remove(URIAlignStep)

    URIDuration = '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/AlignmentDuration/'
    if URIDuration not in sys.path:
        sys.path.append(URIDuration)
    from MakamScore import loadMakamScore

    pathUtils = '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/utilsLyrics/'
    if pathUtils not in sys.path:
        sys.path.append(pathUtils)
        
    
    sys.path.append(URIAlignStep)
            
    from MakamRecording import MakamRecording

    makamScore = loadMakamScore(URI_scorePath)
    makamRecording = MakamRecording(makamScore, URI_wholeAudio_noExt, URI_AudioSectionAnno)
    print makamRecording.sectionIndices
    
    sectionIndices = np.array(makamRecording.sectionIndices)
    ii = np.where(sectionIndices == SECTION_NUM)[0]
    

    beginTss = np.array(makamRecording.beginTs)
    endTss = np.array(makamRecording.endTs)
    
#     listTss = []
#     for beginTs, endTs in zip(beginTss[ii], endTss[ii]):
#         listTss.append((beginTs, endTs))
    return beginTss[ii], endTss[ii]
#     return listTss
#     return np.array(listTss)
    
def calcRelevance(listDetectedTss, beginGrTrTss, endGrTrTss, tolerance=0.5):
        '''
        loop in list of detected listDetectedTss
        return vector of relevances rel(listDetectedTss): 1 - if detected within tolerance of  ground truth, 0 - else
        '''
        lenListDetected = len(listDetectedTss)
        relevances = np.zeros(lenListDetected)
        for i, detectedTs in enumerate(listDetectedTss):
            diffTobeginGrTrTss = abs(beginGrTrTss - detectedTs[0])
            isWithinToleranceBegins = diffTobeginGrTrTss < tolerance
            
            diffToendGrTrTss = abs(endGrTrTss - detectedTs[1])
            isWithinToleranceEnds = diffToendGrTrTss < tolerance
            
            idxBegin = np.where(isWithinToleranceBegins)[0]
            idxEnd = np.where(isWithinToleranceEnds)[0]
#             shape = np.shape(idxBegin)
            if np.shape(idxBegin) == (1,) and np.shape(idxEnd) == (1,):
                if idxBegin[0] == idxEnd[0]:
                    relevances[i] = 1
                    

#             idx = np.where(isWithinTolerance)
        return  relevances

def calcAveragePrecisionAtK(relevances, K, cardinality):
    '''
    get average precision (AveP) for one query as defined in https://en.wikipedia.org/wiki/Information_retrieval#Average_precision
    for binary relevances, k,  query 
    '''
    precisoins = np.zeros(K)
    for k in range(K):
        precisoins[k] = calcPrec(k+1, relevances)
    
    if len(relevances) < K:
        sys.exit(" {} list detected provided, but required precision at K = {} \n Please give more detected results".format(len(relevances), K) )
    sumPrecs = np.dot(precisoins, relevances[:K])
    return sumPrecs/ float(cardinality)
       
    
def calcPrec(k, relevances):
    # :0 has to be :1, and so on
    return np.sum(relevances[:k+1]) / float(k)

def loadDatasetMappingToScores(URIMappings):
    
    dictAcapellaToScores =  dict()
    import csv

    with open(URIMappings, 'rb') as f:
            reader = csv.reader(f, delimiter="\t")
            mapsAll = list(reader)        
    for mapsLine in mapsAll:
        dictAcapellaToScores[mapsLine[0]] = (mapsLine[1],mapsLine[2],mapsLine[3], mapsLine[4]) 
    return dictAcapellaToScores 


def doitEval(argv):
    '''
    main module
    '''   
    
    if len(argv) != 4 :
            print ("usage: {}  <SECTION_NUM>  <URI_wholeAudio_noExt> <K>  ".format(sys.argv[0]) )
            sys.exit();
    # TODO 
    mappingURL = '/Users/joro/Documents/Phd/UPF/ISTANBUL/DatasetMappingToScores'
    dictMappings = loadDatasetMappingToScores(mappingURL)
    URI_wholeAudio_noExt = argv[2]
    if not URI_wholeAudio_noExt in dictMappings:
        sys.exit("{} not in mappings".format(URI_wholeAudio_noExt))
        
    # which K 
    K = int(argv[3])
    querySectionNum = int(argv[1])
    URI_scorePath = dictMappings[URI_wholeAudio_noExt][0]
    
    querySectionNums = []
    LIST_SECTION_NUMSAll = dictMappings[URI_wholeAudio_noExt][2].split(' ')
    for currSectionGroup in LIST_SECTION_NUMSAll:
        currSectionNums = currSectionGroup.split(',')
        currSectionNums = map(int, currSectionNums)
        if querySectionNum in currSectionNums:
            querySectionNums = currSectionNums
            break
    if len(querySectionNums) == 0:
        sys.exit('requested query {} not in list of sections in file {}'.format(querySectionNum,mappingURL))
    
    ######### get ground truth timestamps for all occurrences of sections
    URI_AudioSectionAnno_noExt = dictMappings[URI_wholeAudio_noExt][1]
    URI_AudioSectionAnno = URI_AudioSectionAnno_noExt + '.sectionAnno.json'
    
    beginGrTrTss = numpy.empty(0,); endGrTrTss = numpy.empty(0,)
    for section_num in querySectionNums:
        beginGrTrTssCur, endGrTrTssCur = getGrTruthSegmentsForSection(URI_scorePath, URI_wholeAudio_noExt, URI_AudioSectionAnno, section_num)
        beginGrTrTss = numpy.concatenate([beginGrTrTss,beginGrTrTssCur]);
        endGrTrTss = numpy.concatenate([endGrTrTss,endGrTrTssCur]);  
    cardinality = len(beginGrTrTss)
    
    ######## 
    listDetectedTss = loadResults(URI_wholeAudio_noExt, querySectionNum)
    relevances = calcRelevance(listDetectedTss, beginGrTrTss, endGrTrTss, tolerance=3)
    aveP = calcAveragePrecisionAtK(relevances, K, cardinality)
    
    print beginGrTrTss
    print endGrTrTss
    print listDetectedTss
    print aveP 
    
    return aveP

def computeAverage(avePs):
    '''for list of Average Precisions for queries compute the average 
    '''    
    a = np.array([0, 0, 0.083, 0.083, 0.083, 0.15, 0.15, 0.15, 0.15, 0.15])
    b = np.array([0, 0, 0, 0.042, 0.042, 0.042, 0.042, 0.083, 0.083, 0.15])
    ab = np.vstack((a,b))
    avrg = 3* np.average(ab, axis=0)
    return avrg
    
if __name__ == "__main__":
    aveP = doitEval(sys.argv)
#     doitEval( ["dummy", 8, '/Users/joro/Documents/Phd/UPF/ISTANBUL/idil/Sakin--Gec--Kalma', 2]);
    
    