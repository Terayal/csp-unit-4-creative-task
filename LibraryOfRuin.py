from cmu_graphics import *
#Library game???
import random
import math
app.Startup = True
app.PlayerConfirm = False
app.PlayerConfirmStage = 0
app.CardWidth = 120
app.Xdisplace = 23
app.YStart = 40
app.FontSizeModifier = 2
app.MouseX = 0
app.MouseY = 0
#Ropes
AllCards = []
DisplayedHandCards = []
AllCharacters = []
PlayerSpeedDice = []
EnemySpeedDice = []
app.PausedForClash = False
app.CurrentSpeedBracket = -1
app.ActingDice = []
app.CharacterSpeed = 5
#----------------------------------------------------------------------------------------------
def onMousePress(x,y):
    app.MouseX = x
    app.MouseY = y
    AllDice = PlayerSpeedDice + EnemySpeedDice
    #print(AllDice)
    
    ClickedBackground = True
    for Die in PlayerSpeedDice:
        if Die.ConnectedSprite.hits(x,y):
            ClickedBackground = False
            for PDie in PlayerSpeedDice:
                if PDie != Die:
                    PDie.Clicked = False
                    RemoveTargetLine(PDie)
            
            
    for Die in EnemySpeedDice:
        if Die.ConnectedSprite.hits(x,y):
            ActiveSpeedDie = None
            ActiveCard = None
            
            for PDie in PlayerSpeedDice:
                if PDie.Clicked:
                    ActiveSpeedDie = PDie
                    
            for PCard in DisplayedHandCards:
                if PCard.Clicked:
                    ActiveCard = PCard
                    
            if ActiveSpeedDie != None and ActiveCard != None and app.PlayerConfirmStage == 1:
                
                TargetWithPage(ActiveSpeedDie, ActiveCard, ActiveSpeedDie.ConnectedCharacter, Die)
                
        #elif Die.Clicked:
            #Die.Clicked = False
            #RemoveTargetLine(Die)
            
    for Card in DisplayedHandCards:
        if Card.hits(x,y):
            ClickedBackground = False
        elif Card.Clicked:
            Card.Clicked = False
    
    for Die in AllDice:
        if Die.MousedOver and Die.ConnectedSprite.hits(x,y):
            Die.Clicked = True
            pass
        else:
            if ClickedBackground:
                Die.Clicked = False
                RemoveTargetLine(Die)
    for Card in DisplayedHandCards:
        if Card.MousedOver and Card.hits(x,y):
            Card.Clicked = True
            pass
        else:
            if ClickedBackground:
                Card.Clicked = False
        pass
    pass
def onMouseMove(x,y):
    app.MouseX = x
    app.MouseY = y
    AllDice = PlayerSpeedDice + EnemySpeedDice
    for Die in AllDice:
        if Die.ConnectedSprite.hits(x,y):
            Die.MousedOver = True
        else:
            Die.MousedOver = False
    for Card in DisplayedHandCards:
        if Card.hits(x,y):
            Card.MousedOver = True
        else:
            Card.MousedOver = False
            
#---------------------------------------------------------------------------------------------
            
def onKeyPress(key):
    print(key)
    #HideAllCards()
    if key == "escape":
        for Die in PlayerSpeedDice:
            UntargetSpeedDie(Die)
    if key == "space":
        if app.PlayerConfirmStage == 0 or app.PlayerConfirmStage == 1:
            app.PlayerConfirm = True
        pass
    pass
#--------------------------------------------------------------------------------
def onStep():
    AllDice = PlayerSpeedDice + EnemySpeedDice
    if app.Startup:
        Startup()
        HideAllCards()
    else:
        if app.PlayerConfirmStage == 1 or app.PlayerConfirmStage == 0:
            for Die in AllDice:
                if Die.MousedOver or Die.Clicked:
                    if Die.ConnectedCharacter.ControlledByPlayer:
                        DisplayHand(Die.ConnectedCharacter, Die)
                    if Die.HeldPage != None:
                        Die.HeldPage.visible = True
                else:
                    if Die.ConnectedCharacter.ControlledByPlayer:
                        if not Die.Override:
                            HideHand(Die.ConnectedCharacter)
                            pass
                        pass
                    if Die.HeldPage != None:
                        Die.HeldPage.visible = False
        elif app.PlayerConfirmStage == 2:
            if app.PausedForClash and len(app.ActingDice) > 0:
                #print("doing clash")
                FirstSprite = app.ActingDice[0].ConnectedCharacter.CharacterSprite
                SecondSprite = app.ActingDice[0].TargetDie.ConnectedCharacter.CharacterSprite
                if FirstSprite.hitsShape(SecondSprite):
                    #checks if the two characters are touching
                    ("touching so clash!")
                else:
                    #you can add more complexity of moving together if equal later
                    #print("try to move")
                    MoveATowardB(FirstSprite,SecondSprite)
        #app.PausedForClash = False
        #for Card in AllCards
    if app.PlayerConfirm == True:
        
        if app.PlayerConfirmStage == 0:
            MoveToPageSelect()
            app.PlayerConfirmStage = 1
            app.PlayerConfirm = False
        elif app.PlayerConfirmStage == 1:
            MoveToClashes()
            app.PlayerConfirmStage = 2
            app.PlayerConfirm = False
            
#------------------------------------------------------------------------------------------
            
def CreateLightSprite(Character):
    
    Light = Circle(Character.CharacterSprite.centerX,Character.CharacterSprite.centerY - 80, 10, opacity = 70)
    Character.add(Light)
    Character.LightSprites.append(Light)
    FixLightSpritePositions(Character)
        
def FixLightSpritePositions(Character):
    
    LightDisp = (Character.MaxLight * 20) / -2
    Index = 1
    #print(Character.LightSprites)
    for LightMote in Character.LightSprites:
        LightMote.centerX = Character.CharacterSprite.centerX + LightDisp
        LightMote.centerY = Character.CharacterSprite.centerY - 80
        LightDisp += 20
        
        if Character.Light >= Index:
            LightMote.radius = 10
            LightMote.fill = "gold"
        else:
            LightMote.radius = 7
            LightMote.fill = "brown"
        
        Index += 1
        
def ResethandCardPositions():
    PrevX = 0
    for Card in DisplayedHandCards:
        #ReconstructCard(Card)
        Card.left = PrevX
        Card.centerY = 330
        PrevX = Card.right

def DisplayHand(Character, ThisDie):
    if len(DisplayedHandCards) == 0:
        for Card in Character.Hand:
            #HideHalfCard(Card)
            Card.visible = True
            DisplayedHandCards.append(Card)
            ResethandCardPositions()
    else:
        ResethandCardPositions()
        for Card in DisplayedHandCards:
            if Card.Clicked or Card.MousedOver:
                #DisplayFullCard(Card)
                Card.rotateAngle = -10
                if Card.Clicked:
                    ThisDie.Targetting = True
                    if ThisDie.TargettingLine == None:
                        ThisDie.TargettingLine = Line(ThisDie.ConnectedSprite.centerX, ThisDie.ConnectedSprite.centerY, app.MouseX,app.MouseY, fill="blue")
                    else:
                        ThisDie.TargettingLine.x2 = app.MouseX
                        ThisDie.TargettingLine.y2 = app.MouseY
                
                pass
            else:
                Card.rotateAngle = 0
                #HideHalfCard(Card)
                pass
            
    
    for Die in Character.SpeedDice:
        if not Die == ThisDie:
            Die.Override = True
        else:
            Die.Override = False
        

def ClearList(List):
    while len(List) > 0:
        List.remove(List[0])
        
def HideHand(Character):
    for Card in Character.Hand:
        Card.visible = False
        ClearList(DisplayedHandCards)
    
    for Die in Character.SpeedDice:
        Die.Override = False

def CreateDie(min,max,type,diceList):
    Die = Group()
    Die.type = type
    if Die.type == "slash" or Die.type == "pierce" or Die.type == "blunt":
        Die.color = "red"
    if Die.type == "block" or Die.type == "evade":
        Die.color = "lightBlue"
    if Die.type == "counter":
        Die.color = "yellow"
    Die.min = min
    Die.max = max
    diceList.append(Die)
    
def CreateSpeedDie(min,max,diceList):
    Die = Group()
    Die.speed = 0
    Die.min = min
    Die.max = max
    Die.MousedOver = False
    Die.Clicked = False
    Die.Override = False
    Die.TargettingLine = None
    Die.ClashLine = None
    diceList.append(Die)
    
def CreateDeckList(ListOfNames):
    ListOfInts = []
    for Name in ListOfNames:
        index = 0
        found = False
        for Card in AllCards:
            if not found:
                if(Name == Card.name):
                    #print("found card!")
                    found = True
                    ListOfInts.append(index)
                    pass
                else:
                    index += 1
        pass
    if len(ListOfNames) != len(ListOfInts):
        print("There is a card Missing!!!!!!!!!!")
    return ListOfInts
    
#----------------------------------------------------------------------------------------------
    
def CreateCard(color,cost,name,dice):
    FullCard = Group()
    #seperates the lists because I got destroyed by that a while back
    NewDiceList = list(dice)
    Image = Rect(0,0,app.CardWidth/2,100, border = color, borderWidth = 4)
    FullCard.color = color
    CostCircle = Circle(10,10,10,fill = color)
    CostNumber = Label(cost,10,10)
    FullCard.cost = cost
    NameBox = Rect(0,18,app.CardWidth/2,12, fill=color)
    #NameBox.rotateAngle = -10
    #print(len(name))
    FullCard.fontsize = 15 - int(len(name)/app.FontSizeModifier)
    NameText = Label(name,NameBox.centerX,NameBox.centerY, size = FullCard.fontsize)
    #NameText.rotateAngle = -10
    FullCard.name = name
    FullCard.add(Image,CostCircle,CostNumber,NameBox,NameText)
    #---------------------------------------------------------
    #creates the right dice holding side of the card
    StartY = app.YStart
    for Die in NewDiceList:
        IconCircle = Circle(app.Xdisplace,StartY,4,fill=Die.color)
        FullCard.add(IconCircle)
        DamageText = Label(str(Die.min) + "-" + str(Die.max),app.Xdisplace+20,StartY,fill=Die.color)
        FullCard.add(DamageText)
        StartY += 14
        pass
    FullCard.centerX = 200
    FullCard.DiceList = NewDiceList
    FullCard.Clicked = False
    FullCard.MousedOver = False
    
    AllCards.append(FullCard)

def CopyCard(Card,NewList):
    #creates a copy of the specified card based on it's values, and adds it to the new list
    FullCard = Group()
    Image = Rect(0,0,app.CardWidth/2,100, border = Card.color, borderWidth = 4)
    CostCircle = Circle(10,10,10,fill = Card.color)
    CostNumber = Label(Card.cost,10,10)
    FullCard.cost = Card.cost
    NameBox = Rect(0,18,app.CardWidth/2,12, fill= Card.color)
    #NameBox.rotateAngle = -10
    NameText = Label(Card.name,NameBox.centerX,NameBox.centerY, size = Card.fontsize)
    #NameText.rotateAngle = -10
    FullCard.name = Card.name
    FullCard.add(Image,CostCircle,CostNumber,NameBox,NameText)
    #---------------------------------------------------------------------
    StartY = app.YStart
    NewDiceList = list(Card.DiceList)
    
    for Die in NewDiceList:
        IconCircle = Circle(app.Xdisplace,StartY,4,fill=Die.color)
        FullCard.add(IconCircle)
        DamageText = Label(str(Die.min) + "-" + str(Die.max),app.Xdisplace+20,StartY,fill=Die.color)
        FullCard.add(DamageText)
        StartY += 14
        pass
    FullCard.centerX = 200
    FullCard.DiceList = NewDiceList
    FullCard.Clicked = False
    FullCard.MousedOver = False
    
    NewList.append(FullCard)
    AllCards.append(FullCard)

def CreateCharacter(x,y,facing,ControlledByPlayer, SpeedDiceList,Decklist,MaxLight,MaxHandSize):
    FullCharacter = Group()
    FullCharacter.ControlledByPlayer = ControlledByPlayer
    FullCharacter.MaxLight = MaxLight
    FullCharacter.MaxHandSize = MaxHandSize
    FullCharacter.Light = MaxLight
    NewSpeedDiceList = list(SpeedDiceList)
    
    for Die in NewSpeedDiceList:
        Die.ConnectedCharacter = FullCharacter
        #print("assigned a character to a die")
        
    CharacterSprite = Oval(x,y,30,45)
    FullCharacter.CharacterSprite = CharacterSprite
    Eye = Circle(x+10,y-10,5,fill="red")
    FullCharacter.Eye = Eye
    FullCharacter.add(CharacterSprite, Eye)
    FullCharacter.FacingLeft = ControlledByPlayer
    if FullCharacter.FacingLeft:
        FullCharacter.Eye.centerX = FullCharacter.CharacterSprite.centerX -10
    DiceDisp = 40
    FullCharacter.Library = []
    FullCharacter.Hand = []
    FullCharacter.UnusedDice = []
    if len(NewSpeedDiceList) > 1:
        StartX = x - ((DiceDisp * len(NewSpeedDiceList)) / 3) 
    else:
        StartX = x
    #creates boxes and text for all speed dice
    FullCharacter.SpeedDice = []
    FullCharacter.SpeedDiceText = []
    FullCharacter.LightSprites = []
    for LightMote in range(MaxLight):
        CreateLightSprite(FullCharacter)
    for Die in NewSpeedDiceList:
        SpeedDiceSlot = Rect(StartX-20,y-60,30,30,borderWidth = 4, border = "blue")
        StartX += DiceDisp
        SpeedDiceSlot.fill = "red"
        SpeedDiceText = Label(str(Die.min) + "-" + str(Die.max),0,0)
        SpeedDiceText.centerX = SpeedDiceSlot.centerX
        SpeedDiceText.centerY = SpeedDiceSlot.centerY
        FullCharacter.add(SpeedDiceSlot, SpeedDiceText)
        Die.ConnectedSprite = SpeedDiceSlot
        if ControlledByPlayer:
            PlayerSpeedDice.append(Die)
        else:
            EnemySpeedDice.append(Die)
        Die.HeldPage = None
        Die.TargetDie = None
        Die.TargettedBy = []
        FullCharacter.SpeedDiceText.append(SpeedDiceText)
        FullCharacter.SpeedDice.append(Die)
        
    for CardNum in Decklist:
        #creates copies of all specified cards and adds them to the deck
        CopyCard(AllCards[CardNum],FullCharacter.Library)
        
    #FullCharacter.rotateAngle = facing * 180
    AllCharacters.append(FullCharacter)
    pass
    

def Startup():
    #----------------------------------------------------------------------------------------------
    #create all of the cards base        
    CreateCards()
    #----------------------------------------------------------------------------------------------
    #create characters
    CreateCharacters()
    
    for Character in AllCharacters:
        for drawing in range(5):
            DrawCard(Character)
    #------------------------------------------------------------------------------
    #Hide cards
    
    app.Startup = False
    
def HideAllCards():
    for Card in AllCards:
        Card.visible = False
        #VisibleList(Card.FullDisplay, False)
        #VisibleList(Card.DisplayList, False)
        pass
def CreateCards():
    DiceList = []
    CreateDie(2,3,"pierce",DiceList)
    CreateDie(3,4,"blunt",DiceList)
    CreateDie(1,6,"slash",DiceList)
    CreateDie(2,4,"block",DiceList)
    CreateCard("green",1,"template strike",DiceList)
    
    DiceList = []
    CreateDie(1,4,"evade",DiceList)
    CreateCard("green",0,"Evade",DiceList)
    
    DiceList = []
    CreateDie(2,3,"pierce",DiceList)
    CreateDie(1,4,"blunt",DiceList)
    CreateCard("green",1,"Light Attack",DiceList)
    
    DiceList = []
    CreateDie(1,5,"evade",DiceList)
    CreateDie(2,3,"block",DiceList)
    CreateDie(1,2,"slash",DiceList)
    CreateCard("green",1,"Light Defense",DiceList)
    
    DiceList = []
    CreateDie(3,6,"pierce",DiceList)
    CreateDie(2,6,"block",DiceList)
    CreateCard("green",2,"Chrage and Cover",DiceList)
    
    DiceList = []
    CreateDie(3,5,"slash",DiceList)
    CreateDie(3,5,"slash",DiceList)
    CreateDie(1,3,"pierce",DiceList)
    CreateCard("green",3,"Focused Strikes",DiceList)
    pass

def CreateCharacters():
    SpeedDiceList = []
    CreateSpeedDie(5,9,SpeedDiceList)
    CreateSpeedDie(1,6,SpeedDiceList)
    DeckList = CreateDeckList([
        "Evade","Evade","Chrage and Cover",
    "Chrage and Cover","Light Attack","Light Attack",
    "Light Attack","Light Defense","Focused Strikes"])
    CreateCharacter(90,225,2,False,SpeedDiceList,DeckList,5,7)
    SpeedDiceList = []
    CreateSpeedDie(1,6,SpeedDiceList)
    CreateSpeedDie(1,6,SpeedDiceList)
    CreateSpeedDie(1,6,SpeedDiceList)

    DeckList = CreateDeckList([
        "Evade","Evade","Chrage and Cover",
    "Chrage and Cover","Light Attack","Light Attack",
    "Light Attack","Light Defense","Focused Strikes"])
    #print(DeckList)
    CreateCharacter(290,225,1,True,SpeedDiceList,DeckList,5,7)
    pass

def MoveToPageSelect():
    print("Moving to select")
    for Character in AllCharacters:
        index = 0
        if Character.MaxLight > len(Character.LightSprites):
            CreateLightSprite(Character)
        if Character.Light < Character.MaxLight:
            Character.Light += 1
        if len(Character.Hand) < Character.MaxHandSize:
            DrawCard(Character)
            
        for Die in Character.SpeedDice:
            Die.speed = 0
            
        for DieText in Character.SpeedDiceText:
            DieValue = random.randint(Character.SpeedDice[index].min, Character.SpeedDice[index].max)
            DieText.value = DieValue
            Character.SpeedDice[index].speed = DieValue
            FoundSelf = False
            for Die in Character.SpeedDice:
                if Die.speed < DieValue and not FoundSelf:
                    HeldVal = Die.speed
                    Die.speed = DieValue
                    DieValue = HeldVal
                    Character.SpeedDice[index].speed = DieValue
                    DieText.value = DieValue
                    FoundSelf = True
                    
                if Die == Character.SpeedDice[index]:
                    FoundSelf = True
                    
            #Character.SpeedDice[index].speed = DieValue
            index += 1
            pass
        #print(Character.ControlledByPlayer)
        if not Character.ControlledByPlayer:
            CharacterRandomTarget(Character)
        
def DrawCard(Character):
    if len(Character.Library) > 0 and len(Character.Hand) < 7:
        chance = random.randint(0,len(Character.Library) - 1) 
        EscroCard = Character.Library[chance]
        Character.Hand.append(EscroCard)
        Character.Library.remove(EscroCard)
        
def CharacterRandomTarget(Character):
    print("start targetting")
    for SpeedDie in Character.SpeedDice:
        if SpeedDie.HeldPage == None and len(Character.Hand) > 0:
            for Card in Character.Hand:
                if Card.cost <= Character.Light:
                    if SpeedDie.HeldPage == None:
                        TargetWithPage(SpeedDie, Card, Character, None)
                        pass
                    else:
                        chance = random.randint(1,len(Character.Hand) - 1)
                        if chance == 1:
                            UntargetSpeedDie(SpeedDie)
                            TargetWithPage(SpeedDie, Card, Character, None)



                            
def TargetWithPage(SpeedDie, Card, Character, TargetDie):
    print("Target with page")
    if Card.cost <= Character.Light:
        Character.Light -= Card.cost
        FixLightSpritePositions(Character)
        if SpeedDie.HeldPage != None:
            UntargetSpeedDie(SpeedDie)
        SpeedDie.HeldPage = Card
        Character.Hand.remove(Card)
        TargetSpeedDice = None
        if Character.ControlledByPlayer:
            #chance = random.randint(0,len(EnemySpeedDice) - 1)
            #TargetSpeedDice = EnemySpeedDice[chance]
            print("controlled by player targetting?")
            TargetSpeedDice = TargetDie
            Color = "blue"
            RemoveTargetLine(SpeedDie)
            
        else:
            print("---------------------------------------------------------")
            #print(len(PlayerSpeedDice))
            #print(PlayerSpeedDice)
            #print(PlayerSpeedDice[chance])
            chance = random.randint(0,len(PlayerSpeedDice) - 1)
            TargetSpeedDice = PlayerSpeedDice[chance]
            Color = "red"
    
        SpeedDie.TargetDie = TargetSpeedDice
        TargetSpeedDice.TargettedBy.append(SpeedDie)
        SpeedDieSprite = SpeedDie.ConnectedSprite
        #visuals
        TargetSpeedDiceSprite = TargetSpeedDice.ConnectedSprite
        Card.centerX = SpeedDieSprite.centerX
        Card.centerY = SpeedDieSprite.centerY
        TargetLine = Line(SpeedDieSprite.centerX,SpeedDieSprite.centerY,TargetSpeedDiceSprite.centerX,TargetSpeedDiceSprite.centerY, fill = Color)
        TargetLine.opacity = 30
        SpeedDie.ClashLine = TargetLine
        
def UntargetSpeedDie(SpeedDie):
    if SpeedDie.HeldPage != None:
        print("Untarget")
        EnemyDie = SpeedDie.TargetDie
        EnemyDie.TargettedBy.remove(SpeedDie)
        SpeedDie.ConnectedCharacter.Light += SpeedDie.HeldPage.cost
        FixLightSpritePositions(SpeedDie.ConnectedCharacter)
        SpeedDie.TargetDie = None
        SpeedDie.ConnectedCharacter.Hand.append(SpeedDie.HeldPage)
        SpeedDie.HeldPage = None
        RemoveTargetLine(SpeedDie)
        RemoveClashLine(SpeedDie)
        
    
def RemoveTargetLine(Die):
    #print("tries to remove line")
    if not Die.TargettingLine == None:
        Die.TargettingLine.visible = False
        Die.TargettingLine = None
        
def RemoveClashLine(Die):
    print("tries to remove clash line")
    if not Die.ClashLine == None:
        Die.ClashLine.visible = False
        Die.ClashLine = None
        
def MoveToClashes():
    print("MovingToClashes")
    app.CurrentSpeedBracket = -1
    app.PausedForClash = False
    AllDice = PlayerSpeedDice + EnemySpeedDice
    #fix later because 
    for Die in PlayerSpeedDice:
        print("check " + str(Die.speed) +" vs " + str(app.CurrentSpeedBracket))
        if Die.speed > app.CurrentSpeedBracket:
            app.CurrentSpeedBracket = Die.speed 
            print("check=")
            
    for Die in EnemySpeedDice:
        print("check " + str(Die.speed) +" vs " + str(app.CurrentSpeedBracket))
        if Die.speed > app.CurrentSpeedBracket:
            app.CurrentSpeedBracket = Die.speed
            print("check=")
            
    print("High speed is: " + str(app.CurrentSpeedBracket))
    
    while app.CurrentSpeedBracket > -1 and app.PausedForClash == False:
        for Die in AllDice:
            if not Die.HeldPage == None and app.PausedForClash == False: #makes sure the die has a page and that not paused
                if Die.speed == app.CurrentSpeedBracket:
                    DieAct(Die)
        app.CurrentSpeedBracket -= 1
        
def DieAct(Die):
    app.PausedForClash = True
    TargetDie = Die.TargetDie
    if Die.TargetDie.TargetDie == Die: #checks if enemy die is targetting this die
        print("Clash!!!")
        ClashBetweenPages(Die,TargetDie)
        
    #elif len(TargetDie.ConnectedCharacter.HeldDice) > 0:
        
    else:
        print("One sided attack")
        OneSidedAttack(Die)
        
def OneSidedAttack(Die):
    ActiveCard = Die.HeldPage
    ActiveCard.visible = True
    ActiveCard.centerX = 200
    ActiveCard.centerY = 100
    app.ActingDice.append(Die)
    pass

def ClashBetweenPages(Die,TargetDie):
    app.ActingDice.append(Die)
    app.ActingDice.append(TargetDie)
    pass
            
def ClearActingDice():
    while len(app.ActingDice) > 0:
        app.ActingDice.remove(app.ActingDice[0])
        
def MoveATowardB(FirstSprite,SecondSprite):
    
    if FirstSprite.centerX < SecondSprite.centerX:
        FirstSprite.centerX += app.CharacterSpeed
    else:
        FirstSprite.centerX -= app.CharacterSpeed
            
    if FirstSprite.centerY < SecondSprite.centerY:
        FirstSprite.centerY += app.CharacterSpeed
    else:
        FirstSprite.centerY -= app.CharacterSpeed
    
        
        
cmu_graphics.run()