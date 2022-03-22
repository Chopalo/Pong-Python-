import tkinter as tk
import time as tm

x_size=600
y_size=400
PmidHeight=50 # middle paddle height
PmidWidth=20 # middle paddle width
geom=str(x_size)+str("x")+str(y_size)  #window size

class Player():
    def __init__(self,window,pos,upp,downn):
        self.pos=pos #pos --> [x,y,x2,y2]
        self.window=window
        self.upp=upp
        self.downn=downn
        self.incr=20
    def Update(self,t):
        if t==self.upp:
            self.pos[1]=self.pos[1]-self.incr
            self.pos[3] = self.pos[3] - self.incr
        elif t==self.downn:
            self.pos[1] = self.pos[1] + self.incr
            self.pos[3] = self.pos[3] + self.incr
    def Draw(self,window):
        window.create_rectangle(self.pos[0],self.pos[1],self.pos[2],self.pos[3],fill="white",outline="blue",width=1)

class Ball():
    def __init__(self,window,r):
        self.acc_i=tm.time()
        self.R=r
        self.x=x_size/2-(self.R/2)
        self.y=y_size/2-(self.R/2)
        self.window=window
        self.vx=2
        self.vy=2
        self.CanRestar=False
    def Draw(self,bord1,bord2):
        self.window.create_oval(self.x,self.y,self.x+self.R,self.y+self.R,fill="red",outline="black",width=1)
        self.Update(bord1,bord2)
        self.x = self.x + self.vx
        self.y = self.y + self.vy
    def Update(self,bord1,bord2):
        if(self.y>y_size-self.R or self.y<0):
            self.vy=-self.vy
        elif(self.x>x_size or self.x<0):
            self.vx=2
            self.acc_i=tm.time()
            self.x = x_size / 2 - (self.R / 2)
            self.y = y_size / 2 - (self.R / 2)
            self.CanRestar = False
        elif((self.y<bord1[3] and self.y+self.R>bord1[1]) and self.x<bord1[2]):
            self.vx=-self.vx
        elif((self.y<bord2[3] and self.y+self.R>bord2[1]) and self.x+self.R>bord2[2]):
            self.vx=-self.vx
    def Func_vx(self):
        """
        Change the speed of the ball trough time
        """
        f=0.002*abs(tm.time() / self.acc_i)
        if(self.vx<0):
            self.vx = self.vx - f
        else:
            self.vx=self.vx+f

class Game():
    def __init__(self,mainWin):
        self.mainWin=mainWin
        self.C=tk.Canvas(mainWin,width=x_size,height=y_size,bg="black")
        self.C.grid()
        self.p1 = Player(self.C, [10, (y_size / 2) - PmidHeight, PmidWidth, (y_size / 2) + PmidHeight], 'Z', 'S') #LEFT PLAYER
        self.p2 = Player(self.C, [x_size - 10, (y_size / 2) - PmidHeight, x_size - PmidWidth, (y_size / 2) + PmidHeight],'G','H') #RIGHT PLAYER
        self.ball=Ball(self.C,20)
        self.Gaming()
    def Gaming(self):
        self.C.delete("all")
        self.C.bind_all('<Key>', self.HowKeyIs)
        if(self.ball.CanRestar):
            self.ball.Func_vx()
            self.ball.Draw(self.p1.pos,self.p2.pos)
        self.p1.Draw(self.C)
        self.p2.Draw(self.C)
        self.C.after(10,self.Gaming)
    def HowKeyIs(self,evt):
        t = evt.char.upper()
        if(t==self.p1.upp or t==self.p1.downn):
            self.p1.Update(t)
        if (t == self.p2.upp or t == self.p2.downn):
            self.p2.Update(t)
        if(evt.keycode==27):
            self.mainWin.quit()
        if(evt.keycode==32):
            self.ball.CanRestar=True

def App():
    mainWin=tk.Tk()
    mainWin.geometry(geom)
    Game(mainWin)
    mainWin.mainloop()

App()
