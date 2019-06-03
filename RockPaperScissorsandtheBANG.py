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
.place(relx=(1/len(self.Moves)*self.Player.Human.Buttons.index(Button))+1/len(self.Moves)/2
"""
Moves =  ["Rock","Paper","Scissors", "Spock", "Lizard"] # make a Global list of moves

class Move(tk.Frame):
    def __init__(self,parent,name,index,bind,image,tall = 0,disabled = False, *args, **kwargs):
        _colour = ["Brown","White","pink","green2","LightBlue1"]
        tk.Frame.__init__(self, parent,bg= _colour[index],width=50, *args, **kwargs) #Setup the main Frame (Class, root, background colour, width, [and any other arguments that could be called])
        self.Parent = parent
        self.index = index
        self.image = image
        self.Tall = tk.IntVar()
        self.Tall.set(tall)
        self.Title = ttk.Label(self, text=name, background=_colour[index],width=10,font=("Times", 20, "bold"), anchor='center')
        self.Tall_Label = ttk.Label(self, textvariable=self.Tall, background=_colour[index],font=("Times", 20, "bold"),width=10, anchor='center')
        self.Title.pack()
        self.Tall_Label.pack()
        self.Hover = False
        if not disabled:
            self.config(bd=2,relief="raised")
            self.bind('<Enter>', self.hover)
            self.bind('<Leave>', self.Exit)
            [i.bind('<Button-1>', self.play) for i in [self, self.Title, self.Tall_Label]]
    def hover(self, Event):
        self.Hover = True
        self.Parent.Wait(0.05)
        if self.Hover and "raised" in self.config()["relief"]:
            self.config(relief="sunken", bd=2,width=50)

    def Exit(self, Event):
        self.Hover = False
        self.Parent.Wait(0.05)
        if (not self.Hover) and "sunken" in self.config()["relief"]:
            self.config(relief="raised", bd=2,width=50)
    def play(self, Event):
        pass
class Player(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self, parent, *args, **kwargs) #Setup the main Frame (Class, root, [and any other arguments that could be called])

class PSRLS(tk.Frame):
    def __init__(self,parent,*args, **kwargs):
        tk.Frame.__init__(self, parent,*args, **kwargs) #Setup the main Frame (Class, root, [and any other arguments that could be called])
        self.parent = parent # sets the root from where this class is being run from to self.parent
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
            self.winstats = file[2].strip().split(",") #make a list out of the third line and set it to a self.winstats
            _binds = file[3].strip().split(",") #sets the last line to a temperary variable of binds
        _pictures, self.Global_Pictures = self.GetPictures() #calls a class function of GetPictures which will either grab the pictures from the local directory or from the internet (my github repository) and return two list on of the moves pictures and the other of the Global Pictures

        for i in range(0,5):
            Move(self, Moves[i], i, _binds[i], _pictures[i]).place(relx=(1/len(Moves)*i)+1/len(Moves)/2,anchor="n")

    def Wait(self, t, Global=False):
        if Global:
            self.Time = time.time() + t
        _Time = time.time() + t
        while _Time > time.time() and (Global == (self.Time == _Time)):
            if Global:
                self.parent.update()
        return

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

    def UpdateFile(self):
        with open("psrls.txt","w") as file:
            file.write(",".join([str(tall.Clicks.config()["text"][-1]) for tall in self.Player.Human.Buttons])+"\n")
            file.write(",".join([str(tall.Clicks.config()["text"][-1]) for tall in self.Player.Computer.Buttons])+"\n")
            file.write(str(self.Player.Human.wins)+","+str(self.Player.Computer.wins)+"\n")
            file.write(",".join(self.Binds))
            file.close()
        if self.Player.Human.wins+self.Player.Computer.wins:
            self.Player.Human.winper.set(int(round(self.Player.Human.wins / (self.Player.Human.wins+self.Player.Computer.wins),2)*100))
            self.Player.Computer.winper.set(int(round(self.Player.Computer.wins / (self.Player.Human.wins+self.Player.Computer.wins),2)*100))

if __name__ == "__main__":
    root = tk.Tk() #sets up the window and root
    root.maxsize(960,800) #sets the windows maxsize to 960x800
    root.minsize(960,800) #sets the windows minsize to 960x800
    root.title("Rock, Paper, Scissors, and the Bang") #set the title of the program
    PSRLS(root).pack( fill="both", expand=True) #calles the Paper, Scissors, Rock, Lizard and Spock class and then packs it
    root.mainloop() #runs a mainloop for the root file
