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
"""
self.Parent.Parent.pack_forget() <- restart the view
"""
Moves =  ["Rock","Paper","Scissors", "Spock", "Lizard"] # make a Global list of moves
default_colour = "#fc752b"

class Move(tk.Frame):
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
        self.bind = key
        self.Parent.Parent.Parent.bind(self.keybind, self.Play)

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
        self.Border = tk.Frame(frame, background="#ff9961", bd=0, highlightthickness=0)
        tk.Frame.__init__(self, self.Border, bg=default_colour, *args, **kwargs) #Setup the main Frame (Class, root, [and any other arguments that could be called])
        self.Name = name
        self.Parent = parent
        self.Background = tk.Label(parent,bg=default_colour, height=20, width=960)
        self.Background.lower(self.Border)
        self.image = tk.Label(self, image=parent.Global_Pictures[2], width=446, height=396, bg="#00d0d4") #IMAGE SHOULD BE 450X400
        self.wins = tk.IntVar()
        self.wins.set(wins)
        if binds and pictures:
            self.Buttons = [Move(self, Moves[i], i, tall[i], pictures[i], binds[i]) for i in range(0,len(Moves))]
            self.image.pack(fill="both", padx=(20,10),pady=(10,30))
            self.pack(padx=(0, 4), pady=(0, 8))
            self.Background.place(relx=0)
        else:
            self.Buttons = [Move(self, Moves[i], i, tall[i], pictures[i]) for i in range(0,len(Moves))]
            self.image.pack(fill="both", padx=(10,20),pady=(30,10))
            self.pack(padx=(4, 0), pady=(8, 0))
            self.Background.place(rely=1, relx=0, anchor="sw")

        #setup the display feilds
        self.pack()
        self.Border.pack(side="left")

    def Background_Change(self,colour="#fc752b"):
        self.Background.config(bg=colour)
        self.config(bg=colour)
        pass

class PSRLS(tk.Frame):
    def __init__(self,parent,*args, **kwargs):
        tk.Frame.__init__(self, parent,*args, **kwargs) #Setup the main Frame (Class, root, [and any other arguments that could be called])
        self.Parent = parent # sets the root from where this class is being run from to self.parent
        self.Time = 0 # Sets self.time for the wait function to 0
        if not "psrls.txt" in os.listdir(): #Check in the psrls file is in the programs directory
            #if it isn't then it makes the file
            with open("psrls.txt","w") as file:
                file.write("0,0,0,0,0\n") #First line is the amount of times the human clicks a move (the values are in the same order as the temperary move list eg first value '0' is refering to the 0th element in the move list which is "Rock")
                file.write("0,0,0,0,0\n") #Second line is the amount of tume the computer clicks a move
                file.write("0,0\n") #Third line is for the wins, first value is for the human wins and second value is the computers wins
                file.write("1,2,3,4,5") #forth and final line is the keybind that the user/program has set, deflaut is 1,2,3,4,5 (the keybinds are in the same order as the temperary move list eg first value '1' is refering to the 0th element in the move list which is "Rock")
                file.close() #closes the file
        with open("psrls.txt","r") as file: #opens the psrls file
            file = file.readlines() #places the lines into a list
            _humtall = [int(tall) for tall in file[0].strip().split(",")] #graps the first line and puts into a list of humtall (these are temperary variables)
            _comtall = [int(tall) for tall in file[1].strip().split(",")] #graps the second line and puts into a list of comtall (these are temperary variables)
            _wins = file[2].strip().split(",") #make a list out of the third line and set it to a temperary varibale
            _binds = file[3].strip().split(",") #sets the last line to a temperary variable of binds
        _pictures, self.Global_Pictures = self.GetPictures() #calls a class function of GetPictures which will either grab the pictures from the local directory or from the internet (my github repository) and return two list on of the moves pictures and the other of the Global Pictures
        PlayersFrame = tk.Frame(self)
        self.Human = Player(PlayersFrame,self,"Human", _humtall, _wins[0], _pictures, _binds)
        self.Computer = Player(PlayersFrame,self,"Computer", _comtall, _wins[0], pictures=_pictures)
        PlayersFrame.place(relx=0.5, rely=0.5, anchor='center')

    def Wait(self, t):
        _Time = time.time() + t
        self.Time = time.time() + t

        while _Time > time.time():
            self.Parent.update()
        return self.Time == _Time

    def GetPictures(self):
        _ImgNames = Moves+["i_icon","setting_icon","Waiting"] #compinds two list together (List of moves, Other Pictures) to make a temperary variable for the names of pictures that need to be added
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
            file.write(",".join([str(button.Tall.get()) for button in self.Human.Buttons])+"\n")
            file.write(",".join([str(button.Tall.get()) for button in self.Computer.Buttons])+"\n")
            file.write(str(self.Human.wins.get())+","+str(self.Computer.wins.get())+"\n")
            file.write(",".join([str(button.keybind) for button in self.Human.Buttons]))
            file.close()

if __name__ == "__main__":
    root = tk.Tk() #sets up the window and root
    root.maxsize(960,800) #sets the windows maxsize to 960x800
    root.minsize(960,800) #sets the windows minsize to 960x800
    root.title("Rock, Paper, Scissors, and the Bang") #set the title of the program
    PSRLS(root).pack( fill="both", expand=True) #calles the Paper, Scissors, Rock, Lizard and Spock class and then packs it
    root.mainloop() #runs a mainloop for the root file
