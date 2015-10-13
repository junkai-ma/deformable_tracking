class Config:
    
    def __init__(self,path):
        self.config_paras = {}
        self.config_paras['quietMode'] = False
        self.config_paras['debugMode'] = False
        self.config_paras['sequencePath'] = ''
        #self.config_paras['sequenceName'] = ''
        self.config_paras['resultsPath'] = ''
        
        self.config_paras['framesWidth'] = 320
        self.config_paras['framesHeight'] = 240

        self.config_paras['seed'] = 0
        self.config_paras['searchRadius'] = 30
        self.config_paras['svmC'] = 1.0
        self.config_paras['svmBudgetSize'] = 0

        self.config_paras['initBBox'] = []
        self.config_paras['features'] = []

        for eachLine in open(path,'r'):
            eachLine = eachLine.strip(' ')
            eachLine = eachLine.strip('\t')
            eachLine = eachLine.rstrip('\n')
            if len(eachLine) < 1:
                continue
            if eachLine[0] == '#':
                continue 
            feature = eachLine.split(' ')
            if feature[1] != '=':
                continue
            if feature[0] == 'seed':
                self.config_paras['seed'] = feature[2]
            elif feature[0] == 'quietMode':
                self.config_paras['quietMode'] = feature[2]
            elif feature[0] == 'debugMode':
                self.config_paras['debugMode'] = feature[2]
            elif feature[0] == 'sequencePath':
                self.config_paras['sequencePath'] = feature[2]
            #elif feature[0] == 'sequenceName':
                #self.config_paras['sequenceName'] = feature[2]
            elif feature[0] == 'resultsPath':
                self.config_paras['resultsPath'] = feature[2]
            elif feature[0] == 'framesWidth':
                self.config_paras['resultsWidth'] = feature[2]
            elif feature[0] == 'framesHeight':
                self.config_paras['resultsHeight'] = feature[2]
            elif feature[0] == 'searchRadius':
                self.config_paras['searchRadius'] = feature[2]
            elif feature[0] == 'svmC':
                self.config_paras['svmC'] = feature[2]
            elif feature[0] == 'svmBudgetSize':
                self.config_paras['svmBudgetSize'] = feature[2]
            elif feature[0] == 'feature':
                #print feature
                temp_feature = {'featureType':feature[2],
                                'kernalType':feature[3],
                                'params':[feature[4],]}
                self.config_paras['features'].append(temp_feature)
            elif feature[0] == 'bbox':
                feature[2] = feature[2].lstrip('[')
                feature[2] = feature[2].rstrip(']')
                value = feature[2].split(',')
                for item in value:
                    self.config_paras['initBBox'].append(int(item))
            elif feature[0] == 'startFrame':
                self.config_paras['startFrame'] = int(feature[2])
            elif feature[0] == 'endFrame':
                self.config_paras['endFrame'] = int(feature[2])
            else:
                continue

    def showParas(self):
        print self.config_paras
            
if __name__ == '__main__':
    m_config = Config('mytext.txt')
    print m_config.config_paras
