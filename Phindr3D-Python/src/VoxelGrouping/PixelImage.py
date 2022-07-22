# Tentative Mega voxel class

try:
    from .VoxelGrouping import VoxelGrouping
    from ..Data import *
except ImportError:
    from VoxelGrouping import VoxelGrouping

class PixelImage(VoxelGrouping):
    def __init__(self):
        super().__init__()
        self.pixelBinCenters = None # np array

    def getPixelBinCenters(self, x, metadata, training):
        # required: randFieldID, metadata, image params (tileinfo)
        pixelsForTraining = np.zeros((300000, metadata.GetNumChannels()))
        startVal = 0
        endVal = 0
        for i, id in enumerate(metadata.getTrainingFields()):
            d = metadata.getImageInformation(metadata.GetImage(id))
            info = metadata.getTileInfo(d, metadata.theTileInfo)
            randZ = d[2] // 2
            iTmp = self.getTrainingPixels(metadata.GetImage(id), metadata, randZ, training, metadata.theTileInfo)
            pixelsForTraining[startVal:endVal+iTmp.shape[0], :] = iTmp
            startVal += iTmp.shape[0]
            endVal += iTmp.shape[0]
        pixelsForTraining = pixelsForTraining[np.sum(pixelsForTraining, axis=1) > 0, :]
        self.pixelBinCenters = self.getPixelBins(pixelsForTraining, metadata, self.numVoxelBins)

    def getTrainingPixels(self, image, metadata, randZ, training, tileinfo):
        slices = image.stackLayers.keys()
        slices = np.array([slices[i] for i in metadata.Generator.choice(len(slices), size=randZ, replace=False, shuffle=False)])
        trPixels = np.zeros((training.pixelsPerImage*randZ, metadata.GetNumChannels()))
        startVal = 0
        if metadata.intensityNormPerTreatment:
            grpVal = np.argwhere(metadata.GetTreatmentTypes() == image.GetTreatment()[0])
        slices = slices[0:(len(slices)//2)]
        for zplane in slices:
            croppedIM = np.zeros((tileinfo.origX, tileinfo.origY, metadata.GetNumChannels()))
            for jChan in range(metadata.GetNumChannels):
                if metadata.intensityNormPerTreatment:
                    img = image.stackLayers[zplane].channels[jChan + 1].channelPath
                    croppedIM[:,:, jChan] = training.rescaleIntensity(io.imread(img, '.tif'))  # add params later
                else:
                    img = image.stackLayers[zplane].channels[jChan + 1].channelPath
                    croppedIM[:,:, jChan] = training.rescaleIntensity(io.imread(img, '.tif'))  # add params later
            xEnd = -tileinfo.xOffsetEnd
            if xEnd == -0:
                xEnd = None
            yEnd = -tileinfo.yOffsetEnd
            if yEnd == -0:
                yEnd = None
            croppedIM = croppedIM[tileinfo.xOffsetStart:xEnd, tileinfo.yOffsetStart:yEnd, :]
            croppedIM = np.reshape(croppedIM, (tileinfo.croppedX*tileinfo.croppedY, metadata.GetNumChannels()))
            croppedIM = croppedIM[np.sum(croppedIM > metadata.intensityThreshold, axis=1) > metadata.GetNumChannels()/3, :]
            croppedIM = self.selectPixelsbyWeights(croppedIM)
            if croppedIM.shape[0] >= training.pixelsPerImage:
                trPixels[startVal:startVal + training.pixelsPerImage, :] = np.array([croppedIM[i,:] for i in metadata.Generator.choice(croppedIM.shape[0],size=training.pixelsPerImage, replace=False, shuffle=False)])
                startVal += croppedIM.shape[0]
        if trPixels.size == 0:
            trPixels = np.zeros((training.pixelsPerImage*randZ, metadata.GetNumChannels()))
        return trPixels

    def selectPixelsbyWeights(self, x):
        n, bin_edges = np.histogram(x, bins=(int(1/0.025) + 1), range=(0,1), )
        q = np.digitize(x, bin_edges)
        n = n / np.sum(n)
        p = np.zeros(q.shape)
        for i in range(0, n.shape[0]):
            p[q==i] = n[i]
        p = 1 - p
        p = np.sum(p>np.random.random((q.shape)), axis=1)
        p = p != 0
        p = x[p, :]
        return p