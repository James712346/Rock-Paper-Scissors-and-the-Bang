import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import time
import os
try:
    from PIL import Image, ImageTk
except:
    print("Failed to load PIL library")
    print("You may need to install this library for the game to load pictures, use:")
    print("     python -m pip install Pillow")
    print("to install")

Moves =  ["Rock","Paper","Scissors", "Spock", "Lizard"] # make a Global list of moves
default_colour = "#fc752b" #Default orange background
default_key = ["1","2","3","4","5"] #Defualt Keybinds
class Settings_Window(tk.Toplevel): #<-- must use tk.Toplevel and not tk.Tk()
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent, bg=default_colour) #<-- can't use tk.Tk() again or the tk.StringVar() won't work!
        self.title("Settings") #set the title of the window
        self.maxsize(480,800) #sets the windows maxsize to 960x800
        self.Parent = parent
        self.keybinds = [self.keybind_setting(self,i) for i in range(0,5)]
        self.Reset_Keybinds = tk.Button(self, text="Reset Keybinds",font=("Calibri",20),bg="#ff9961", command=self.reset_keybinds)
        self.Reset_Data = tk.Button(self, text="Reset Data",font=("Calibri",20),bg="#ff9961", command=self.Parent.Reset_Data)
        self.Reset_Keybinds.grid(row=6, column=0, pady=(10,10), padx=(30,10))
        self.Reset_Data.grid(row=6, column=1, pady=(10,10), padx=(10,30))
        self.close_btn = tk.Button(self, text="Close",bg="#ff9961",font=("Calibri",20),command=self.close)
        self.close_btn.grid(row=7, pady=(10,10), columnspan=2)
        self.protocol("WM_DELETE_WINDOW", self.close)
    def close(self):
        self.Parent.Session = 1
        self.destroy()
    def reset_keybinds(self):
        for i in range(0, 5):
            self.keybinds[i].entry_text.set(default_key[i].upper())
            self.Parent.Human.Buttons[i].ChangeKeybind(default_key[i].lower())
    class keybind_setting():
        def __init__(self,parent,index):
            self.Parent = parent
            self.index = index
            self.keybind = self.Parent.Parent.Human.Buttons[self.index].keybind
            tk.Label(parent,bg=default_colour, text=Moves[index],font=("Calibri",40), width=6).grid(row=index, column=0, padx=(30, 10), pady=(5,5))
            self.entry_text = tk.StringVar() # the text in  your entry
            self.entry_text.set(self.keybind.upper())
            self.entry = tk.Entry(parent,width = 6,textvariable=self.entry_text,justify='center',bg="#ff9961",font=("Calibri",40))
            self.entry.grid(row=index, column=1, padx=(10,30), pady=(5,5)) # the entry
            self.entry_text.trace("w", self.character_limit)
            #self.entry_text.set("Test") <-- Trace pick this up!!!!
        def character_limit(self,x,y,z):
            if len(self.entry_text.get()) > 0:
                self.entry_text.set(self.entry_text.get()[-1].upper())
                self.Parent.Parent.Human.Buttons[self.index].ChangeKeybind(self.entry_text.get().lower())
            if self.entry_text.get() == "":
                self.Parent.Parent.Human.Buttons[self.index].ChangeKeybind(default_key[self.index])
            for i in self.Parent.keybinds:
                if i.keybind == self.entry_text.get() and self.entry_text.get() != "":
                    i.entry_text.set(self.keybind)
                    self.Parent.Parent.Human.Buttons[i.index].ChangeKeybind(self.keybind.lower())
            self.keybind = self.entry_text.get() if self.entry_text.get() != "" else default_key[self.index]

class Help_Window(tk.Toplevel):
    def __init__(self,parent):
        tk.Toplevel.__init__(self, parent, bg=default_colour)
        self.title("Instructions") #set the title of the window
        self.maxsize(960,800) #sets the windows maxsize to 960x800
        self.minsize(960,800)
        Title = tk.Label(self, text="Instructions", font=("Calibri",40), bg=default_colour)
        Title.grid(row=0)
        self.Parent = parent
        self.keybind = tk.Frame(self, relief='sunken',bd=2, bg= default_colour)
        self.Rules = tk.Frame(self, relief='sunken',bd=2, bg= default_colour)
        tk.Label(self.keybind, text="KeyBinds",  bg=default_colour,font=("Calibri",28)).grid(row=0,column=0, columnspan=2)
        tk.Label(self.Rules, text="Rules",  bg=default_colour,font=("Calibri",28)).grid(row=0,column=0)
        self.protocol("WM_DELETE_WINDOW", self.close)
        try:
            for move in self.Parent.Human.Buttons:
                tk.Label(self.keybind, text=Moves[move.index],justify='center', font=("Calibri",40), bg=default_colour).grid(row=move.index+1, column=0, sticky="nswe", padx=(10,10), pady=(5,5))
                tk.Label(self.keybind, text=move.keybind.upper(),justify='center', font=("Calibri",40), bg=default_colour).grid(row=move.index+1, column=1, sticky="nswe", padx=(10,10), pady=(5,5))
                tk.Label(self.Rules, text=Moves[move.index],justify='center', font=("Calibri",28), bg=default_colour, relief="raised", width=7).grid(row=move.index+1, column=0, sticky="nswe", padx=(10,10), pady=(5,5))
                tk.Label(self.Rules, text="wins against",justify='center', font=("Calibri",28), bg=default_colour).grid(row=move.index+1, column=1, sticky="nswe", pady=(5,5))
                wins = [Moves[move2] for move2 in range(0,5) if ((len(Moves) + move.index - move2)%len(Moves)%2)]
                tk.Label(self.Rules, text=wins[0],justify='center', font=("Calibri",28), bg=default_colour, relief="raised", width=7).grid(row=move.index+1, column=2, sticky="nswe", padx=(10,10), pady=(5,5))
                tk.Label(self.Rules, text=wins[1],justify='center', font=("Calibri",28), bg=default_colour, relief="raised", width=7).grid(row=move.index+1, column=3, sticky="nswe", padx=(10,10), pady=(5,5))
        except:
            Title.config(text="Welcome")
            for move in range(0,5):
                tk.Label(self.keybind, text=Moves[move],justify='center', font=("Calibri",40), bg=default_colour).grid(row=move+1, column=0, sticky="nswe", padx=(10,10), pady=(5,5))
                tk.Label(self.keybind, text=default_key[move],justify='center', font=("Calibri",40), bg=default_colour).grid(row=move+1, column=1, sticky="nswe", padx=(10,10), pady=(5,5))
                tk.Label(self.Rules, text=Moves[move],justify='center', font=("Calibri",28), relief="raised", bg=default_colour, width=7).grid(row=move+1, column=0, sticky="nswe", padx=(10,10), pady=(5,5))
                tk.Label(self.Rules, text="wins against",justify='center', font=("Calibri",28), bg=default_colour).grid(row=move+1, column=1, sticky="nswe", pady=(5,5))
                wins = [Moves[move2] for move2 in range(0,5) if ((len(Moves) + move - move2)%len(Moves)%2)]
                tk.Label(self.Rules, text=wins[0],justify='center', font=("Calibri",28), relief="raised", bg=default_colour, width=7).grid(row=move+1, column=2, sticky="nswe", padx=(10,10), pady=(5,5))
                tk.Label(self.Rules, text=wins[1],justify='center', font=("Calibri",28), relief="raised", bg=default_colour, width=7).grid(row=move+1, column=3, sticky="nswe", padx=(10,10), pady=(5,5))
        self.keybind.grid(rowspan=2, row=1, column=0, padx=(10,10))
        self.Rules.grid(row=1, column=1, padx=(10,10))
        self.Intructions = tk.Text(self, bd=2,font=("Calibri",19), width=46, height=10, bg=default_colour)
        self.Intructions.grid(rowspan=2,row=2, column=1, pady=(10,10))
        self.Intructions.insert(tk.END, "Instructions\nThe game is an expansion on the game Rock, Paper,\nScissors. Each player picks a variable and reveals it at the\nsame time. The winner is the one who defeats the others.\nTo Play/Pick a Move you must either use the set keybind\nfor the Move or click the Moves Button, the background\nalternates green or red depeneded on if you win or lose\nagainst the computer. The numbers under the moves\nshow the number of times in which that move has been\nused.")
        self.Intructions.config(state="disabled")
        self.close_btn = tk.Button(self, text="Close",bg="#ff9961",font=("Calibri",20),command=self.close)
        self.close_btn.grid(row=3,column=0, pady=(10,10))
        self.keybind.grid_columnconfigure(0, weight=1)
        self.keybind.grid_columnconfigure(1, weight=1)
    def close(self):
        self.Parent.Session = 1
        self.destroy()

class Move_Btn(tk.Frame):
    def __init__(self,parent,name,index, tall = 0, image=None, bind=None, Computer = False, *args, **kwargs):
        _colour = ["Brown","White","pink","green2","LightBlue1"]
        tk.Frame.__init__(self, parent.Parent,bg= _colour[index],width=50, *args, **kwargs) #Setup the main Frame (Class, root, background colour, width, [and any other arguments that could be called])
        self.Parent = parent
        self.index = index
        self.image = image
        self.keybind = bind
        self.Tall = tk.IntVar()
        self.Tall.set(tall)
        self.Title = ttk.Label(self, text=name, background=_colour[index],width=10,font=("Times", 20, "bold"), anchor='center')
        self.Tall_Label = ttk.Label(self, textvariable=self.Tall, background=_colour[index],font=("Times", 20, "bold"),width=10, anchor='center')
        self.Title.pack()
        self.Tall_Label.pack()
        if bind: #check if its the human's or computer's buttons (no images or binds means its a computer but if there are binds and images then thats means its a Humans)
            self.backup = tk.Frame(parent.Parent,bg= _colour[index],width=50, relief="raised", *args, **kwargs) #Making a direct copy of the self frame
            self.config(relief="raised")
            ttk.Label(self.backup, text=name, background=_colour[index],width=10,font=("Times", 20, "bold"), anchor='center').pack()
            ttk.Label(self.backup, textvariable=self.Tall, background=_colour[index],font=("Times", 20, "bold"),width=10, anchor='center').pack()
            self.backup.lower(self) #lowering it below the Mainframe, this object is to helps to hind the glitch of the frame disappearing for a second when the user hovers over it
            self.config(bd=2,relief="raised") #if it is the human's buttons then i enables the functions of click, hovering and keybinds
            self.Parent.Parent.Parent.bind(self.keybind, self.Play)
            self.bind('<Enter>', self.Entry)
            self.bind('<Leave>', self.Exit)
            [i.bind('<Button-1>', self.Play) for i in [self, self.Title, self.Tall_Label]]
            self.place(relx=(1/len(Moves)*self.index)+1/len(Moves)/2,anchor="n", y=10)
            self.backup.place(relx=(1/len(Moves)*self.index)+1/len(Moves)/2,anchor="n", y=10)
        else:
            self.place(relx=(1/len(Moves)*self.index)+1/len(Moves)/2,anchor="n",rely=1, y=-80)
    def Entry(self, Event):
        #self.Parent.Parent.Wait(0.1) #Giving the program time to catch up with the user by adding a delay to this event
        if "raised" in self.config()["relief"]: #if the relief configuration is set to raised then contiune
            self.config(relief="sunken", bd=2,width=50) #this makes sure that its not configuring the relief to the same value as i had some problem when it did

    def Exit(self, Event):
        #self.Parent.Parent.Wait(0.1) #Giving the program time to catch up with the user by adding a delay to this event
        if "sunken" in self.config()["relief"]: #if the relief configuration is set to sunken then contiune
            self.config(relief="raised", bd=2,width=50) #this makes sure that its not configuring the relief to the same value as i had some problem when it did

    def ChangeKeybind(self,key):
        self.Parent.Parent.Parent.unbind(self.keybind)
        self.keybind = key
        self.Parent.Parent.Parent.bind(self.keybind, self.Play)
        self.Parent.Parent.update()

    def Play(self, Opposition):
        self.Tall.set(self.Tall.get()+1)
        self.Parent.image.config(image=self.image)
        if self.keybind:
            Opposition = random.randint(0, 4)
            self.Parent.Parent.Computer.Buttons[Opposition].Play(self.index)
        self.Parent.wins.set(self.Parent.wins.get()+ ((len(Moves) + self.index - Opposition)%len(Moves)%2))
        self.Parent.Background_Change(default_colour if not (len(Moves) + self.index - Opposition)%len(Moves) else "Green" if (len(Moves) + self.index - Opposition)%len(Moves)%2 else "Red")
        if self.keybind:
            self.Parent.Parent.update()
            if self.Parent.Parent.Wait(5):
                self.Parent.Background_Change()
                self.Parent.Parent.Computer.Background_Change()


class Player(tk.Frame):
    def __init__(self, frame, parent, name, tall, wins, pictures=None,binds=None, *args, **kwargs):
        self.Border = tk.Frame(frame, background="#ff9961", bd=0, highlightthickness=0) #sets up a Frame to act like a Border and set the background colour to the wanted colour
        tk.Frame.__init__(self, self.Border, bg=default_colour, *args, **kwargs) #Setup the main Frame inside the border frame then packed with padding showing the desired border (this methord is used as tkinter adds a border on each side and we want it to only show on only some sides and not all of them)
        self.Name = name #sets class variable for the name
        self.Parent = parent # sets class variable for the Parent
        self.Background = tk.Label(parent,bg=default_colour, height=20, width=960)
        self.Background.lower(self.Border)
        self.image = tk.Label(self, image=parent.Global_Pictures[2], width=446, height=396, bg="#00d0d4") #IMAGE SHOULD BE 450X400
        self.wins = tk.IntVar()
        self.wins.set(wins)
        self.WinLbl = tk.Label(self.Parent, textvariable=self.wins,font=("Calibri",20),bg=default_colour)
        self.NameLbl = tk.Label(self.Parent, text=self.Name, font=("Calibri",20),bg=default_colour)
        if binds and pictures:
            self.Buttons = [Move_Btn(self, Moves[i], i, tall[i], pictures[i], binds[i]) for i in range(0,len(Moves))]
            self.image.pack(fill="both", padx=(20,10),pady=(10,30))
            self.pack(padx=(0, 4), pady=(0, 8))
            self.Background.place(relx=0)
            self.NameLbl.place(y=110, relx=0.5, anchor="center")
            self.WinLbl.place(y=150, relx=0.5, anchor="center")
        else:
            self.Buttons = [Move_Btn(self, Moves[i], i, tall[i], pictures[i]) for i in range(0,len(Moves))]
            self.image.pack(fill="both", padx=(10,20),pady=(30,10))
            self.pack(padx=(4, 0), pady=(8, 0))
            self.Background.place(rely=1, relx=0, anchor="sw")
            self.NameLbl.place(rely=1,y=-110, relx=0.5, anchor="center")
            self.WinLbl.place(rely=1,y=-150, relx=0.5, anchor="center")
        #setup the display feilds
        self.pack()
        self.Border.pack(side="left")

    def Background_Change(self,colour="#fc752b"):
        self.Background.config(bg=colour) #set the Background of the Buttons to colour
        self.config(bg=colour) #set the Background of the Players frame to colour
        self.NameLbl.config(bg=colour)
        self.WinLbl.config(bg=colour)
        pass

class PSRLS(tk.Frame):
    def __init__(self,parent,*args, **kwargs):
        tk.Frame.__init__(self, parent,*args, **kwargs) #Setup the main Frame (Class, root, [and any other arguments that could be called])
        self.Parent = parent # sets the root from where this class is being run from to self.parent
        self.Time = 0 #Sets self.time for the wait function to 0
        self.Session = 1 #sets variable called Session to 1 so that the program knows if either the help or setting window is open if not then this variable should be set to 1
        self.Parent.protocol("WM_DELETE_WINDOW", self.Exit)
        if not "psrls.txt" in os.listdir(): #Check in the psrls file is in the programs directory
            #if it isn't then it makes the file and assumes that this is the first time being run therefore the program will open the help window
            self.Parent.withdraw() #hides the main root window so only the help_window show
            self.Session = Help_Window(self) #call the help_window and set this class to self.session
            while self.Session != 1: #loops intill the help window closes
                self.Parent.update()
            self.Parent.deiconify() #Shows the root window after the closer of the help_window
            with open("psrls.txt","w") as file:
                file.write("0,0,0,0,0\n") #First line is the amount of times the human clicks a move (the values are in the same order as the temperary move list eg first value '0' is refering to the 0th element in the move list which is "Rock")
                file.write("0,0,0,0,0\n") #Second line is the amount of tume the computer clicks a move
                file.write("0,0\n") #Third line is for the wins, first value is for the human wins and second value is the computers wins
                file.write(",".join(default_key)) #forth and final line is the keybind that the user/program has set, deflaut is 1,2,3,4,5 (the keybinds are in the same order as the temperary move list eg first value '1' is refering to the 0th element in the move list which is "Rock")
                file.close() #Closes the file so that it can be reopen in a later on in the program
        with open("psrls.txt","r") as file: #opens the psrls file
            file = file.readlines() #places the lines into a list
            _humtall = [int(tall) for tall in file[0].strip().split(",")] #graps the first line and puts into a list of humtall (these are temperary variables of the number of time this move has been played)
            _comtall = [int(tall) for tall in file[1].strip().split(",")] #graps the second line and puts into a list of comtall (these are temperary variables of the number of time this move has been played)
            _wins = file[2].strip().split(",") #make a list out of the third line and set it to a temperary varibale
            _binds = file[3].strip().split(",") #sets the last line to a temperary variable of binds
        _pictures, self.Global_Pictures = self.GetPictures() #calls a class function of GetPictures which will either grab the pictures from the local directory or from the internet (my github repository) and return two list on of the moves pictures and the other of the Global Pictures
        PlayersFrame = tk.Frame(self) #sets up frame to contain the Human and Computers Classes
        self.Human = Player(PlayersFrame,self,"Human", _humtall, _wins[0], _pictures, _binds) #Calls the player function with values for the computer class
        self.Computer = Player(PlayersFrame,self,"Computer", _comtall, _wins[0], _pictures) #Calls the player function with values for the computer class
        self.settingbtn = tk.Button(self, image=self.Global_Pictures[0], command=self.settings, width=60, height=60) #sets up a button to open the settings window
        self.helpbtn = tk.Button(self, image=self.Global_Pictures[1],  command=self.help, width=60, height=60) #sets up a button to open the help window
        self.settingbtn.place(relx=0.05, x=10, y=130,  anchor="center") #Places the settings btn
        self.helpbtn.place(relx=0.95,x=-10, y=130,  anchor="center") #Places the help btn
        PlayersFrame.place(relx=0.5, rely=0.5, anchor='center') #places the Frame containing the Human's and Computer's Classes
    def Exit(self):
        if self.Session != 1: #if the self.Session isn't 1 and is set to the one of the windows
            self.Session.destroy() #Destroy the open window
        self.Parent.destroy() #Destroy the Main window

    def settings(self):
        if self.Session == 1: #if self.session is 1
            self.Session = Settings_Window(self) #call the settings_window and set this class to self.session
        else:
            messagebox.showerror("Session Error", "Either Help or Settings Window is alread open!") #else show an error expaining to the user that either the setting or help window is open
    def help(self):
        if self.Session == 1: #if self.session is 1
            self.Session = Help_Window(self) #call the Help_Window and set this class to self.session
        else:
            messagebox.showerror("Session Error", "Either Help or Settings Window is alread open!") #else show an error expaining to the user that either the setting or help window is open

    def Wait(self, t):
        _Time = time.time() + t #Sets a local variable only acceptable inside this function to the time.time() plus the number of seconds
        self.Time = time.time() + t #sets the class value called Time to the value of time.time() plus the number of seconds
        while _Time > time.time(): #loops intil the new time.time() is bigger than the local time variable
            self.Parent.update() #Updates the tk root class
        return self.Time == _Time #send back a bool depended on if the local time variable is equal to the class variable
    def Reset_Data(self):
        with open("psrls.txt","w") as file: #overwrites the original file
            file.write("0,0,0,0,0\n") #First line is the amount of times the human clicks a move (the values are in the same order as the temperary move list eg first value '0' is refering to the 0th element in the move list which is "Rock")
            file.write("0,0,0,0,0\n") #Second line is the amount of tume the computer clicks a move
            file.write("0,0\n") #Third line is for the wins, first value is for the human wins and second value is the computers wins
            file.write(",".join([str(button.keybind) for button in self.Human.Buttons])) #forth and final line is the keybind that the user/program has set, deflaut is 1,2,3,4,5 (the keybinds are in the same order as the temperary move list eg first value '1' is refering to the 0th element in the move list which is "Rock")
            file.close() #Closes the file so that it can be reopen in a later on in the program
        [button.Tall.set(0) for button in self.Human.Buttons]
        [button.Tall.set(0) for button in self.Computer.Buttons] #Sets all button's values for the number of plays
        self.Human.wins.set(0) #set the winning value for human to 0
        self.Computer.wins.set(0) #set the winning value for human to 0
        self.Human.Background_Change()
        self.Computer.Background_Change() #resets the background tot he default_colour
    def GetPictures(self):
        _ImgNames = Moves+["setting_icon","i_icon","Waiting"] #compinds two list together (List of moves, Other Pictures) to make a temperary variable for the names of pictures that need to be added
        _ImgObjects = [] #temperary variable for the functions/objects of pictures that will be returned once this function is over
        print("Loading Pictures...")
        for Img in _ImgNames: #Loop over all the name of pictures
            try:
                _ImgObjects.append(ImageTk.PhotoImage(Image.open(Img+".png"))) #grabs the local picture
            except: # if an error occurs then the program will atempt to grab the online version
                try:
                    import urllib.request as urllib #imports the urllib to grab the picture from te url
                    import io #imports the io library to convert the data from urllib to readable data for pillow library
                    _ImgObjects.append(ImageTk.PhotoImage(Image.open(io.BytesIO(urllib.urlopen("https://raw.githubusercontent.com/James712346/Rock-Paper-Scissors-and-the-Bang/master/"+Img+".png").read())))) #Grabs the Pictures from my github repository
                except:
                    _ImgObjects.append("Failed") #if the program fails to grab the image then it appends and prints into the console that the file has filed
                    print("Failed to load",Img+".png") #also when it time to display these images the program will note that the picture failed to load and will display text instead of the img
        print("Finished Loading pictures")
        return _ImgObjects[:-3], _ImgObjects[-3:]  #returns the ImgObjects
    def update(self):
        with open("psrls.txt","w") as file:
            file.write(",".join([str(button.Tall.get()) for button in self.Human.Buttons])+"\n") #Collects the number of plays from the Humans buttons and writes it to the file
            file.write(",".join([str(button.Tall.get()) for button in self.Computer.Buttons])+"\n") #Collects the number of plays from the Computers buttons and writes it to the file
            file.write(str(self.Human.wins.get())+","+str(self.Computer.wins.get())+"\n") #Collects the wins from the Human's and computer's win variable and writes it to the file
            file.write(",".join([str(button.keybind) for button in self.Human.Buttons])) #Grabs the keybinds values from the Human's Button and writes it to the file
            file.close() #Closes the file so that it can be reopen in a later on in the program #Closes the file so that it can be reopen in a later on in the program and writes it to the file

if __name__ == "__main__":
    root = tk.Tk("Main", "Rock, Paper, Scissors, and the Bang") #sets up the window and root
    root.maxsize(960,800) #sets the windows maxsize to 960x800
    root.minsize(960,800) #sets the windows minsize to 960x800
    root.title("Rock, Paper, Scissors, and the Bang") #set the title of the program
    PSRLS(root).pack(fill="both", expand=True) #calles the Paper, Scissors, Rock, Lizard and Spock class and then packs it
    root.mainloop() #runs a mainloop for the root file
