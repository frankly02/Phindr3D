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
except ImportError:
    from VoxelBase import *

class SuperVoxelImage(VoxelBase):
    def __init__(self):
        super().__init__()
        self.superVoxelBinCenters = None # np array

    def getPixelBinCenters(self, x, metadata):
        # Creates x (tilesForTraining) based on data, then passes x with numBinCenters into getPixelBins
        # required parameters: pixelbincenters(voxels), randFieldID, metadata, image params (tileinfo)
        tilesForTraining = []
        # do stuff here

        # pass into getPixelBins
        self.superVoxelBinCenters = self.getPixelBins(tilesForTraining)


# end class SuperVoxelImage