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
    from .PixelImage import *
    from ..Data import *
except ImportError:
    from PixelImage import *
    from src.Data import *

class SuperVoxelImage(VoxelBase):
    def __init__(self):
        super().__init__()
        self.superVoxelBinCenters = None # np array

    def getSuperVoxelBinCenters(self, metadata, training):
        # Same as getPixelBinCenters, but super
        # required: randFieldID, metadata, pixels, image params (tileinfo)
        pixelCenters = PixelImage.getPixelBinCenters(3, metadata, training)
        pixelBinCenterDifferences = np.array([DataFunctions.mat_dot(pixelCenters, pixelCenters, axis=1)]).T
        tilesForTraining = []
        for id in training.randFieldID:
            d = metadata.getImageInformation(metadata.GetImage(id))
            info = metadata.getTileInfo(d, metadata.theTileInfo)
            superVoxelProfile, fgSuperVoxel = self.getTileProfiles(metadata.GetImage(id), metadata, training)
            

        # pass into getPixelBins
        self.superVoxelBinCenters = self.getPixelBins(tilesForTraining)


# end class SuperVoxelImage