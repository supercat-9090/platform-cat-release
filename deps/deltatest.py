#0.6.2.1
print("loading modules...")
import  pygame                                                  #imports pygame, the game libary-
from    pygame.locals   import *                                #imports pygame.local
import  time                                                    #imports the time libary for functions like sleep()
from    math            import ceil                             #imports the ceiling (round up) function
import  random                                                  #imports the random libary
from    os              import listdir, sep                     #gets the file seperator / or \
print("modules loaded")                                         #prints after modules has loaded
pygame.display.init()                                           #initialises display
pygame.display.set_caption("Platform-Cat")                      #sets caption

# setup window
windowDefaultSize   = (640,640)                                 #sets window size
icon                = pygame.transform.scale(pygame.image.load("tiles"+sep+"flagtop"+sep+"icon.png"),(128,128))
screenFlags         = pygame.RESIZABLE| pygame.DOUBLEBUF        #sets flags
window              = pygame.display.set_mode(windowDefaultSize,screenFlags)       #applys flags, makes window resizable

pygame.display.set_icon(icon)                                   #sets the icon for the window
#Creates variables-----------------------------------------------------------------------------------------

#mpos=[0,0]
toolbarBlockDisplayPos=[0,0]                                    #temporary variable before it gets replaced
pygame.font.init()                                              #initializes pygame fonts
font                = pygame.font.SysFont("courier", 20)        #sets font to courier(Monospace font)
smallfont           = pygame.font.SysFont("courier", 15)

solidBlocks         = [1,2,5,6]                                 #Sets some of the blocks to be solid
checkpointBlocks    = [3,4]                                     #Sets some of the blocks to be checkpoints
player              = 0                                         #temperory player so functions will not freak out                                 
selectbox           = []                                        
tpos                = [16,16]
#mposrender          = ""
running             = True                                      #if the game is running
clock               = pygame.time.Clock()                       #pygame's clock

selectedBlock       = 0                                         #current block selected (in edit mode ) 
tick                = 0                                         #the current tick the 
currenttick         = 0                                         #the time of the latest tick
oldtick             = 0                                         #the time of the second latest tick
tickspeed           = 0                                         #how long each tick takes
cursorColour        = (0,255,255)                               #colour of the cursor (box)
mousePressed        = False                                     
mouseButton         = 1
mousetilepos        = [0,0]
mode="edit"
fps30               = False
ttime               = 0
fpscounter          = 60
dtime               = 1 
tiletime            = 0
ptime               = 0
cameratime          = 0
MCtime              = 0
background          = pygame.image.load("background.png")
background          = pygame.transform.scale(background,(640,640))
showdebug           = False
#loads world------------

def loadworld(filename):    
    global error
    global world  
    try:
        world=open(filename,"r") 
    except:
        print("World "+filename+" could not be found")
        quit()
        exit()
        

loadworld("world.txt")
world=world.read()      #reads world file
world=world.split("\n") #splits the Y axis
for i in world: #splits X axis
    if i =="":
        del world[world.index(i)]
    else:
        world[world.index(i)]=world[world.index(i)].split()
worldsize=[len(world[0]),len(world)]

for i in range(worldsize[1]):
    error=False
    
    for j in range(worldsize[0]):
        world[i][j]=int(world[i][j])
#functions-----------------------------------------------------------------------------------------
def save():  #save function savfunc
    savetxt=""
    for i in range(len(world)):
        for j in range(len(world[i])):        
            savetxt=savetxt+str(world[i][j])+" "
            savetxt.replace(" ","",-1)
        savetxt+="\n"
    
    worldWrite=open("world.txt","w")
    worldWrite.write(savetxt)
worldrot=[]
for i in range(len(world)):
    worldrot.append([])
    for j in range(len(world[0])):
        worldrot[i].append(0)

def blockcolltrue(entity=player, blockList=solidBlocks):
    try:
        for collblock in blockList:
            if collblock in [world[int(entity.pos[1]//64)][int(entity.pos[0]//64)] or collblock in [world[int(entity.pos[1]//64)][int(entity.pos[0]//64)]],
                world[(int(ceil(entity.pos[1]/64)))][int(entity.pos[0]//64)],
                world[int(entity.pos[1]//64)][int(ceil(entity.pos[0]/64))],
                world[int(ceil(entity.pos[1]/64))][int(ceil(entity.pos[0]/64))]]:
                return True

        
    except:
        return False
    return False

#sets up the entity class
events=pygame.event.get()
class entity:
    """
    The entity class----
    Functions:
        update()
            Updates the entity, run every frame

    """
    def __init__(self,entityType="default",pos=[0,0],v=[0,0],f=[2,2],a=[0,0],rot = 0,controls=[],speed=4,image=pygame.image.load("tiles"+sep+"empty"+sep+"icon.png").convert_alpha(),jump=True,coyote=4,maxcoyote=6,jumpheight=60,coll=True,hitbox=[0,0,64,64],alwaysshowhitbox=False,rect=[(0,0,255),0],g=[0,0],oldpos=[0,0],roundpos=True,voiddeath=False,spawnpoint=[0,0]):
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
        self.coll               = coll
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
    def update(self):
        global events
        global fpscounter
        global dtime
        #print(dtime)
        global checkpointBlocks
        self.oldpos=self.pos
        self.maxcoyote=6/dtime
        self.v=[self.a[0]*dtime+self.v[0],self.a[1]*dtime+self.v[1]]#updates velocity using accelaration
        self.v=[self.g[0]*dtime+self.v[0],self.g[1]*dtime+self.v[1]]#updates velocity using gravity
        self.v=[self.v[0]/self.f[0]**dtime,self.v[1]/self.f[1]**dtime]#updates velocity using friction
        
        self.pos[0] +=self.v[0]*dtime#updates postion based on velocity
        
        if blockcolltrue(self,solidBlocks) and self.coll:
            self.pos[0] -=self.v[0]
            self.v[0]=0
            
        
        self.pos[1] +=self.v[1]*dtime
        if blockcolltrue(self,solidBlocks) and self.coll:
            self.pos[1] -=self.v[1]
            if self.jump and self.v[1]>0:
                self.coyote=self.maxcoyote
            self.v[1]=0
        if blockcolltrue(self,checkpointBlocks):
            self.spawnpoint=self.pos
        if self.v[1]>0:
            if self.coyote>0:
                self.coyote-=1
        self.hitbox=[self.pos[0],self.pos[1],self.hitbox[2],self.hitbox[3]]
        if self.roundpos:
            self.pos=[round(self.pos[0]),round(self.pos[1])]
        if self.alwaysshowhitbox:
            pygame.draw.rect(window,self.rect[0],[self.hitbox[0]-camera.pos[0],self.hitbox[1]-camera.pos[1],self.hitbox[2],self.hitbox[3],],self.rect[1])
        window.blit(self.image,(self.pos[0]-camera.pos[0],self.pos[1]-camera.pos[1]))
        if self.voideath and (self.pos[1]>128+len(world)*64):
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
        if self.moveDir[0] == 1:
            self.image=self.imageright
        if self.moveDir[0] == -1:
            self.image=self.imageleft
        if len(self.controls)>4:
            self.a=[self.moveDir[0]*self.speed,self.moveDir[1]*self.speed]
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
    img("tiles"+sep+"cloud"+sep+"icon.png",True)
         ]
errortile=pygame.transform.scale(img("error.png"),(64,64))
for i in tile:
    tile[tile.index(i)]=pygame.transform.scale(tile[tile.index(i)],(64,64))

for i in tile:
    selectbox.append([tpos[0],tpos[1]])
    tpos[0]+=64          
player=entity(controls=[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT],jump=True,speed=6,jumpheight=30,image=pygame.transform.scale(img("Cat"+sep+"cat_0001.png",True),(64,64)))
camera=entity(entityType="camera",coll=False, alwaysshowhitbox=False)




 

 
print("loading functions...")
def blittiles():
    blockDisplayPosition=[0-camera.pos[0],0-camera.pos[1]]
    currentBlockPos=[0,0]
    winx,winy=window.get_size()
    blockIndex=0
    tileStartPos = [round(camera.pos[0]//64),round(camera.pos[1]//64)]
    for i in range(tileStartPos[1],len(world)): #Draws the tile one by one
        if blockDisplayPosition[1]>winy:
            break
        for j in range(tileStartPos[0],len(world[i])):
            blockDisplayPosition=[0-camera.pos[0]+j*64,0-camera.pos[1]+i*64]
            if blockDisplayPosition[0]>winx:
                break
            try:
                window.blit(tile[(world[i][j])],blockDisplayPosition)
                if showdebug:
                    window.blit(smallfont.render(str(blockIndex),True,(0,0,0),(255,255,255)),blockDisplayPosition)
                    window.blit(smallfont.render(str(i)+" "+str(j),True,(0,0,0),(255,255,255)),(blockDisplayPosition[0],blockDisplayPosition[1]+20))
                blockIndex+=1
            except:
                window.blit(errortile,blockDisplayPosition)

            currentBlockPos[0]+=1
        currentBlockPos[0]=0
        currentBlockPos[1]+=1
def blitcursor():
    global mouseTilePos
    if mouseTilePos[0]>=len(world[0]) or mouseTilePos[0]<0 or mouseTilePos[1]>=len(world)or mouseTilePos[1]<0: #sets cursor colour
        cursorcolour=(255,0,0)
    else:
        cursorcolour=(0,255,255)

    if mpos[1]>80 and mode=="edit":
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)
    if mpos[1]>80 or not mode=="edit":
        pygame.draw.rect(window,cursorcolour,(mouseTilePos[0]*64-camera.pos[0],mouseTilePos[1]*64-camera.pos[1],64,64),5)#draws the cursor
events=pygame.event.get()
debugpos=[0,100]
blockselectpos=[16,16]
#grav_max=8
#grav_strenght=2
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
            if event.key==pygame.K_c:
                blockselectpos[0]+=64
                
            if event.key==pygame.K_v:
                blockselectpos[0]-=64
    if mousePressed:
        try:
            if mpos[1]>80 and mbutton==1:
                world[mouseTilePos[1]][mouseTilePos[0]]=selectedBlock
            elif mpos[1]>80 and mbutton==3:
                world[mouseTilePos[1]][mouseTilePos[0]]=0
            else:
                for selectpos in selectbox:
                    
                    if mpos[0]>selectpos[0] and mpos[1]>selectpos[1] and mpos[0]<selectpos[0]+32 and mpos[1]<selectpos[1]+32:
                       
                        selectedBlock =selectbox.index(selectpos)

    
        except:
            pass 
    #pygame.draw.rect(window,(128,128,128),(0,0,4096,80))#draws the selection underlay
    
    for tile_selected in tile:#display select icons
        
        if tile.index(tile_selected)==selectedBlock:
            #pygame.draw.rect(window,(0,0,255),(toolbarBlockDisplayPos[0]-5,toolbarBlockDisplayPos[1]-5,32+10,32+10),5)
            window.blit(pygame.transform.scale(tile_selected,(32,32)),toolbarBlockDisplayPos)
        else:
            temptile=tile_selected.copy()
            temptile.set_alpha(100)
            window.blit(pygame.transform.scale(temptile,(32,32)),toolbarBlockDisplayPos)
        toolbarBlockDisplayPos[0]+=64
    toolbarBlockDisplayPos=[blockselectpos[0],blockselectpos[1]]
    tpos=[16,16]
    for i in tile:
        selectbox.append([tpos[0],tpos[1]])
        tpos[0]+=64

def mouseupdate():
    global mpos
    global mouseTilePos
    global mousePressed
    global events
    global mposrender
    global mbutton
    mpos= pygame.mouse.get_pos()
    mouseTilePos=[round((camera.pos[0]+mpos[0])/64),round((camera.pos[1]+mpos[1])/64)]
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
    global dtime
    currenttick=time.time()
    tickspeed=currenttick-oldtick
    try:
        fpscounter=1/tickspeed
    except:
        fpscounter=500
    if fpscounter>12:
        dtime = 60/fpscounter
    else:
        dtime = 5
    oldtick=time.time()
    clock.tick(200)
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
def camerafollow(entity=player):
    camera.pos=[entity.pos[0]-320,entity.pos[1]-320]
def text(text,pos):
    window.blit(font.render(str(text),True,(0,0,0),(255,255,255)),pos,)

def debugmenu(): #debug function DF
    global ttime,tiletime,ptime,cameratime,MCtime

    window.blit(font.render("Mouse Pos: "+mposrender,True, (0,0,0), (255,255,255)),debugpos)#debug for mouse
    try:
        window.blit(font.render("pos: "+str(round(player.pos[0],3))+" "+str(round(player.pos[1],3))+" "+"v: "+str(round(player.v[0],3))+" "+str(round(player.v[1],3))+" "+"a: "+str(round(player.a[0],3))+" "+str(round(player.a[1],3))+" "+"f: "+str(round(player.f[0],3))+" "+str(round(player.f[1],3)),True,(0,0,0),(255,255,255)),[debugpos[0],debugpos[1]+20])
        
    except:
        pass

    text(player.coll,(debugpos[0],debugpos[1]+60))
    window.blit(font.render("Coyote: "+str(player.coyote),True,(0,0,0),(255,255,255)),(debugpos[0],debugpos[1]+80),)
    text("FPS: "+str(round(fpscounter)),(debugpos[0],debugpos[1]+100))
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
            
        try:
            blocksUnderPlayer = [world[(player.pos[1]+5)//64+1][player.pos[0]//64],world[(player.pos[1]+5)//64+1][player.pos[0]//64+1]]
        except:
            blocksUnderPlayer = [0,0]
        if 5 in blocksUnderPlayer:
            player.f=[1.1,1.1]
            player.speed=2
        elif not 0 in blocksUnderPlayer:
            player.f=[2,1.1]
            player.speed=6
        player.g=[0,1]
        player.voideath=True

def gameupdate():
    global events
    events=pygame.event.get()
    
    mouseupdate()
    checkforquit()
    checkvideoresize()
def defaultgameloop(FPS=60):
    global mposrender
    global events
    global ttime,tiletime,ptime,cameratime,MCtime
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
    #window.blit(background,(0,0))
    tilestarttime=time.time()
    blittiles()
    tileendtime=time.time()
    tiletime=tileendtime-tilestarttime
    blitcursor()
    playerstarttime=time.time()
    player.update()
    playerendtime=time.time()
    ptime=playerendtime-playerstarttime
    camerastarttime=time.time()
    camera.update()
    cameraendtime=time.time()
    cameratime=cameraendtime-camerastarttime 
    camerafollow(player)
    playereditmode()
    mposrender=str(mpos)
    if showdebug:       
        debugmenu()
    totalenttime=time.time()
    ttime=totalenttime-totalstarttime
    for i in leaves:
        i.update()
        if i.v[1]==0:
            leaves.remove(i)
    if tick//60==tick/60:
        leaves.append(entity(pos=[0,0],image=leafimg,coll=True,g=[0,0.5],a=[1,0]))
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

    pygame.display.flip() #loads the screen 
print("loading complete")   
leafimg = pygame.image.load("particles"+sep+"leaf.png")
leafimg = pygame.transform.scale(leafimg,(32,32))
leaves=[entity(pos=[0,0],image=leafimg,coll=True,g=[0,0.5],a=[1,0])]
player.spawnpoint=[0, 576]
player.respawn()
mode="play"
mousetilepos=[0,0]


while running:
    try:  
        defaultgameloop(60)
        
    except KeyboardInterrupt:
        save()
        quit()
pygame.quit()
#Game loop start---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------