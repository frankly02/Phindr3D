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

import os
import re
import pandas as pd
import numpy as np

class DataFunctions:
    """Static methods for Metadata handling. Referenced from
    https://github.com/DWALab/Phindr3D/tree/9b95aebbd2a62c41d3c87a36f1122a78a21019c8/Lib
    and
    https://github.com/SRI-RSST/Phindr3D-python/blob/ba588bc925ef72c72103738d17ea922d20771064/phindr_functions.py
    No constructor. All parameters and methods are static.
    """

    @staticmethod
    def createMetadata(folder_path, regex, mdatafilename='metadata_python.txt'):
        """
        This function creates a metadata txt file in the same format as used in the matlab Phindr implementation

        folder_path: path to image folder (full or relative)
        regex: regular expression matching image file names. must include named groups for all required image attributes (wellID, field, treatment, channel, stack, etc.)
        Matlab style regex can be adapted by adding P before group names. ex. : "(?P<WellID>\w+)__(?P<Treatment>\w+)__z(?P<Stack>\d+)__ch(?P<Channel>\d)__example.tiff"
        mdatafilename: filename for metadatafile that will be written.

        regex groups MUST INCLUDE Channel and Stack and at least one other image identification group
        regex groups CANNOT include ImageID or _file.
        """

        f = os.listdir(folder_path)
        metadatafilename = f'{os.path.abspath(folder_path)}\\{mdatafilename}'
        #read images in folder
        rows = []
        for i, file in enumerate(f):
            m = re.fullmatch(regex, file)
            if m != None:
                d = m.groupdict()
                d['_file'] = os.path.abspath(f'{folder_path}\\{file}')
                rows.append(d)
        #make sure rows is not empty and that Channel and Stack are in the groups.
        if len(rows) == 0:
            print('\nFailed to create metadata. No regex matches found in folder.\n')
            return None
        if ('Channel' not in rows[0].keys()) or ('Stack' not in rows[0].keys()):
            print('\nFailed to create metadata. regex must contain "Channel" and "Stack" groups.')
            return None
        tmpdf = pd.DataFrame(rows)
        #make new dataframe with desired colummns
        tags = tmpdf.columns
        channels = np.unique(tmpdf['Channel'])
        cols = []
        for chan in channels:
            cols.append(f'Channel_{chan}')
        for tag in tags:
            if tag not in ['Channel', 'Stack', '_file']:
                cols.append(tag)
        cols.append('Stack')
        cols.append('MetadataFile')
        df = pd.DataFrame(columns=cols)
        #add data to the new dataframe
        stacksubset = [tag for tag in tags if tag not in ['Channel', '_file']]
        idsubset = [tag for tag in tags if tag not in ['Channel', '_file', 'Stack']]
        df[stacksubset] = tmpdf.drop_duplicates(subset = stacksubset)[stacksubset]
        df.reset_index(inplace=True, drop=True)
        #add unique image ids based on the "other tags"
        idtmp = tmpdf.drop_duplicates(subset = idsubset)[idsubset].reset_index(drop=True)
        idtmp.reset_index(inplace=True)
        idtmp.rename(columns={'index':'ImageID'}, inplace=True)
        idtmp['ImageID'] = idtmp['ImageID'] + 1
        df = pd.merge(df, idtmp, left_on=idsubset, right_on=idsubset)
        #give metadatafilename
        df['MetadataFile'] = metadatafilename
        # fill in file paths for each channel
        for chan in channels:
            chandf = tmpdf[tmpdf['Channel']==chan].reset_index(drop=True)
            df[f'Channel_{chan}'] = chandf['_file']
        df.to_csv(metadatafilename, sep='\t', index=False)
        print(f'Metadata file created at \n{metadatafilename}')


# end DataFunctions


