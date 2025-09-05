#!/usr/bin/env python3

#0.6.2.1
print("loading modules...")
import  pygame                                                      #imports pygame, the game libary 
from    pygame.locals   import *                                    #imports pygame.local
import  time                                                        #imports the time libary for functions like sleep()
from    math            import ceil                                 #imports the ceiling (round up) function
import  random                                                      #imports the random libary
from    os              import listdir, sep                         #gets the file seperator / or \
print("modules loaded")                                             #prints after modules has loaded
pygame.display.init()                                               #initialises display
pygame.display.set_caption("Platform-Cat")                          #sets caption

# setup window
windowDefaultSize   = (640,360)                                     #sets window size
icon                = pygame.transform.scale(pygame.image.load("tiles"+sep+"flagtop"+sep+"icon.png"),(128,128))     #sets icon to a flag 
screenFlags         = pygame.RESIZABLE| pygame.DOUBLEBUF | pygame.SCALED            #sets flags
window              = pygame.display.set_mode(windowDefaultSize,screenFlags)        #applys flags, makes window resizable

pygame.display.set_icon(icon)                                       #sets the icon for the window
#Creates variables-----------------------------------------------------------------------------------------


toolbarBlockDisplayPos=[0,0]                                        #temporary variable before it gets replaced
pygame.font.init()                                                  #initializes pygame fonts
font                = pygame.font.SysFont("courier", 10)            #sets font to jetbrains mono
smallfont           = pygame.font.SysFont("courier", 8)             #small font for some debugging purposes
numfont             = pygame.font.Font("pixel.ttf", 32)             #small font for some debugging purposes

solidBlocks         = [1,2,5,6,10]                                  #Sets some of the blocks to be solid
checkpointBlocks    = [3,4]                                         #Sets some of the blocks to be checkpoints
selectbox           = []                                        
tpos                = [16,16]
running             = True                                          #if the game is running
clock               = pygame.time.Clock()                           #pygame's clock
selectedBlock       = 0                                             #current block selected (in edit mode ) 
tick                = 0                                             #the current tick the 
currenttick         = 0                                             #the time of the latest tick
oldtick             = 0                                             #the time of the second latest tick
tickspeed           = 0                                             #how long each tick takes
cursorColour        = (0,255,255)                                   #colour of the cursor (box)
mousePressed        = False                                         #is the mouse pressed?
mouseButton         = 1                                             #which mouse button is pressed                           
mousetilepos        = [0,0]                                         #which tile the mouse is on
mode                = "edit"                                                         #the mode
fps30               = False                                         #unused for now
ttime               = 0                                             #Debug stuff
tiletime            = 0                                             #Debug stuff
ptime               = 0                                             #Debug stuff
cameratime          = 0                                             #Debug stuff
MCtime              = 0                                             #Debug stuff
background          = pygame.image.load("background.png")           #unused for now
background          = pygame.transform.scale(background,(640,640))  #unused for now
showdebug           = False                                         #Show debug menu?
blockSize           = 32                                            #Block size
fullscreen          = False                                         #if the game is fullscreen
snowballs           = []                                             #snowballs
savebutton          = (32*16,16,16,16)
tick60              = 0
oldtick60           = 0
screen60            = 1 
screenfps           = 0
coins               = 0

#functions-----------------------------------------------------------------------------------------
class tilemap:
    def __init__(self):
        self.size=[0,0]
        self.map =[]
    def loadstr(self,string):
        string=string.split("\n") #splits the Y axis
        for i in string: #splits X axis
            if i =="":
                del string[string.index(i)]
            else:
                string[string.index(i)]=string[string.index(i)].split()
        self.size=[len(string[0]),len(string)]

        for i in range(self.size[1]):
            error=False
    
            for j in range(self.size[0]):
                string[i][j]=int(string[i][j])
        self.map = string
    def blit(self,window,camera):
        blockDisplayPosition=[0-camera.pos[0],0-camera.pos[1]]
        currentBlockPos=[0,0]
        winx,winy=window.get_size()
        blockIndex=0
        tileStartPos = [round(camera.pos[0]//blockSize),round(camera.pos[1]//blockSize)]
    
    
        for i in range(tileStartPos[1],len(self.map)): #Draws the tile one by one
            if blockDisplayPosition[1]>winy:
                break
            for j in range(tileStartPos[0],len(self.map[i])):
                blockDisplayPosition=[0-camera.pos[0]+j*blockSize,0-camera.pos[1]+i*blockSize]
                if blockDisplayPosition[0]>winx:
                    break
                try:
                    window.blit(tile[(self.map[i][j])],blockDisplayPosition)
                    if showdebug:
                        window.blit(smallfont.render(str(i)+" "+str(j),False,(0,0,0),(255,255,255)),(blockDisplayPosition[0],blockDisplayPosition[1]))
                        pygame.draw.rect(window,(255,255,255),(blockDisplayPosition,(blockSize,blockSize)),1)
                    blockIndex+=1
                except:
                    window.blit(errortile,blockDisplayPosition)

                currentBlockPos[0]+=1
            currentBlockPos[0]=0
            currentBlockPos[1]+=1
    def surface(self,camera):
        surface = pygame.Surface((640,360),pygame.SRCALPHA)
        blockDisplayPosition=[0-camera.pos[0],0-camera.pos[1]]
        currentBlockPos=[0,0]
        winx,winy=surface.get_size()
        blockIndex=0
        tileStartPos = [round(camera.pos[0]//blockSize),round(camera.pos[1]//blockSize)]
    
    
        for i in range(tileStartPos[1],len(self.map)): #Draws the tile one by one
            if blockDisplayPosition[1]>winy:
                break
            for j in range(tileStartPos[0],len(self.map[i])):
                blockDisplayPosition=[0-camera.pos[0]+j*blockSize,0-camera.pos[1]+i*blockSize]
                if blockDisplayPosition[0]>winx:
                    break
                try:
                    if self.map[i][j] != 0:
                        surface.blit(tile[(self.map[i][j])],blockDisplayPosition)
                    if showdebug:
                        surface.blit(smallfont.render(str(i)+" "+str(j),False,(0,0,0),(255,255,255)),(blockDisplayPosition[0],blockDisplayPosition[1]))
                        pygame.draw.rect(surface,(255,255,255),(blockDisplayPosition,(blockSize,blockSize)),1)
                    blockIndex+=1
                except:
                    surface.blit(errortile,blockDisplayPosition)

                currentBlockPos[0]+=1
            currentBlockPos[0]=0
            currentBlockPos[1]+=1
        return surface.convert_alpha()
    def size(self):
        return [len(self.map[0]),len(self.map)]
    def convertToStr(self):
        savetxt=""
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):        
                savetxt=savetxt+str(self.map[i][j])+" "
            savetxt+="\n"
        return savetxt
world = tilemap()
worldtxt=open("world.txt","r")
worldtxt=worldtxt.read()      #reads world file
world.loadstr(worldtxt)

for i in range(len(world.map)):
    for j in range(len(world.map[0])):
        if world.map[i][j]==12:world.map[i][j]=8

#sets up the entity class
events=pygame.event.get()
class entity:
    """
    The entity class----
    Functions:
        update()
            Updates the entity, run every frame

    """
    def __init__(self,entityType="default",pos=[0,0],v=[0,0],f=[2,2],a=[0,0],rot = 0,controls=[],speed=4,image=pygame.image.load("tiles"+sep+"empty"+sep+"icon.png").convert_alpha(),jump=True,coyote=4,maxcoyote=6,jumpheight=60,coll=True,hitbox=[0,0,blockSize,blockSize],alwaysshowhitbox=False,rect=[(0,0,255),0],g=[0,0],oldpos=[0,0],roundpos=True,voiddeath=False,spawnpoint=[0,0],flip=True):
        self.pos                = pos
        self.entityType         = entityType
        self.v                  = v
        self.f                  = f
        self.a                  = a
        self.rot                = rot
        self.controls           = controls
        self.image              = image
        self.imageright         = image
        self.imageleft          = pygame.transform.flip(image,True,False)
        self.speed              = speed
        self.jump               = jump
        self.coyote             = coyote
        self.jumpheight         = jumpheight
        self.hitbox             = hitbox
        self.alwaysshowhitbox   = alwaysshowhitbox
        self.rect               = rect
        self.g                  = g
        self.oldpos             = oldpos
        self.maxcoyote          = maxcoyote
        self.roundpos           = roundpos
        self.voideath           = voiddeath
        self.spawnpoint         = spawnpoint
        self.helddownkeys       = []
        self.moveDir            = [0,0]
        self.faceright          = False
        self.flip               = flip
        self.right              = True
        self.coll               = coll
    
    def blockcolltrue(self,blockList,tilemap):
        try:
            for collblock in blockList:
                if collblock in [tilemap[int(self.pos[1]//blockSize)][int(self.pos[0]//blockSize)] or collblock in [tilemap[int(self.pos[1]//blockSize)][int(self.pos[0]//blockSize)]],
                    tilemap[(int(ceil(self.pos[1]/blockSize)))][int(self.pos[0]//blockSize)],
                    tilemap[int(self.pos[1]//blockSize)][int(ceil(self.pos[0]/blockSize))],
                    tilemap[int(ceil(self.pos[1]/blockSize))][int(ceil(self.pos[0]/blockSize))]]:
                    return True
        except:
            return False
        return False
    def update(self):
        global events
        global fpscounter
        global checkpointBlocks
        self.oldpos=self.pos
        self.v=[self.a[0]+self.v[0],self.a[1]+self.v[1]]#updates velocity using accelaration
        self.v=[self.g[0]+self.v[0],self.g[1]+self.v[1]]#updates velocity using gravity
        self.v=[self.v[0]/self.f[0],self.v[1]/self.f[1]]#updates velocity using friction
        self.pos[0] +=self.v[0]#updates postion based on velocity

        if self.blockcolltrue(solidBlocks,world.map) and self.coll:
            self.pos[0] -=self.v[0]
            self.v[0]=0
        self.pos[1] +=self.v[1]
        if self.blockcolltrue(solidBlocks,world.map) and self.coll:
            self.pos[1] -=self.v[1]
            if self.jump and self.v[1]>0:
                self.coyote=self.maxcoyote
            self.v[1]=0
        if self.blockcolltrue(checkpointBlocks,world.map):
            self.spawnpoint=self.pos
        if self.v[1]>0:
            if self.coyote>0:
                self.coyote-=1

        self.hitbox=[self.pos[0],self.pos[1],self.hitbox[2],self.hitbox[3]]
        if self.roundpos:
            self.pos=[round(self.pos[0]),round(self.pos[1])]
        if self.alwaysshowhitbox:
            pygame.draw.rect(window,self.rect[0],[self.hitbox[0]-camera.pos[0],self.hitbox[1]-camera.pos[1],self.hitbox[2],self.hitbox[3],],self.rect[1])
        if self.pos[0]>camera.pos[0] and self.pos[1]>camera.pos[1] and self.pos[0]<(camera.pos[0]+window.get_size()[0]) and self.pos[0]<(camera.pos[0]+window.get_size()[0]):
            window.blit(self.image,(self.pos[0]-camera.pos[0],self.pos[1]-camera.pos[1]))
        if self.voideath and (self.pos[1]>128+len(world.map)*blockSize):
            self.pos=self.spawnpoint
        if len(self.controls)>7:
            self.doublewasd=True
        else:
            self.doublewasd=False
        if len(self.controls)>=4:
            if self.jump:
                for i in range(1):
                    for event in events:
                #check for keyups
                        if event.type == pygame.KEYDOWN:
                            if event.key == self.controls[1]:
                                self.moveDir[0] = -1
                            if event.key == self.controls[3]:
                                self.moveDir[0] = 1
                            if event.key == self.controls[0] and self.coyote>0:
                                self.coyote=0
                                self.v[1] =-self.jumpheight
                            if event.key == self.controls[2]:
                                self.moveDir[1] = 1

                        elif event.type == pygame.KEYUP:
                            if event.key == self.controls[1] or event.key == self.controls[3]:
                                self.moveDir[0] = 0
                            if event.key == self.controls[0] or event.key == self.controls[2]:
                                self.moveDir[1] = 0
            else:
                for i in range(1):
                    for event in events:
                #check for keyups
                        if event.type == pygame.KEYDOWN:
                            if event.key == self.controls[1]:
                                self.moveDir[0] = -1
                            if event.key == self.controls[3]:
                                self.moveDir[0] = 1
                            if event.key == self.controls[0]:
                                self.moveDir[1] =-1
                            if event.key == self.controls[2]:
                                self.moveDir[1] =1

                        elif event.type == pygame.KEYUP:
                            if event.key == self.controls[1] or event.key == self.controls[3]:
                                self.moveDir[0] = 0
                            if event.key == self.controls[0] or event.key == self.controls[2]:
                                self.moveDir[1] = 0    
        if self.doublewasd:
            if self.jump:
                for i in range(1):
                    for event in events:
                #check for keyups
                        if event.type == pygame.KEYDOWN:
                            if event.key == self.controls[4+1]:
                                self.moveDir[0] = -1
                            if event.key == self.controls[4+3]:
                                self.moveDir[0] = 1
                            if event.key == self.controls[4+0] and self.coyote>0:
                                self.v[1] =-self.jumpheight
                            if event.key == self.controls[4+2]:
                                self.moveDir[1] =1

                        elif event.type == pygame.KEYUP:
                            if event.key == self.controls[4+1] or event.key == self.controls[4+3]:
                                self.moveDir[0] = 0
                            if event.key == self.controls[4+0] or event.key == self.controls[4+2]:
                                self.moveDir[1] =  0                               
        
            else:
                for i in range(1):
                    for event in events:
                #check for keyups
                        if event.type == pygame.KEYDOWN:
                            if event.key == self.controls[4+1]:
                                self.moveDir[0] = -1
                            if event.key == self.controls[4+3]:
                                self.moveDir[0] = 1
                            if event.key == self.controls[4+0]:
                                self.moveDir[1] =-1
                            if event.key == self.controls[4+2]:
                                self.moveDir[1] =1

                        elif event.type == pygame.KEYUP:
                            if event.key == self.controls[4+1] or event.key == self.controls[4+3]:
                                self.moveDir[0] = 0
                            if event.key == self.controls[4+0] or event.key == self.controls[4+2]:
                                self.moveDir[1] =  0
        if self.flip:
            if self.moveDir[0] == 1:

                self.right=True
            if self.moveDir[0] == -1:

                self.right = False
            if len(self.controls)>4:
                self.a=[self.moveDir[0]*self.speed,self.moveDir[1]*self.speed]
        if self.right:
            self.image=self.imageright
        else:
            self.image=self.imageleft
    def respawn(self):
        self.pos=self.spawnpoint



def img(image,trans=False):
    if trans:
        return pygame.image.load(image).convert_alpha()
    else:    
        return pygame.image.load(image).convert()

print("loading images...")
tile=[img("tiles"+sep+"empty"+sep+"icon.png",True),  #imports tile images
    img("tiles"+sep+"grass"+sep+"icon.png"),
    img("tiles"+sep+"dirt"+sep+"icon.png"),
    img("tiles"+sep+"flagtop"+sep+"icon.png",True),
    img("tiles"+sep+"flagbottom"+sep +"icon.png",True),
    img("tiles"+sep+"ice"+sep+"icon.png"),
    img("tiles"+sep+"snow"+sep+"icon.png"),
    img("tiles"+sep+"cloud"+sep+"icon.png",True),
    img("tiles"+sep+"coin"+sep+"Sprite-0001.png",True),
    img("tiles"+sep+"log"+sep+"icon.png"),
    img("tiles"+sep+"snowdirt"+sep+"icon.png"),
    img("tiles"+sep+"snow spawner"+sep+"icon.png"),
    img("tiles"+sep+"empty"+sep+"icon.png",True),
         ]
errortile=pygame.transform.scale(img("error.png"),(blockSize,blockSize))
for i in tile:
    tile[tile.index(i)]=pygame.transform.scale(tile[tile.index(i)],(blockSize,blockSize))

for i in tile:
    selectbox.append([tpos[0],tpos[1]])
    tpos[0]+=32          
player=entity(controls=[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT],jump=True,speed=6,jumpheight=25,image=pygame.transform.scale(img("Cat"+sep+"idle.png",True),(blockSize,blockSize)))
camera=entity(entityType="camera",coll=False, alwaysshowhitbox=False)

jumpimg             = pygame.transform.scale(img("Cat"+sep+"jump2.png",True),(blockSize*2,blockSize*2))
jumpnomove          = pygame.transform.scale(img("Cat"+sep+"jumpnomove.png",True),(blockSize,blockSize*2))
idleimg             = pygame.transform.scale(img("Cat"+sep+"idle.png",True),(blockSize,blockSize))
fallimg             = pygame.transform.scale(img("Cat"+sep+"fall2.png",True),(blockSize,blockSize*2))

 

 
print("loading functions...")

def blitcursor():
    global mouseTilePos
    if mouseTilePos[0]>=len(world.map[0]) or mouseTilePos[0]<0 or mouseTilePos[1]>=len(world.map)or mouseTilePos[1]<0: #sets cursor colour
        cursorcolour=(255,0,0)
    else:
        cursorcolour=(0,255,255)
    if mpos[1]>80 or not mode=="edit":
        pygame.draw.rect(window,cursorcolour,(mouseTilePos[0]*blockSize-camera.pos[0],mouseTilePos[1]*blockSize-camera.pos[1],blockSize,blockSize),5)#draws the cursor
events=pygame.event.get()
debugpos=[0,100]
blockselectpos=[16,16]
def editmenu():
    global mouseTilePos
    global events
    global selectedBlock
    global blockselectpos
    global toolbarBlockDisplayPos
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_n:
                selectedBlock+=1
                selectedBlock%=len(tile)
            if event.key==pygame.K_b:
                selectedBlock-=1
                selectedBlock%=len(tile)

    if mousePressed:
        try:
            if mpos[1]>80 and mbutton==1:
                world.map[mouseTilePos[1]][mouseTilePos[0]]=selectedBlock
            elif mpos[1]>80 and mbutton==3:
                world.map[mouseTilePos[1]][mouseTilePos[0]]=0
            else:
                for selectpos in selectbox:
                    
                    if mpos[0]>selectpos[0] and mpos[1]>selectpos[1] and mpos[0]<selectpos[0]+16 and mpos[1]<selectpos[1]+16:
                       
                        selectedBlock =selectbox.index(selectpos)

    
        except:
            pass 
    
    blockselectpos=[16,16]
    for tile_selected in tile:#display select icons
        
        if tile.index(tile_selected)==selectedBlock:
            window.blit(pygame.transform.scale(tile_selected,(16,16)),toolbarBlockDisplayPos)
        else:
            temptile=tile_selected.copy()
            temptile.set_alpha(100)
            window.blit(pygame.transform.scale(temptile,(16,16)),toolbarBlockDisplayPos)
        toolbarBlockDisplayPos[0]+=32
    toolbarBlockDisplayPos=[blockselectpos[0],blockselectpos[1]]
    tpos=[16,16]
    for i in tile:
        selectbox.append([tpos[0],tpos[1]])
        tpos[0]+=32

def mouseupdate():
    global mpos
    global mouseTilePos
    global mousePressed
    global events
    global mposrender
    global mbutton
    mpos= pygame.mouse.get_pos()
    mouseTilePos=[round((camera.pos[0]+mpos[0])/blockSize),round((camera.pos[1]+mpos[1])/blockSize)]
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed=True
            mbutton = event.button
        elif event.type==pygame.MOUSEBUTTONUP:
            mousePressed=False

    mposrender=str(mpos)   
def checkforquit():
    global running
    global events
    for event in events:
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False
        elif event.type == pygame.QUIT:
            running = False
def checkvideoresize():
    global window
    for event in events:
        if event.type == pygame.VIDEORESIZE:
            pygame.display._resize_event(event)

def gametick(FPS=60):
    global clock
    global tick
    global currenttick
    global oldtick
    global tickspeed
    global fpscounter
    currenttick=time.time()
    tickspeed=currenttick-oldtick
    fpscounter=1/tickspeed

    oldtick=time.time()
    clock.tick(FPS)
    tick+=1
def checkmodechange():
    global events
    global mode
    for event in events:
        #check for keyups
        if event.type == pygame.KEYDOWN:

            if event.key==pygame.K_e:
                if mode =="edit":
                    mode="play"
                else:
                    mode="edit"
def checkdebugchange():
    global events
    global showdebug
    for event in events:
        #check for keyups
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_h:
                showdebug=not showdebug

def text(text,pos):
    window.blit(font.render(str(text),False,(0,0,0),(255,255,255)),(pos[0],pos[1]))
def debugmenu(): #debug function DF
    global ttime,tiletime,ptime,cameratime,MCtime,fpscounter,gamefps
    global screen60 ,screenfps
    debugpos = (0,100)
    window.blit(font.render("Mouse Pos: "+mposrender,True, (0,0,0), (255,255,255)),debugpos)#debug for mouse
    try:
        window.blit(font.render("pos: "+str(round(player.pos[0],3))+" "+str(round(player.pos[1],3))+" "+"v: "+str(round(player.v[0],3))+" "+str(round(player.v[1],3))+" "+"a: "+str(round(player.a[0],3))+" "+str(round(player.a[1],3))+" "+"f: "+str(round(player.f[0],3))+" "+str(round(player.f[1],3)),True,(0,0,0),(255,255,255)),[debugpos[0],debugpos[1]+20])
        
    except:
        pass

    text(player.coll,(debugpos[0],debugpos[1]+60))
    window.blit(font.render("Coyote: "+str(player.coyote),True,(0,0,0),(255,255,255)),(debugpos[0],debugpos[1]+80),)
    text("FPS: "+str(round(gamefps)),(debugpos[0],debugpos[1]+100))
    text("Screen FPS: "+str(round(screenfps)),(debugpos[0],debugpos[1]+120))
    '''
    text(f"""Expected total \t0.0167""",(debugpos[0],debugpos[1]+120))
    text(f"Total time \t\t{round(ttime,5)}",(debugpos[0],debugpos[1]+140))
    text(f"tiles \t\t{tiletime}",(debugpos[0],debugpos[1]+160))
    text(f"player  \t\t{ptime}",(debugpos[0],debugpos[1]+180))
    text(f"camera \t\t{cameratime}",(debugpos[0],debugpos[1]+200))
    text(f"Mode change \t{MCtime}",(debugpos[0],debugpos[1]+220))
    '''
def playereditmode():
    if mode=="edit":
        editmenu()
        player.jump=False
        player.f=[2,2]
        player.g=[0,0]
        player.coll=False
        player.voideath=False
        player.speed=10
        
 

    else:
        player.jump=True
        player.f[1]=1.1
        player.coll=True
        player.voideath=True
    
        try:
            blocksUnderPlayer = [world.map[(player.pos[1]+5)//blockSize+1][player.pos[0]//blockSize],world.map[(player.pos[1]+5)//blockSize+1][player.pos[0]//blockSize+1]]
        except:
            blocksUnderPlayer = [0,0]
        if 5 in blocksUnderPlayer:
            player.f=[1.1,1.1]
            player.speed=2
        elif not 0 in blocksUnderPlayer:
            player.f=[2,1.1]
            player.speed=7
        player.g=[0,1]
def gameupdate():
    global events
    events=pygame.event.get()
    
    mouseupdate()
    checkforquit()
    checkvideoresize()
def defaultgameloop(FPS=60):
    global mposrender
    global events
    global ttime,tiletime,ptime,cameratime,MCtime,window,fullscreen
    global tick60,oldtick60,gamefps,screen60,screenfps
    global coins
    if tick/60 == tick//60:
        tick60 = time.time() 
        tick60diff = tick60 - oldtick60
        oldtick60=tick60
        gamefps=60/tick60diff
        screenfps = screen60
        screen60=0
    gametick(60)
    totalstarttime=time.time()
    gupdatestarttime=time.time()
    gameupdate()
    gupdateendtime=time.time()
    gupdatetime=gupdateendtime-gupdatestarttime
    MCstarttime=time.time()
    checkmodechange()
    checkdebugchange()
    MCendtime=time.time()
    MCtime=MCendtime-MCstarttime
    window.fill([100,230,255])#background
    playerstarttime=time.time()
    playerendtime=time.time()
    ptime=playerendtime-playerstarttime
    camerastarttime=time.time()
    camera.pos[0]=player.pos[0]-320

    camera.pos[1]=player.pos[1]-180
    cameraendtime=time.time()
    cameratime=cameraendtime-camerastarttime
    
    playereditmode()
    mposrender=str(mpos)
    totalenttime=time.time()
    ttime=totalenttime-totalstarttime
    for i in snowballs:
        if i.pos[0]>camera.pos[0] and i.pos[0]<camera.pos[0]+window.get_size()[0]:
            i.update()
        if i.v[1]==0:
            snowballs.remove(i)

    if tick//60==tick/60:
        pass
    for i in range(len(world.map)):
        for j in range(len(world.map[1])):
            
            if world.map[i][j]==11 and random.randint(1,60)==1:
                snowballs.append(entity(pos=[j*blockSize+random.randint(0,blockSize),i*blockSize+random.randint(0,blockSize)],image=snowimg,coll=True,g=[0,0.25],a=[0.5,0]))
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:

                fullscreen = not fullscreen
                if fullscreen:
                    screenFlags         = pygame.RESIZABLE| pygame.DOUBLEBUF | pygame.SCALED | pygame.FULLSCREEN        #sets flags
                    window              = pygame.display.set_mode(window.get_size(),screenFlags)       #applys flags, makes window resizable
                else:
                    screenFlags         = pygame.RESIZABLE| pygame.DOUBLEBUF | pygame.SCALED       #sets flags
                    window              = pygame.display.set_mode(window.get_size(),screenFlags)       #applys flags, makes window resizable
                
    
    if player.v[1]<-2:
        if abs(player.v[0])>4:
            player.imageright = jumpimg
        else:
            player.imageright = jumpnomove
    elif player.v[1]>2:
        player.imageright = fallimg

    else:
        player.imageright = idleimg
    player.imageleft          = pygame.transform.flip(player.imageright,True,False)
    try:
        if mode == "play":
            if 8 in [world.map[int(player.pos[1]//blockSize)][int(player.pos[0]//blockSize)]]:
                world.map[int(player.pos[1]//blockSize)][int(player.pos[0]//blockSize)] = 12
                coins+=1
            if 8 in [world.map[(int(ceil(player.pos[1]/blockSize)))][int(player.pos[0]//blockSize)]]:
                world.map[(int(ceil(player.pos[1]/blockSize)))][int(player.pos[0]//blockSize)] = 12
                coins+=1
            if 8 in [world.map[int(player.pos[1]//blockSize)][int(ceil(player.pos[0]/blockSize))]]:
                world.map[int(player.pos[1]//blockSize)][int(ceil(player.pos[0]/blockSize))] = 12
                coins+=1
            if 8 in [world.map[int(ceil(player.pos[1]/blockSize))][int(ceil(player.pos[0]/blockSize))]]:
                world.map[int(ceil(player.pos[1]/blockSize))][int(ceil(player.pos[0]/blockSize))] = 12
                coins+=1
    except:
        pass
    if pygame.Rect(savebutton).collidepoint(mpos) and mousePressed and mode=="edit":
        worldtxt = open("world.txt","w")
        coins+=1
        worldtxt.write(world.convertToStr())
        print("saved")
    if fpscounter>=60:
        tilestarttime=time.time()
        window.blit(world.surface(camera),(0,0))
        tileendtime=time.time()
        if showdebug:       
            debugmenu()
            player.alwaysshowhitbox=True
        else:
            player.alwaysshowhitbox=False
            tiletime=tileendtime-tilestarttime
        if mode =="edit":
            blitcursor()
            pygame.draw.rect(window,(255,200,200),savebutton)
        else:
            window.blit(numfont.render(str(coins),False,(0,0,0)),(0,0))
        screen60 +=1
    player.update()
    camera.update()
    if fpscounter>=60:
        pygame.display.flip() #loads the screen 
print("loading complete")   
snowimg = pygame.image.load("particles"+sep+"smallsnow.png")
snowimg = pygame.transform.scale(snowimg,(8,8))
snowballs=[entity(pos=[0,0],image=snowimg,coll=True,g=[0,0.25],a=[1,0])]
player.spawnpoint=[100*blockSize, 88*blockSize]
player.respawn()
mode="play"
mousetilepos=[0,0]


while running:
    try:  
        defaultgameloop(60)
        '''
        print(f"""

    Expected total \t0.0167
    Total time \t\t{ttime}
    tiles \t\t{tiletime}
    player  \t\t{ptime}
    camera \t\t{cameratime}
    Mode change \t{MCtime}  
    """)
    '''
    except KeyboardInterrupt:
       save(world.map,"world.txt")
       quit()
pygame.quit()
#Game loop start---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
