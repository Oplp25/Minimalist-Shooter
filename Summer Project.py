import pygame, time, random, os

pygame.init()

#Initialising variables
win=pygame.display.set_mode((640,640))
pygame.display.set_caption('Shooter')
font = pygame.font.SysFont(None, 100)
halfFont=pygame.font.SysFont(None,75)
newFont =  pygame.font.SysFont(None, 50)
loadTextNew=halfFont.render('Pick a save file to load',True,(255,0,0),(0,0,0))
titleText=font.render('Shooter',True,(255,0,0),(0,0,0))
nextLevelText=newFont.render('Next Level',True,(255,0,0),(0,200,0))
upgradeText=newFont.render('Upgrade',True,(255,0,0),(0,200,0))
saveText=newFont.render('Save',True,(255,0,0),(0,200,0))
loadText=newFont.render('Load',True,(255,0,0),(0,200,0))
listOfBarriers=[pygame.Rect(0,0,640,40),pygame.Rect(0,0,40,640),pygame.Rect(600,0,40,640),pygame.Rect(0,600,640,40),pygame.Rect(120,120,80,40),pygame.Rect(440,120,80,40),pygame.Rect(280,120,80,80),pygame.Rect(160,160,40,40),pygame.Rect(440,160,40,40),pygame.Rect(80,200,40,80),pygame.Rect(520,200,40,80),pygame.Rect(280,280,80,80),pygame.Rect(80,360,40,80),pygame.Rect(520,360,40,80),pygame.Rect(160,440,40,40),pygame.Rect(440,440,40,40),pygame.Rect(440,480,80,40),pygame.Rect(120,480,80,40),pygame.Rect(280,440,80,80)]
bullets=[]
startButtonHitbox=pygame.Rect(40,160,240,80)
upgradeButtonHitbox=pygame.Rect(40,280,240,80)
saveButtonHitbox=pygame.Rect(40,400,240,80)
loadButtonHitbox=pygame.Rect(40,520,240,80)
buttonList=[startButtonHitbox,upgradeButtonHitbox,saveButtonHitbox,loadButtonHitbox]

#class for all the bullets that the soldiers fire and that inflicts damage
class bullet(object):
    def __init__(self,direction,x,y):
        self.x=x
        self.y=y
        self.vel=direction
    
    def move(self):
        self.y=self.y-(10*self.vel)
        
    def checkCollisions(self):
        self.hitbox=pygame.Rect(self.x,self.y,8,8)
        for i in listOfBarriers:
            if self.hitbox.colliderect(i):
                bullets.remove(self)
        for i in soldiers:
            if self.hitbox.colliderect(i.hitbox):
                i.hp-=1
                if i.hp<=0:
                    soldiers.remove(i)
                bullets.remove(self)
    def draw(self):
        pygame.draw.rect(win,(0,0,0),(self.x,self.y,8,8))
 
#class of the player character as well as all the enemies.
class soldier(object):
    def __init__(self,team,x,y):
        self.team=team
        self.x=x
        self.y=y
        self.hp=3
        if self.team=='red':
            self.xp=0
        self.bulletCountdown=30
        self.hitbox=pygame.Rect(self.x,self.y,40,24)
        self.moveTimer=20
        if self.team =='blue':
            self.colour=(0,0,255)
        elif self.team =='red':
            self.colour=(255,0,0)
        self.rotation=0
        '''
            0
            |
          3-+-1
            |
            2
        '''
        
    def createBullet(self):
        if self.bulletCountdown>=30:
            if self.team=='blue':
                x=True
                for i in soldiers:
                    if i!=player and i!=self and i.y<self.y and self.x<i.x<self.x+40:
                         x=False
                if x:
                    bullets.append(bullet(-1,self.x+16,self.y+24))
                    self.bulletCountdown=0
            else:
                bullets.append(bullet(1,self.x+16,self.y))
                self.bulletCountdown=0
    
    #move function for the AI
    def move(self):
        if self.moveTimer>=20:
            self.direction=random.randint(0,3)
            self.moveTimer=0
        else:
             self.moveTimer+=1
        if self.direction==0 and checkMove(self,'up'):
            self.y-=5
        elif self.direction==1 and checkMove(self,'right'):
            self.x+=5
        elif self.direction==2 and checkMove(self,'down'):
            self.y+=5
        elif self.direction==3 and checkMove(self,'left'):
            self.x-=5
    def draw(self):
        self.hitbox=pygame.Rect(self.x,self.y,40,24)
        pygame.draw.rect(win,self.colour,(self.x+8,self.y,24,24))
        pygame.draw.rect(win,self.colour,(self.x,self.y+8,8,8))
        pygame.draw.rect(win,self.colour,(self.x+32,self.y+8,8,8))
        pygame.draw.rect(win,(100,255,100),(self.x+8,self.y-16,self.hp*8,8))
        if self.hp<3:
            pygame.draw.rect(win,(255,100,100),(self.x+8+self.hp*8,self.y-16,(3-self.hp)*8,8))

#Function that draws the level based on the pygame.Rect objects in the list listOfBarriers
def drawLevel():
    win.fill((220,220,220))
    for i in listOfBarriers:
        pygame.draw.rect(win,(0,200,0),i)
    #Obsolete algorithm to draw the level
    '''x=0
    y=0
    step=40
    f=open('level.txt','r')
    for i in f:
        for g in i:
            if g=='=':
                pygame.draw.rect(win,(0,200,0),(x,y,step,step))
            x+=step
        x=0
        y+=step
    f.close()'''

#Function that stats every new level. Makes a black screen with information on the level, then initialises all the enemy soldier objets and resets all the player's variables
def beginLevel(level):
    win.fill((0,0,0))
    text=font.render('level '+str(level),True,(255,0,0))
    win.blit(text,(225,275))
    pygame.display.update()
    time.sleep(2)
    drawLevel()
    for i in range(level):
        soldiers.append(soldier('blue',(600/(level+1))*(i+1),80))
    player.bulletCountdown=30
    player.hp=3
    player.x=300
    player.y=560

#A function to check if a soldier would move into a wall. Returns True if the soldier does not walk into a wall 
def checkMove(soldier,direction):
    if direction=='up':
        y=soldier.y-5
        hitbox=pygame.Rect(soldier.x,y,40,24)
        for i in listOfBarriers:
            if hitbox.colliderect(i):
                return False
        for i in soldiers:
            if hitbox.colliderect(i.hitbox) and i!=soldier:
                return False
        return True
    
    elif direction=='down':
        y=soldier.y+5
        hitbox=pygame.Rect(soldier.x,y,40,24)
        for i in listOfBarriers:
            if hitbox.colliderect(i):
                return False
        for i in soldiers:
            if hitbox.colliderect(i.hitbox) and i!=soldier:
                return False
        return True
    
    elif direction=='left':
        x=soldier.x-5
        hitbox=pygame.Rect(x,soldier.y,40,24)
        for i in listOfBarriers:
            if hitbox.colliderect(i):
                return False
        for i in soldiers:
            if hitbox.colliderect(i.hitbox) and i!=soldier:
                return False
        return True
    
    elif direction=='right':
        x=soldier.x+5
        hitbox=pygame.Rect(x,soldier.y,40,24)
        for i in listOfBarriers:
            if hitbox.colliderect(i):
                return False
        for i in soldiers:
            if hitbox.colliderect(i.hitbox) and i!=soldier:
                return False
        return True

def upgrade():
    pass
def save(trueLevel):
    win.fill((0,0,0))
    text=newFont.render('Name Your Save',True,(255,0,0),(0,0,0))
    win.blit(text,(175,175))
    pygame.draw.rect(win,(0,200,0),(190,375,240,80))
    win.blit(saveText,(270,400))
    pygame.display.update()
    saving=True
    saveName=''
    isCapital=0
    capsLockOn=0
    while saving:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                y=1
                if event.key==pygame.K_RETURN:
                    saving=False
                    break
                if isCapital==1:
                    saveName=saveName+str(pygame.key.name(event.key).upper())
                    y=0
                isCapital=0
                if event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT or event.key==pygame.K_CAPSLOCK:
                    if capsLockOn==0:
                        isCapital=1
                    if event.key==pygame.K_CAPSLOCK:
                        if capsLockOn==0:
                            capsLockOn=1
                        else:
                            capsLockOn=0
                    y=0
                if y==1:
                    saveName=saveName+str(pygame.key.name(event.key))
                    
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(190,375,240,80).collidepoint(pygame.mouse.get_pos()):
                    saving=False
                    break
        name=newFont.render(saveName,True,(255,0,0),(0,0,0))
        win.blit(name,(275-len(saveName)*5,275))
        pygame.display.update()
        
    f=open("C:/Users/jakob/OneDrive/Documents/A-Levels/Computer Science/Misc. Code/Summer Project/Saves/"+saveName+".txt",'w')
    f.write(str(level)+','+str(player.xp))
    f.close()
    menu(trueLevel)

def load():
    saves=[('Saves/'+name) for i,j,k in os.walk('C:/Users/jakob/OneDrive/Documents/A-Levels/Computer Science/Misc. Code/Summer Project/Saves') for name in k]
    buttons=[]
    for i in range(len(saves)):
        if len(saves)<=5:
            buttons.append(pygame.Rect(80,(500/len(saves))*i+120,480,80))
        elif len(saves)<=10:
            if i<=4:
                buttons.append(pygame.Rect(40,108*(i+1),240,80))
            else:
                buttons.append(pygame.Rect(360,108*(i-4),240,80))
    win.fill((0,0,0))
    win.blit(loadTextNew,(20,20))
    for index,i in enumerate(buttons):
        pygame.draw.rect(win,(0,200,0),i)
        saveInUse=saves[index].split('/')[1].split('.')[0]
        if len(saves)<=5:
            savesText=halfFont.render(saveInUse,True,(255,0,0))
            if len(saveInUse)<=11:
                   win.blit(savesText,(200,(500/len(saves))*index+135))
            else:
                win.blit(savesText,(80,(500/len(saves))*index+135))
        else:
            savesText=newFont.render(saveInUse,True,(255,0,0))
            if index<=4:
                win.blit(savesText,(80,(108)*index+135))
            else:
                win.blit(savesText,(400,(108)*(index-5)+135))
    pygame.display.update()
    loading=True
    while loading:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                for index,i in enumerate(buttons):
                    if i.collidepoint(pygame.mouse.get_pos()):
                        f=open(saves[index],'r')
                        line=f.readline()
                        f.close()
                        attributeList=line.split(',')
                        level=attributeList[0]
                        player.xp=attributeList[1]
                        loading=False
                        break
    return level
def menu(trueLevel):
    win.fill((0,0,0))
    for i in buttonList:
        pygame.draw.rect(win,(0,200,0),i)
    win.blit(titleText,(200,10))
    win.blit(nextLevelText,(70,185))
    win.blit(upgradeText,(90,305))
    win.blit(saveText,(115,425))
    win.blit(loadText,(115,545))
    pygame.display.update()
    runMenu=True
    while runMenu:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                for i in buttonList:
                    if i.collidepoint(pygame.mouse.get_pos()):
                        if i==startButtonHitbox:
                            beginLevel(trueLevel)
                            runMenu=False
                        elif i==upgradeButtonHitbox:
                            upgrade()
                        elif i==saveButtonHitbox:
                            save(trueLevel)
                        elif i==loadButtonHitbox:
                            level=load()
                            return int(level)
            elif event.type==pygame.QUIT:
                pygame.quit()
                exit()
    return True
#initialising more variables
player=soldier('red',300,560)
soldiers=[player]
level=1
finalLevel=5

#function that draws the GUI
def draw():
    drawLevel()
    for i in soldiers:
        i.draw()
    for i in bullets:
        i.draw()
    pygame.display.update()
    
#initialising more variables
clock=pygame.time.Clock()

#running the menu
menuRunning=True
while menuRunning:
    x1=menu(level)
    if type(x1)==int:
        level=x1
    else:
        menuRunning=False
run=True
won=False
#Gameloop
while run:
    clock.tick(30)
    events=pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    #Checking if the mouse is clicked
        elif event.type==pygame.MOUSEBUTTONDOWN:
            player.createBullet()
    
    #Movement
    keys=pygame.key.get_pressed()
    if keys[pygame.K_d] and checkMove(player,'right'):
        player.x+=5
    elif keys[pygame.K_a] and checkMove(player,'left'):
        player.x-=5
    if keys[pygame.K_s] and checkMove(player,'down'):
        player.y+=5
    elif keys[pygame.K_w] and checkMove(player,'up'):
        player.y-=5
    
    #Checking if the level is completed, the game is won or the player is dead.
    if player.hp==0:
        won=False
        run=False
    elif soldiers==[player]:
        if level==finalLevel:
            won=True
            run=False
        else:
            level+=1
            #running the menu
            menuRunning=True
            while menuRunning:
                x1=menu(level)
                if type(x1)==int:
                    level=x1
                else:
                    menuRunning=False
    
    #Incrementing all the variables, enemies trying to shoot and bullet moving
    for i in soldiers:
        i.bulletCountdown+=1
        if i!=player:
            i.move()
            i.createBullet()
    for i in bullets:
        i.move()
        i.checkCollisions()
    draw()
    
#Win or lose screens
if won:
    win.fill((0,0,0))
    text=font.render('You Win!',True,(255,0,0))
    win.blit(text,(200,275))
    pygame.display.update()
else:
    win.fill((0,0,0))
    text=font.render('You Lose!',True,(255,0,0))
    win.blit(text,(175,275))
    pygame.display.update()

#a way to exit the you won/lost screen
while True:
    events=pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                pygame.quit()
                exit()