
from operator import indexOf
import os, sys
from tabnanny import check
import tkinter
import json
from typing import List
import Quick_GUI
from random import shuffle

class SoundList(object):
#----------------------------------------------Iintiate----------------------------------------#
    def __init__(self, Master, Directory = os.environ["HOMEPATH"]):
        self.Master = Master
        self.Directory = Directory
        self.Current = os.getcwd()
        self.QuickGUI = Quick_GUI.Check(Master)

#-------------------------------------------List generate--------------------------------------#
    def List_generate(self, Directory):
        List = []
        self.SongList = {}
        for x in os.listdir(Directory):
            if x.endswith(".mp3") or x.endswith(".wav")== True:

                self.SongList[x.split(".")[0]] = Directory + "\\" + x

        print("{} Songs generated.".format(len(self.SongList)))
        self.List_save()

    def List_add(self, File):
        if File.endswith("mp3") or File.endswith("wav") == True:
            self.__Songlist[(File.split("\\")[-1]).split(".")[0]] = File
            with open(self.__loaded_list, "w") as Rewrite:
                json.dump(self.__Songlist, Rewrite)
            return self.__Songlist

#---------------------------------------------List Save----------------------------------------#
    def List_save(self):
        name = self.QuickGUI.NAME()
        if os.path.exists(self.Current + "/SongList") == False:
            os.makedirs(self.Current + "/SongList")
        with open(self.Current + "/SongList/"+name+".json","w") as NewList:
            json.dump(self.SongList, NewList)
        print("List {} generated".format(name))

    def List_rewirte(self, deletefile):
        choice = self.QuickGUI.Check_whidow("Do you want to delete this song?")
        if choice == True:
            del self.__Songlist[deletefile]
            with open(self.__loaded_list, "w") as Rewrite:
                json.dump(self.__Songlist, Rewrite)
            return self.__Songlist

#---------------------------------------------List Load----------------------------------------#
    def List_read(self):
        Songlist_json = self.QuickGUI.LIST()
        if Songlist_json.split(".")[1] == "json":
            self.__loaded_list = Songlist_json
            with open(Songlist_json) as F:
                self.__Songlist = json.load(F)
            return self.__Songlist
        else: 
            print("List_read: Empty")        


#----------------------------------------------SongList----------------------------------------#
class SongList(object):

    #initial---------------------------------------------------------------//
    def __init__(self):
        self.__List_Onloaded = None
        self.__List_Original = None
        self.__List_Shuffled = None
        self.__Flag__Listed = False
        self.__Flag__shuffled = False
    #Iter------------------------------------------------------------------\\
    def __iter__(self):
        return self.__List_Onloaded
    
    #SongList_Create-------------------------------------------------------//
    def SongList_generate(self, SongDict):
        self.__SongDict = SongDict
        self.__List_Original = [x for x in SongDict.keys()]
        self.__Current = self.__List_Original[0]
        self.List_mode()
    
    def Change_List(self, SongDict):
        self.__SongDict = SongDict
        self.__List_Original = [x for x in SongDict.keys()]
        if self.__Flag__Listed == True:
            self.List_mode()
        elif self.__Flag__shuffled == True:
            self.Shuffle_mode()

    #return next song------------------------------------------------------
    def __next__(self):
        length = len(self.__List_Onloaded)
        index = indexOf(self.__List_Onloaded, self.__Current)
        index = (index+1) % length
        self.__Current = self.__List_Onloaded[index]
        return self.__SongDict[self.__List_Onloaded[index]]

    #return last song------------------------------------------------------
    def Last_song(self):
        length = len(self.__List_Onloaded)
        index = indexOf(self.__List_Onloaded, self.__Current)
        if index - 1 == -1: index = length-1
        else: index -= 1
        return self.__SongDict[self.__List_Onloaded[index]]

    #Record----------------------------------------------------------------
    @property
    def Current(self):
        return self.__Current

    @Current.setter
    def Current(self, song):
        self.__Current = song

    @property
    def SongList(self):
        return self.__List_Shuffled

    #Sequence list---------------------------------------------------------
    def List_mode(self):
        #flag
        self.__Flag__Listed, self.__Flag__shuffled = True, False

        self.__List_Onloaded = self.__List_Original
        print("List_mode on gear")

    #repeat----------------------------------------------------------------
    def Repeat_mode(self):
        self.__List_Onloaded = [self.__Current]
        print("Repeat_mode on gear")

    #shuffle---------------------------------------------------------------
    def Shuffle_mode(self):
        #flag
        self.__Flag__Listed, self.__Flag__shuffled = False, True
        self.__List_Onloaded = self.__List_Original[0:]
        shuffle(self.__List_Onloaded)
        print("Shuffle_mode on gear")
        
#mx.List_mode()
#for i in range(100):
 #   a = next(mx)
#
