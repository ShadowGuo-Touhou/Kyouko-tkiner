#1.接收音乐文件
#2.提取封面，保存到cache
#3.删除封面

import os
from io import BytesIO
from PIL import Image
from mutagen.id3 import ID3

class CoverGetter(object):
    #Init------------------------------------------------------------------
    def __init__(self, path):
        self.__Cover_path = os.getcwd()+"/pre/cache/cover.png"
        self.generateCover(path)

    #Cover get-------------------------------------------------------------
    def generateCover(self, songpath):
        covertag = ID3(songpath)
        coverstream = covertag.get("APIC:").data
        cover = Image.open(BytesIO(coverstream))
        cover = cover.resize((356, 356))
        cover.save(os.getcwd()+"/pre/cache/cover.png", format="png")
    
    @property
    def Get_Cover(self):
        return self.__Cover_path
                
