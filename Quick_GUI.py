from random import randint
import tkinter
from tkinter import END, ttk
import os
from tkinter.messagebox import showinfo
import SoundList

class Fileviewer():

    def __init__(self, MASTER, directory=os.environ["HOMEPATH"]):
    #------------------------------------------------MAIN-----------------------------------------------#
        #print("Filevier: invoke")
        self.Main = tkinter.Toplevel(master=MASTER)
        self.Main.resizable(False, False)
        self.Main.title("File selector")
        self.directory = directory
        
    #----------------------------------------------LISTBOX----------------------------------------------#

            #Listbox container
        ListBox_frame = ttk.Frame(self.Main, height=40, width=100)
            #ListBox components
        self.ListBox = tkinter.Listbox(ListBox_frame, selectmode="extended", width=90)
        listBox_scrollbar = ttk.Scrollbar(ListBox_frame, orient="vertical",command=self.ListBox.yview)
        self.ListBox['yscrollcommand'] = listBox_scrollbar.set

            #Layout
        ListBox_frame.grid(column=0, row = 1, columnspan=3)
        #ListBox_frame.pack(fill = tkinter.X)
        self.ListBox.grid(column=0, row=0, sticky="W")
        listBox_scrollbar.grid(column = 1, row = 0, sticky="NS")

    #---------------------------------------------DIRECTORY---------------------------------------------#
            #Directory containers
        Directory_frame = ttk.Frame(self.Main, height = 1, width=100)
            #Directory components
        self.Directory_box = tkinter.Text(Directory_frame, height=1, width=60)
        self.Directory_retrieve = ttk.Button(Directory_frame, text="back", width=5)
        self.Directory_go = ttk.Button(Directory_frame, text="yes", width=5)
        self.Directory_list = []
            #Layout
        Directory_frame.grid(column=0, row=0, columnspan=3)
        self.Directory_box.grid(column=1, row=0)
        self.Directory_retrieve.grid(column=0, row=0)
        self.Directory_go.grid(column=2, row=0)

    #------------------------------------------------File------------------------------------------------#
            #File container
        File_frame = ttk.Frame(self.Main, height=1, width=100)
            #File components
        self.File_box = tkinter.Text(File_frame, height=1, width=65)
        self.File_return = ttk.Button(File_frame, text = "go", width=5)

            #Layout
        File_frame.grid(column=0, row=2, columnspan=3)
        self.File_box.grid(column=0, row=0)
        self.File_return.grid(column=1, row=0)

        #command BIND----------------------------------------------------------
        self.Directory_retrieve.bind("<Button-1>", self.__Directory_box_retrieve)
        self.Directory_go.bind('<Button-1>', self.__Directory_Go)
        self.ListBox.bind("<Double-Button-1>", self.__Directory_change)
        self.ListBox.bind("<<ListboxSelect>>", self.__File_box_update)
        self.File_return.bind("<Button-1>", self.__File_Return)
        self.Main.protocol("WM_DELETE_WINDOW", self.__ON_CLOSING_MAIN)

        self.RETURNVAL = None
#----------------------------------------------COMMAND----------------------------------------------#
        

    #Listbox Update--------------------------------------------------------\\
    def __ListBox_update(self,directory):
        Files = os.listdir(directory)
        self.ListBox.delete(0, END)
        for i in Files:
            self.ListBox.insert(0, i)

        #print("LISTBOX UPDATE\n")


    #Directory box update--------------------------------------------------\\
    def __Directory_box_update(self, directory):
        self.Directory_box.delete("1.0", END)
        self.Directory_box.insert("1.0", directory)
        try:
            if self.Directory_list[len(self.Directory_list)-1] != directory:
                self.Directory_list.append(directory)
        except:
            self.Directory_list.append(directory)
        print(directory)

        #print("DIRECTORY BOX UPDATE\n")


    #Directory retrieve----------------------------------------------------\\
    def __Directory_box_retrieve(self, event):
        if len(self.Directory_list)-2 >= 0:
            self.Directory_list.pop()
            Directory_last = self.Directory_list[len(self.Directory_list)-1]

            #------------------------------------------\\
            self.Directory_box.delete("1.0", END)
            self.Directory_box.insert("1.0", self.Directory_list[len(self.Directory_list)-2])
            #print("DIRECTORY BOX RETRIEVE\n")
            #------------------------------------------\\

            self.__Directory_box_update(Directory_last)
            self.__ListBox_update(Directory_last)
        else:
            showinfo(title="Last Directory", message="This is the last directory!")
    


    #Directory go----------------------------------------------------------\\
    def __Directory_Go(self, event):
        Directory = (self.Directory_box.get("1.0", END)).strip("\n")
        if os.path.isdir(Directory) == True:
            self.__Directory_box_update(Directory)
            self.__ListBox_update(Directory)

        else:
            showinfo(title="No such file", message="No such file exists!")    

    #Get selected ListBox content------------------------------------------\\
    def __Curselection(self):
        selected_file = str(self.ListBox.get(self.ListBox.curselection()))
        return self.Directory_list[len(self.Directory_list)-1]+"\\"+selected_file

    #Directory change------------------------------------------------------\\
    def __Directory_change(self, event):
        File = self.__Curselection()
        File = File.strip("\n")
        if os.path.isdir(File) == True:
            try:
                self.__ListBox_update(File)
                self.__Directory_box_update(File)
            except WindowsError as a:
                showinfo(title="ERROR!", message=a)    

    #File box update-------------------------------------------------------\\

    def __File_box_update(self, event):
        self.File_box.delete("1.0", END)
        self.File_box.insert("1.0", self.__Curselection())
    

    #File return-----------------------------------------------------------\\
    def __File_Return(self, event):
        self.RETURNVAL = self.File_box.get("1.0", END)
        self.Main.quit()
        self.Main.destroy()
    
    def __ON_CLOSING_MAIN(self):
        self.Main.quit()
        self.Main.destroy()


    def Return_File(self):
        #Initiate ListBox
        self.__ListBox_update(self.directory)
        #Initiate Directory Box
        self.__Directory_box_update(self.directory)


        #Initiate window
        self.Main.mainloop()
        return self.RETURNVAL.strip("\n")




#---------------------------------------------New Class----------------------------------------#
class Check():
    def __init__(self, Master):
        self.Master = Master
        self.__MAIN = Master
        #self.__MAIN.withdraw()
        self.current = os.getcwd()
        
#-----------------------------------------------Yes/No-----------------------------------------#
    def __Button_Handler(self, choice):
        self.__Choice = False
        if choice == "yes":
            self.__Choice = True
        else:
            self.__Choice = False
        self.__Temp_window.quit()
        self.__Temp_window.destroy()
    
    def Check_whidow(self, operation):
        self.__Temp_window = tkinter.Toplevel(self.__MAIN)
        self.__Temp_window.geometry(f"{170}x{100}+{self.__MAIN.winfo_screenwidth()//2}+{self.__MAIN.winfo_screenheight()//2}")
        self.__Temp_window.title(operation)
        WORD = ttk.Label(self.__Temp_window, justify="center", text=operation)
        YES = ttk.Button(self.__Temp_window, text="yes", command=lambda:self.__Button_Handler("yes"))
        NO = ttk.Button(self.__Temp_window, text="NO", command=lambda:self.__Button_Handler("NO"))
        WORD.pack(side="top")
        YES.pack(side="left", ipady=30)
        NO.pack(side="right",ipady=30)

        self.__Temp_window.protocol("WM_DELETE_WINDOW", self.__ON_CLOSING_SAVE)
        self.__Temp_window.mainloop()
        return(self.__Choice)

    def __ON_CLOSING_SAVE(self):
        self.__Temp_window.quit()
        self.__Temp_window.destroy()


#-----------------------------------------------NAMER------------------------------------------#
    def NAME(self):
        self.__Temp_window2 = tkinter.Toplevel(self.__MAIN)
        self.__Temp_window2.geometry(f"{170}x{70}+{self.__MAIN.winfo_screenwidth()//2}+{self.__MAIN.winfo_screenheight()//2}")
        self.__Temp_window2.title("Name")
        tag = ttk.Label(self.__Temp_window2, text="Name of Songlist")
        frame = ttk.Frame(self.__Temp_window2, height=100, width=100)
        self.NameBox = tkinter.Text(frame, height=1, width=100)
        Send = ttk.Button(frame, text="Confirm", command=self.__Name_get)
        tag.pack()
        frame.pack()
        self.NameBox.pack(pady=1)
        Send.pack()

        self.__Temp_window2.protocol("WM_DELETE_WINDOW", self.__ON_CLOSING_NAME)
        self.__Temp_window2.mainloop()
        return self.__Name
    
    def __Name_get(self):
        Name = self.NameBox.get("1.0", END)
        if Name == "\n":
            self.__Name = "Songlist" + str(randint(0, 9999))
        else:
            self.__Name = Name.strip("\n")
        self.__Temp_window2.quit()
        self.__Temp_window2.destroy()
    
    def __ON_CLOSING_NAME(self):
        self.__Temp_window2.quit()
        self.__Temp_window2.destroy()

#----------------------------------------------Filelist----------------------------------------#

    def __Listbox_selected(self, event):
        selected_file = self.__Listbox.selection_get()+".json"
        self.__Songlist = self.Songlist_list[selected_file]
        self.__ListWindow.quit()
        self.__ListWindow.destroy()
    
    def __Listbox_add(self):
        #print("__Listbox_add: invoke")
        List_generate = SoundList.SoundList(self.__MAIN)
        temp = Fileviewer(self.Master, "C:/")
        directory = temp.Return_File()
        del temp
        if directory != None:
            List_generate.List_generate(directory)
            self.__Listbox_update()
        else: 
            print("__Listbox_add: Empty")
        
    def __Listbox_delete(self):
        self.Check_whidow("Do you want to delete this list")
        if self.__Choice == True:
            selected_file = self.__Listbox.selection_get()+".json"
            os.remove(self.Songlist_list[selected_file])
            self.__Listbox_update()
        
    #update the content of listbox
    def __Listbox_update(self):
        self.__Listbox.delete(0, END)
        songlist_raw = os.listdir(self.current + "/SongList")
        self.Songlist_list = {}
        for i in songlist_raw:
            self.Songlist_list[i] = self.current+"/SongList/"+i

        for i in self.Songlist_list:
            self.__Listbox.insert(END, i.split(".")[0])

    def LIST(self):
        self.__ListWindow = tkinter.Toplevel(self.__MAIN)
        #self.__ListWindow.geometry(f"{}x{70}+{self.__MAIN.winfo_screenwidth()//2-self.__MAIN.winfo_width()}+{self.__MAIN.winfo_screenheight()//2-self.__MAIN.winfo_height()}")
       
        #Listbox---------------------------------------------------------------//
        ListBox_Frame = ttk.Frame(self.__ListWindow, relief="sunken")
        self.__Listbox = tkinter.Listbox(ListBox_Frame, selectmode="extended", width=20, height=10)
        listBox_scrollbar = ttk.Scrollbar(ListBox_Frame, orient="vertical",command=self.__Listbox.yview)
        self.__Listbox['yscrollcommand'] = listBox_scrollbar.set
        #bind
        #print("LIST: invoke")
        self.__Listbox.bind("<Double-Button-1>", self.__Listbox_selected, add="+")
        #File load-------------------------------------------------------------
        addButton = tkinter.PhotoImage(file=self.current+"/pre/add.png")
        Listbox_add = tkinter.Button(self.__ListWindow, image=addButton, command= self.__Listbox_add)
        deleteButton = tkinter.PhotoImage(file=self.current+"/pre/delete.png")
        Listbox_delete = ttk.Button(self.__ListWindow, image=deleteButton, command= self.__Listbox_delete)

        #File delete-----------------------------------------------------------


        #position
        ListBox_Frame.pack()
        self.__Listbox.grid(column=0, row=0)
        listBox_scrollbar.grid(column=1, row=0, sticky="EW")
        Listbox_add.pack(side="left")
        Listbox_delete.pack(side="right")
        #ListBox Content-------------------------------------------------------
        self.__Listbox_update()

        #Return----------------------------------------------------------------
        
        self.__Songlist = None
        self.__ListWindow.mainloop()

        return self.__Songlist

    
        