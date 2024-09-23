from back.processor import Processor
from back.stats import Stats
from back.colorimetryN import Colorimetry

import os

if __name__ == '__main__':
    multi = [r'./CBERS_4A_WPM_20220803_211_144_L2_PP_BAND1.tif',
             r'./CBERS_4A_WPM_20220803_211_144_L2_PP_BAND2.tif',
             r'./CBERS_4A_WPM_20220803_211_144_L2_PP_BAND3.tif']
    pan = r'./CBERS_4A_WPM_20220803_211_144_L2_PP_BAND0.tif'
    outh = r'./teste.tif'

    # Processor().run(multi, pan, outh, Stats.pansharp)
    Processor().run(multi, pan, outh, Stats.pca)
    # Processor().run(multi, pan, outh, Colorimetry.hsv)
    
