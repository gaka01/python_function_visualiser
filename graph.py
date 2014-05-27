#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#A program used to visualise mathematical functions from the type y=f(x)
#Program written by Galin Dobchev (gaka)
#Please enter your function below where marked
#Use arrow keys or mouse to navigate, mouse scroll to zoom
#Hit Esc to exit
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@




import pygame,sys
import math
import time #for the fps
from pygame.locals import *

def function(xx):
    x=pix_to_coor((xx,0))[0]


    #Type your function here
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    try:
        fx=x**2
        y=fx
    except:
        y=0

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #Example: fx=x**2-2*x+1   // f(x)=x^2-2x+1
    #         y=fx            // y=f(x)

    #Example: fx=x**3-2*x**2+1// f(x)=x^3-2x^2+1
    #         y=2*fx          // y=2f(x)
    #                         // for y=f(2x) please just replace x with 2*x in fx


    #Example:
    #fx=x
    #if x>0:
    #    y=2*fx
    #if x<0:
    #    y=2/fx
    #else:
    #    y=fx

    
    return coor_to_pix((x,y))

def quit_program():
    pygame.quit()
    sys.exit()

def coor_to_pix((x,y)):
    xx=coorc[0]+(x*psize)
    yy=coorc[1]-(y*psize)
    return(xx,yy)

def pix_to_coor((xx,yy)):
    x=(xx-coorc[0])/psize
    y=(yy-coorc[1])/psize*(-1)
    return (x,y)
def in_screen((xx,yy)):
    if xx<0 or xx>size[0]:
        return False
    if yy<0 or yy>size[1]:
        return False
    return True
    

    


size=(600,600) #size of window
fps=60.0 #how many frames per second
psize=20.0 #how much pixels is 1 (coordinate to pixel convertation) (the bigger the number the more you are zoomed in)
msize=20.0 #how much to move when pressed up down left right
dlsize=20.0 #where to draw meter lines
zsize=10.0 #zoom size, how much to zoom
zsize2=zsize #zoom size 2 .. idk
pftime=time.time()

coorc=(size[0]/2.0,size[1]/2.0) #find center (dont change)
bgcolor=(255,255,255)  #colors and shit
ccolor=(0,0,255)
scolor=(200,200,200)
s2color=(100,100,100)
dcolor=(0,0,0)
mbuttons=(0,0,0) #variable for storing mouse buttons clicked
cpos=(0,0)
cursize=15
curcolor=(255,0,0)
curpos=(0,0)
snap=20


pygame.init() #pygame init stuff
screen=pygame.display.set_mode((size[0],size[1]),0,32)
font1=pygame.font.Font(None, 22) #prepearing some fonts blah blah ..


while True: #main loop
    if time.time()-pftime>1.0/fps:
        pftime=time.time()
        screen.lock()
        pygame.draw.rect(screen,bgcolor,Rect(0,0,size[0],size[1]))

        
        xx=coorc[0] #draw lines for each x=1 2 3 4 ..
        xx2=xx
        c=0
        while xx<size[0] or xx2>0:
            col=scolor
            if not c%10:
                col=s2color
                c=0
            pygame.draw.line(screen,col,(xx,0),(xx,size[1]))
            pygame.draw.line(screen,col,(xx2,0),(xx2,size[1]))            
            xx+=dlsize
            xx2-=dlsize
            c+=1

        yy=coorc[1] #same for y
        yy2=yy
        c=0
        while yy<size[1] or yy2>0:
            col=scolor
            if not c%10:
                col=s2color
                c=0
            pygame.draw.line(screen,col,(0,yy),(size[0],yy))
            pygame.draw.line(screen,col,(0,yy2),(size[0],yy2))
            yy+=dlsize
            yy2-=dlsize
            c+=1

        



        print dlsize
        
        #draw center lines (0,0)
        pygame.draw.line(screen,ccolor,(0,coorc[1]),(size[0],coorc[1])) 
        pygame.draw.line(screen,ccolor,(coorc[0],0),(coorc[0],size[1]))

        #pygame.draw.line(screen,dcolor,coor_to_pix((1,1)),coor_to_pix((2,2)))


        pos=pygame.mouse.get_pos()
        curpos=pos
        
        
        xx=0.0
        ctc=[size[0],(0,0)]
        ppoint=function(xx)
        while xx<size[0]: #loop for drawing points from the function and connecting them
            
            xy=function(xx) #calculate y pixel for each x pixel
            if in_screen(xy) or in_screen(ppoint):
                pygame.draw.line(screen,dcolor,ppoint,xy)
                d=math.sqrt((abs(xy[0]-pos[0])**2+(abs(xy[1]-pos[1])**2)))
                if d<ctc[0]:
                    ctc[0]=d
                    ctc[1]=xy
                    
            ppoint=xy
            xx+=1
        screen.unlock()

        if ctc[0]<snap:
            print ctc
            curpos=ctc[1]

        #draw cursor        
        pygame.draw.line(screen,curcolor,(curpos[0],curpos[1]-cursize),(curpos[0],curpos[1]+cursize)) 
        pygame.draw.line(screen,curcolor,(curpos[0]-cursize,curpos[1]),(curpos[0]+cursize,curpos[1]))


        text1=font1.render("x: "+str(pix_to_coor(curpos)[0]),1,(0,0,0,0))
        text2=font1.render("y: "+str(pix_to_coor(curpos)[1]),1,(0,0,0,0))
        screen.blit(text1, (5,5))
        screen.blit(text2, (5,20))

    if mbuttons[0]==1:
        move=pygame.mouse.get_rel()
        coorc=(coorc[0]+move[0],coorc[1]+move[1])
    
    #pygame events stuff
    for event in pygame.event.get():
        if event.type== QUIT:
            quit_program()
        elif event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                quit_program()
            elif event.key==K_RIGHT:
                coorc=(coorc[0]-msize,coorc[1])
            elif event.key==K_LEFT:
                coorc=(coorc[0]+msize,coorc[1])
            elif event.key==K_UP:
                coorc=(coorc[0],coorc[1]+msize)
            elif event.key==K_DOWN:
                coorc=(coorc[0],coorc[1]-msize)
            elif event.key==K_r:
                coorc=(size[0]/2,size[1]/2)
                psize=20
        elif event.type==MOUSEBUTTONDOWN:
            move=pygame.mouse.get_rel()
            mbuttons=pygame.mouse.get_pressed()
            if event.button==4:
                cpos=pix_to_coor(curpos)
                psize+=zsize
                dlsize+=zsize2
                coorc=coor_to_pix(((cpos[0]-pix_to_coor(curpos)[0])*(-1),(cpos[1]-pix_to_coor(curpos)[1])*(-1)))                #dlsize+=zsize
                if dlsize>=zsize*zsize:
                    dlsize/=zsize
                    zsize2/=zsize



            elif event.button==5:
                if psize>zsize:
                    cpos=pix_to_coor(curpos)
                    psize-=zsize
                    dlsize-=zsize2
                    coorc=coor_to_pix(((cpos[0]-pix_to_coor(curpos)[0])*(-1),(cpos[1]-pix_to_coor(curpos)[1])*(-1)))  
                    if dlsize<=zsize:
                        dlsize*=zsize
                        zsize2*=zsize



        elif event.type==MOUSEBUTTONUP:
            mbuttons=pygame.mouse.get_pressed()
            

    pygame.display.update()
