# Copyright (C) 2022 Sunnybrook Research Institute
# This file is part of src <https://github.com/DWALab/Phindr3D>.
#
# src is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# src is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with src.  If not, see <http://www.gnu.org/licenses/>.

try:
    from .VoxelBase import *
    from ..Data import *
    from .SuperVoxelImage import *
except ImportError:
    from VoxelBase import *

class MegaVoxelImage(VoxelBase):
    def __init__(self):
        super().__init__()
        self.megaVoxelBinCenters = None # np array

    def getMegaVoxelBinCenters(self, metadata, training, pixelImage):
        # Same as getSuperVoxelBinCenters, but mega
        # required: randFieldID, metadata, supervoxels, image params (tileinfo)
        megaVoxelsforTraining = []
        for id in training.randFieldID:
            d = metadata.getImageInformation(metadata.GetImage(id))
            info = metadata.getTileInfo(d, metadata.theTileInfo)
            pixelCenters = pixelImage.getPixelBinCenters(3, metadata, training)
            pixelBinCenterDifferences = np.array([DataFunctions.mat_dot(pixelCenters, pixelCenters, axis=1)]).T
            superVoxelProfile, fgSuperVoxel = self.getTileProfiles(metadata.GetImage(id), pixelCenters, pixelBinCenterDifferences, info)
            superVoxel = SuperVoxelImage()
            superVoxel.getSuperVoxelBinCenters(metadata, training, pixelImage)
        # megaVoxelBinCenters is an np array that represents the megavoxels
        self.megaVoxelBinCenters = self.getPixelBins(megaVoxelsforTraining)

    def getMegaVoxelProfile(self, tileProfile, info, fgSuperVoxel, metadata, training, superVoxel, analysis=False):
        # function called in getMegaVoxelBinCenters
        temp1 = np.array([DataFunctions.mat_dot(superVoxel.superVoxelBinCenters, superVoxel.superVoxelBinCenters, axis=1)]).T
        temp2 = DataFunctions.mat_dot(tileProfile[fgSuperVoxel], tileProfile[fgSuperVoxel], axis=1)
        a = np.add(temp1, temp2).T - 2*(tileProfile[fgSuperVoxel] @ superVoxel.superVoxelBinCenters.T)
        minDis = np.argmin(a, axis=1) + 1 # mindis+1 here
        x = np.zeros(tileProfile.shape[0], dtype='uint8')
        x[fgSuperVoxel] = minDis
        # had to change x shape here from matlab form to more numpy like shape
        x = np.reshape(x, (int(info.croppedZ/info.tileZ), int(info.croppedX/info.tileX), int(info.croppedY/info.tileY)))
        # pad first dimension
        x = np.concatenate([np.zeros((info.superVoxelZAddStart, x.shape[1], x.shape[2])), x, np.zeros((info.superVoxelZAddEnd, x.shape[1], x.shape[2]))], axis=0)
        # pad second dimension
        x = np.concatenate([np.zeros((x.shape[0], info.superVoxelXAddStart, x.shape[2])), x, np.zeros((x.shape[0], info.superVoxelXAddEnd, x.shape[2]))], axis=1)
        # pad third dimension
        x = np.concatenate([np.zeros((x.shape[0], x.shape[1], info.superVoxelYAddStart)), x, np.zeros((x.shape[0], x.shape[1], info.superVoxelYAddEnd))], axis=2)
        x = x.astype(np.uint8)
        # question: where is megaVoxelTile info?: In metadata class tileinfo, not info
        mvTileInfo = metadata.theTileInfo
        self.numMegaVoxelX = x.shape[1]//mvTileInfo.megaVoxelTileX
        self.numMegaVoxelY = x.shape[2]//mvTileInfo.megaVoxelTileY
        self.numMegaVoxelZ = x.shape[0]//mvTileInfo.megaVoxelTileZ
        mvTileInfo.numMegaVoxelsXY = int(x.shape[1] * x.shape[2] / (mvTileInfo.megaVoxelTileY * mvTileInfo.megaVoxelTileX))
        mvTileInfo.numMegaVoxels = int((mvTileInfo.numMegaVoxelsXY*x.shape[0])/mvTileInfo.megaVoxelTileZ)
        sliceCounter = 0
        startVal = 0
        endVal = mvTileInfo.numMegaVoxelsXY
        try:
            megaVoxelProfile = np.zeros((mvTileInfo.numMegaVoxels, self.numSuperVoxelBins + 1))
        except Exception as e:
            print(e)
            raise(e)
        fgMegaVoxel = np.zeros(mvTileInfo.numMegaVoxels)
        tmpData = np.zeros((mvTileInfo.numMegaVoxelsXY, int(mvTileInfo.megaVoxelTileX*mvTileInfo.megaVoxelTileY*mvTileInfo.megaVoxelTileZ)))
        startCol = 0
        endCol = (mvTileInfo.megaVoxelTileX * mvTileInfo.megaVoxelTileY)
        for iSuperVoxelImagesZ in range(0, x.shape[0]):
            sliceCounter += 1
            tmpData[:, startCol:endCol] = VoxelFunctions.im2col(x[iSuperVoxelImagesZ, :, :], (mvTileInfo.megaVoxelTileX, mvTileInfo.megaVoxelTileY)).T
            startCol += (mvTileInfo.megaVoxelTileX * mvTileInfo.megaVoxelTileY)
            endCol += (mvTileInfo.megaVoxelTileX * mvTileInfo.megaVoxelTileY)
            if sliceCounter == mvTileInfo.megaVoxelTileZ:
                fgMegaVoxel[startVal:endVal] = (np.sum(tmpData!=0, axis=1)/tmpData.shape[1]) >= training.megaVoxelThresholdTuningFactor
                for i in range(0, self.numSuperVoxelBins+1):
                    megaVoxelProfile[startVal:endVal, i] = np.sum(tmpData == i, axis=1)
                sliceCounter = 0
                tmpData = np.zeros((mvTileInfo.numMegaVoxelsXY, mvTileInfo.megaVoxelTileX*mvTileInfo.megaVoxelTileY*mvTileInfo.megaVoxelTileZ))
                startCol = 0
                endCol = (mvTileInfo.megaVoxelTileX*mvTileInfo.megaVoxelTileY)
                startVal += mvTileInfo.numMegaVoxelsXY
                endVal += mvTileInfo.numMegaVoxelsXY

# end class MegaVoxelImage