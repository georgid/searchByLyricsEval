'''
Created on Jul 26, 2015

@author: joro
'''
from Evaluation import getGrTruthSegmentsForSection, calcRelevance

if __name__=="__main__":

    URI_scorePath = '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/ussak--sarki--aksak--bu_aksam_gun--tatyos_efendi' ;
    URI_AudioSectionAnno_noExt = '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data-synthesis/ussak--sarki--aksak--bu_aksam_gun--tatyos_efendi/Sakin--Gec--Kalma/Sakin--Gec--Kalma'
    URI_AudioSectionAnno = URI_AudioSectionAnno_noExt + '.sectionAnno.json'
    URI_wholeAudio_noExt = '/Users/joro/Documents/Phd/UPF/ISTANBUL/idil/Sakin--Gec--Kalma';
    SECTION_NUM = 3
    
    beginGrTrTss, endGrTrTss = getGrTruthSegmentsForSection(URI_scorePath, URI_wholeAudio_noExt, URI_AudioSectionAnno, SECTION_NUM) 
    
    listDetectedTss = []
    listDetectedTss.append((25.0,34.0))
    listDetectedTss.append((26.0,28.0))
    listDetectedTss.append((51.0,60.0))
    relevances = calcRelevance(listDetectedTss, beginGrTrTss, endGrTrTss)
    
    # should be 1, 0, 1
    print relevances