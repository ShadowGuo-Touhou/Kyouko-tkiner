import pygame.mixer as mx
import tkinter
from tkinter import END, INSERT, ttk
from os import getcwd, path
import Cover_Get, SoundList, Quick_GUI

class Kyouko():
    def __init__(self):
    #-----------------------------------------------MIXER------------------------------------------#
        mx.init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
        self.__counter = 0
        self.SongList = SoundList.SongList()
        self.__Flag_repeat = False
        self.__Flag_List = False
        self.__Flag_Shuffle = False
    #--------------------------------------------ROOT WINDOW---------------------------------------#
        self.ROOT = tkinter.Tk(screenName="Kyouko", className="TK")
        self.ROOT.title("Kyouko")
        self.ROOT.geometry(f"{500}x{500}+{self.ROOT.winfo_screenwidth()//2-250}+{self.ROOT.winfo_screenheight()//2-300}")
        self.ROOT.resizable(False,False)
        self.ROOT.iconbitmap(getcwd()+"/pre/favicon.ico")  

        self.DIRECTORY=""
    #----------------------------------------------MUSICBOX----------------------------------------#
        self.Musicbox_frame = ttk.Frame(self.ROOT)
        self.Musicbox = tkinter.Listbox(self.Musicbox_frame, height = 30, width=20, selectmode="extended")
        #scrollbars
        Musicbox_yscrollbar = ttk.Scrollbar(self.Musicbox_frame, orient="vertical",command= self.Musicbox.yview)
        Musicbox_xscrollbar = ttk.Scrollbar(self.Musicbox_frame, orient="horizontal",command= self.Musicbox.xview)
        self.Musicbox["yscrollcommand"] = Musicbox_yscrollbar.set
        self.Musicbox["xscrollcommand"] = Musicbox_xscrollbar.set
        #position
        self.Musicbox_frame.grid(row=0, column=0, rowspan=100)
        self.Musicbox.grid(row=0, column=0)
        Musicbox_yscrollbar.grid(row=0, column=1, sticky="NS")
        Musicbox_xscrollbar.grid(row=1, column=0, sticky="EW")

    #---------------------------------------------COVERIMAGE---------------------------------------#
        Cover_frame = ttk.Frame(self.ROOT, height=356, width=356)
        Cover = tkinter.PhotoImage(height=356, width=356)
        self.Cover_image = ttk.Label(Cover_frame,image=Cover, relief="groove")

        #position
        Cover_frame.grid(row=0, column=1, sticky="N", rowspan=2)
        Cover_frame.grid_propagate(False)
        self.Cover_image.grid(row=0, column=0)

    #-------------------------------------------CONTROL PANEL--------------------------------------#
        Control_frame_top = ttk.Frame(self.ROOT, height= 72, width=356)
        Control_frame_bottom = ttk.Frame(self.ROOT, height= 72, width=356)

    #Top panel-------------------------------------------------------------\\
        self.playbutton = tkinter.PhotoImage(file=getcwd()+"/pre/play.png")
        self.pausebutton = tkinter.PhotoImage(file=getcwd()+"/pre/pause.png")
        self.Control_play_pause = ttk.Button(Control_frame_top, image=self.pausebutton, command=self.Mixer_pause)
        self.repeat_off = tkinter.PhotoImage(file=getcwd()+"/pre/repeat.png")
        self.repeat_on = tkinter.PhotoImage(file=getcwd()+"/pre/repeat_on.png")
        self.Control_repeat = ttk.Button(Control_frame_top, image=self.repeat_off, command=self.Repeat)
        self.shuffle_off = tkinter.PhotoImage(file=getcwd()+"/pre/shuffle.png")
        self.shuffle_on = tkinter.PhotoImage(file=getcwd()+"/pre/shuffle_on.png")
        self.Control_shuffle = ttk.Button(Control_frame_top, image=self.shuffle_off, command=self.Shuffle)

        #display song name
        SongName_Frame = ttk.Frame(self.ROOT, width=400, height=20)
        self.SongName = ttk.Label(SongName_Frame, relief="solid", justify="center")

        #arrow
        next_arrow = tkinter.PhotoImage(file=getcwd()+"/pre/Go_right.png")
        self.Control_next = ttk.Button(Control_frame_top, image=next_arrow, command=lambda: self.Mixer_load(next(self.SongList)))
        last_arrow = tkinter.PhotoImage(file=getcwd()+"/pre/Go_left.png")
        self.Control_last = ttk.Button(Control_frame_top, image=last_arrow, command= lambda:self.Mixer_load(self.SongList.Last_song()))

    #Bottom panel----------------------------------------------------------
        listbutton = tkinter.PhotoImage(file=getcwd()+"/pre/list.png")
        self.Control_soundlist = ttk.Button(Control_frame_bottom, image=listbutton, command=self.Musicbox_update)
        addbutton = tkinter.PhotoImage(file=getcwd()+"/pre/add.png")
        self.Control_add = ttk.Button(Control_frame_bottom,image=addbutton, command=self.Musicbox_add)
        deletebutton = tkinter.PhotoImage(file=getcwd()+"/pre/delete.png")
        self.Control_delete = ttk.Button(Control_frame_bottom, image=deletebutton, command=self.Musicbox_delete)
        placeholder = ttk.Label(Control_frame_bottom, width=40)

        #position
        
        

        SongName_Frame.grid(row=2, column=1, columnspan=100)
        SongName_Frame.grid_propagate(False)
        self.SongName.place(y=10, x=176, anchor="center")

        Control_frame_top.grid(row=3, column=1, sticky="N")
        self.Control_shuffle.grid(row=1, column=0)
        self.Control_last.grid(row=1, column=1)
        self.Control_play_pause.grid(row=1, column=2, sticky="N")
        self.Control_next.grid(row=1, column=3)
        self.Control_repeat.grid(row=1, column=4)


        Control_frame_bottom.grid(row=4, column=1, sticky="N")
        self.Control_soundlist.grid(row=0, column=0, sticky="W",)
        placeholder.grid(row=0, column=1)
        self.Control_add.grid(row=0, column=4, sticky="W")
        self.Control_delete.grid(row=0, column=5, sticky="w")

        #---------------------------------------------Soundlist----------------------------------------#
        self.SoundList = SoundList.SoundList(self.ROOT)

        #command bind
        self.Musicbox.bind("<Double-Button-1>", self.Musicbox_choose)

        #Froze the button in case user make illegal operation
        self.__Button__Disable()
        self.ROOT.mainloop()

#----------------------------------------------FUNCTION----------------------------------------#

    #Display list----------------------------------------------------------\\
    def Musicbox_update(self):
        #get song list in dictionary
        temp_list = self.SoundList.List_read()
        #SongList flag
        self.__Flag_List = True
        #Set in List_mode
        self.SongList.SongList_generate(temp_list)
        #Unfrozen button
        self.__Button__Able()

        #update Musicbox content
        self.Musicbox_playlist = temp_list
        self._Musicbox_update()

    #Musicbox update-------------------------------------------------------\\
    def _Musicbox_update(self):
        self.SongList.Change_List(self.Musicbox_playlist)
        self.Musicbox.delete(0,END)
        for x in self.Musicbox_playlist.keys():
            self.Musicbox.insert(END, x)
        print("{} Songs loaded".format(len(self.Musicbox_playlist)))
        
    #Musicbox delete-------------------------------------------------------\\
    def Musicbox_delete(self):
        path = self.Musicbox.selection_get()
        self.Musicbox_playlist = self.SoundList.List_rewirte(path)
        self._Musicbox_update()
        
    #Musicbox add----------------------------------------------------------//
    def Musicbox_add(self):
        temp = Quick_GUI.Fileviewer(self.ROOT, "C:\\")
        SoundFile = temp.Return_File()
        self.Musicbox_playlist = self.SoundList.List_add(SoundFile)
        self._Musicbox_update()

    #Choose music in list--------------------------------------------------\\
    def Musicbox_choose(self, event):
        Music_file = self.Musicbox_playlist[self.Musicbox.selection_get()]
        self.Mixer_load(Music_file)
        
    #Display Cover---------------------------------------------------------\\
    def Cover_display(self, path):
        #pass in file path
            cover = Cover_Get.CoverGetter(path)
            cover = cover.Get_Cover
            cover = tkinter.PhotoImage(file=cover)
            self.Cover_image.config(image=cover)
    
    #Disable botton to prevent bugs-----------------------------------------\\
    def __Button__Disable(self):
        self.Control_shuffle.state(['disabled'])
        self.Control_last.state(['disabled'])
        self.Control_play_pause.state(["disabled"])
        self.Control_next.state(['disabled'])
        self.Control_repeat.state(['disabled'])
        self.Control_add.state(['disabled'])
        self.Control_delete.state(['disabled'])

    def __Button__Able(self):
        self.Control_shuffle.state(['!disabled'])
        self.Control_last.state(['!disabled'])
        self.Control_play_pause.state(["!disabled"])
        self.Control_next.state(['!disabled'])
        self.Control_repeat.state(['!disabled'])
        self.Control_add.state(['!disabled'])
        self.Control_delete.state(['!disabled'])

#------------------------------------------Mixer functions-------------------------------------#
    def Mixer_load(self, music):
        #Update current song in SongList
        self.SongList.Current = music.split("\\")[-1].split(".")[0]
        print(self.SongList.Current + " loaded")
        #get cover
        self.Cover_display(music)
        #Unpause
        if self.__counter % 2 ==1:
            self.Mixer_pause()
        #Display song name
        self.SongName.config(text=self.SongList.Current)

        mx.music.load(music)
        mx.music.play()

        #check if Songended
        self.Mixer_Song_end()

    def Mixer_pause(self):
        self.__counter += 1
        if self.__counter % 2 == 1:
            self.Control_play_pause.config(image=self.playbutton)
            mx.music.pause()
            self.ROOT.after_cancel(self.Mixer_Song_end_recursive_check)
        else:
            self.Control_play_pause.config(image=self.pausebutton)
            mx.music.unpause()
            self.Mixer_Song_end()

    #Song end--------------------------------------------------------------//
    def Mixer_Song_end(self):
        pos = mx.music.get_pos()
        #print(pos)
        if pos == -1:
            print("Song ended")
            self.Mixer_load(next(self.SongList))
        else:
            self.Mixer_Song_end_recursive_check = self.ROOT.after(3000, self.Mixer_Song_end)

#---------------------------------------------Play mode----------------------------------------#
    def Shuffle(self):
        #list on, repeat off, shuffle off
        if (self.__Flag_List == True and self.__Flag_repeat == False):
            self.SongList.Shuffle_mode()
            self.__Flag_List = False
            self.__Flag_Shuffle = True
            self.Control_shuffle.config(image=self.shuffle_on)
            
        #list on, repeat on, shuffle off
        elif (self.__Flag_List == True and self.__Flag_repeat == True):
            self.__Flag_List = False
            self.__Flag_Shuffle = True
            self.Control_shuffle.config(image=self.shuffle_on)
        
        #list off, repeat off, shuffle on
        elif (self.__Flag_List == False and self.__Flag_repeat == False):
            self.SongList.List_mode()
            self.__Flag_List = True
            self.__Flag_Shuffle = False
            self.Control_shuffle.config(image=self.shuffle_off)

        #list off, repeat on, shuffle on
        elif (self.__Flag_List == False and self.__Flag_repeat == True):
            self.__Flag_List = True
            self.__Flag_Shuffle = False
            self.Control_shuffle.config(image=self.shuffle_off)

    def Repeat(self):
        #list on, repeat off, shuffle off
        if (self.__Flag_List == True and self.__Flag_Shuffle == False and self.__Flag_repeat == False):
            self.SongList.Repeat_mode()
            self.__Flag_repeat = True
            self.Control_repeat.config(image=self.repeat_on)

        #list off, repeat off, shuffle on
        elif (self.__Flag_List == False and self.__Flag_Shuffle == True and self.__Flag_repeat == False):
            self.SongList.Repeat_mode()
            self.__Flag_repeat = True
            self.Control_repeat.config(image=self.repeat_on)

        #list on, repeat on, shuffle off
        elif (self.__Flag_List == True and self.__Flag_Shuffle == False and self.__Flag_repeat == True):
            self.SongList.List_mode()
            self.__Flag_repeat = False
            self.Control_repeat.config(image=self.repeat_off)


        #list on, repeat on, shuffle off
        elif (self.__Flag_List == False and self.__Flag_Shuffle == True and self.__Flag_repeat == True):
            self.SongList.Shuffle_mode()
            self.__Flag_repeat = False
            self.Control_repeat.config(image=self.repeat_off)

x = Kyouko()