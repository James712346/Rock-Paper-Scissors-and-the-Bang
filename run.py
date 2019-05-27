import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import time
import os
default_colour = "#fc752b"

class Border(ttk.Frame):
    def __init__(self, master, bordercolor=None, borderleft=0, bordertop=0, borderright=0, borderbottom=0, interiorwidget=tk.Frame, **kwargs):
        tk.Frame.__init__(self, master, background=bordercolor, bd=0, highlightthickness=0)
        self.interior = interiorwidget(self)
        self.interior.grid(padx=(borderleft, borderright), pady=(bordertop, borderbottom))
        self.grid(**kwargs)

class TheMove(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.waiting = ImageTk.PhotoImage(Image.open("Waiting.png"))
        self.image = tk.Label(self, image=self.waiting, width=446, height=396, bg="#00d0d4") #IMAGE SHOULD BE 450X400

class Button_Card(tk.Frame):
    def __init__(self, parent, Name, clicks, index, disabled = False, *args, **kwargs):
        Colours = ["Brown","White","pink","green2","LightBlue1"]
        tk.Frame.__init__(self, parent,bg=Colours[index],width=50, *args, **kwargs)
        self.parent = parent
        self.index = index
        self.title = ttk.Label(self, text=Name, background=Colours[index],width=10,font=("Times", 20, "bold"), anchor='center')
        self.title.pack()
        self.Clicks = ttk.Label(self, text=clicks, background=Colours[index],font=("Times", 20, "bold"),width=10, anchor='center')
        self.Clicks.pack()
        if not disabled:
            self.config(bd=1,relief="raised")
            self.bind('<Enter>', self.hover)
            self.bind('<Leave>', self.Exit)
            [i.bind('<Button-1>', self.click) for i in [self, self.title, self.Clicks]]
    def Play(self, *args, **kwargs):
        self.parent.Play(self.index)
    def add1(self):
        self.Clicks.config(text=self.Clicks.config()["text"][-1]+1)
    def hover(self, Event):
        self.config(relief="sunken",bd=1)
    def Exit(self, Event):
        self.config(relief="raised",bd=1)
    def click(self, Event):
        self.parent.Play(self.index)

class Player(tk.Frame):
    def __init__(self,parent,*args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.Human = Border(self, "#ff9961", borderright=4, borderbottom=8, interiorwidget=TheMove, row=1, column=0).interior
        self.Human.image.pack(fill="both", padx=(20,10),pady=(10,30))
        self.Human.config(bg=default_colour)
        self.Computer = Border(self, "#ff9961", borderleft=4, bordertop=8,interiorwidget=TheMove, row=1, column=1).interior
        self.Computer.image.pack(fill="both", padx=(10,20),pady=(30,10))
        self.Computer.config(bg=default_colour)

class PSRLS(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.Moves = ["Rock","Paper","Scissors", "Spock", "Lizard"]

        if not "psrls.txt" in os.listdir():
            #make a psrls file
            with open("psrls.txt","w") as file:
                file.write("0,0,0,0,0\n")
                file.write("0,0,0,0,0\n")
                file.write("1,2,3,4,5")
                file.close()
        with open("psrls.txt","r") as file:
            file = file.readlines()
            humtall = [int(tall) for tall in file[0].strip().split(",")]
            comtall = [int(tall) for tall in file[1].strip().split(",")]
            self.Binds = file[2].strip().split(",")

        try:
            self.MovesImgs = [ImageTk.PhotoImage(Image.open(move+".png")) for move in self.Moves]
        except:
            import urllib.request as urllib
            import io
            self.MovesImgs = [ImageTk.PhotoImage(Image.open(io.BytesIO(urllib.urlopen("https://rpsls.net/images/"+move+".png").read()))) for move in self.Moves]
        self.TimeofWin = 0
        self.parent = parent
        tk.Frame.__init__(self, parent, *args, **kwargs)
        __tempvar1 = tk.Label(self,bg=default_colour, height=20, width=960)
        __tempvar2 = tk.Label(self,bg=default_colour, height=20, width=960)
        __tempvar1.place(relx=0)
        __tempvar2.place(rely=1, relx=0, anchor="sw")
        self.Player = Player(self)
        self.Player.place(rely=0.5, relx=0.5, anchor="center")
        self.Player.Human.Buttons = [Button_Card(self, move, humtall[self.Moves.index(move)], self.Moves.index(move)) for move in self.Moves]
        self.Player.Human.Title = tk.Label(self, text="Human",fg="White",bg=default_colour, font=("Arial", 20))
        self.Player.Human.Title.place(y=105, relx=0.5 ,anchor="center",)
        [Button.place(relx=(1/len(self.Moves)*self.Player.Human.Buttons.index(Button))+1/len(self.Moves)/2, y=10, anchor="n") for Button in self.Player.Human.Buttons]
        self.Player.Human.Background = __tempvar1
        self.Player.Computer.Background = __tempvar2
        self.Player.Computer.Buttons = [Button_Card(self, move, comtall[self.Moves.index(move)], self.Moves.index(move), disabled =True) for move in self.Moves]
        self.Player.Computer.Title = tk.Label(self, text="Computer",fg="White",bg=default_colour, font=("Arial", 20))
        self.Player.Computer.Title.place(y=-105, rely=1, relx=0.5 ,anchor="center")
        [Button.place(relx=(1/len(self.Moves)*self.Player.Computer.Buttons.index(Button))+1/len(self.Moves)/2, rely=1, y=-80, anchor="n")for Button in self.Player.Computer.Buttons]
        [self.parent.bind(self.Binds[i],self.Player.Human.Buttons[i].Play) for i in range(0,len(self.Moves))]
        self.parent.protocol("WM_DELETE_WINDOW", self.close)
    def Play(self, Human):
        Computer = random.randint(0,len(self.Moves)-1)
        self.Player.Human.image.config(image=self.MovesImgs[Human])
        self.Player.Computer.image.config(image=self.MovesImgs[Computer])
        self.Player.Computer.Buttons[Computer].add1()
        self.Player.Human.Buttons[Human].add1()
        with open("psrls.txt","w") as file:
            file.write(",".join([str(tall.Clicks.config()["text"][-1]) for tall in self.Player.Human.Buttons])+"\n")
            file.write(",".join([str(tall.Clicks.config()["text"][-1]) for tall in self.Player.Computer.Buttons])+"\n")
            file.write(",".join(self.Binds))
            file.close()
        if not (len(self.Moves) + Human - Computer)%len(self.Moves):
            print(self.Moves[Human],"-",self.Moves[Computer])
            #self.winlosetext.config(text="Draw")
            self.Player.Human.config(bg=default_colour)
            self.Player.Human.Background.config(bg=default_colour)
            self.Player.Computer.config(bg=default_colour)
            self.Player.Computer.Background.config(bg=default_colour)
            self.Player.Human.Title.config(bg=default_colour)
            self.Player.Computer.Title.config(bg=default_colour)
            self.TimeofWin = time.time()
            localTimeofWin = time.time()
            while time.time() <= self.TimeofWin+5 and self.TimeofWin == localTimeofWin:
                self.parent.update() #Added this so the game won't freeze when waiting for 5 seconds
            self.Player.Computer.image.config(image=self.Player.Computer.waiting)
            self.Player.Human.image.config(image=self.Player.Human.waiting)
        elif (len(self.Moves) + Human - Computer)%len(self.Moves)%2:
            print(self.Moves[Human],"->",self.Moves[Computer]) #win
            self.Winner(self.Player.Human)
        else:
            print(self.Moves[Human],"<-",self.Moves[Computer]) #loss
            self.Winner(self.Player.Computer)
    def Winner(self,winner):
        loser = self.Player.Computer if winner == self.Player.Human else self.Player.Human
        self.TimeofWin = time.time()
        localTimeofWin = time.time()
        winner.config(bg="Green")
        winner.Background.config(bg="Green")
        winner.Title.config(bg="Green")
        loser.Title.config(bg="Red")
        loser.config(bg="Red")
        loser.Background.config(bg="Red")
        while time.time() <= self.TimeofWin+5 and self.TimeofWin == localTimeofWin:
            self.parent.update() #Added this so the game won't freeze when waiting for 5 seconds
        if self.TimeofWin == localTimeofWin:
            winner.config(bg=default_colour)
            winner.Background.config(bg=default_colour)
            winner.Title.config(bg=default_colour)
            loser.config(bg=default_colour)
            loser.Background.config(bg=default_colour)
            loser.Title.config(bg=default_colour)
            loser.image.config(image=loser.waiting)
            winner.image.config(image=winner.waiting)
            print("Clearing...")
    def close(self):
        self.TimeofWin = time.time()
        self.parent.destroy()
        print("Closing")
if __name__ == "__main__":
    root = tk.Tk()
    root.maxsize(960,800)
    root.minsize(960,700)
    root.title("Rock, Paper, Scissors, and the Bang")
    PSRLS(root).pack( fill="both", expand=True)
    root.mainloop()
