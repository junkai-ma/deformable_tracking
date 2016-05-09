import SampleLoc


class PartSamples:
    def __init__(self,objectLoc,sampleStyle = 'radial'):
        self.parts = []

        for eachpart in objectLoc.partsList:
            if sampleStyle == 'radial':
                samples = SampleLoc.RadialSample(eachpart,10,8)
            elif sampleStyle == 'pixel':
                samples = SampleLoc.PixelSample(eachpart,10,True)

            self.parts.append(samples)
        
    def GetOnePartFeature(self,index,imagerep):
        assert index < len(self.parts)
        
        featureValue = []

        for eachpart in self.parts[index]:
            featureValue.append(imagerep.Sum(eachpart))

        return featureValue


    def GetFeatureGroup(self,imagerep):
        self.featureGroup = []

        for (i,item) in enumerate(self.parts):
            self.featureGroup.append(self.GetOnePartFeature(i,imagerep))

