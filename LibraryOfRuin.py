from cmu_graphics import *
#Library game???
#lista becomes list because lista doesnt exista
#I am switching to VS code fully because of file size problems on CMU
# am running to shape count problems?
app.setMaxShapeCount(40000)
import random
import math
app.Startup = True
app.Debug = False
app.PlayerConfirm = False
app.PlayerConfirmStage = 0
app.CardWidth = 110
app.Xdisplace = 18
app.YStart = 40
app.FontSizeModifier = 2
app.MouseX = 0
app.MouseY = 0
AllTotalCards = []
AllDisplayCards = []
app.DisplayedHandCards = []
AllCharacters = []
AllFightingCharacters = []
DeadCharacters = []

app.ActiveCharacterCards = []
app.AttributedCharacterCards = []
app.UnusedCharacterCards = []

PlayerSpeedDice = []
EnemySpeedDice = []
DeadSpeedDice = []
app.PausedForClash = False
app.CurrentSpeedBracket = -1
app.ActingDice = []
app.CharacterSpeed = 10
Background = Rect(0,0,app.width,app.height,fill="burlywood")
app.XScreenDialation = app.width / 400
app.YScreenDialation = app.height / 400
app.BlackScreen = Rect(0,0,app.width,app.height,visible = False)
app.GamoverText = Label("Game Over",app.width/2,app.height/2, fill = "white",visible = False, size = 20)
app.WinText = Label("You Win",app.width/2,app.height/2, fill = "white",visible = False, size =20)
app.ContinueText = Label("Press Space To Continue",app.width/2,app.height/2 + 50 * app.YScreenDialation, fill = "white",visible = False)
app.AutoProgressPages = True
app.AutoProgressStagesForTesting = False
app.AutoProgressTimer = 10
app.AutoProgressStageTimer = 10
app.InAFight = False

app.InMainMenu = True
PlayerCharacters = []
app.ChosenCharacter = None
XDisp = 7
Button = Circle(25,25,15,fill="red",border = "darkred")
X1 = Line(Button.left + XDisp,Button.top + XDisp,Button.right - XDisp,Button.bottom - XDisp)
X2 = Line(Button.right - XDisp,Button.top + XDisp, Button.left + XDisp, Button.bottom - XDisp)
XButton = Group(Button,X1,X2)
app.Menu = None
app.ActiveTextInput = None
app.TemporaryButtons = []
app.CharactersUnlocked = 1
app.AttributionMax = 6
app.UnlockedAttribution = False
app.StagesUnlocked = 1
app.FightsUnlocked = 1
app.CurrentEmotionLevelCap = 1
app.CurrentTeamEmotionLevel = 0
app.ChosenAbnoPages = []
app.SinglePressLock = False
app.StoryStages = []
app.StageSymbols = []

app.Floors = [] 
app.CurrentFloor = None
app.DisplayedFloor = None
app.CurrentBattle = None
app.CurrentFight = None
app.CurrentPart = 0
app.DeckBuilderYDisp = 0
DeckbuildingBack = Rect(200,0,200,400,visible = False)

app.FadingParticles = []

#----------------------------------------------------------------------------------------------
#Inputs
def onMousePress(x,y):
    if app.SinglePressLock == False:
        #print(app.width)
        #print(app.height)
        #app.SinglePressLock = True
        app.MouseX = x
        app.MouseY = y
        if app.InAFight:
            if app.PlayerConfirmStage == 7:
                print("choosing an abno page")
                for Button in app.TemporaryButtons:
                    if Button.hits(x,y):
                        if Button.Type == "Page":
                            app.ChosenAbnoPage = Button.ConnectedPage
                            app.ChosenAbnoPages.append(Button.ConnectedPage) #adds to list to remove from options 
                            DeleteTempButtons()
                            if app.ChosenAbnoPage.SingleTarget:
                                app.PlayerConfirmStage = 8
                                ReminderText = Label("Please pick a character to apply to!!!",200 * app.XScreenDialation,350 * app.YScreenDialation,size = 20)
                                app.TemporaryButtons.append(ReminderText)
                            else:
                                for ChosenCharacter in PlayerCharacters: #for all ally pages just run chosen player on all
                                    print("Chose " + Character.name)
                                    for Effect in app.ChosenAbnoPage.Effect:
                                        AddPassiveEffect(ChosenCharacter,Effect)
                                ResetAllCharacterPositions()
                                app.PlayerConfirmStage = 0
                                for Button in app.TemporaryButtons:
                                    Button.visible = False
                                app.TemporaryButtons.clear()
                            
            elif app.PlayerConfirmStage == 8:
                print("choosing a character for abno page")
                ChosenCharacter = None
                for Die in PlayerSpeedDice:
                    if Die.ConnectedSprite.hits(x,y):
                        ChosenCharacter = Die.ConnectedCharacter
                
                for Character in AllFightingCharacters:
                    if Character.ControlledByPlayer and Character.CharacterSprite.hits(x,y):
                        ChosenCharacter = Character
                
                if ChosenCharacter != None:
                    print("Chose " + Character.name)
                    for Effect in app.ChosenAbnoPage.Effect:
                        AddPassiveEffect(ChosenCharacter,Effect)
                    ResetAllCharacterPositions()
                    app.PlayerConfirmStage = 0
                    for Button in app.TemporaryButtons:
                        Button.visible = False
                    app.TemporaryButtons.clear()
                
            else:
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
                                
                        for PCard in app.DisplayedHandCards:
                            if PCard.Clicked:
                                ActiveCard = PCard
                                
                        if ActiveSpeedDie != None and ActiveCard != None and app.PlayerConfirmStage == 1:
                            
                            TargetWithPage(ActiveSpeedDie, ActiveCard, ActiveSpeedDie.ConnectedCharacter, Die)
                            
                for Card in app.DisplayedHandCards:
                    if Card.hits(x,y):
                        ClickedBackground = False
                        Card.Clicked = True
                        print("did hit card")
                    elif Card.Clicked:
                        Card.Clicked = False
                    else:
                        if ClickedBackground:
                            Card.Clicked = False
                
    
                for Die in AllDice:
                    if Die.ConnectedSprite.hits(x,y):
                        Die.Clicked = True
                        print("this die's speed is: " + str(Die.speed) + " Connected to: " + Die.ConnectedCharacter.name)
                        pass
                    else:
                        if ClickedBackground:
                            Die.Clicked = False
                            RemoveTargetLine(Die)
                if app.Debug == True:
                    for Character in AllCharacters:
                        if Character.CharacterSprite.hits(x,y):
                            print("Clicked: " + Character.name)
                            if Character.visible == True:
                                print("Who is visisble")
                            else:
                                print("Who is invisisble")
                        
                for Character in AllFightingCharacters:
                    if Character.CharacterSprite.hits(x,y):
                        Character.Clicked = True
                        print("Clicked fighting: " + Character.name)
                    else:
                        if ClickedBackground:
                            Character.Clicked = False
    #------------------------------------------------------------------------------------
        elif app.InMainMenu:
            if app.Menu == "CharacterSelect":
                for Character in PlayerCharacters:
                    if Character.NameBoard.hits(x,y):
                        app.ActiveTextInput = Character.NameBoard
                        Character.NameBoard.Text.fill = "blue"
                    elif Character.NameBoard == app.ActiveTextInput:
                        app.ActiveTextInput = None
                        Character.NameBoard.Text.fill = "black"
                for Button in app.TemporaryButtons:
                    if Button.hits(x,y):
                        if Button.Type != "locked":
                            HideCharacterSelect()
                            SavedButtom = Button
                            DeleteTempButtons()

                            if SavedButtom.Type == "Deck":
                                app.ChosenCharacter = SavedButtom.ConnectedCharacter
                                DisplayLibrary(Button.ConnectedCharacter)
                                app.Menu = "EditDeck"
                            elif SavedButtom.Type == "EditCharacter":
                                app.ChosenCharacter = SavedButtom.ConnectedCharacter
                                DisplayCharacterEdit(app.ChosenCharacter)
                                app.Menu = "EditCharacter"
                                app.ChosenCharacter.OverrideCard.visible = True
                            
                            
            elif app.Menu == "MainMenu":
                for Button in app.TemporaryButtons:
                    if Button.hits(x,y):
                        if Button.Type != "locked":
                            HideCharacterSelect()
                            DeleteTempButtons()
                            XButton.visible = True
                            
                        if Button.Type == "CharacterSelect":
                            print("main menu to character select")
                            DisplayCharacterSelect()
                            app.Menu = "CharacterSelect"
                        elif Button.Type == "ProgressionTree":
                            app.Menu = "ProgressionTree"
                            DisplayProgressionTree()
                        elif Button.Type == "FloorSelect":
                            app.Menu = "FloorSelect"
                            DisplayFloorSelect()
                        elif Button.Type == "Instructions":
                            app.Menu = "Instructions"
                            print("WIP LOL")
                            
            elif app.Menu == "ProgressionTree":
                #stages dont actually exist these are all battles in terms of creation labeling
                for Stage in app.StoryStages:
                    for Fight in Stage.ListOfFights:
                        Icon = Fight.FightIcon
                        if Icon.visible == True and Icon.hits(x,y):
                            print("Starting battle!")
                            app.CurrentBattle = Stage
                            app.CurrentFight = Stage.ListOfFights[int(Icon.Text.value) - 1]
                            
                            StartBattle(Stage.ListOfFights[int(Icon.Text.value) - 1])
                            
            elif app.Menu == "FloorSelect":
                for Button in app.TemporaryButtons:
                    if Button.hits(x,y):
                        if Button.Type != "locked":
                            SavedButton = Button
                            DeleteTempButtons()

                            if SavedButton.Type == "Abnormalities":
                                DisplayFloorAbnormalities(SavedButton.ConnectedFloor)
                                app.Menu = "Abnormalities"
                                
                            elif SavedButton.Type == "Battles":
                                DisplayFloorBattles(SavedButton.ConnectedFloor)
                                app.Menu = "EnlightenmentBattles"
                                
                            elif SavedButton.Type == "SetActive":
                                app.CurrentFloor = SavedButton.ConnectedFloor
                                app.CharactersUnlocked = app.CurrentFloor.CharactersUnlocked
                                app.CurrentEmotionLevelCap = app.CurrentFloor.CurrentEmotionLevelCap
                                DisplayFloorSelect()
                                
                                

            elif app.Menu == "EnlightenmentBattles":
                
                for Floor in app.Floors:
                    for Stage in Floor.EnlightenmentStages:
                        for Fight in Stage.ListOfFights: #again realisitcally only 1 but idk I am lazy
                            Icon = Fight.FightIcon
                            if Icon.visible == True and Icon.hits(x,y):
                                print("Starting battle!")
                                app.CurrentFloor = Floor
                                app.CharactersUnlocked = app.CurrentFloor.CharactersUnlocked
                                app.CurrentEmotionLevelCap = app.CurrentFloor.CurrentEmotionLevelCap
                                app.CurrentBattle = Stage
                                app.CurrentFight = Stage.ListOfFights[int(Icon.Text.value) - 1]
                                
                                StartBattle(Stage.ListOfFights[int(Icon.Text.value) - 1])

                            
            elif app.Menu == "EditDeck":
                for DisplayCard in AllDisplayCards:
                    if DisplayCard.hits(x,y):
                        if len(app.ChosenCharacter.Library) < 9:
                            #check for 3 of a kind
                            duplicates = 0
                            for Card in app.ChosenCharacter.Library:
                                if Card.name == DisplayCard.name:
                                    duplicates += 1
                            if duplicates < 3:
                                CopyCard(DisplayCard, app.ChosenCharacter.Library)
                                DisplayLibrary(app.ChosenCharacter)
                                print("added card to library!")
                                
                #for Character in PlayerCharacters:
                for Card in app.ChosenCharacter.Library:
                    if Card.hits(x,y):
                        app.ChosenCharacter.Library.remove(Card)
                        Card.visible = False
                        DisplayLibrary(app.ChosenCharacter)
                        print("removed card from character library")
                            
            elif app.Menu == "EditCharacter":
                if app.ChosenCharacter.NameBoard.hits(x,y):
                    app.ActiveTextInput = app.ChosenCharacter.NameBoard
                    app.ChosenCharacter.NameBoard.Text.fill = "blue"
                elif app.ChosenCharacter.NameBoard == app.ActiveTextInput:
                    app.ActiveTextInput = None
                    app.ChosenCharacter.NameBoard.Text.fill = "black"
                for Card in app.UnusedCharacterCards:
                    if Card.hits(x,y):
                        AssignOverrideCard(app.ChosenCharacter,Card)
                        DisplayCharacterEdit(app.ChosenCharacter)
                        
                pass
            
                            
            if XButton.hits(x,y):
                if app.Menu == "EditDeck":
                    app.Menu = "CharacterSelect"
                    HideEditDeck()
                    app.DeckBuilderYDisp = 0
                    print("Xed out of deck edit")
                    DisplayCharacterSelect()
                elif app.Menu == "EditCharacter":
                    app.Menu = "CharacterSelect"
                    for Card in app.UnusedCharacterCards:
                        Card.visible = False
                    app.DeckBuilderYDisp = 0
                    DeleteTempButtons()
                    app.ChosenCharacter.OverrideCard.visible = False
                    print("Xed out of character edit")
                    DisplayCharacterSelect()
                elif app.Menu == "CharacterSelect":
                    app.Menu = "MainMenu"
                    HideCharacterSelect()
                    DeleteTempButtons()
                    DisplayMainMenu()
                elif app.Menu == "ProgressionTree":
                    app.Menu = "MainMenu"
                    app.DeckBuilderYDisp = 0
                    for Stage in app.StoryStages:
                        Stage.visible = False
                    for Symbol in app.StageSymbols:
                        Symbol.visible = False
                    DeleteTempButtons()
                    DisplayMainMenu()
                    
                elif app.Menu == "FloorSelect":
                    app.Menu = "MainMenu"
                    DeleteTempButtons()
                    DisplayMainMenu()
                
                elif app.Menu == "Instructions":
                    app.Menu = "MainMenu"
                    DeleteTempButtons()
                    DisplayMainMenu()
                    
                elif app.Menu == "EnlightenmentBattles":
                    app.Menu = "FloorSelect"
                    DeleteTempButtons()
                    for Floor in app.Floors:
                        for Symbol in Floor.EnlightenmentStageSymbols:
                            Symbol.visible = False
                        for Stage in Floor.EnlightenmentStages:
                            Stage.visible = False
                    DisplayFloorSelect()
                    
                elif app.Menu == "Abnormalities":
                    app.Menu = "FloorSelect"
                    DeleteTempButtons()
                    DisplayFloorSelect()
                    
                elif app.Menu == "FloorSelect":
                    app.Menu = "MainMenu"
                    DeleteTempButtons()
                    DisplayMainMenu()

            print("Clicked while in menu")
        
def onMouseMove(x,y):
    app.MouseX = x
    app.MouseY = y
    if app.InAFight:
        AllDice = PlayerSpeedDice + EnemySpeedDice
        for Die in AllDice:
            if Die.ConnectedSprite.hits(x,y):
                Die.MousedOver = True
            else:
                Die.MousedOver = False
        for Card in app.DisplayedHandCards:
            if Card.hits(x,y):
                Card.MousedOver = True
                FixupCard(Card)
            else:
                Card.MousedOver = False
        
        for Character in AllFightingCharacters:
            if Character.CharacterSprite.hits(x,y):
                Character.MousedOver = True
            else:
                Character.MousedOver = False
                
    elif app.InMainMenu:
        if app.Menu == "ProgressionTree":
            for Stage in app.StoryStages:
                for Fight in Stage.ListOfFights:
                    Icon = Fight.FightIcon
                    if Icon.hits(x,y):
                        Icon.border = "lightblue"
                        Icon.Text.fill = "lightblue"
                    else:
                        Icon.border = "orange"
                        Icon.Text.fill = "orange"
                        
        elif app.Menu == "EnlightenmentBattles":
            for Floor in app.Floors:
                for Stage in Floor.EnlightenmentStages:
                    for Fight in Stage.ListOfFights: #again realisitcally only 1 but idk I am lazy
                        Icon = Fight.FightIcon
                        if Icon.hits(x,y):
                            Icon.border = "lightblue"
                            Icon.Text.fill = "lightblue"
                        else:
                            Icon.border = "orange"
                            Icon.Text.fill = "orange"
                        
        elif app.Menu == "MainMenu":
            for Button in app.TemporaryButtons:
                if Button.hits(x,y):
                    Button.border = "grey"
                    Button.Text.fill = "grey"
                else:
                    Button.border = "black"
                    Button.Text.fill = "black"
                    
        elif app.Menu == "CharacterSelect":
            for Button in app.TemporaryButtons:
                if Button.Type == "Deck" or Button.Type == "EditCharacter":
                    if Button.hits(x,y):
                        Button.border = "grey"
                        Button.Text.fill = "grey"
                    else:
                        Button.border = "black"
                        Button.Text.fill = "black"
                        
def onKeyPress(key):
    print(key)
    if key == "tab":
        if app.AutoProgressPages:
            app.AutoProgressPages = False
            print("Disabled auto progressing pages")
        else:
            app.AutoProgressPages = True
            print("enabled auto progressing pages")
    if key == "enter":
        if app.AutoProgressStagesForTesting:
            app.AutoProgressStagesForTesting = False
            print("Disabled auto stage progression")
        else:
            app.AutoProgressStagesForTesting = True
            print("enabled auto stage progression")
    if app.InAFight:
        if key == "escape":
            for Die in PlayerSpeedDice:
                UntargetSpeedDie(Die)
                print("hiding hand")
                HideHand(Die.ConnectedCharacter)
        elif key == "space":
            #if app.PlayerConfirmStage == 0 or app.PlayerConfirmStage == 1 or app.PlayerConfirmStage == 2:
            app.PlayerConfirm = True
            pass
        elif key == "r" and app.PlayerConfirmStage == 1:
            for Character in AllFightingCharacters:
                if Character.ControlledByPlayer and not Character.Staggered:
                    CharacterRandomTarget(Character)
        
    elif app.InMainMenu:
        if app.Menu == "CharacterSelect" or app.Menu == "EditCharacter":
            if app.ActiveTextInput != None:
                if key == "backspace":
                    
                    app.ActiveTextInput.Text.value = app.ActiveTextInput.Text.value[0:-1]

                #elif key == "space":
                    #app.ActiveTextInput.Text.value += " "
                elif len(key) == 1:
                    app.ActiveTextInput.Text.value += key
                    
        if app.Menu == "EditDeck" or app.Menu == "EditCharacter":
            if key == "up":
                MoveDisplayCards(10)
                
            elif key == "down":
                MoveDisplayCards(-10)
        pass
    
def onKeyHold(keys):
    if app.Menu == "EditDeck" or app.Menu == "EditCharacter" or app.Menu == "ProgressionTree":
        for key in keys:
            if key == "up":
                MoveDisplayCards(10)
                
            elif key == "down":
                MoveDisplayCards(-10)
                
    elif app.Menu == "Abnormalities":
        for key in keys:
            if key == "right":
                MoveDisplayCards(10)
                
            elif key == "left":
                MoveDisplayCards(-10)
    

#def onMouseRelease(x,y):
    #app.SinglePressLock = False
        
#--------------------------------------------------------------------------------
#Main
def onStep():
    AllDice = PlayerSpeedDice + EnemySpeedDice
    if app.Startup:
        Startup()
        HideAllSetupCards()
        #app.ChosenCharacter = PlayerCharacters[0]
        #DisplayLibrary(PlayerCharacters[0])
        CreateStoryStages()
        app.Menu = "MainMenu"
        DisplayMainMenu()

    elif app.InAFight:
        if app.PlayerConfirmStage == 1 or app.PlayerConfirmStage == 0:
            for Character in AllFightingCharacters:
                if (not Character.Staggered and Character.Stagger <= 0) or Character.Health <= 0:
                    Stagger(Character)
                if Character.Health <= 0:
                    KillCharacter(Character)
                    
                if Character.MousedOver or Character.Clicked:
                    Character.AdditionalInfoBoard.visible = True
                else:
                    Character.AdditionalInfoBoard.visible = False
                   
                HasClickedDie = False 
                ClickedDie = None
                for Die in Character.SpeedDice:
                    if Die.MousedOver or Die.Clicked:
                        HasClickedDie = True
                        ClickedDie = Die
                        if Die.HeldPage != None:
                            Die.HeldPage.visible = True
                            Die.HeldPage.centerX = Die.ConnectedSprite.centerX
                            Die.HeldPage.centerY = Die.ConnectedSprite.centerY
                    else:
                        if Die.HeldPage != None:
                            Die.HeldPage.visible = False
                
                if Character.Staggered != True:
                
                    if HasClickedDie or Character.MousedOver or Character.Clicked:
                        Character.AdditionalInfoBoard.visible = True
                    else:
                        Character.AdditionalInfoBoard.visible = False
                    
                    if HasClickedDie and Character.ControlledByPlayer:
                        DisplayHand(Character, ClickedDie)
                    elif Character.ControlledByPlayer and Character.HandOnDisplay:
                        print("hiding hand")
                        HideHand(Character)
                    
                        
                    
            
        elif app.PlayerConfirmStage == 2:
            if app.PausedForClash and len(app.ActingDice) > 0:
                #print("doing clash")
                FirstSprite = app.ActingDice[0].ConnectedCharacter
                if app.ActingDice[0].TargetDie != None:
                    SecondSprite = app.ActingDice[0].TargetDie.ConnectedCharacter
                    if FirstSprite.CharacterSprite.hitsShape(SecondSprite.CharacterSprite):
                        #checks if the two characters are touching
                        #print("touching so wait for confirm to clash!")
                        for Character in AllFightingCharacters:
                            if Character.MousedOver or Character.Clicked:
                                Character.AdditionalInfoBoard.visible = True
                            else:
                                Character.AdditionalInfoBoard.visible = False
                            
                            if Character.Staggered or Character.Health <= 0:
                                Stagger(Character)
                            if Character.Health <= 0:
                                KillCharacter(Character)
                        if app.AutoProgressPages and not app.PlayerConfirm:
                            app.AutoProgressTimer -= 1
                        if app.PlayerConfirm == True or app.AutoProgressTimer == 0:
                            ClashBetweenSpeedDice(app.ActingDice[0],app.ActingDice[0].TargetDie)
                            app.PlayerConfirm = False
                            app.AutoProgressTimer = 10
                    else:
                        #you can add more complexity of moving together if equal later
                        MoveATowardB(FirstSprite,SecondSprite.CharacterSprite)
                        app.PlayerConfirm = False
                else:
                    print("Failed to find bc acting die lost it's target die")
                    if app.ActingDice[0].HeldPage != None:
                        RestorePage(app.ActingDice[0].HeldPage)
                        UntargetSpeedDie(app.ActingDice[0])
                    else: 
                        print("Also failed to find held page wtf")
                        ClearActingDice()
            else:
                MoveToClashes()
                
        elif app.PlayerConfirmStage == 3:
            app.RoundNum += 1
            ResetAllCharacterPositions()
            
            if app.PlayerConfirmStage != 7:
                app.PlayerConfirmStage = 0
            
        #app.PausedForClash = False
        if (app.AutoProgressStagesForTesting or app.PlayerConfirmStage == 0) and not app.PlayerConfirm and app.PlayerConfirmStage != 10:
            app.AutoProgressStageTimer -= 1
    
        if app.PlayerConfirm == True or app.AutoProgressStageTimer == 0:
            
            app.AutoProgressStageTimer = 10

            if app.PlayerConfirmStage == 0:
                MoveToPageSelect()
                print("confirm stage is " + str(app.PlayerConfirmStage))
                if app.PlayerConfirmStage != 7: #caused problems of overriding assigning abno page
                    app.PlayerConfirmStage = 1
                app.PlayerConfirm = False
                if app.AutoProgressStagesForTesting:
                    onKeyPress("r")
            elif app.PlayerConfirmStage == 1:
                for Character in AllFightingCharacters:
                    HideHand(Character)
                MoveToClashes()
                app.PlayerConfirmStage = 2
                app.PlayerConfirm = False
            elif app.PlayerConfirmStage == 10:
                ContinueAfterFight()
                app.InAFight = False
                app.InMainMenu = True
                app.Menu = "MainMenu"
                DisplayMainMenu()
                for Character in AllCharacters:
                    ResetCharacterLibrary(Character)
    elif app.InMainMenu:
        #not much will probably happen in here tbh
        pass
    
    for Particle in app.FadingParticles:
        if Particle.opacity - Particle.Fade <= 0:
            Particle.visible = False
            app.FadingParticles.remove(Particle)
        else:
            Particle.opacity -= Particle.Fade
            Particle.centerX += Particle.XVel
            Particle.centerY += Particle.YVel
            Particle.rotateAngle += Particle.Rotation
        
#----------------------------------------------------------------------------------------
#Deckbuilding and main hub

def DisplayProgressionTree():
    print("Displaying progression tree")
    StartY = 300 + app.DeckBuilderYDisp
    index = 1
    
    for Stage in app.StoryStages:
        if app.StagesUnlocked >= index:
            
            Stage.visible = True
            Stage.centerY = StartY
            Stage.centerX = 200
            Stage.visible = True
            StartY -= 100 
            
            subindex = 1
            for Fight in Stage.ListOfFights:
                if Stage.FightsUnlocked >= subindex:
                    Fight.FightIcon.visible = True
                    Fight.FightIcon.Text.visible = True
                else:
                    Fight.FightIcon.visible = False
                    Fight.FightIcon.Text.visible = False
                
                subindex += 1
                
            if len(app.StageSymbols) >= index:
                Symbol = app.StageSymbols[index - 1]
                Symbol.visible = True
                Symbol.width = 60
                Symbol.height = 40
                Symbol.left = Stage.left + 5
                Symbol.centerY = StartY + 100
                Symbol.toFront()
        index += 1
        
def DisplayFloorBattles(Floor):
    print("Displaying floor progression tree")
    StartY = 300
    index = 1
    #Floor.EnlightenmentUnlocked = 1 #testing
    if Floor.EnlightenmentUnlocked == 0:
        print("not high enough unlock yet")
        NothingHere = Rect(50,100,300,200,fill = "lightBlue",border = "black")
        NothingHere.Text = Label("Not enough of the main story completed for unlock",NothingHere.centerX,NothingHere.centerY)
        NothingHere.ConnectedFloor = Floor
        NothingHere.Type = "Locked"
        app.TemporaryButtons.append(NothingHere)
    else:
        for Stage in Floor.EnlightenmentStages:
            if Floor.EnlightenmentUnlocked >= index:
                
                Stage.visible = True
                Stage.centerY = StartY
                Stage.centerX = 200
                Stage.visible = True
                StartY -= 100 
                
                subindex = 1
                for Fight in Stage.ListOfFights:
                    if Stage.FightsUnlocked >= subindex:
                        Fight.FightIcon.visible = True
                        Fight.FightIcon.Text.visible = True
                    else:
                        Fight.FightIcon.visible = False
                        Fight.FightIcon.Text.visible = False
                    
                    subindex += 1
                    
                if len(Floor.EnlightenmentStageSymbols) >= index:
                    Symbol = Floor.EnlightenmentStageSymbols[index - 1]
                    Symbol.visible = True
                    Symbol.width = 60
                    Symbol.height = 40
                    Symbol.left = Stage.left + 5
                    Symbol.centerY = StartY + 100
                    Symbol.toFront()
            index += 1
            
def DisplayFloorAbnormalities(Floor):
    app.DisplayedFloor = Floor
    if len(Floor.EmotionPayoffs[0]) == 0:
        print("not high enough unlock yet")
        NothingHere = Rect(50,100,300,200,fill = "lightBlue",border = "black")
        NothingHere.Text = Label("Complete 1 Floor Battle on this floor to unlock",NothingHere.centerX,NothingHere.centerY)
        NothingHere.ConnectedFloor = Floor
        NothingHere.Type = "Locked"
        app.TemporaryButtons.append(NothingHere)
    else:
        
        PageWidth = 400 * app.XScreenDialation / 3
        StartX = 0 + app.DeckBuilderYDisp
        Index = 0
        for EmotionLevel in Floor.EmotionPayoffs:
            Index += 1
            print("new emotion level")
            for AbnoPage in EmotionLevel:
                print("ordering payoff")
                Page = Group()
                Outline = Rect(StartX,50 * app.YScreenDialation,PageWidth,300 * app.YScreenDialation)
                if AbnoPage.Positive:
                    Outline.fill = "green"
                    Outline.border = "darkGreen"
                else:
                    Outline.fill = "red"
                    Outline.border = "darkRed"
                Outline.borderWidth = 8
                Page.add(Outline)
                Title = Label(AbnoPage.name,Outline.centerX,100 * app.YScreenDialation,size = 20 * app.XScreenDialation)
                Page.add(Title)
                TargetTitle = Label("Idk Target",Outline.centerX,130 * app.YScreenDialation,size = 18 * app.XScreenDialation)
                if AbnoPage.SingleTarget:
                    TargetTitle.value = "Single target"
                else:
                    TargetTitle.value = "World Effect"
                LevelTitle = Label("Level: " + str(Index),Outline.centerX,145 * app.YScreenDialation,size = 18 * app.XScreenDialation)
                Page.Text = Group(Title,TargetTitle,LevelTitle)
                PartitionedText = CardPartition(AbnoPage.Description)
                StartY = 160 * app.YScreenDialation
                for Line in PartitionedText:
                    #Textline = Label(Line,Outline.centerX,StartY)
                    Line.size = 16 * app.YScreenDialation
                    Line.centerX = Outline.centerX
                    Line.centerY = StartY
                    StartY += 12 * app.YScreenDialation
                    Page.add(Line)
                    Page.Text.add(Line)
                Page.Type = "Page"
                app.TemporaryButtons.append(Page)
                StartX += PageWidth


def DisplayMainMenu():
    
    LeftSide = 50
    ProgressionTreeButton = Rect(LeftSide,25,400 - LeftSide * 2,75,fill = "yellow",border = "black")
    ProgressionTreeButton.Type = "ProgressionTree"
    ProgressionTreeButton.Text = Label("Story Mode",ProgressionTreeButton.centerX,ProgressionTreeButton.centerY)
    app.TemporaryButtons.append(ProgressionTreeButton)
    
    CharacterSelectButton = Rect(LeftSide,125,400 - LeftSide * 2,75,fill = "lightgreen",border = "black")
    CharacterSelectButton.Type = "CharacterSelect"
    CharacterSelectButton.Text = Label("Edit Characters",CharacterSelectButton.centerX,CharacterSelectButton.centerY)
    app.TemporaryButtons.append(CharacterSelectButton)
    
    UnlockPathButton = Rect(LeftSide,225,400 - LeftSide * 2,75,fill = "red",border = "black")
    UnlockPathButton.Type = "FloorSelect"
    UnlockPathButton.Text = Label("Floor Select",UnlockPathButton.centerX,UnlockPathButton.centerY)
    app.TemporaryButtons.append(UnlockPathButton)
    
    InstructionButton = Rect(LeftSide,325,400 - LeftSide * 2,50,fill = "LightGrey",border = "black")
    InstructionButton.Type = "Instructions"
    InstructionButton.Text = Label("Instructions",InstructionButton.centerX,InstructionButton.centerY)
    app.TemporaryButtons.append(InstructionButton)
    
    #XButton.toFront()
    XButton.visible = False
    
    pass

def HideCharacterSelect():
    for Character in PlayerCharacters:
        Character.visible = False
        Character.AdditionalInfoBoard.visible = False
        
def DeleteTempButtons():
    while len(app.TemporaryButtons) > 0:
        if app.TemporaryButtons[0].Type != "locked" and app.TemporaryButtons[0].Type != "Attribution Slot":
            app.TemporaryButtons[0].Text.visible = False
        app.TemporaryButtons[0].visible = False
        app.TemporaryButtons.remove(app.TemporaryButtons[0])


def DisplayCharacterSelect():
    StartX = 40
    index = 0
    for Character in PlayerCharacters:
        
        MaxHealth = Character.MaxHealth
        MaxStagger = Character.MaxStagger

        Character.Health = MaxHealth
        Character.Stagger = MaxStagger
        UpdateBars(Character)
        for RunItThrice in range(2):
            FixUpCharacter(Character)
            print("Fixed up " + Character.name)

        if index < app.CharactersUnlocked:
            Character.visible = True
            FixUpCharacter(Character)
            Character.centerX = StartX
            Character.centerY = 100
            HideCharacterUI(Character)
            
            Character.AdditionalInfoBoard.centerX = StartX + 5
            Character.AdditionalInfoBoard.centerY = 205
            
            Character.AdditionalInfoBoard.visible = True
            Character.NameBoard.Text.visible = True
            Character.NameBoard.visible = True
            
            EditDeckButton = Circle(StartX + 5,280,40,fill = "lightgreen",border = "black")
            EditDeckButton.ConnectedCharacter = Character
            EditDeckButton.Type = "Deck"
            EditDeckButton.Text = Label("Edit Deck",EditDeckButton.centerX,EditDeckButton.centerY)
            EditCharacterButton = Circle(StartX + 5,360,40,fill = "lightblue",border = "black")
            EditCharacterButton.Text = Label("Edit Character",EditCharacterButton.centerX,EditCharacterButton.centerY)
            EditCharacterButton.ConnectedCharacter = Character
            EditCharacterButton.Type = "EditCharacter"
            app.TemporaryButtons.append(EditDeckButton)
            app.TemporaryButtons.append(EditCharacterButton)
        
        else:
            LockBox = Rect(0,0,80,385,fill = "grey")
            LockBox.centerX = StartX
            LockBox.bottom = 400
            LockBox.Type = "locked"
            app.TemporaryButtons.append(LockBox)
            
        StartX += 83
        index += 1
        
def DisplayFloorSelect():
    
    print("Displaying Enlightenment tree")
    StartY = 0

    for Floor in app.Floors: #the larger overarcing "stage" in progression
        if Floor.Unlocked:
            print("unlocked Stage")
            BattleContainer = Rect(-80,-20,100 + 5 * 50,70,fill = "black", border = "orange")
            BattleContainer.top = StartY
            StartY = BattleContainer.bottom + 2
            BattleContainer.centerX = 220
            BattleContainer.Type = "locked"
            app.TemporaryButtons.append(BattleContainer)
            
            SetActiveButton = Rect(0,0,40,40,fill = "grey",border = "black")
            SetActiveButton.centerY = BattleContainer.centerY
            SetActiveButton.centerX = BattleContainer.left + 40
            SetActiveButton.ConnectedFloor = Floor
            SetActiveButton.Type = "SetActive"
            SetActiveButton.Text = Label("",SetActiveButton.centerX,SetActiveButton.centerY)
            if app.CurrentFloor == Floor:
                SetActiveButton.Text.value = "X"
            else:
                SetActiveButton.Text.value = ""

            EnlightenmentBattlesButton = Rect(0,0,140,40,fill = "lightGreen",border = "black")
            EnlightenmentBattlesButton.ConnectedFloor = Floor
            EnlightenmentBattlesButton.Type = "Battles"
            EnlightenmentBattlesButton.centerY = BattleContainer.centerY
            EnlightenmentBattlesButton.left = BattleContainer.left + 60
            EnlightenmentBattlesButton.Text = Label("Floor Battles",EnlightenmentBattlesButton.centerX,EnlightenmentBattlesButton.centerY)
            #also need Team Abnos and Active select button
            TeamAbnormalitiesButton = Rect(0,0,140,40,fill = "lightBlue",border = "black")
            TeamAbnormalitiesButton.centerY = BattleContainer.centerY
            TeamAbnormalitiesButton.left = BattleContainer.left + 200
            TeamAbnormalitiesButton.Text = Label("Floor Buffs",TeamAbnormalitiesButton.centerX,TeamAbnormalitiesButton.centerY)
            TeamAbnormalitiesButton.ConnectedFloor = Floor
            TeamAbnormalitiesButton.Type = "Abnormalities"
            app.TemporaryButtons.append(EnlightenmentBattlesButton)
            app.TemporaryButtons.append(TeamAbnormalitiesButton)
            app.TemporaryButtons.append(SetActiveButton)
            
        else:
            print("locked Stage")
            LockBox = Rect(0,0,400,400/7,fill = "grey",border = "black")
            LockBox.top = StartY
            StartY = LockBox.bottom + 2
            LockBox.left = 0
            LockBox.Type = "locked"
            app.TemporaryButtons.append(LockBox)
        

        
def DisplayCharacterEdit(Character):
    StartX = 240
    StartY = 65 + app.DeckBuilderYDisp
    print(str(len(AllDisplayCards)) + " unique cards in total")
    index = 1
    FixUpCharacter(Character)
    HideCharacterUI(Character)
    Character.visible = True
    Character.centerX = 55
    Character.centerY = 270
    
    Character.AdditionalInfoBoard.centerX = 55
    Character.AdditionalInfoBoard.centerY = 360
    
    Character.AdditionalInfoBoard.visible = True
    
    CheckSortUnused()
    
    AltY = 30
    Altindex = 0
    if app.UnlockedAttribution:
        for Count in range(4):
            if len(Character.OverrideCard.AttributedCards) < Altindex + 1:
                #make them temp buttons or smthn
                Slot = Rect(105,index * 100 + 5,60,95)
                Icon = Circle(Slot.centerX,Slot.centerY,10,border = "yellow")
                PlusDisp = 5
                Plus1 = Line(Slot.centerX,Icon.top + PlusDisp,Slot.centerX,Icon.bottom - PlusDisp,fill="yellow")
                Plus2 = Line(Icon.left + PlusDisp,Slot.centerY,Icon.right - PlusDisp,Slot.centerY,fill="yellow")
                AttributionSlot = Group(Slot,Icon,Plus1,Plus2)
                AttributionSlot.Type = "Attribution Slot"
                app.TemporaryButtons.append(AttributionSlot)
                #there is no attributed so...
                pass
            else:
                Character.OverrideCard.AttributedCards[Altindex].centerX = 135
                Character.OverrideCard.AttributedCards[Altindex].centerY = 100 * Altindex + 53
        
            Altindex += 1
        
    
    for Card in app.UnusedCharacterCards:
        Card.visible = True
        Card.centerX = StartX
        Card.centerY = StartY
        StartX += 65
        if index != 0:
            if index % 3 == 0:
                StartX -= 65 * 3
                StartY += 125
        index += 1
    pass

def CheckSortUnused():
    #first check if already in order
    Lowest = -1
    AlreadySorted = True
    for Card in app.UnusedCharacterCards:
        if Card.SortNumber >= Lowest:
            Lowest = Card.SortNumber
        else:
            AlreadySorted = False
    if not AlreadySorted:
        EscroList = []
        while len(app.UnusedCharacterCards) > 0:
            Lowest = 99999
            QuickFindList = []
            for Card in app.UnusedCharacterCards:
                if Card.SortNumber < Lowest:
                    QuickFindList.clear()
                    QuickFindList.append(Card)
                    Lowest = Card.SortNumber
                elif Card.SortNumber == Lowest:
                    QuickFindList.append(Card)

            while len(QuickFindList) > 0:
                EscroList.append(QuickFindList[0])
                app.UnusedCharacterCards.remove(QuickFindList[0])
                QuickFindList.remove(QuickFindList[0])
        
        #once all is in escro
        while len(EscroList) > 0:
            app.UnusedCharacterCards.append(EscroList[0])
            EscroList.remove(EscroList[0])
            
            
def DisplayLibrary(Character):
    DeckbuildingBack.visible = True
    print("refreshing cards on library display")
    print(str(len(Character.Library)) + " cards in library so no issues?")
    DisplayDeckBuilder()
    index = 1
    #sort character library by cost
    SortLibrary(Character.Library)
    StartX = 35
    StartY = 100
    for Card in Character.Library:
        Card.visible = True
        Card.centerX = StartX
        Card.centerY = StartY
        StartX += 65
        if index != 0:
            if index % 3 == 0:
                StartX -= 65 * 3
                StartY += 125
        index += 1
        
def SortLibrary(Library):
    TempLibrary = list(Library)
    Cost = 0
    for round in range(10):
        for Card in TempLibrary:
            if Card.cost == Cost:
                Library.remove(Card)
                Library.append(Card)
                pass
        Cost += 1
        
def MoveDisplayCards(YDisp):
    print("moving editor +" + str(YDisp))
    app.DeckBuilderYDisp += YDisp
    if app.Menu == "ProgressionTree":
        if app.DeckBuilderYDisp < 0:
            app.DeckBuilderYDisp = 0
    else:
        if app.DeckBuilderYDisp > 0:
            app.DeckBuilderYDisp = 0
    if app.Menu == "EditDeck":
        DisplayDeckBuilder()
    elif app.Menu == "EditCharacter":
        DisplayCharacterEdit(app.ChosenCharacter)
    elif app.Menu == "Abnormalities":
        DeleteTempButtons()
        DisplayFloorAbnormalities(app.DisplayedFloor)
    elif app.Menu == "ProgressionTree":
        DeleteTempButtons()
        DisplayProgressionTree()
        
        
def DisplayDeckBuilder():
    #Sorts the all cards list by cost
    StartX = 240
    StartY = 65 + app.DeckBuilderYDisp
    SortLibrary(AllDisplayCards)
    print(str(len(AllDisplayCards)) + " unique cards in total")
    index = 1
    for Card in AllDisplayCards:
        Card.visible = True
        Card.centerX = StartX
        Card.centerY = StartY
        StartX += 65
        if index != 0:
            if index % 3 == 0:
                StartX -= 65 * 3
                StartY += 125
        index += 1
        
def HideEditDeck():
    DeckbuildingBack.visible = False
    for Character in PlayerCharacters:
        for Card in Character.Library:
            Card.visible = False
    for Card in AllDisplayCards:
        Card.visible = False
        
def ContinueAfterFight():
    print("Moving to main menu")
    app.BlackScreen.visible = False
    app.ContinueText.visible = False
    app.WinText.visible = False
    app.GamoverText.visible = False
    for Card in AllTotalCards:
        Card.visible = False
    RelevantDice = PlayerSpeedDice + EnemySpeedDice
    for Die in RelevantDice:
        RemoveClashLine(Die)
        
def StartBattle(Fight):
    #hides all the menuing
    XButton.visible = False
    app.ChosenAbnoPages = [] 
    print("Let it begin!")
    #for Floor in app.Floors:
    for Stage in app.StoryStages:# + app.EnlightenmentStages:
        Stage.visible = False
        
    for Floor in app.Floors:
        for Symbol in Floor.EnlightenmentStageSymbols:
            Symbol.visible = False
        for Stage in Floor.EnlightenmentStages:
            Stage.visible = False
            
    for Symbol in app.StageSymbols:
        Symbol.visible = False
    #app.AutoProgressStagesForTesting = False
    app.InAFight = True
    app.InMainMenu = False
    app.PlayerConfirmStage = 0
    for Character in Fight.ListOfParts[app.CurrentPart].ListOfFighters: #adds all enemies
        print("Character added " + Character.name)
        Character.Health = Character.MaxHealth
        Character.Stagger = Character.MaxStagger
        UpdateBars(Character)
        AllFightingCharacters.append(Character)
        for Die in Character.SpeedDice:
            #print("die added")
            EnemySpeedDice.append(Die)
            
    index = 0        
    for Count in range(app.CharactersUnlocked): #adds all player characters
        Character = PlayerCharacters[index]
        if len(Character.Library) < 9:
            SupplementLibrary(Character)
        Character.Health = Character.MaxHealth
        Character.Stagger = Character.MaxStagger
        UpdateBars(Character)
        AllFightingCharacters.append(Character)
        Character.AdditionalInfoBoard.right = 400 * XScreenDialation
        Character.AdditionalInfoBoard.top = 0
        for Die in Character.SpeedDice:
            PlayerSpeedDice.append(Die)
        index += 1
            
    for Character in AllFightingCharacters:
        Character.visible = True
        
        for Passive in Character.AttributedPassives:
            AddPassiveEffect(Character,Passive)
        
        if Character.ControlledByPlayer:
            Character.NameBoard.Text.visible = False
            Character.NameBoard.visible = False
        
        Character.Health = Character.MaxHealth
        Character.Stagger = Character.MaxStagger

        Character.Staggered = False
        Character.ClearStaggered = False
        if Character.StartingLight != None:
            Character.Light = Character.StartingLight
        else:
            Character.Light = Character.MaxLight
        FixLightSpritePositions(Character)
        ShuffleList(Character.Library)
        for drawing in range(4):
            DrawCard(Character)
            
    app.RoundNum = 0

    ResetAllCharacterPositions()

def SupplementLibrary(Character):
    TargetCard = AllDisplayCards[0]
    while len(Character.Library) < 9:
        
        #check for 3 of a kind
        
        duplicates = 0
        for Card in Character.Library:
            if Card.name == TargetCard.name:
                duplicates += 1
        if duplicates < 3:
            CopyCard(TargetCard, Character.Library)
            print("added card to library!")
        else:
            if TargetCard == AllDisplayCards[0]:
                TargetCard = AllDisplayCards[1]
            else:
                TargetCard = AllDisplayCards[2]
        
def FightEnd(Victory):
    print("ending fight")   
        
    if len(app.CurrentFight.ListOfParts) - 1 <= app.CurrentPart or not Victory:
        print("fight completed")
        
        for Character in AllCharacters:
            DissapearCharacter(Character, True)
        
        app.CurrentPart = 0
        AllFightingCharacters.clear()
        EnemySpeedDice.clear()
        PlayerSpeedDice.clear()
        DeadCharacters.clear()
        DeadSpeedDice.clear()
        
        for Character in AllCharacters:
            HeldLevel = Character.EmotionLevel #resets light
            for Count in range(HeldLevel):
                print("light removed from " + Character.name)
                RemoveLight(Character)
                
            Character.EmotionCoins.clear()
            Character.BankedEmotionCoins.clear()
            #print(Character.EmotionLevel)
            ResetEmotionBar(Character)
                
            if len(Character.LightSprites) > Character.MaxLight:
                print("overmaxxing the light! this is the problem")
        
        app.BlackScreen.visible = True
        app.BlackScreen.toFront()
        app.ContinueText.visible = True
        app.ContinueText.toFront()
        app.CurrentTeamEmotionLevel = 0
        if Victory:
            app.WinText.visible = True
            app.WinText.toFront()
            CheckForSpecialStageEndEvents(app.CurrentBattle.StageNum,app.CurrentFight.FightNumber,app.CurrentBattle.IsSpecialStage)
            if not app.CurrentBattle.IsSpecialStage and app.CurrentBattle.StageNum == app.StagesUnlocked:
                if len(app.CurrentBattle.ListOfFights) == 1:
                    app.StagesUnlocked += 1
                else:
                    if app.CurrentFight.FightNumber == app.CurrentBattle.FightsUnlocked:
                        app.CurrentBattle.FightsUnlocked += 1
                        if app.CurrentBattle.FightsUnlocked > len(app.CurrentBattle.ListOfFights):
                            #app.CurrentBattle.FightsUnlocked = 1
                            app.StagesUnlocked += 1
            
            if app.CurrentBattle.IsSpecialStage:
                print("adding abno rewards to floor")
                for Card in app.CurrentFight.RewardCards:
                    app.CurrentFloor.EmotionPayoffs[Card.Level - 1].append(Card)
                    
                app.CurrentFight.RewardCards.clear()
            else:
                for Card in app.CurrentFight.RewardCards:
                    AllDisplayCards.append(Card)
                app.CurrentFight.RewardCards.clear()
                for CharacterCard in app.CurrentFight.RewardCharacters:
                    app.UnusedCharacterCards.append(CharacterCard)
                    CharacterCard.SortNumber = len(app.UnusedCharacterCards)
                app.CurrentFight.RewardCharacters.clear()
                
        else:
            app.GamoverText.visible = True
            app.GamoverText.toFront()
        
        app.PlayerConfirmStage = 10
    
    else:
        print("next part lol")
        
        ResetAllCharacterPositions() #this levels up team which we dont want if victory with no after or loss

        for Character in AllCharacters:
            DissapearCharacter(Character, False)
        
        app.CurrentPart += 1
        print("app.Currentpart = " + str(app.CurrentPart))
        print("Compared against " + str(len(app.CurrentFight.ListOfParts) - 1))
        for Character in AllFightingCharacters:
            CheckForEmotionLevelup(Character)
            Character.EmotionCoins.clear()
            ResetEmotionBar(Character)
            
        AllFightingCharacters.clear()
        EnemySpeedDice.clear()
        PlayerSpeedDice.clear()
        DeadCharacters.clear()
        DeadSpeedDice.clear()
        
        #do the hand reseter
        for Character in AllCharacters:
            ResetCharacterLibrary(Character)
            
        for Card in AllTotalCards:
            Card.visible = False
            
        Particle = Rect(0,0,400,400)
        Particle.Rotation = 0
        Particle.XVel = 0
        Particle.YVel = 0
        Particle.Fade = 2
        app.FadingParticles.append(Particle)
        if not app.PlayerConfirmStage == 7: #should fix mid stage emotion level ups breaking!
            app.PlayerConfirmStage = 0
        #adds next enemies
        for Character in app.CurrentFight.ListOfParts[app.CurrentPart].ListOfFighters:
            print("Character added " + Character.name)
            Character.Health = Character.MaxHealth
            Character.Stagger = Character.MaxStagger
            UpdateBars(Character)
            AllFightingCharacters.append(Character)
            for Die in Character.SpeedDice:
                EnemySpeedDice.append(Die)
                
        index = 0     
        #readds the players
        for Count in range(app.CharactersUnlocked):
            Character = PlayerCharacters[index]
            if len(Character.Library) < 9:
                SupplementLibrary(Character)
            Character.Stagger = Character.MaxStagger
            UpdateBars(Character)
            AllFightingCharacters.append(Character)
            for Die in Character.SpeedDice:
                PlayerSpeedDice.append(Die)
            index += 1
                
        #runs some of fight startup
        for Character in AllFightingCharacters:
            Character.visible = True
            if Character.ControlledByPlayer:
                Character.NameBoard.Text.visible = False
                Character.NameBoard.visible = False
            
            Character.Staggered = False
            Character.ClearStaggered = False
            if Character.StartingLight != None:
                Character.Light = Character.StartingLight
            else:
                Character.Light = Character.MaxLight
            FixLightSpritePositions(Character)
            for drawing in range(4):
                DrawCard(Character)
                
        ResetAllCharacterPositions()
        
def DissapearCharacter(Character,RemovePassives):
    Character.visible = False
    ClearExtraDice(Character)
    for Die in Character.SpeedDice:
        if Die.TargettingLine != None:
            Die.TargettingLine.visible = False
            Die.TargettingLine = None
            
    RemovalList = []
    for Effect in Character.StatusEffects:
        if Effect.BaseEffect or RemovePassives: #checks for both of this is an always remove base effect, or we are removing all
            RemovalList.append(Effect)
            Effect.visible = False
            print("effect removed from " + Character.name)
            Character.remove(Effect)
    
    #Character.StatusEffects.clear()
    for Effect in RemovalList:
        Character.StatusEffects.remove(Effect)
    
    for Effect in Character.NextTurnStatusEffects: #these are always base
        Effect.visible = False
        print("effect removed from " + Character.name)
        Character.remove(Effect)
        
    Character.NextTurnStatusEffects.clear()
    
    Character.EmotionBar.visible = False
    Character.AdditionalInfoBoard.visible = False
    
def CheckForSpecialStageEndEvents(StageNum,FightNum,IsSpecial):
    if not IsSpecial:
        if StageNum == 2 and FightNum == 2:
            if app.Floors[0].EnlightenmentUnlocked < 1:
                app.Floors[0].EnlightenmentUnlocked = 1
        elif StageNum == 2 and FightNum == 3:
            if not app.Floors[1].Unlocked:
                app.Floors[1].Unlocked = True
        elif StageNum == 3 and FightNum == 1:
            if app.Floors[1].EnlightenmentUnlocked < 1:
                app.Floors[1].EnlightenmentUnlocked = 1
        elif StageNum == 4 and FightNum == 1:
            if not app.Floors[2].Unlocked:
                app.Floors[2].Unlocked = True
    else:    #this is an elightenment stage    
        print("stage number is " + str(StageNum))
        if StageNum == 1 and app.CurrentFloor.CharactersUnlocked < 2:
            print("trying to get characters unlocked to 2")
            app.CurrentFloor.CharactersUnlocked = 2
            app.CurrentFloor.CurrentEmotionLevelCap = 2
            app.CharactersUnlocked = app.CurrentFloor.CharactersUnlocked
            app.CurrentEmotionLevelCap = app.CurrentFloor.CurrentEmotionLevelCap
            
#------------------------------------------------------------------------------------------
#Updates and fixes for fight
            
        
def FixLightSpritePositions(Character):
    
    LightDisp = (Character.MaxLight * 20) / -2
    Index = 1
    
    ActiveLight = 0
    #print("We have this many dice: " + str(len(Character.SpeedDice)))
    for Die in Character.SpeedDice:
        if Die.HeldPage != None:
            ActiveLight += Die.HeldPage.cost
            #print("We have found a page of cost: " + str(Die.HeldPage.cost))
        else:
            #print("this page holds nothing?")
            pass
    #print("We have this much active: " + str(ActiveLight))
    
    for LightMote in Character.LightSprites:
        LightMote.centerX = Character.CharacterSprite.centerX + LightDisp
        LightMote.centerY = Character.CharacterSprite.centerY - 80
        LightDisp += 20

        
        #print("We have this much light: " + str(Character.Light))
        #print("We have this much total: " + str(Character.MaxLight))
        
        if Character.Light >= Index:
            LightMote.radius = 10
            LightMote.fill = "gold"
        elif ActiveLight >= Index - Character.Light:
            LightMote.radius = 7
            LightMote.fill = "brown"
        else:
            LightMote.radius = 4
            LightMote.fill = "grey"
        
        Index += 1
        
def ResethandCardPositions():
    if len(app.DisplayedHandCards) == 8:
        PrevX = -40
    else:
        PrevX = 0
    for Card in app.DisplayedHandCards:
        #ReconstructCard(Card)
        FixupCard(Card)
        Card.left = PrevX
        Card.centerY = 330
        PrevX = Card.right

def FixupCard(Card):
    #print("fix up")
    LowEnd = Card.Frame.centerY - 19
    if len(Card.OnUseText) > 0:
        for line in Card.OnUseText:
            line.left = app.Xdisplace + Card.Frame.left - 14
            line.top = LowEnd
            LowEnd = line.bottom + 2
            
    for Die in Card.DiceList:
        Die.IconCircle.centerX = app.Xdisplace + Card.Frame.left
        Die.IconCircle.top = LowEnd
        LowEnd = Die.IconCircle.bottom + 2
        
        Die.TypeSprite.centerX = Die.IconCircle.centerX
        Die.TypeSprite.centerY = Die.IconCircle.centerY
        Die.DamageRangeText.centerX = Die.IconCircle.centerX + 20
        Die.DamageRangeText.centerY = Die.IconCircle.centerY
        #print(Die.AddEffectDescription)
        if Die.AddEffectDescription != None:
            #print(len(Die.AddEffectDescription))
            #print("found the group?")
            for line in Die.AddEffectDescription:
                line.left = Die.IconCircle.centerX - 14
                #line.centerY = Die.IconCircle.centerY
                line.top = LowEnd
                LowEnd = line.bottom + 2
                #print("setting line low end at" + str(LowEnd))
        
        #Die.TypeSprite.visible = True
        Die.TypeSprite.opacity = 100
        Die.TypeSprite.toFront()

def FixUpCharacter(Character):
    print("fixing up " + Character.name)
    X = Character.CharacterSprite.centerX
    Y = Character.CharacterSprite.centerY
    if len(Character.SpeedDice) > 1:
        StartX = X - ((40 * len(Character.SpeedDice)) / 3) 
    else:
        StartX = X
    
    if Character.ControlledByPlayer:
        Character.NameBoard.centerY = Y - 50
        Character.NameBoard.centerX = StartX
        Character.NameBoard.Text.centerY = Character.NameBoard.centerY
        Character.NameBoard.Text.centerX = StartX
    
    for Die in Character.SpeedDice:
        Die.ConnectedSprite.centerX = StartX #-20
        Die.ConnectedSprite.centerY = Y - 50
        
        Die.ConnectedText.centerX = Die.ConnectedSprite.centerX
        Die.ConnectedText.centerY = Die.ConnectedSprite.centerY
        
        StartX += 40

    Character.EmotionBar.EmotionLevelText.value = Character.EmotionLevel
    FixLightSpritePositions(Character)


def DisplayHand(Character, ThisDie):
    Character.HandOnDisplay = True
    if len(app.DisplayedHandCards) == 0:
        for Card in Character.Hand:
            #print("displaying " + str(len(app.DisplayedHandCards)))
            Card.visible = True
            Card.toFront()
            app.DisplayedHandCards.append(Card)
            ResethandCardPositions()
    else:
        ResethandCardPositions()
        for Card in app.DisplayedHandCards:
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

def ClearExtraDice(Character):
    for die in range(len(Character.UnusedDice)):
        ResolveAndRemoveExtraDie(Character.UnusedDice)
        
def HideHand(Character):
    Character.HandOnDisplay = False
    for Card in Character.Hand:
        Card.visible = False
        ClearList(app.DisplayedHandCards)
    
    for Die in Character.SpeedDice:
        Die.Override = False
#------------------------------------------------------------------------------------------------------------------------    
#Setup

def CreateStoryStages():
    #the order of the main story stages really matters
    #first act stages and abnos
    CreateRatsStage()
    CreateYunStage()
    CreateBrotherStage()
    CreateHookStage()
    
    #second act stages
    CreateChefStage()

    CreateBloodBathStage()
    CreateScorchedGirlStage()
    
    CreateStorySymbols()

def CreateStorySymbols():
    
    Rat = AssignSymbol("Rat")
    app.StageSymbols.append(Rat)
    
    Yun = AssignSymbol("Yun")
    app.StageSymbols.append(Yun)
    
    BloodBath = AssignSymbol("BloodBath")
    app.Floors[0].EnlightenmentStageSymbols.append(BloodBath)
    
def AssignSymbol(SpriteName):
    if SpriteName == "Rat":
        Rat = Polygon(77,154,84,141,119,126,153,106,157,84,177,74,194,85,193,85,226,139,244,162,246,205,209,226,177,228,141,225,179,213,157,212,154,216,177,160,157,178,135,208,116,217,129,166,107,207,105,170,79,153,111,147,105,163,81,150)
        RatEye = Circle(137,140,10,fill = "red")
        RatNose = Polygon(77,154,84,141,105,170,fill="pink")
        RatTail = Group(Line(245,199,288,163),Line(295,92,288,163),Line(295,92,271,72),Line(247,82,271,72),Line(247,82,247,102),Line(271,106,247,102),Line(271,106,272,89),Line(259,86,272,89))
        FullRat = Group(Rat,RatTail)
        FullRat.fill = "grey"
        FullRat.add(RatEye)
        FullRat.add(RatNose)
        FullRat.visible = False
        return FullRat
        
    elif SpriteName == "Yun":
        Yun1 = Circle(200,100,50,fill = "grey",border = "yellow",borderWidth = 5)
        Yun2 = Circle(200,100,25)
        Yun3 = Rect(100,175,200,30,fill = "grey",border = "yellow",borderWidth = 5)
        Yun4 = Rect(150,205,25,60,fill = "grey",border = "yellow",borderWidth = 5)
        Yun5 = Rect(225,205,25,60,fill = "grey",border = "yellow",borderWidth = 5)
        Yun6 = Polygon(75,275,200,355,325,275,335,290,200,380,65,290,fill = "grey",border = "yellow",borderWidth = 4)
        FullYun = Group(Yun1,Yun2,Yun3,Yun4,Yun5,Yun6)
        FullYun.visible = False
        return FullYun
        
    elif SpriteName == "BloodBath":
        Chalice = Polygon(169,199,175,238,190,253,190,270,169,284,231,284,210,270,210,253,225,238,231,199,fill = "grey")
        Blood = Oval(200,200,62,30,fill = "red")
        FullBloodBath = Group(Chalice,Blood)
        FullBloodBath.visible = False
        return FullBloodBath
        
    else:
        DefaultSprite = Oval(200,200,30,45)
        DefaultSprite.visible = False
        return DefaultSprite
        
def CreateChefStage():
    
    Battle = Group()
    ListOfFights = []
    
    Fight = Group()
    Fight.FightNumber = 0
    Fight.RewardCards = []
    Fight.RewardCharacters = []
    Fight.ListOfParts = []
    
    Part = Group()
    Part.ListOfFighters = []
    
    print("creating chef's cards")
    
    for Spam in range(2):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [2,1,0,2,1,0]
        AttributedPassives = []
        CreateCharacterCard("Jack","green",SpeedDiceList,3,42,22,ResistanceList,Fight.RewardCharacters,"Chef",AttributedPassives)
    for Spam in range(2):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [0,2,1,0,2,1]
        AttributedPassives = []
        CreateCharacterCard("Pierre","green",SpeedDiceList,3,42,22,ResistanceList,Fight.RewardCharacters,"Chef",AttributedPassives)
    
    print("creating chef reward cards")
    
    DiceList = []
    CreateDie(2,6,"slash",DiceList,"Next2Bind","On Hit","Enemy",False) #hit 2 bind
    CreateDie(2,5,"blunt",DiceList,None,None,None,False)
    CreateCard("green",2,"Ingredient Hunt",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,6,"blunt",DiceList,"NextParalysis","On Hit","Enemy",False) #hit paralysis
    CreateDie(1,4,"evade",DiceList,None,None,None,False)
    CreateCard("green",1,"Trim Ingerdients",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(3,4,"pierce",DiceList,"NextBleed","On Hit","Enemy",False) #on hit 1 bleed
    CreateCard("blue",0,"Appetite",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(2,6,"blunt",DiceList,"X=BleedRegain Health","On Hit","Self",False) #hit gain health based on bleed 
    CreateDie(2,3,"block",DiceList,None,None,None,False)
    CreateCard("blue",1,"Cruelty",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(3,4,"slash",DiceList,None,None,None,False)
    CreateDie(1,12,"evade",DiceList,None,None,None,False)
    CreateCard("purple",1,"Keep It Fresh",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,6,"pierce",DiceList,None,None,None,False)
    CreateDie(4,4,"slash",DiceList,"4Regain Health","On Hit","Self",False) #hit gain 4 health
    CreateCard("purple",1,"Cook Everything",DiceList,Fight.RewardCards,None) #Fight.RewardCards
    
    
    
    SpeedDiceList = []
    CreateSpeedDie(2,5,SpeedDiceList)
    DeckList = CreateDeckList(["Organ Harvesting","Organ Harvesting","Backstreets Shove","Claw Off","Run Away"])
    ResistanceList = [0,0,1,0,1,0]
    AttributedPassives = []
    Pierre = CreateCharacter(170,105,2,False,SpeedDiceList,DeckList,3,35,18,ResistanceList,"Pierre",Part.ListOfFighters,"Chef",AttributedPassives,1)
    
    print("Pierre done")
    
    SpeedDiceList = []
    CreateSpeedDie(2,5,SpeedDiceList)
    DeckList = CreateDeckList(["Rat's Guide","Rat's Guide","Backstreets Shove","Claw Off","Run Away"])
    ResistanceList = [0,1,0,0,2,1]
    AttributedPassives = []
    Jack = CreateCharacter(120,170,2,False,SpeedDiceList,DeckList,3,35,15,ResistanceList,"Jack",Part.ListOfFighters,"Chef",AttributedPassives,1)
    
    print("Jack done")
    
    Fight.ListOfParts.append(Part)
    ListOfFights.append(Fight)
    
    BattleContainer = Rect(-80,-20,100 + len(ListOfFights) * 50,80,fill = "black", border = "orange")
    Battle.add(BattleContainer)
    
    index = 0
    for Fight in ListOfFights:
        FightIcon = Rect(index * 55,0,40,40,fill = "black", border = "orange")
        FightIcon.rotateAngle = -45
        FightNumber = Label(str(index + 1),FightIcon.centerX,FightIcon.centerY,fill = "orange")
        
        #Battle.Icon = FightIcon
        Battle.add(FightIcon)
        Battle.add(FightNumber)
        FightIcon.Text = FightNumber
        Fight.FightIcon = FightIcon
        index += 1
    
    Battle.ListOfFights = ListOfFights
    Battle.FightsUnlocked = 1
    Battle.visible = False
    Battle.StageNum = 5
    Battle.IsSpecialStage = False
    Battle.EmotionLevelCap = 2
    app.StoryStages.append(Battle) 

def CreateHookStage():
    
    Battle = Group()
    ListOfFights = []
    
    Fight = Group()
    Fight.FightNumber = 0
    Fight.ListOfParts = []
    
    Part = Group()
    Part.ListOfFighters = []
    Fight.RewardCards = []
    Fight.RewardCharacters = []
    
    print("creating Hook's reward cards")
    
    for Spam in range(3):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [0,1,1,0,1,1]
        AttributedPassives = []
        CreateCharacterCard("Hook Fixer","green",SpeedDiceList,3,42,22,ResistanceList,Fight.RewardCharacters,"Yun",AttributedPassives)
        
    for Spam in range(3):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [0,1,2,0,1,2]
        AttributedPassives = []
        CreateCharacterCard("McCulin","blue",SpeedDiceList,3,42,22,ResistanceList,Fight.RewardCharacters,"Yun",AttributedPassives)
        
    for Spam in range(2):
        SpeedDiceList = []
        CreateSpeedDie(2,4,SpeedDiceList)
        ResistanceList = [2,0,0,2,0,0]
        AttributedPassives = []
        CreateCharacterCard("Taein","purple",SpeedDiceList,3,46,22,ResistanceList,Fight.RewardCharacters,"Yun",AttributedPassives)
    #add final named hook member
    
    DiceList = []
    CreateDie(3,5,"blunt",DiceList,"3Reduce","Clash Win","FollowingOpponentDie",False) #3Reduce 3 max val opps next die
    CreateDie(3,4,"pierce",DiceList,"2NextBleed","On Hit","Enemy",False) #hit inflict 2 bleed
    CreateCard("blue",2,"Defend This!",DiceList,Fight.RewardCards,None) 
    
    DiceList = []
    CreateDie(5,6,"pierce",DiceList,"2NextBleed","On Hit","Enemy",False) #hit inflict 2 bleed
    CreateDie(2,3,"slash",DiceList,None,None,None,False)
    CreateCard("purple",2,"Overpower",DiceList,Fight.RewardCards,None) 
    
    DiceList = []
    CreateDie(2,4,"blunt",DiceList,"1NextBleed","On Hit","Enemy",False) #hit inflict 1 bleed
    CreateDie(3,5,"pierce",DiceList,"1NextBleed","On Hit","Enemy",False) #hit inflict 1 bleed
    CreateDie(3,5,"slash",DiceList,None,None,None,False)
    CreateCard("purple",3,"Rampage",DiceList,Fight.RewardCards,None) 
    
    DiceList = []
    CreateDie(1,4,"slash",DiceList,None,None,None,False)
    CreateCard("green",0,"Track",DiceList,Fight.RewardCards,"1Regain Health") #Recover 1 hp
    
    DiceList = []
    CreateDie(1,7,"evade",DiceList,None,None,None,False)
    CreateDie(2,2,"pierce",DiceList,"1NextBleed","On Hit","Enemy",False) #hit inflict 1 bleed
    CreateDie(2,6,"pierce",DiceList,"1NextBleed","On Hit","Enemy",False) #hit inflict 1 bleed
    CreateCard("green",2,"Goin' First",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,6,"slash",DiceList,"1Regain Health","On Hit","Self",False) #hit regain 1 health
    CreateDie(2,6,"slash",DiceList,"1Regain Health","On Hit","Self",False)
    CreateCard("blue",2,"Mutilate",DiceList,Fight.RewardCards,"Effect2NextProtection") #Effect2AllNextProtection


    SpeedDiceList = []
    CreateSpeedDie(1,4,SpeedDiceList)
    DeckList = CreateDeckList(["Track","Track","Wallop","Preemptive Strike","Mutilate","Mutilate","Rampage","Rampage"])
    ResistanceList = [0,1,2,0,2,2]
    AttributedPassives = []
    Hook1 = CreateCharacter(90,175,2,False,SpeedDiceList,DeckList,2,18,7,ResistanceList,"Hook Fixer",Part.ListOfFighters,"Hook",AttributedPassives,None)
    
    print("Hok1 done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,4,SpeedDiceList)
    DeckList = CreateDeckList(["Track","Track","Wallop","Preemptive Strike","Mutilate","Mutilate","Rampage","Rampage"])
    ResistanceList = [0,1,2,0,2,2]
    AttributedPassives = []
    Hook2 = CreateCharacter(90,275,2,False,SpeedDiceList,DeckList,2,18,7,ResistanceList,"Hook Fixer",Part.ListOfFighters,"Hook",AttributedPassives,None)
    
    print("Hook2 done")
    
    Fight.ListOfParts.append(Part)
    #------------------------------------------------
    #first part fighters/\
    
    Part = Group()
    Part.ListOfFighters = []
    
    SpeedDiceList = []
    CreateSpeedDie(2,3,SpeedDiceList)
    DeckList = CreateDeckList(["Track","Track","Quickness","Preemptive Strike","Defend This!","Mutilate","Mutilate","Rampage"])
    ResistanceList = [0,0,2,0,2,1]
    AttributedPassives = []
    Naoki = CreateCharacter(90,175,2,False,SpeedDiceList,DeckList,2,21,10,ResistanceList,"Naoki",Part.ListOfFighters,"Hook",AttributedPassives,None)
    
    print("Naoki done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,3,SpeedDiceList)
    DeckList = CreateDeckList(["Track","Track","Quickness","Preemptive Strike","Overpower","Mutilate","Mutilate","Rampage"])
    ResistanceList = [0,2,0,1,2,0]
    AttributedPassives = []
    McCullin = CreateCharacter(90,275,2,False,SpeedDiceList,DeckList,2,22,9,ResistanceList,"McCullin",Part.ListOfFighters,"Hook",AttributedPassives,None)
    
    print("McCullin done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,3,SpeedDiceList)
    DeckList = CreateDeckList(["Track","Track","Quickness","Preemptive Strike","Goin' First","Mutilate","Mutilate","Rampage"])
    ResistanceList = [0,0,2,0,0,2]
    AttributedPassives = []
    Taein = CreateCharacter(140,225,2,False,SpeedDiceList,DeckList,2,21,10,ResistanceList,"Taein",Part.ListOfFighters,"Hook",AttributedPassives,None)
    
    print("Taein done")

    
    Fight.ListOfParts.append(Part)
    
    ListOfFights.append(Fight)
    
    BattleContainer = Rect(-80,-20,100 + len(ListOfFights) * 50,80,fill = "black", border = "orange")
    Battle.add(BattleContainer)
    
    index = 0
    for Fight in ListOfFights:
        Fight.FightNumber = index + 1
        FightIcon = Rect(index * 55,0,40,40,fill = "black", border = "orange")
        FightIcon.rotateAngle = -45
        FightNumber = Label(str(Fight.FightNumber),FightIcon.centerX,FightIcon.centerY,fill = "orange")
        
        #Battle.Icon = FightIcon
        Battle.add(FightIcon)
        Battle.add(FightNumber)
        FightIcon.Text = FightNumber
        Fight.FightIcon = FightIcon
        index += 1
    
    Battle.ListOfFights = ListOfFights
    Battle.FightsUnlocked = 1
    Battle.visible = False
    Battle.StageNum = 4
    Battle.IsSpecialStage = False
    Battle.EmotionLevelCap = 2
    app.StoryStages.append(Battle)

def CreateBrotherStage():
    
    Battle = Group()
    ListOfFights = []
    Fight = Group()
    Fight.FightNumber = 0
    Fight.ListOfParts = []
    
    Part = Group()
    Part.ListOfFighters = []
    Fight.RewardCards = []
    Fight.RewardCharacters = []
    
    for Spam in range(3):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [2,0,1,2,0,1]
        AttributedPassives = []
        CreateCharacterCard("Brother WIP","green",SpeedDiceList,3,43,22,ResistanceList,Fight.RewardCharacters,"Brotherhood",AttributedPassives)
    
    DiceList = []
    CreateDie(2,5,"block",DiceList,None,None,None,False) 
    CreateDie(3,4,"block",DiceList,"NextParalysis","Clash Win","Enemy",False) #clash win para
    CreateDie(1,3,"blunt",DiceList,"NextParalysis","On Hit","Enemy",False) # hit para "NextFragile","On Hit","Enemy"
    CreateCard("blue",1,"E-endure",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,6,"pierce",DiceList,"NextParalysis","On Hit","Enemy",False) #hit para
    CreateDie(2,5,"blunt",DiceList,None,None,None,False)
    CreateCard("green",2,"B-blow It Up!",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(2,3,"pierce",DiceList,None,None,None,False)
    CreateDie(1,1,"slash",DiceList,None,None,None,False)
    CreateDie(3,3,"slash",DiceList,None,None,None,False)
    CreateCard("green",2,"C-chop It Off",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(2,4,"slash",DiceList,None,None,None,False)
    CreateDie(3,4,"evade",DiceList,None,None,None,False)
    CreateCard("blue",2,"D-dried Up",DiceList,Fight.RewardCards,"Effect2NextStrength")
    
    DiceList = []
    CreateDie(1,12,"blunt",DiceList,"2NextParalysis","On Hit","Enemy",False) #2para
    CreateCard("purple",3,"YOLO",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(2,3,"blunt",DiceList,None,None,None,False)
    CreateCard("purple",0,"C-charge Up!",DiceList,Fight.RewardCards,["EffectNextParalysis","Gain Light"]) #restore 1 light and gain 1 para idk how to do 2 yet

    SpeedDiceList = []
    CreateSpeedDie(1,3,SpeedDiceList)
    DeckList = CreateDeckList(["Dodge and Strike","Dodge and Strike","E-endure","E-endure","E-endure","B-blow It Up!","B-blow It Up!","C-chop It Off"])
    ResistanceList = [0,2,0,0,2,0]
    AttributedPassives = []
    Mo = CreateCharacter(90,175,2,False,SpeedDiceList,DeckList,3,24,12,ResistanceList,"Mo",Part.ListOfFighters,"Brotherhood",AttributedPassives,None)
    
    print("Mo done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,3,SpeedDiceList)
    DeckList = CreateDeckList(["Dodge and Strike","Dodge and Strike","Quickness","E-endure","E-endure","D-dried Up","YOLO","YOLO"])
    ResistanceList = [0,1,0,1,2,0]
    AttributedPassives = []
    Consta = CreateCharacter(140,225,2,False,SpeedDiceList,DeckList,3,22,6,ResistanceList,"Consta",Part.ListOfFighters,"Brotherhood",AttributedPassives,None)
    
    print("Consta done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,3,SpeedDiceList)
    DeckList = CreateDeckList(["C-charge Up!","C-charge Up!","E-endure","E-endure","D-dried Up","D-dried Up","C-chop It Off","C-chop It Off"])
    ResistanceList = [0,0,1,1,0,2]
    AttributedPassives = []
    Arnold = CreateCharacter(190,275,2,False,SpeedDiceList,DeckList,3,22,10,ResistanceList,"Arnold",Part.ListOfFighters,"Brotherhood",AttributedPassives,None)
    
    print("Arnold done")
    
    Fight.ListOfParts.append(Part)
    ListOfFights.append(Fight)
    
    BattleContainer = Rect(-80,-20,100 + len(ListOfFights) * 50,80,fill = "black", border = "orange")
    Battle.add(BattleContainer)
    
    index = 0
    for Fight in ListOfFights:
        Fight.FightNumber = index + 1
        FightIcon = Rect(index * 55,0,40,40,fill = "black", border = "orange")
        FightIcon.rotateAngle = -45
        FightNumber = Label(str(Fight.FightNumber),FightIcon.centerX,FightIcon.centerY,fill = "orange")
        
        #Battle.Icon = FightIcon
        Battle.add(FightIcon)
        Battle.add(FightNumber)
        FightIcon.Text = FightNumber
        Fight.FightIcon = FightIcon
        index += 1
    
    Battle.ListOfFights = ListOfFights
    Battle.FightsUnlocked = 1
    Battle.visible = False
    Battle.StageNum = 3
    Battle.IsSpecialStage = False
    Battle.EmotionLevelCap = 2
    app.StoryStages.append(Battle)

def CreateYunStage():
    
    Battle = Group()
    ListOfFights = []
    Fight = Group()
    Fight.FightNumber = 0
    Fight.ListOfParts = []
    
    Part = Group()
    Part.ListOfFighters = []
    Fight.RewardCards = []
    Fight.RewardCharacters = []
    
    print("creating yun's reward cards")
    
    for Spam in range(3):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [2,0,1,2,0,1]
        AttributedPassives = []
        CreateCharacterCard("Yun's Guy","green",SpeedDiceList,3,43,22,ResistanceList,Fight.RewardCharacters,"Yun",AttributedPassives)
    
    DiceList = []
    CreateDie(1,4,"evade",DiceList,None,None,None,False) 
    CreateDie(1,2,"slash",DiceList,None,None,None,False) 
    CreateCard("green",0,"Dodge and Strike",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,4,"pierce",DiceList,None,None,None,False)
    CreateDie(1,4,"pierce",DiceList,None,None,None,False)
    CreateCard("green",1,"Thrust",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(2,6,"blunt",DiceList,None,None,None,False)
    CreateDie(2,4,"blunt",DiceList,None,None,None,False)
    CreateCard("green",2,"Wallop",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(3,5,"slash",DiceList,None,None,None,False)
    CreateDie(1,8,"evade",DiceList,None,None,None,False)
    CreateCard("green",2,"Preemptive Strike",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,4,"blunt",DiceList,None,None,None,False) 
    CreateDie(1,6,"evade",DiceList,None,None,None,False)
    CreateCard("green",1,"Quickness",DiceList,Fight.RewardCards,"EffectNextHaste") #On use gain haste
    
    DiceList = []
    CreateDie(2,3,"pierce",DiceList,None,None,None,False)
    CreateDie(3,4,"block",DiceList,"Gain Light","Clash Win","Self",False) #on clash win restore light
    CreateCard("green",1,"Preperation",DiceList,Fight.RewardCards,None)

    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Evade","Evade","Light Attack","Light Attack","Light Defense","Light Defense",])
    ResistanceList = [2,1,0,2,1,0]
    AttributedPassives = []
    Yun1 = CreateCharacter(90,175,2,False,SpeedDiceList,DeckList,3,15,7,ResistanceList,"Grade 9 Yun Fixer",Part.ListOfFighters,"Yun",AttributedPassives,None)
    
    print("Yun1 done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Evade","Evade","Light Attack","Light Attack","Light Defense","Light Defense",])
    ResistanceList = [0,2,1,0,2,1]
    AttributedPassives = []
    Yun2 = CreateCharacter(90,275,2,False,SpeedDiceList,DeckList,3,15,7,ResistanceList,"Grade 9 Yun Fixer",Part.ListOfFighters,"Yun",AttributedPassives,None)
    
    print("Yun2 done")
    
    Fight.ListOfParts.append(Part)
    ListOfFights.append(Fight)
    
    #-------------------------------------------------------------------------------------------------
    #first yun fight /\
    
    Fight = Group()
    Fight.FightNumber = 0
    Fight.ListOfParts = []
    
    Part = Group()
    Part.ListOfFighters = []
    Fight.RewardCards = []
    Fight.RewardCharacters = []
    
    print("creating finn's reward card")
    
    for Spam in range(4):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [0,2,1,0,2,1]
        AttributedPassives = []
        CreateCharacterCard("Finn","blue",SpeedDiceList,3,42,22,ResistanceList,Fight.RewardCharacters,"Yun",AttributedPassives)
    
    DiceList = []
    CreateDie(2,6,"block",DiceList,None,None,None,False)
    CreateDie(2,5,"block",DiceList,None,None,None,False) 
    CreateDie(2,6,"blunt",DiceList,None,None,None,False)
    CreateCard("purple",2,"Struggle",DiceList,Fight.RewardCards,"Effect2NextProtection") #On use gain 2 protection next scene 
    

    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Thrust","Thrust","Preperation","Preperation","Wallop","Wallop","Struggle","Struggle"])
    ResistanceList = [0,1,2,0,1,2]
    AttributedPassives = []
    Finn = CreateCharacter(90,175,2,False,SpeedDiceList,DeckList,2,18,6,ResistanceList,"Finn",Part.ListOfFighters,"Yun",AttributedPassives,2)
    
    print("Finn done")
    
    Fight.ListOfParts.append(Part)
    ListOfFights.append(Fight)
    #print(ListOfFights)
    #----------------------------------------------------------------------------------------------
    #2nd yun fight/\
    
    Fight = Group()
    Fight.FightNumber = 0
    Fight.ListOfParts = []
    
    Part = Group()
    Part.ListOfFighters = []
    Fight.RewardCards = []
    Fight.RewardCharacters = []
    
    print("creating yun3's reward cards")
    
    for Spam in range(3):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [0,1,2,0,1,2]
        AttributedPassives = []
        CreateCharacterCard("Eri","blue",SpeedDiceList,3,42,22,ResistanceList,Fight.RewardCharacters,"Yun",AttributedPassives)
        
    for Spam in range(2):
        SpeedDiceList = []
        CreateSpeedDie(2,4,SpeedDiceList)
        ResistanceList = [2,0,0,2,0,0]
        AttributedPassives = []
        CreateCharacterCard("Yun","purple",SpeedDiceList,3,46,22,ResistanceList,Fight.RewardCharacters,"Yun",AttributedPassives)
    
    DiceList = []
    CreateDie(2,6,"block",DiceList,"3Reduce","Clash Win","FollowingOpponentDie",False) #3Reduce 3 max val opps next die
    CreateDie(2,4,"slash",DiceList,None,None,None,False) 
    CreateDie(2,3,"slash",DiceList,None,None,None,False) 
    CreateCard("green",2,"Time for a Test",DiceList,Fight.RewardCards,None) 
    
    DiceList = []
    CreateDie(1,5,"slash",DiceList,"NextFragile","On Hit","Enemy",False) #hit inflict fragile
    CreateDie(3,4,"block",DiceList,None,None,None,False)
    CreateCard("blue",1,"Feelin' Good",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,9,"evade",DiceList,"Increase2","Clash Win","FollowingDie",False) #win +2 power next die 2IncreaseFollowingDie
    CreateDie(2,4,"slash",DiceList,"2NextFragile","On Hit","Enemy",False) #hit inflict 2 fragile
    CreateCard("blue",2,"You're Too Slow",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(4,8,"blunt",DiceList,None,None,None,False)
    CreateDie(3,4,"block",DiceList,None,None,None,False)
    CreateDie(3,4,"pierce",DiceList,None,None,None,False)
    CreateCard("purple",3,"Commandeering",DiceList,Fight.RewardCards,"Effect2AllPlayersNextProtection") #Effect2AllNextProtection


    SpeedDiceList = []
    CreateSpeedDie(1,3,SpeedDiceList)
    DeckList = CreateDeckList(["Dodge and Strike","Dodge and Strike","Preperation","Preperation","Thrust","Wallop","Wallop","Preemptive Strike"])
    ResistanceList = [2,0,1,2,0,1]
    AttributedPassives = []
    Yun1 = CreateCharacter(90,175,2,False,SpeedDiceList,DeckList,3,17,8,ResistanceList,"Grade 9 Yun Fixer",Part.ListOfFighters,"Yun",AttributedPassives,None)
    
    print("Yun1 done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Dodge and Strike","Dodge and Strike","Preperation","Preperation","Thrust","Wallop","Wallop","Preemptive Strike"])
    ResistanceList = [0,1,2,0,1,2]
    AttributedPassives = []
    Yun2 = CreateCharacter(90,275,2,False,SpeedDiceList,DeckList,3,17,8,ResistanceList,"Grade 9 Yun Fixer",Part.ListOfFighters,"Yun",AttributedPassives,None)
    
    print("Yun2 done")
    
    Fight.ListOfParts.append(Part)
    #------------------------------------------------
    #first part fighters/\
    
    Part = Group()
    Part.ListOfFighters = []
    
    SpeedDiceList = []
    CreateSpeedDie(2,3,SpeedDiceList)
    DeckList = CreateDeckList(["Dodge and Strike","Dodge and Strike","Preperation","Preperation","Commandeering"])
    ResistanceList = [2,0,0,2,0,0]
    AttributedPassives = []
    Yun = CreateCharacter(90,175,2,False,SpeedDiceList,DeckList,3,22,10,ResistanceList,"Yun",Part.ListOfFighters,"Yun",AttributedPassives,None)
    
    print("Yun done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,3,SpeedDiceList)
    DeckList = CreateDeckList(["Thrust","Wallop","Feelin' Good","Feelin' Good","Preperation","Preperation","Time for a Test","Time for a Test"])
    ResistanceList = [0,1,2,0,1,2]
    AttributedPassives = []
    Eri = CreateCharacter(90,275,2,False,SpeedDiceList,DeckList,3,22,8,ResistanceList,"Eri",Part.ListOfFighters,"Yun",AttributedPassives,None)
    
    print("Eri done")

    
    Fight.ListOfParts.append(Part)
    
    ListOfFights.append(Fight)
    
    BattleContainer = Rect(-80,-20,100 + len(ListOfFights) * 50,80,fill = "black", border = "orange")
    Battle.add(BattleContainer)
    
    index = 0
    for Fight in ListOfFights:
        Fight.FightNumber = index + 1
        FightIcon = Rect(index * 55,0,40,40,fill = "black", border = "orange")
        FightIcon.rotateAngle = -45
        FightNumber = Label(str(Fight.FightNumber),FightIcon.centerX,FightIcon.centerY,fill = "orange")
        
        #Battle.Icon = FightIcon
        Battle.add(FightIcon)
        Battle.add(FightNumber)
        FightIcon.Text = FightNumber
        Fight.FightIcon = FightIcon
        index += 1
    
    Battle.ListOfFights = ListOfFights
    Battle.FightsUnlocked = 1
    Battle.visible = False
    Battle.StageNum = 2
    Battle.IsSpecialStage = False
    Battle.EmotionLevelCap = 1
    app.StoryStages.append(Battle)
    
def CreateRatsStage():
    
    Battle = Group()
    ListOfFights = []
    
    Fight = Group()
    Fight.FightNumber = 0
    Fight.RewardCards = []
    Fight.RewardCharacters = []
    Fight.ListOfParts = []
    
    Part = Group()
    Part.ListOfFighters = []
    

    print("creating rat's cards")
    
    for Spam in range(2):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [2,1,0,2,1,0]
        AttributedPassives = []
        CreateCharacterCard("Rat1","green",SpeedDiceList,3,42,22,ResistanceList,Fight.RewardCharacters,"Rat",AttributedPassives)
    for Spam in range(2):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [0,2,1,0,2,1]
        AttributedPassives = []
        CreateCharacterCard("Rat2","green",SpeedDiceList,3,42,22,ResistanceList,Fight.RewardCharacters,"Rat",AttributedPassives)
    for Spam in range(2):
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [1,0,2,1,0,2]
        AttributedPassives = []
        CreateCharacterCard("Rat3","green",SpeedDiceList,3,42,22,ResistanceList,Fight.RewardCharacters,"Rat",AttributedPassives)
    
    DiceList = []
    CreateDie(1,2,"slash",DiceList,None,None,None,False)
    CreateCard("purple",1,"Organ Harvesting",DiceList,None,None)
    
    DiceList = []
    CreateDie(1,1,"slash",DiceList,None,None,None,False)
    CreateDie(1,2,"evade",DiceList,None,None,None,False)
    CreateCard("green",1,"Rat's Guide",DiceList,None,None)
    
    DiceList = []
    CreateDie(1,1,"blunt",DiceList,None,None,None,False)
    CreateDie(1,2,"block",DiceList,None,None,None,False)
    CreateCard("purple",1,"Sneaky Blow",DiceList,None,None)
    
    DiceList = []
    CreateDie(1,2,"pierce",DiceList,None,None,None,False)
    CreateCard("blue",1,"Backstreets Shove",DiceList,None,None)
    
    DiceList = []
    CreateDie(1,2,"blunt",DiceList,None,None,None,False)
    CreateCard("green",1,"Claw Off",DiceList,None,None)
    
    DiceList = []
    CreateDie(1,3,"evade",DiceList,None,None,None,False)
    CreateCard("blue",1,"Run Away",DiceList,None,None)
    
    
    print("creating rat's reward cards")
    
    DiceList = []
    CreateDie(3,6,"slash",DiceList,"NextBleed","On Hit","Enemy",False) #hit bleed
    CreateDie(3,5,"slash",DiceList,"NextBleed","On Hit","Enemy",False) #hit bleed
    CreateDie(1,4,"block",DiceList,None,None,None,False)
    CreateCard("purple",3,"Gut Harvesting",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,6,"block",DiceList,None,None,None,False)
    CreateDie(3,4,"blunt",DiceList,"NextBleed","On Hit","Enemy",False) #hit bleed
    CreateDie(1,7,"evade",DiceList,None,None,None,False)
    CreateCard("green",2,"Rat's Survival",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(3,7,"blunt",DiceList,"2NextBleed","Clash Win","Enemy",False) #clash win 2 bleed
    CreateDie(1,3,"block",DiceList,None,None,None,False)
    CreateCard("purple",2,"Dirty Strike",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,8,"pierce",DiceList,"NextBleed","On Hit","Enemy",False) #hit bleed
    CreateCard("blue",1,"Backstreets Dash",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,4,"slash",DiceList,"NextBleed","On Hit","Enemy",False) #hit bleed
    CreateDie(1,4,"blunt",DiceList,None,None,None,False)
    CreateCard("green",1,"Bite Off",DiceList,Fight.RewardCards,None)
    
    DiceList = []
    CreateDie(1,6,"evade",DiceList,None,None,None,False)
    CreateDie(1,6,"evade",DiceList,None,None,None,False)
    CreateDie(1,4,"blunt",DiceList,None,None,None,False)
    CreateCard("blue",1,"Skitter Away",DiceList,Fight.RewardCards,None)
    
    
    
    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Organ Harvesting","Organ Harvesting","Backstreets Shove","Claw Off","Run Away"])
    ResistanceList = [2,1,0,2,1,0]
    AttributedPassives = []
    Rat1 = CreateCharacter(170,105,2,False,SpeedDiceList,DeckList,1,10,5,ResistanceList,"Lenny",Part.ListOfFighters,"Rat",AttributedPassives,1)
    
    print("rat1 done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Rat's Guide","Rat's Guide","Backstreets Shove","Claw Off","Run Away"])
    ResistanceList = [0,2,1,0,2,1]
    AttributedPassives = []
    Rat2 = CreateCharacter(120,170,2,False,SpeedDiceList,DeckList,1,10,5,ResistanceList,"Mang-Chi",Part.ListOfFighters,"Rat",AttributedPassives,1)
    
    print("rat2 done")
    
    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Sneaky Blow","Sneaky Blow","Backstreets Shove","Claw Off","Run Away"])
    ResistanceList = [1,0,2,1,0,2]
    AttributedPassives = []
    Rat3 = CreateCharacter(70,235,2,False,SpeedDiceList,DeckList,1,10,5,ResistanceList,"Pete",Part.ListOfFighters,"Rat",AttributedPassives,1)
    
    print("rat3 done")
    Fight.ListOfParts.append(Part)
    ListOfFights.append(Fight)
    
    BattleContainer = Rect(-80,-20,100 + len(ListOfFights) * 50,80,fill = "black", border = "orange")
    Battle.add(BattleContainer)
    
    index = 0
    for Fight in ListOfFights:
        FightIcon = Rect(index * 55,0,40,40,fill = "black", border = "orange")
        FightIcon.rotateAngle = -45
        FightNumber = Label(str(index + 1),FightIcon.centerX,FightIcon.centerY,fill = "orange")
        
        #Battle.Icon = FightIcon
        Battle.add(FightIcon)
        Battle.add(FightNumber)
        FightIcon.Text = FightNumber
        Fight.FightIcon = FightIcon
        index += 1
    
    Battle.ListOfFights = ListOfFights
    Battle.FightsUnlocked = 1
    Battle.visible = False
    Battle.StageNum = 1
    Battle.IsSpecialStage = False
    Battle.EmotionLevelCap = 1
    app.StoryStages.append(Battle)
    
def CreateBloodBathStage():
    
    Battle = Group()
    ListOfFights = []
    
    Fight = Group()
    Fight.FightNumber = 0
    Fight.RewardCards = []
    Fight.RewardCharacters = []
    Fight.ListOfParts = []
    
    Part = Group()
    Part.ListOfFighters = []
    
    #creating bath's unique unobtainable cards
    
    DiceList = []
    CreateDie(1,6,"blunt",DiceList,"3NextParalysis","On Hit","Enemy",False)
    CreateCard("blue",1,"Depression",DiceList,None,None)
    
    DiceList = []
    CreateDie(1,3,"blunt",DiceList,None,None,None,False)
    CreateDie(1,3,"blunt",DiceList,None,None,None,False)
    CreateDie(1,3,"blunt",DiceList,None,None,None,False)
    CreateCard("blue",2,"Pale Hands",DiceList,None,None) #if all 3 hit stagger the op idk how we will though
    
    DiceList = []
    CreateDie(1,4,"block",DiceList,None,None,None,False)
    CreateDie(1,4,"block",DiceList,None,None,None,False)
    CreateDie(1,4,"block",DiceList,None,None,None,False)
    CreateCard("blue",0,"Sinking",DiceList,None,None)
    
    #creating the abnormailty pages #name,level,positive,single target,description,effect(s),list
    CreateAbnormailyPage("Blood",2,False,True,"Defensive dice gain 1-2 power; Recieve +3-5 stagger damage",["Create PassiveRolledDefensiveNum+1-2","Create PassiveRecievedAllStaggerNum+3-5"],Fight.RewardCards)
    CreateAbnormailyPage("Scars",1,True,True,"Take 2-5 less damage from slash attacks; 20% chance to negate attack",["Create PassiveRecievedSlashDamageNum-2-5","Scars"],Fight.RewardCards)
    CreateAbnormailyPage("Pale Hands",1,True,True,"After 3 hits on the same target deal 3-10 Stagger (resets when switching target)",["Pale Hands"],Fight.RewardCards)
    
    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Depression","Pale Hands","Sinking"])
    ResistanceList = [-1,0,1,-1,1,2]
    AttributedPassives = ["Create PassiveRecievedSlashDamageNum-2-5","Create PassiveRolledDefensiveNum+1-2","Pale Hands"]
    BloodBath = CreateCharacter(170,175,2,False,SpeedDiceList,DeckList,3,30,10,ResistanceList,"Bloody Cup",Part.ListOfFighters,"BloodBath",AttributedPassives,1)
    #has passives of 1-5 less damage from slash and 3 bind but +3 max block
    print("Bloodbath done")
    
    Fight.ListOfParts.append(Part)
    ListOfFights.append(Fight)
    
    BattleContainer = Rect(-80,-20,100 + len(ListOfFights) * 50,80,fill = "black", border = "white")
    Battle.add(BattleContainer)
    
    index = 0
    for Fight in ListOfFights:
        FightIcon = Rect(index * 55,0,40,40,fill = "black", border = "orange")
        FightIcon.rotateAngle = -45
        FightNumber = Label(str(index + 1),FightIcon.centerX,FightIcon.centerY,fill = "orange")
        
        #Battle.Icon = FightIcon
        Battle.add(FightIcon)
        Battle.add(FightNumber)
        FightIcon.Text = FightNumber
        Fight.FightIcon = FightIcon
        index += 1
    
    Battle.ListOfFights = ListOfFights
    Battle.FightsUnlocked = 1
    Battle.visible = False
    Battle.StageNum = 1
    Battle.IsSpecialStage = True
    Battle.EmotionLevelCap = 0 #special stages always emotion level cap 0
    app.Floors[0].EnlightenmentStages.append(Battle)

def CreateScorchedGirlStage():
    
    Battle = Group()
    ListOfFights = []
    
    Fight = Group()
    Fight.FightNumber = 0
    Fight.RewardCards = []
    Fight.RewardCharacters = []
    Fight.ListOfParts = []
    
    Part = Group()
    Part.ListOfFighters = []
    
    #creating scorched girl's and match's unique unobtainable cards
    
    DiceList = []
    CreateDie(1,8,"evade",DiceList,None,None,None,False)
    CreateCard("blue",0,"Broken Hope",DiceList,None,None)
    
    DiceList = []
    CreateDie(1,4,"evade",DiceList,None,None,None,False)
    CreateDie(3,3,"blunt",DiceList,"3Burn","On Hit","Enemy",False) #inflict 3 burn on hit
    CreateCard("blue",3,"Ember",DiceList,None,None) #on use lose 5 hp
    
    DiceList = []
    CreateDie(15,20,"blunt",DiceList,None,None,None,False)
    CreateCard("blue",4,"Fourth Match Flame",DiceList,None,None)
    
    #creating the abnormailty pages #name,level,positive,single target,description,effect(s),list
    CreateAbnormailyPage("Ashes",1,True,True,"On hit inflict 1-3 burn; On hit 40% chance to gain effect: On hit inflict 1 burn next scene (does not stack)",["Create PassiveDealtAllCreate Status1-3Burn","Ashes"],Fight.RewardCards)
    CreateAbnormailyPage("Footfalls",2,False,False,"On clash, if the librarian's hp is 20% or lower, deal 30% target's max hp (max 36) and inflict 1-3 burn, then die",["Footfalls"],Fight.RewardCards)
    CreateAbnormailyPage("Matchlight",1,False,True,"First 2 pages you use after this gain matchlight: on use gain ember; increase first die max by ember; at 4+ ember 25% chance to take X damage, X = ember",["Matchlight"],Fight.RewardCards)
    
    SpeedDiceList = []
    CreateSpeedDie(6,6,SpeedDiceList)
    DeckList = CreateDeckList(["Fourth Match Flame"])
    ResistanceList = [-2,-2,-2,2,2,2]
    AttributedPassives = ["Scorched Girl Mourn","Scorched Girl Clumsy"] #lose 50% max hp on match death and get staggered, on stagger lose all light
    ScorchedGirl = CreateCharacter(170,200,2,False,SpeedDiceList,DeckList,4,500,5,ResistanceList,"Scorched Girl",Part.ListOfFighters,"Scorched Girl",AttributedPassives,0)
    print("Scorched girl done")

    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Broken Hope","Ember"])
    ResistanceList = [0,0,1,0,0,2]
    AttributedPassives = []
    Match1 = CreateCharacter(100,130,2,False,SpeedDiceList,DeckList,3,25,15,ResistanceList,"Match1",Part.ListOfFighters,"Match",AttributedPassives,3)
    print("Match1 done")

    SpeedDiceList = []
    CreateSpeedDie(1,2,SpeedDiceList)
    DeckList = CreateDeckList(["Broken Hope","Ember"])
    ResistanceList = [0,0,1,0,0,2]
    AttributedPassives = []
    Match1 = CreateCharacter(100,300,2,False,SpeedDiceList,DeckList,3,25,15,ResistanceList,"Match2",Part.ListOfFighters,"Match",AttributedPassives,1)
    print("Match2 done")
    
    Fight.ListOfParts.append(Part)
    ListOfFights.append(Fight)
    
    BattleContainer = Rect(-80,-20,100 + len(ListOfFights) * 50,80,fill = "black", border = "white")
    Battle.add(BattleContainer)
    
    index = 0
    for Fight in ListOfFights:
        FightIcon = Rect(index * 55,0,40,40,fill = "black", border = "orange")
        FightIcon.rotateAngle = -45
        FightNumber = Label(str(index + 1),FightIcon.centerX,FightIcon.centerY,fill = "orange")
        
        #Battle.Icon = FightIcon
        Battle.add(FightIcon)
        Battle.add(FightNumber)
        FightIcon.Text = FightNumber
        Fight.FightIcon = FightIcon
        index += 1
    
    Battle.ListOfFights = ListOfFights
    Battle.FightsUnlocked = 1
    Battle.visible = False
    Battle.StageNum = 1
    Battle.IsSpecialStage = True
    Battle.EmotionLevelCap = 0 #special stages always emotion level cap 0
    app.Floors[1].EnlightenmentStages.append(Battle)


def GenerateTypeSprite(Type):
    if Type == "slash":
        Slash = Polygon(200,100,205,110,215,120,218,123,228,125,234,117,236,107,234,93,229,106,226,114,216,111,205,103,fill = "white")#, border = "orange")
        Slash.width = 6
        Slash.height = 6
        return Slash
    elif Type == "pierce":
        Pierce = Polygon(63,222,253,173,312,218,257,260,fill = "white")#,border = "orange")
        PierceRing = Polygon(248,172,238,155,226,148,218,150,213,160,208,175,203,198,202,229,207,263,217,274,231,280,240,276,248,261,239,258,235,263,
        224,258,217,234,215,208,216,190,218,175,226,169,239,175,fill = "white",border = "orange")
        PierceGroup = Group(Pierce,PierceRing)
        PierceGroup.width = 6
        PierceGroup.height = 6
        return PierceGroup
    elif Type == "blunt":
        Blunt = Polygon(352,255,55,279,95,243,107,165,142,220,135,63,171,111,183,22,255,182,281,122,320,225, fill="white")
        Blunt.width = 6
        Blunt.height = 6
        return Blunt
    elif Type == "block":
        BlockShield = Polygon(87,181,131,167,168,147,194,147,231,167,277,175,280,228,267,266,246,291,214,314,178,314,126,290,94,255,83,216,fill="white")
        ShieldLineV = Line(181,147,196,314,fill = "lightBlue")
        ShieldLineH = Line(87,235,280,228,fill = "lightBlue")
        BlockIcon = Group(BlockShield,ShieldLineV,ShieldLineH)
        BlockIcon.width = 6 *(3/4)
        BlockIcon.height = 7 *(3/4)
        return BlockIcon
    elif Type == "evade":
        Evade = Polygon(180,355,250,326,274,291,277,259,250,251,201,254,130,248,63,227,37,184,63,139,102,111,155,84,141,65,241,53,186,115,170,103,
        122,135,113,161,119,185,151,209,206,216,270,213,311,215,336,228,355,260,346,295,321,314,284,338,252,350,fill="white")
        Evade.width = 6
        Evade.height = 6
        return Evade
        
def CreateDie(min,max,type,diceList,Effect,Trigger,Target,Counter): 
    Die = Group()
    Die.type = type
    #Die.TypeSprite = None
    
    Die.TypeSprite = GenerateTypeSprite(Die.type)
    
    if Die.type == "slash" or Die.type == "pierce" or Die.type == "blunt":
        Die.color = "red"
    elif Die.type == "block" or Die.type == "evade":
        Die.color = "lightBlue"
        
    if Counter:
        Die.color = "yellow"
    
    
    Die.min = min
    Die.max = max
    Die.MaxModifier = 0
    Die.MinModifier = 0
    Die.Effect = Effect
    Die.Trigger = Trigger
    Die.Target = Target
    Die.Counter = Counter
    
    Die.IconCircle = Circle(0,0,4,fill=Die.color)
    
    Die.DamageRangeText = Label(str(Die.min) + "-" + str(Die.max),0,0,fill=Die.color)
    
    Description = None
    if Trigger != None:
        
        Description = ParseForDescription(Effect,Trigger,Target)
        #print(Description)
    
    Die.AddEffectDescription = None
        
    if Description != None and Description != "":
        
        PartitionedDescription = CardPartition(Description)
        Die.AddEffectDescription = PartitionedDescription
        pass
        
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
    #for each card name in a pre prepped list of strings finds that card and adds it's number from AllTotalCards into a new list to be copied out
    for Name in ListOfNames:
        index = 0
        found = False
        for Card in AllTotalCards:
            if not found:
                if(Name == Card.name):
                    #print("found card named: " + Card.name)
                    found = True
                    ListOfInts.append(index)
                    pass
                else:
                    index += 1
        pass
    if len(ListOfNames) != len(ListOfInts):
        print("There is a card Missing!!!!!!!!!!")
        print("Only " + str(len(ListOfInts)) + " were found and copied")
    return ListOfInts
    
def CreateLightSprite(Character):
    
    Light = Circle(Character.CharacterSprite.centerX,Character.CharacterSprite.centerY - 80, 10, opacity = 70)
    Character.add(Light)
    Character.LightSprites.append(Light)
    FixLightSpritePositions(Character)
    
def CreateEmotionBar(Character,List):

    EmotionReq = 3 + 2 * Character.EmotionLevel
    #print("emotion req is " + str(EmotionReq))
    FullEmotionBar = Group()
    StartX = 0
    
    for Count in range(EmotionReq):
        EmotionBar = Rect(StartX,0,30,20,fill = "grey",border = "black")
        StartX = EmotionBar.right
        FullEmotionBar.add(EmotionBar)
        List.append(EmotionBar)
    
    FullEmotionBar.width = 70
    FullEmotionBar.height = 15
    
    EmotionLevelText = Label(Character.EmotionLevel,FullEmotionBar.left - 10,10)
    FullEmotionBar.EmotionLevelText = EmotionLevelText
    FullEmotionBar.add(EmotionLevelText)
    List.append(EmotionLevelText)
    
    return FullEmotionBar
    
def UpdateEmotionBar(Character):
    index = 0
    Character.EmotionBar.centerX = Character.CharacterSprite.centerX
    Character.EmotionBar.centerY = Character.CharacterSprite.centerY - 100
    #print("emotion list length = " + str(len(Character.EmotionBarList)))
    for Count in range(len(Character.EmotionCoins)):
        #print("index is " + str(index))
        if Character.EmotionCoins[index] == True: #checking if positive
            Character.EmotionBarList[index].fill = "green"
        else:
            Character.EmotionBarList[index].fill = "red"
        index += 1
def ResetEmotionBar(Character):
    Character.EmotionBar.visible = False
    Character.remove(Character.EmotionBar)
    Character.EmotionBarList.clear()
    Character.EmotionBar = CreateEmotionBar(Character,Character.EmotionBarList)
    Character.add(Character.EmotionBar)
    UpdateEmotionBar(Character)
#----------------------------------------------------------------------------------------------
    
def CreateCard(color,cost,name,dice,AddToList,OnUseEffect):
    FullCard = Group()
    #seperates the lists because I got destroyed by that a while back
    NewDiceList = list(dice)
    Image = Rect(0,0,app.CardWidth/2,120, border = color, borderWidth = 4)
    FullCard.Frame = Image
    FullCard.color = color
    CostCircle = Circle(10,10,10,fill = color)
    CostNumber = Label(cost,10,10)
    FullCard.cost = cost
    NameBox = Rect(0,18,app.CardWidth/2,12, fill=color)
    FullCard.CardBox = NameBox
    #NameBox.rotateAngle = -10
    #print(len(name))
    FullCard.fontsize = 15 - int(len(name)/app.FontSizeModifier)
    NameText = Label(name,NameBox.centerX,NameBox.centerY, size = FullCard.fontsize)
    #NameText.rotateAngle = -10
    FullCard.name = name
    FullCard.Used = False
    FullCard.add(Image,CostCircle,CostNumber,NameBox,NameText)
    
    FullCard.OnUseEffect = OnUseEffect
    #---------------------------------------------------------
    #creates the right dice holding side of the card
    StartY = app.YStart
    
    FullCard.OnUseText = []
    #create on use text 
    if OnUseEffect != None:
        if type(FullCard.OnUseEffect) == list:
            Description = ""
            for Effect in OnUseEffect:
                
                Description += ParseForDescription(Effect,"On Use","Self")
                Description += ": "
            
            PartitionedText = CardPartition(Description)
            FullCard.OnUseText = PartitionedText
            for line in PartitionedText:
                line.left = app.Xdisplace - 14
                line.centerY = StartY
                FullCard.add(line)
                StartY = line.bottom + 4
            
        else:
            Description = ParseForDescription(OnUseEffect,"On Use","Self")
            PartitionedText = CardPartition(Description)
            FullCard.OnUseText = PartitionedText
            for line in PartitionedText:
                line.left = app.Xdisplace - 14
                line.centerY = StartY
                FullCard.add(line)
                StartY = line.bottom + 4
        

    for Die in NewDiceList:
        Die.IconCircle.centerX = app.Xdisplace
        Die.IconCircle.centerY = StartY
        FullCard.add(Die.IconCircle)
        
        Die.TypeSprite.centerX = app.Xdisplace
        Die.TypeSprite.centerY = StartY
        FullCard.add(Die.TypeSprite)
        
        Die.DamageRangeText.centerX = app.Xdisplace+15
        Die.DamageRangeText.centerY = StartY
        if Die.AddEffectDescription != None:
            StartY += 1
            for line in Die.AddEffectDescription:
                StartY += 7
                line.left = app.Xdisplace - 14
                line.centerY = StartY
                FullCard.add(line)
            StartY -= 6
        FullCard.add(Die.DamageRangeText)
        StartY += 14
        pass

    FullCard.centerX = 200
    FullCard.UsedDiceList = []
    FullCard.DiceList = NewDiceList
    FullCard.Clicked = False
    FullCard.MousedOver = False
    
    
    
    #FullCard.IsDisplayCard = True
    if AddToList != None:
        AddToList.append(FullCard)
    AllTotalCards.append(FullCard)
    FullCard.visible = False
    

def CopyCard(Card,NewList):
    #creates a copy of the specified card based on it's values, and adds it to the new list
    FullCard = Group()
    Image = Rect(0,0,app.CardWidth/2,120, border = Card.color, borderWidth = 4)
    FullCard.Frame = Image
    FullCard.color = Card.color
    CostCircle = Circle(10,10,10,fill = Card.color)
    CostNumber = Label(Card.cost,10,10)
    FullCard.cost = Card.cost
    NameBox = Rect(0,18,app.CardWidth/2,12, fill= Card.color)
    FullCard.CardBox = NameBox
    NameText = Label(Card.name,NameBox.centerX,NameBox.centerY, size = Card.fontsize)
    FullCard.name = Card.name
    FullCard.Used = False
    FullCard.add(Image,CostCircle,CostNumber,NameBox,NameText)
    
    FullCard.OnUseEffect = Card.OnUseEffect
    #---------------------------------------------------------------------
    StartY = app.YStart
    
    #create on use text 
    FullCard.OnUseText = []
    if FullCard.OnUseEffect != None:
        if type(FullCard.OnUseEffect) == list:
            Description = ""
            for Effect in FullCard.OnUseEffect:
                
                Description += ParseForDescription(Effect,"On Use","Self")
                Description += ": "
            
            PartitionedText = CardPartition(Description)
            FullCard.OnUseText = PartitionedText
            for line in PartitionedText:
                line.left = app.Xdisplace - 14
                line.centerY = StartY
                FullCard.add(line)
                StartY = line.bottom + 4
            
        else:
            Description = ParseForDescription(FullCard.OnUseEffect,"On Use","Self")
            PartitionedText = CardPartition(Description)
            FullCard.OnUseText = PartitionedText
            for line in PartitionedText:
                line.left = app.Xdisplace - 14
                line.centerY = StartY
                FullCard.add(line)
                StartY = line.bottom + 4
    
    #switched from setting new list to old list bc type icons failing
    NewDiceList = []
    for CardDie in Card.DiceList:
        CreateDie(CardDie.min,CardDie.max,CardDie.type,NewDiceList,CardDie.Effect,CardDie.Trigger,CardDie.Target,CardDie.Counter)
    

    for Die in NewDiceList:
        Die.IconCircle.centerX = app.Xdisplace
        Die.IconCircle.centerY = StartY
        FullCard.add(Die.IconCircle)
        
        Die.TypeSprite.centerX = app.Xdisplace
        Die.TypeSprite.centerY = StartY
        FullCard.add(Die.TypeSprite)
        
        Die.DamageRangeText.centerX = app.Xdisplace+15
        Die.DamageRangeText.centerY = StartY
        if Die.AddEffectDescription != None:
            StartY += 1
            for line in Die.AddEffectDescription:
                StartY += 7
                line.left = app.Xdisplace - 14
                line.centerY = StartY
                FullCard.add(line)
            StartY -= 6
        FullCard.add(Die.DamageRangeText)
        StartY += 14
    FullCard.centerX = 200
    FullCard.DiceList = NewDiceList
    FullCard.UsedDiceList = []
    FullCard.Clicked = False
    FullCard.MousedOver = False
    
    
    
    if NewList != None:
        NewList.append(FullCard)
    AllTotalCards.append(FullCard)
    FullCard.visible = False
    #FullCard.IsDisplayCard = False

def CreateCharacter(x,y,facing,ControlledByPlayer,SpeedDiceList,Decklist,MaxLight,MaxHealth,MaxStagger,ResistanceList, name, ListToAddTo,SpriteName,AttributedPassives,StartingLight):
    FullCharacter = Group()
    FullCharacter.StartX = x
    FullCharacter.StartY = y 
    FullCharacter.ControlledByPlayer = ControlledByPlayer
    
    FullCharacter.MaxLight = MaxLight
    FullCharacter.MaxHandSize = 8
    FullCharacter.Light = MaxLight
    FullCharacter.StartingLight = StartingLight
    
    FullCharacter.MaxHealth = MaxHealth
    FullCharacter.Health = FullCharacter.MaxHealth
    
    FullCharacter.MaxStagger = MaxStagger
    FullCharacter.Stagger = FullCharacter.MaxStagger
    FullCharacter.Staggered = False
    FullCharacter.ClearStaggered = False 
    
    FullCharacter.SpeedDice = []
    FullCharacter.LightSprites = []
    FullCharacter.Library = []
    FullCharacter.Hand = []
    
    FullCharacter.AttributedPassives = AttributedPassives
    
    FullCharacter.EmotionCoins = []
    FullCharacter.BankedEmotionCoins = []
    FullCharacter.EmotionLevel = 0
    
    FullCharacter.EmotionBarList = []
    FullCharacter.EmotionBar = CreateEmotionBar(FullCharacter,FullCharacter.EmotionBarList) #creates the bar and assigns to list
    FullCharacter.add(FullCharacter.EmotionBar)
    FullCharacter.EmotionBar.visible = False
    
    FullCharacter.HandOnDisplay = False
    
    FullCharacter.Graveyard = []
    FullCharacter.UnusedDice = []
    NewSpeedDiceList = list(SpeedDiceList)
    
    for Die in NewSpeedDiceList:
        Die.ConnectedCharacter = FullCharacter
        #print("assigned a character to a die")
        
    CharacterSprite = AssignSymbol(SpriteName)
    CharacterSprite.width = 60
    CharacterSprite.height = 40
    FullCharacter.CharacterSprite = CharacterSprite

    FullCharacter.add(CharacterSprite)
    FullCharacter.FacingLeft = ControlledByPlayer

    HealthBar = Rect(0,0,40,20,fill = "red")
    HealthBar.right = FullCharacter.CharacterSprite.centerX
    HealthBar.centerY = FullCharacter.CharacterSprite.centerY + 40
    FullCharacter.HealthBar = HealthBar
    FullCharacter.add(HealthBar)
    
    HealthBarText = Label(str(FullCharacter.Health),0,0)
    HealthBarText.centerY = HealthBar.centerY
    HealthBarText.centerX = HealthBar.centerX
    FullCharacter.HealthBarText = HealthBarText
    FullCharacter.add(HealthBarText)
    
    StaggerBar = Rect(0,0,40,20,fill = "yellow")
    StaggerBar.left = FullCharacter.CharacterSprite.centerX
    StaggerBar.centerY = FullCharacter.CharacterSprite.centerY + 40
    FullCharacter.StaggerBar = StaggerBar
    FullCharacter.add(StaggerBar)
    
    StaggerBarText = Label(str(FullCharacter.Stagger),0,0)
    StaggerBarText.centerY = StaggerBar.centerY
    StaggerBarText.centerX = StaggerBar.centerX
    FullCharacter.StaggerBarText = StaggerBarText
    FullCharacter.add(StaggerBarText)
    
    for LightMote in range(MaxLight):
        CreateLightSprite(FullCharacter)
    
    CreateSpeedDice(NewSpeedDiceList,FullCharacter)

    for CardNum in Decklist:
        #creates copies of all specified cards and adds them to the deck
        CopyCard(AllTotalCards[CardNum],FullCharacter.Library)
        
    AdditionalInfoBoard = Group()
    AdditionalInfoBoard.TextList = []
        
    InfoBoardBackGround = Rect(-10,-10,90,60,fill="grey")
    AdditionalInfoBoard.add(InfoBoardBackGround)
    FullCharacter.ResistanceList = ResistanceList
    GenerateResistanceBoard(ResistanceList,AdditionalInfoBoard)
        
    AdditionalInfoBoard.top = 0
    if ControlledByPlayer:
        AdditionalInfoBoard.centerX = 350
    else:
        AdditionalInfoBoard.centerX = 50
        
    
    FullCharacter.AdditionalInfoBoard = AdditionalInfoBoard
    AdditionalInfoBoard.visible = False
        
    FullCharacter.name = name
    if ControlledByPlayer:
        NameBoard = Rect(0,0,80,30, fill = "grey", border = "darkgrey")
        NameBoard.centerX = FullCharacter.CharacterSprite.centerX
        NameBoard.centerY = FullCharacter.CharacterSprite.centerY - 50
        NameText = Label(name, 0, 0)
        NameText.centerX = NameBoard.centerX
        NameText.centerY = NameBoard.centerY
        NameBoard.Text = NameText
        FullCharacter.NameBoard = NameBoard
        FullCharacter.add(NameBoard,NameText)
    
    FullCharacter.StatusEffects = []
    FullCharacter.NextTurnStatusEffects = []
    
    FullCharacter.AttributedCards = []
    FullCharacter.OverrideCard = None
    
    FullCharacter.Clicked = False
    FullCharacter.MousedOver = False
    FullCharacter.visible = False

    #if ControlledByPlayer:
        #PlayerCharacters.append(FullCharacter)

    AllCharacters.append(FullCharacter)
    if ListToAddTo != None:
        ListToAddTo.append(FullCharacter)
        

def CreateSpeedDice(NewSpeedDiceList,FullCharacter):
    #print("is this running?")
    DiceDisp = 40
    
    if len(NewSpeedDiceList) > 1:
        StartX = FullCharacter.CharacterSprite.centerX - ((DiceDisp * len(NewSpeedDiceList)) / 3) 
    else:
        StartX = FullCharacter.CharacterSprite.centerX
    #creates boxes and text for all speed dice
    
    for Die in NewSpeedDiceList:
        SpeedDiceSlot = Rect(StartX-20,FullCharacter.CharacterSprite.centerY-60,30,30,borderWidth = 4, border = "blue")
        StartX += DiceDisp
        SpeedDiceSlot.fill = "red"
        SpeedDiceText = Label(str(Die.min) + "-" + str(Die.max),0,0)
        SpeedDiceText.centerX = SpeedDiceSlot.centerX
        SpeedDiceText.centerY = SpeedDiceSlot.centerY
        FullCharacter.add(SpeedDiceSlot, SpeedDiceText)
        Die.ConnectedSprite = SpeedDiceSlot
        Die.ConnectedText = SpeedDiceText
            
        Die.HeldPage = None
        Die.TargetDie = None
        Die.IntendedTargetDie = None
        Die.TargettedBy = []
        #FullCharacter.SpeedDiceText.append(SpeedDiceText)
        FullCharacter.SpeedDice.append(Die)
    

def CreateCharacterCard(Name,color,SpeedDiceList,MaxLight,MaxHealth,MaxStagger,ResistanceList,List,SpriteName,AttributedPassives):
    FullCharacterCard = Group()
    FullCharacterCard.AttributedCards = []
    FullCharacterCard.MaxLight = MaxLight
    FullCharacterCard.MaxHealth = MaxHealth
    FullCharacterCard.MaxStagger = MaxStagger
    FullCharacterCard.ResistanceList = ResistanceList
    FullCharacterCard.SortNumber = 0
    FullCharacterCard.Library = []
    
    FullCharacterCard.AttributedPassives = AttributedPassives

    FullCharacterCard.SpeedDice = list(SpeedDiceList)
    
    FullCharacterCard.Background = Rect(0,0,80,120,fill = "lightgrey",border = color)
    DispY = 0
    
    FullCharacterCard.Sprite = AssignSymbol(SpriteName)
    FullCharacterCard.Sprite.width = 60
    FullCharacterCard.Sprite.height = 40
    
    FullCharacterCard.Name = Label(Name,FullCharacterCard.Background.centerX,10 + DispY,fill = "black")
    DispY += 20
    FullCharacterCard.LightGroup = Group()
    FullCharacterCard.LightGroup.Icon = Circle(15,5 + DispY,4,fill = "yellow")
    FullCharacterCard.LightGroup.Text = Label(MaxLight,35,5 + DispY,fill = "black")
    DispY += 20
    FullCharacterCard.HealthText = Label(MaxHealth,15,DispY,fill = "red")
    FullCharacterCard.StaggerText = Label(MaxStagger,45,DispY,fill = "yellow")
    DispY += 10
    FullCharacterCard.DiceGroup = Group()
    FullCharacterCard.DiceGroup.Icon = Rect(4,DispY,10,10,fill = "blue")
    FullCharacterCard.DiceGroup.Text = Label(str(FullCharacterCard.SpeedDice[0].min) + "-" + str(FullCharacterCard.SpeedDice[0].max) + " X " + str(len(FullCharacterCard.SpeedDice)),40,DispY + 5,fill = "black")
    
    DispY += 17
    
    FullCharacterCard.AdditionalInfoBoard = Group()
    FullCharacterCard.AdditionalInfoBoard.TextList = []
    GenerateResistanceBoard(ResistanceList,FullCharacterCard.AdditionalInfoBoard)
    FullCharacterCard.AdditionalInfoBoard.centerY += DispY
    FullCharacterCard.AdditionalInfoBoard.centerX += 5

    FullCharacterCard.add(FullCharacterCard.Background)
    FullCharacterCard.add(FullCharacterCard.Name)
    FullCharacterCard.add(FullCharacterCard.LightGroup.Icon)
    FullCharacterCard.add(FullCharacterCard.LightGroup.Text)
    FullCharacterCard.add(FullCharacterCard.HealthText)
    FullCharacterCard.add(FullCharacterCard.StaggerText)
    FullCharacterCard.add(FullCharacterCard.DiceGroup.Icon)
    FullCharacterCard.add(FullCharacterCard.DiceGroup.Text)
    FullCharacterCard.add(FullCharacterCard.AdditionalInfoBoard)
    FullCharacterCard.visible = False
    if List != None:
        List.append(FullCharacterCard)
        
        
def AssignOverrideCard(Character,OverrideCard):
    
    print("Assigned override")
    app.ActiveCharacterCards.append(OverrideCard)
    app.UnusedCharacterCards.remove(OverrideCard)
    OverrideCard.visible = True
    OverrideCard.centerX = 50
    OverrideCard.centerY = 120
    
    #needs to happen first because this is the only way too see both
    if OverrideCard.Sprite != None:
        Character.CharacterSprite.visible = False
        Character.remove(Character.CharacterSprite)
        Character.CharacterSprite = OverrideCard.Sprite
        Character.CharacterSprite.visible = True
        Character.add(OverrideCard.Sprite)
    
    if Character.OverrideCard != None:
        RemoveOverrideCard(Character)
    Character.OverrideCard = OverrideCard
    
    
    for Die in OverrideCard.SpeedDice:
        Die.ConnectedCharacter = Character
    Character.MaxHealth = OverrideCard.MaxHealth
    Character.Health = Character.MaxHealth
    Character.MaxStagger = OverrideCard.MaxStagger
    Character.Stagger = Character.MaxStagger
    Character.MaxLight = OverrideCard.MaxLight
    Character.Light = Character.MaxLight
    Character.ResistanceList = OverrideCard.ResistanceList
    Character.AttributedPassives = OverrideCard.AttributedPassives
    #Character.SpeedDice = OverrideCard.SpeedDice
    CreateSpeedDice(OverrideCard.SpeedDice,Character)
    for Die in Character.SpeedDice:
        Die.ConnectedCharacter = Character
    
    UpdateBars(Character)
    RefreshResistances(Character)
    if app.Startup == False:
        #DisplayCharacterEdit(Character)
        FixUpCharacter(Character)
    
def RemoveOverrideCard(Character):
    print("Removed override")
    for Die in Character.OverrideCard.SpeedDice:
        Die.ConnectedCharacter = None
    app.ActiveCharacterCards.remove(Character.OverrideCard)
    app.UnusedCharacterCards.append(Character.OverrideCard)
    Character.OverrideCard.visible = True
    Character.OverrideCard = None
    for Die in Character.SpeedDice:
        Die.ConnectedCharacter = None
        Die.visible = False
    Character.SpeedDice.clear()


    
def GenerateResistanceBoard(ResistanceList,AdditionalInfoBoard):
    index = 0
    Xdisplace = 0
    Ydisplace = 20
    ResColor = "Red"
    for ResValue in ResistanceList:
        Sprite = None
        if (index % 3) == 0:
            Sprite = GenerateTypeSprite("slash")
        elif (index % 3) == 1:
            Sprite = GenerateTypeSprite("pierce")
        elif (index % 3) == 2:
            Sprite = GenerateTypeSprite("blunt")
        else:
            print("MASSIVE ERROR failed to find type sprite resistance")
        if index > 2:
            Xdisplace = 40
            ResColor = "yellow"
        Sprite.centerX = Xdisplace
        Sprite.centerY = Ydisplace * (index % 3)
        Sprite.fill = ResColor
        AdditionalInfoBoard.add(Sprite)
        ResTextVal = None
        if ResValue == 2:
            ResTextVal = "Fatal"
        elif ResValue == 1:
            ResTextVal = "Weak"
        elif ResValue == 0:
            ResTextVal = "Normal"
        elif ResValue == -1:
            ResTextVal = "Endured"
        elif ResValue == -2:
            ResTextVal = "Ineffective"
        elif ResValue == -3:
            ResTextVal = "Immune"
        else:
            print("MASSIVE ERROR failed to find type sprite resistance 2")
        ResText = Label(ResTextVal,Xdisplace + 20, Ydisplace * (index % 3),size = 8)
        AdditionalInfoBoard.add(ResText)
        AdditionalInfoBoard.TextList.append(ResText)
        index += 1
    
    
            
def Startup():
    #----------------------------------------------------------------------------------------------
    #create all of the cards base        
    CreateCards()
    #----------------------------------------------------------------------------------------------
    #create characters
    CreateCharacters()
    
    
    for Count in range(7):
        Floor = Group()
        Floor.CharactersUnlocked = 1
        Floor.EnlightenmentStages = []
        Floor.EnlightenmentStageSymbols = []
        Floor.EnlightenmentUnlocked = 0
        if app.Debug == True:
            Floor.EnlightenmentUnlocked = 5
        Floor.CurrentEmotionLevelCap = 1
        Floor.Unlocked = False
        Floor.EmotionPayoffs = [[],[],[]] #the different levels 1-3 have containers
        app.Floors.append(Floor)
        
    app.Floors[0].Unlocked = True
    if app.Debug == True:
        app.Floors[1].Unlocked = True
    #app.Floors[2].Unlocked = True
    app.CurrentFloor = app.Floors[0]
    
    #------------------------------------------------------------------------------
    #Hide cards
    
    app.Startup = False
    
def HideAllSetupCards():
    #this is only called at setup lol
    for Card in AllTotalCards:
        Card.visible = False
        pass
def CreateCards():
    DiceList = []
    CreateDie(2,3,"pierce",DiceList,None,None,None,False)
    CreateDie(3,4,"blunt",DiceList,None,None,None,False)
    CreateDie(1,6,"slash",DiceList,None,None,None,False)
    CreateDie(2,4,"block",DiceList,None,None,None,True)
    CreateCard("green",1,"template strike",DiceList,None,None)
    
    DiceList = []
    CreateDie(1,4,"evade",DiceList,None,None,None,False)
    CreateCard("green",0,"Evade",DiceList,AllDisplayCards,None)
    
    DiceList = []
    CreateDie(2,3,"pierce",DiceList,None,None,None,False)
    CreateDie(1,4,"blunt",DiceList,None,None,None,False)
    CreateCard("green",1,"Light Attack",DiceList,AllDisplayCards,None)
    
    DiceList = []
    CreateDie(1,5,"evade",DiceList,None,None,None,False)
    CreateDie(2,3,"block",DiceList,None,None,None,False)
    CreateDie(1,2,"slash",DiceList,None,None,None,False)
    CreateCard("green",1,"Light Defense",DiceList,AllDisplayCards,None)
    
    DiceList = []
    CreateDie(3,6,"pierce",DiceList,None,None,None,False)
    CreateDie(2,6,"block",DiceList,None,None,None,False)
    CreateCard("green",2,"Charge and Cover",DiceList,AllDisplayCards,None)
    
    DiceList = []
    CreateDie(3,5,"slash",DiceList,None,None,None,False)
    CreateDie(3,5,"slash",DiceList,None,None,None,False)
    CreateDie(1,3,"pierce",DiceList,None,None,None,False)
    CreateCard("green",3,"Focused Strikes",DiceList,AllDisplayCards,None)
    pass

def CreateCharacters():
    
    index = 1
    for count in range(5):
        SpeedDiceList = []
        #CreateSpeedDie(1,4,SpeedDiceList)
        DeckList = CreateDeckList([
            "Charge and Cover","Charge and Cover",
        "Charge and Cover","Light Attack","Light Attack",
        "Light Attack","Light Defense","Light Defense","Focused Strikes"])
        ResistanceList = [2,1,0,2,1,0]
        AttributedPassives = []
        CreateCharacter(290,75 + index * 100,1,True,SpeedDiceList,DeckList,3,30,15,ResistanceList,"Roland" + str(index),PlayerCharacters,"Peasant",AttributedPassives,None)
        index += 1
    CharacterCardsLen = len(app.UnusedCharacterCards)
    for Character in PlayerCharacters:
        SpeedDiceList = []
        CreateSpeedDie(1,4,SpeedDiceList)
        ResistanceList = [2,1,0,2,1,0]
        AttributedPassives = []
        CreateCharacterCard("Peasant","green",SpeedDiceList,3,30,15,ResistanceList,app.UnusedCharacterCards,"Peasant",AttributedPassives)
        AssignOverrideCard(Character,app.UnusedCharacterCards[CharacterCardsLen]) #we dont need -1 bc we want the new one
        Character.OverrideCard.visible = False
    

#------------------------------------------------------------------------------------------------------
def MoveToPageSelect():
    print("Moving to select")
    for Character in AllFightingCharacters:
        
        if Character.Staggered != True and app.RoundNum != 0:
            DrawCard(Character)
            
        for Die in Character.SpeedDice:
            Die.speed = 0
            
        RollSpeedDice(Character)
        
        #print(Character.ControlledByPlayer)
        if not Character.ControlledByPlayer and not Character.Staggered:
            EscroList = []
            index = 9
            for Count in range(10):
                if len(Character.Hand) > 0:
                    for Card in Character.Hand:
                        if Card.cost >= index: #grabs all cards of the cost with slight failure and skipping for randomness but could be fixed with removal list
                            EscroList.append(Card)
                            Character.Hand.remove(Card)
                    index -= 1
            for Card in EscroList:
                Character.Hand.append(Card)
            EscroList.clear()
            #order the hand so we have an expensive card use first but also a little gamba ai
            #ShuffleList(Character.Hand)
            CharacterRandomTarget(Character)
        
def DrawCard(Character):
    if len(Character.Library) > 0 and len(Character.Hand) < Character.MaxHandSize:
        chance = random.randint(0,len(Character.Library) - 1) 
        EscroCard = Character.Library[chance]
        FixupCard(EscroCard)
        Character.Hand.append(EscroCard)
        Character.Library.remove(EscroCard)
        
    elif len(Character.Hand) < Character.MaxHandSize and len(Character.Graveyard) > 0:
        
        GraveyardToLibrary(Character)
        
        chance = random.randint(0,len(Character.Library) - 1) 
        EscroCard = Character.Library[chance]
        FixupCard(EscroCard)
        Character.Hand.append(EscroCard)
        Character.Library.remove(EscroCard)
        
def GraveyardToLibrary(Character):
    ShuffleList(Character.Graveyard)
    for Card in Character.Graveyard:
        Character.Library.append(Card)
    Character.Graveyard.clear()
    
def ShuffleList(List):
    EscroList = []
    while len(List) > 0:
        chance = random.randint(0,len(List) - 1)
        EscroList.append(List[chance])
        List.remove(List[chance])
    while len(EscroList) > 0:
        List.append(EscroList[0])
        EscroList.remove(EscroList[0])
        
def GainLight(Character):
    
    if Character.MaxLight > len(Character.LightSprites): 
        for Gap in range(Character.MaxLight - len(Character.LightSprites)):
            CreateLightSprite(Character)
    if Character.Light < Character.MaxLight:
        Character.Light += 1
        
    FixLightSpritePositions(Character)
    
def RemoveLight(Character):
    
    if len(Character.LightSprites) > 0:
        print("removing light from " + Character.name)
        Character.MaxLight -= 1
        Character.EmotionLevel -= 1
        Character.LightSprites[0].visible = False
        Character.remove(Character.LightSprites[0])
        Character.LightSprites.remove(Character.LightSprites[0])
        
        
def RollSpeedDice(Character):
    
    Modifier = 0
    for Effect in Character.StatusEffects:
        if Effect.name == "Haste":
            Modifier += Effect.Count
        elif Effect.name == "Bind":
            Modifier -= Effect.Count
    
    index = 0
        
    for Die in Character.SpeedDice:
        DieValue = random.randint(Die.min, Die.max) + Modifier
        
        Die.ConnectedText.value = DieValue
        Die.speed = DieValue
        FoundSelf = False
        for OtherDie in Character.SpeedDice: #only runs once so is susectible to failing to fully organize with 3+ dice
            if Die == OtherDie:
                FoundSelf = True
            if OtherDie.speed < Die.speed and not FoundSelf:
                print("swapping " + str(Die.speed) + " and " + str(OtherDie.speed))
                HeldVal = OtherDie.speed
                #swap
                OtherDie.speed = Die.speed
                Die.speed = HeldVal
                #update text
                OtherDie.ConnectedText.value = OtherDie.speed
                Die.ConnectedText.value = Die.speed
                FoundSelf = True
                
            
                
        #Character.SpeedDice[index].speed = DieValue
        index += 1
        pass
        
def CharacterRandomTarget(Character):
    #print("start targetting")
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
    #print("Target with page")
    if Card.cost <= Character.Light or (SpeedDie.HeldPage != None and Card.cost <= Character.Light + SpeedDie.HeldPage.cost):
        Character.Light -= Card.cost
        if SpeedDie.HeldPage != None:
            UntargetSpeedDie(SpeedDie)
        SpeedDie.HeldPage = Card
        Character.Hand.remove(Card)
        TargetSpeedDice = None
        FixLightSpritePositions(Character)
        if Character.ControlledByPlayer:
            #chance = random.randint(0,len(EnemySpeedDice) - 1)
            #TargetSpeedDice = EnemySpeedDice[chance]
            #print("controlled by player targetting?")
            if TargetDie != None:
                TargetSpeedDice = TargetDie
            else:
                if len(EnemySpeedDice) - 1 >= 0: #makes sure there are enemies
                    chance = random.randint(0,len(EnemySpeedDice) - 1)
                    TargetDie = EnemySpeedDice[chance]
                    TargetSpeedDice = TargetDie
                else:
                    print("failed to find enemy for random targetting")
                    if len(PlayerSpeedDice) == 0:
                        FightEnd(False)
                    elif len(EnemySpeedDice) == 0:
                        FightEnd(True)
                    print("attempting return escape")
                    return "failed"
            if TargetDie != None:
                if TargetDie.TargetDie == SpeedDie:
                    Color = "yellow"
                    print("response clash")
                    RemoveTargetLine(SpeedDie)
                    TargetDie.IntendedTargetDie = TargetDie.TargetDie
                    TargetDie.TargetDie = SpeedDie
                    SwitchClashColors(TargetDie, "yellow")
                else:
                    
                    if TargetDie.HeldPage == None or TargetDie.speed >= SpeedDie.speed:
                        Color = "blue"
                        RemoveTargetLine(SpeedDie)
                    else:
                        print("outspeeds force clash")
                        #print(str(TargetDie.speed) + "vs" + str(SpeedDie.speed))
                        Color = "yellow"
                        RemoveTargetLine(SpeedDie)
                        if TargetDie.IntendedTargetDie != None:
                            SwitchClashColors(TargetDie.TargetDie, "blue")
                            TargetDie.TargetDie = SpeedDie
                            SwitchClashColors(TargetDie, "yellow")
                        else:
                            TargetDie.IntendedTargetDie = TargetDie.TargetDie
                            TargetDie.TargetDie = SpeedDie
                            SwitchClashColors(TargetDie, "yellow")
            
        else:
            chance = random.randint(0,len(PlayerSpeedDice) - 1)
            TargetSpeedDice = PlayerSpeedDice[chance]
            Color = "red"
    
        SpeedDie.TargetDie = TargetSpeedDice
        #TargetSpeedDice.TargettedBy.append(SpeedDie)
        SpeedDieSprite = SpeedDie.ConnectedSprite
        #visuals
        TargetSpeedDiceSprite = TargetSpeedDice.ConnectedSprite
        #print("moving card to speed die")
        Card.centerX = SpeedDieSprite.centerX
        Card.centerY = SpeedDieSprite.centerY
        if SpeedDie.ClashLine != None:
            RemoveClashLine(SpeedDie)
        TargetLine = Line(SpeedDieSprite.centerX,SpeedDieSprite.centerY,TargetSpeedDiceSprite.centerX,TargetSpeedDiceSprite.centerY, fill = Color)
        TargetLine.opacity = 30
        SpeedDie.ClashLine = TargetLine
        
def UntargetSpeedDie(SpeedDie):
    if SpeedDie.HeldPage != None:
        if SpeedDie.HeldPage.Used == True: #the page has started to be used so no refund
            RestorePage(SpeedDie.HeldPage)
        else:
            SpeedDie.ConnectedCharacter.Light += SpeedDie.HeldPage.cost
            FixLightSpritePositions(SpeedDie.ConnectedCharacter)

        #print("Untarget")
        if SpeedDie.TargetDie != None:
            EnemyDie = SpeedDie.TargetDie
            if EnemyDie.TargetDie == SpeedDie and SpeedDie.TargetDie == EnemyDie:
                if EnemyDie.IntendedTargetDie != None:
                    EnemyDie.TargetDie = EnemyDie.IntendedTargetDie
                    EnemyDie.IntendedTargetDie = None
                    SwitchClashColors(EnemyDie, "Red")
                else:
                    SwitchClashColors(EnemyDie, "Red")
                    pass
        #EnemyDie.TargettedBy.remove(SpeedDie)
        SpeedDie.TargetDie = None
        SpeedDie.ConnectedCharacter.Hand.append(SpeedDie.HeldPage)
        SpeedDie.HeldPage = None
        RemoveTargetLine(SpeedDie)
        RemoveClashLine(SpeedDie)
        
    
def SwitchClashColors(Die, Color):
    RemoveClashLine(Die)
    if not Die.TargetDie == None:
        SpeedDieSprite = Die.ConnectedSprite
        TargetSpeedDiceSprite = Die.TargetDie.ConnectedSprite
        TargetLine = Line(SpeedDieSprite.centerX,SpeedDieSprite.centerY,TargetSpeedDiceSprite.centerX,TargetSpeedDiceSprite.centerY, fill = Color)
        TargetLine.opacity = 30
        Die.ClashLine = TargetLine
    
def RemoveTargetLine(Die):
    #print("tries to remove line")
    if not Die.TargettingLine == None:
        Die.TargettingLine.visible = False
        Die.TargettingLine = None
        
def RemoveClashLine(Die):
    #print("tries to remove clash line")
    if not Die.ClashLine == None:
        Die.ClashLine.visible = False
        Die.ClashLine = None
        
def MoveToClashes():
    #print("MovingToClashes")
    for Character in AllFightingCharacters:
        HideCharacterUI(Character)
        
    AllDice = PlayerSpeedDice + EnemySpeedDice
    for Die in AllDice:
        RemoveClashLine(Die)
        Die.Clicked = False
        Die.MousedOver = False
        if Die.HeldPage != None:
            Die.HeldPage.visible = False
        
    app.CurrentSpeedBracket = -1
    app.PausedForClash = False
    
    #finds highest speed to start 
    for Die in PlayerSpeedDice:
        #print("check " + str(Die.speed) +" vs " + str(app.CurrentSpeedBracket))
        if Die.speed > app.CurrentSpeedBracket:
            app.CurrentSpeedBracket = Die.speed 
            #print("check=")
            
    for Die in EnemySpeedDice:
        #print("check " + str(Die.speed) +" vs " + str(app.CurrentSpeedBracket))
        if Die.speed > app.CurrentSpeedBracket:
            app.CurrentSpeedBracket = Die.speed
            #print("check=")
            
    #print("High speed is: " + str(app.CurrentSpeedBracket))
    Hit = False
    while app.CurrentSpeedBracket > -1 and app.PausedForClash == False:
        for Die in AllDice:
            if Die.HeldPage != None and len(Die.HeldPage.DiceList) > 0 and app.PausedForClash == False: #makes sure the die has a page and that not paused
                if Die.speed == app.CurrentSpeedBracket:
                    DieAct(Die)
                    Hit = True
            elif Die.HeldPage != None and app.PausedForClash == False and len(Die.HeldPage.DiceList) == 0: # check for empty pages
                if Die.speed == app.CurrentSpeedBracket:
                    print("the page is empty wtf")
                    RestorePage(Die.HeldPage)
                    #app.CurrentSpeedBracket += 1
        app.CurrentSpeedBracket -= 1
    if Hit == False:
        print("used all pages!!!")
        #this is breaking the auto for some reason
        app.PlayerConfirmStage = 3
        
def DieAct(Die):
    app.PausedForClash = True
    app.ActingDice.append(Die)
    TargetDie = Die.TargetDie
    
    #Activates on use effect of this card
    if Die.HeldPage.OnUseEffect != None:
        if type(Die.HeldPage.OnUseEffect) == list: #if multiple effects
            for Effect in Die.HeldPage.OnUseEffect:
                ActivateCardAbility(Effect,Die)
        else:
            ActivateCardAbility(Die.HeldPage.OnUseEffect, Die)
    #Resolve die value buffs and nerfs
    ResolveDieValueChanges(Die)
    
    if Die.TargetDie.TargetDie == Die: #checks if enemy die is targetting this die
        
        #print("Clash!!!")
        ShowPagesClashBetweenPages(Die)
        
            #Activates on use effect of the other clashing card
        if Die.TargetDie.HeldPage != None and Die.TargetDie.HeldPage.OnUseEffect != None:
            if type(Die.TargetDie.HeldPage.OnUseEffect) == list:
                for Effect in Die.TargetDie.HeldPage.OnUseEffect:
                    ActivateCardAbility(Effect, Die.TargetDie)
            else:
                 ActivateCardAbility(Die.TargetDie.HeldPage.OnUseEffect, Die.TargetDie)
        ResolveDieValueChanges(Die.TargetDie)
        
        pass
        
    #checks for extra dice to clash with
    elif TargetDie != None and TargetDie.ConnectedCharacter != None and len(TargetDie.ConnectedCharacter.UnusedDice) > 0:
        ShowPagesClashBetweenPageAndExtra(Die)
        
    else:
        #print("One sided attack")
        ShowOneSidedAttackPage(Die)
        pass
        
        
        
def ShowOneSidedAttackPage(Die):
    ActiveCard = Die.HeldPage
    ActiveCard.visible = True
    ActiveCard.rotateAngle = 0
    ActiveCard.centerX = 200
    ActiveCard.centerY = 100
    pass
def ShowPagesClashBetweenPageAndExtra(Die):
    if Die != None:
        ActiveCard = Die.HeldPage
        CharSprite = Die.ConnectedCharacter
        OtherActiveCard = Die.TargetDie.ConnectedCharacter.UnusedDice[0]#Die.TargetDie.HeldPage
        if ActiveCard != None:
            ActiveCard.visible = True
            ActiveCard.rotateAngle = 0
            ActiveCard.centerX = CharSprite.centerX
            ActiveCard.centerY = CharSprite.centerY - 50
            if OtherActiveCard != None:
                OtherActiveCard.visible = True
                OtherActiveCard.rotateAngle = 0
                if Die.TargetDie.ConnectedCharacter.centerX > CharSprite.centerX:
                    OtherActiveCard.left = ActiveCard.right
                else:
                    OtherActiveCard.right = ActiveCard.left
                    
                OtherActiveCard.centerY = CharSprite.centerY - 50
    pass

def ShowPagesClashBetweenPages(Die):
    if Die != None:
        ActiveCard = Die.HeldPage
        CharSprite = Die.ConnectedCharacter
        OtherActiveCard = Die.TargetDie.HeldPage
        if ActiveCard != None:
            ActiveCard.visible = True
            ActiveCard.rotateAngle = 0
            ActiveCard.centerX = CharSprite.centerX
            ActiveCard.centerY = CharSprite.centerY - 50
            if OtherActiveCard != None:
                OtherActiveCard.visible = True
                OtherActiveCard.rotateAngle = 0
                if Die.TargetDie.ConnectedCharacter.centerX > CharSprite.centerX:
                    OtherActiveCard.left = ActiveCard.right
                else:
                    OtherActiveCard.right = ActiveCard.left
                    
                OtherActiveCard.centerY = CharSprite.centerY - 50
    pass
            
def ClearActingDice():
    while len(app.ActingDice) > 0:
        app.ActingDice.remove(app.ActingDice[0])
        
def HideCharacterUI(Character):
    print(Character.name)
    for Die in Character.SpeedDice:
        Die.ConnectedSprite.visible = False
        Die.ConnectedText.visible = False
    
    for Light in Character.LightSprites:
        Light.visible = False
        
    Character.EmotionBar.visible = False

def ShowCharacterUI(Character):
    for Die in Character.SpeedDice:
        Die.ConnectedSprite.visible = True
        Die.ConnectedText.visible = True
    
    for Light in Character.LightSprites:
        Light.visible = True
        
    Character.EmotionBar.visible = True
    UpdateEmotionBar(Character)
        
def MoveATowardB(Character,SecondSprite):
    #FirstFullSprite = Group(Character.CharacterSprite,Character.Eye)
    if Character.centerX < SecondSprite.centerX:
        Character.centerX += app.CharacterSpeed
    else:
        Character.centerX -= app.CharacterSpeed
            
    if Character.centerY < SecondSprite.centerY:
        Character.centerY += app.CharacterSpeed
    else:
        Character.centerY -= app.CharacterSpeed
        
def ClashBetweenSpeedDice(FirstDie,SecondDie):
    if FirstDie.HeldPage != None and len(FirstDie.HeldPage.DiceList) > 0:
        FirstDie.HeldPage.Used = True
        if SecondDie.HeldPage != None and len(SecondDie.HeldPage.DiceList) > 0 and SecondDie.TargetDie == FirstDie:
            print("Clash with page")
            SecondDie.HeldPage.Used = True
            ContestOfTwoDice(FirstDie,SecondDie)
            pass
        elif len(SecondDie.ConnectedCharacter.UnusedDice) > 0:
            print("Clash with extra dice")
            ClashingWithExtraDice(FirstDie,SecondDie.ConnectedCharacter.UnusedDice,SecondDie.ConnectedCharacter)
            pass
        else:
            print("one sided attack")
            OneSidedRolling(FirstDie,SecondDie)
    elif SecondDie.HeldPage != None and len(SecondDie.HeldPage.DiceList) > 0:
        print("one sided attack from second, miracle?")
        SecondDie.HeldPage.Used = True
        OneSidedRolling(SecondDie,FirstDie)
    else:
        print("This may be the cause of standstill? something broke in clash, trying to escape")
        if FirstDie.HeldPage != None:
            print("Trying to fix by untargetting and reconstructing bc found held pages")
            UntargetSpeedDie(FirstDie)
            
        if SecondDie.HeldPage != None:
            print("Trying to fix by untargetting and reconstructing bc found held pages")
            UntargetSpeedDie(SecondDie)
        else:
            print("Trying to fix by removing acting dice bc no held page")
            ClearActingDice()
            
        
def TriggerClashPassives(Character1,Character2):
    for Effect in Character1.StatusEffects:
        if Effect.BaseEffect == False and Effect.Trigger == "Clash": #I was thinking of also doing types but timing problems with bleed
            print("Clash trigger passive activating: " + Effect.name)
            if Effect.name == "Footfalls":
                if Character1.Health <= Character1.MaxHealth/5:
                    FootfallsDamage = Character2.MaxHealth * 3 /10 
                    if FootfallsDamage > 36:
                        FootfallsDamage = 36
                    Character2.Health -= FootfallsDamage
                    Chance2 = random.randint(1,3)
                    for Count in range (Chance2):
                        AddStatusEffect(Character2,"Burn",False)
                    Character1.Health = 0


def ClashingWithExtraDice(FirstDie, ExtraDieList, ExtraDiceCharacter):
    
    ShowPagesClashBetweenPageAndExtra(FirstDie)
    ExtraDieList[0].visible = True

    #before dice are rolled and bro dies to bleed
    TriggerClashPassives(FirstDie.ConnectedCharacter,ExtraDiceCharacter)
    
    FirstDieResult = RollDie(FirstDie.HeldPage.DiceList[0],FirstDie.ConnectedCharacter)
    FirstDieType = FirstDie.HeldPage.DiceList[0].type
    SecondDieResult = RollDie(ExtraDieList[0].TrueDie,ExtraDiceCharacter)
    SecondDieType = ExtraDieList[0].TrueDie.type
    
    #This one cannot be as easily be made more efficent because it uses different die removals based on extra or not
    # I could solve this by making a extra bool but I will leave that to furute me
    
    if FirstDieResult > SecondDieResult:
        
        AddEmotion(FirstDie.ConnectedCharacter,True)
        if FirstDie.HeldPage.DiceList[0].Trigger == "Clash Win":
            TriggerDieEffect(FirstDie.HeldPage.DiceList[0],FirstDie.ConnectedCharacter,ExtraDiceCharacter)
            
        AddEmotion(ExtraDiceCharacter,False)
        if ExtraDieList[0].TrueDie.Trigger == "Clash Lose":
            TriggerDieEffect(ExtraDieList[0].TrueDie,ExtraDiceCharacter,FirstDie.ConnectedCharacter)
        
        if FirstDieType == "slash" or FirstDieType == "pierce" or FirstDieType == "blunt":
            
            if FirstDie.HeldPage.DiceList[0].Trigger == "On Hit":
                TriggerDieEffect(FirstDie.HeldPage.DiceList[0],FirstDie.ConnectedCharacter,ExtraDiceCharacter)
            
            if SecondDieType == "block":
                TakeDamage(ExtraDiceCharacter,FirstDie.ConnectedCharacter,FirstDieResult-SecondDieResult,FirstDieType)
                print(("First won but blocked and Dealt: ") + str(FirstDieResult) + " damage")
            else:
                TakeDamage(ExtraDiceCharacter,FirstDie.ConnectedCharacter,FirstDieResult,FirstDieType)
                print(("First won and Dealt: ") + str(FirstDieResult) + " damage")
            
            ResolveAndRemoveDie(FirstDie)
            ResolveAndRemoveExtraDie(ExtraDieList)
            
        elif FirstDieType == "block":
            print("Blocked")
            ExtraDiceCharacter.Stagger -= FirstDieResult-SecondDieResult
            UpdateBars(ExtraDiceCharacter)
            for count in range(FirstDieResult-SecondDieResult):
                CreateParticle(ExtraDiceCharacter.CharacterSprite.centerX,ExtraDiceCharacter.CharacterSprite.centerY,5,"yellow")
            AttackAnimation("block",ExtraDiceCharacter)
            ResolveAndRemoveDie(FirstDie)
            ResolveAndRemoveExtraDie(ExtraDieList)
            
            
        elif FirstDieType == "evade":
            print("Evaded")
            FirstDie.ConnectedCharacter.Stagger += FirstDieResult-SecondDieResult
            AttackAnimation("evade",FirstDie.ConnectedCharacter)
            if FirstDie.ConnectedCharacter.Stagger > FirstDie.ConnectedCharacter.MaxStagger:
                FirstDie.ConnectedCharacter.Stagger = FirstDie.ConnectedCharacter.MaxStagger
                
            UpdateBars(FirstDie.ConnectedCharacter)
            
            ResolveAndRemoveExtraDie(ExtraDieList)
            if SecondDieType == "block" or SecondDieType == "evade":
                ResolveAndRemoveDie(FirstDie)
            
            
    elif SecondDieResult > FirstDieResult:
        
        AddEmotion(ExtraDiceCharacter,True)
        if ExtraDieList[0].TrueDie.Trigger == "Clash Win":
            TriggerDieEffect(ExtraDieList[0].TrueDie,ExtraDiceCharacter,FirstDie.ConnectedCharacter)
            
        AddEmotion(FirstDie.ConnectedCharacter,False)
        if FirstDie.HeldPage.DiceList[0].Trigger == "Clash Lose":
            TriggerDieEffect(FirstDie.HeldPage.DiceList[0],FirstDie.ConnectedCharacter,ExtraDiceCharacter)
        
        if SecondDieType == "slash" or SecondDieType == "pierce" or SecondDieType == "blunt":
            
            if ExtraDieList[0].TrueDie.Trigger == "On Hit":
                TriggerDieEffect(ExtraDieList[0].TrueDie,ExtraDiceCharacter,FirstDie.ConnectedCharacter)
            
            if FirstDieType == "block":
                TakeDamage(FirstDie.ConnectedCharacter,ExtraDiceCharacter,SecondDieResult-FirstDieResult,SecondDieType)
                print(("Second won but blocked and Dealt: ") + str(SecondDieResult-FirstDieResult) + " damage")
            else:
                TakeDamage(FirstDie.ConnectedCharacter,ExtraDiceCharacter,SecondDieResult,SecondDieType)
                print(("Second won and Dealt: ") + str(SecondDieResult) + " damage")
            
            ResolveAndRemoveDie(FirstDie)
            ResolveAndRemoveExtraDie(ExtraDieList)
            
        elif SecondDieType == "block":
            print("Blocked")
            FirstDie.ConnectedCharacter.Stagger -= SecondDieResult-FirstDieResult
            UpdateBars(FirstDie.ConnectedCharacter)
            for count in range(SecondDieResult-FirstDieResult):
                CreateParticle(FirstDie.ConnectedCharacter.CharacterSprite.centerX,FirstDie.ConnectedCharacter.CharacterSprite.centerY,5,"yellow")
            AttackAnimation("block",FirstDie.ConnectedCharacter)
            ResolveAndRemoveDie(FirstDie)
            ResolveAndRemoveExtraDie(ExtraDieList)
            
            
        elif SecondDieType == "evade":
            print("Evaded")
            ExtraDiceCharacter.Stagger += SecondDieResult-FirstDieResult
            AttackAnimation("evade",ExtraDiceCharacter)
            if ExtraDiceCharacter.Stagger > ExtraDiceCharacter.MaxStagger:
                ExtraDiceCharacter.Stagger = ExtraDiceCharacter.MaxStagger
                
            UpdateBars(ExtraDiceCharacter)
                
            ResolveAndRemoveDie(FirstDie)
            if FirstDieType == "block" or FirstDieType == "evade":
                ResolveAndRemoveExtraDie(ExtraDieList)

        
    else:
        ResolveAndRemoveDie(FirstDie)
        ResolveAndRemoveExtraDie(ExtraDieList)
        AddEmotion(FirstDie.ConnectedCharacter,True)
        AddEmotion(ExtraDiceCharacter,True)
        print("Equal results no damage")
    
    
    if FirstDie.HeldPage == None or len(FirstDie.HeldPage.DiceList) == 0:
        ResolveAndRemovePage(FirstDie)
        app.PausedForClash = False
        ClearActingDice()

def ContestOfTwoDice(FirstDie,SecondDie):
    
    print("Clash!!!")

    #before dice are rolled and bro dies to bleed
    TriggerClashPassives(FirstDie.ConnectedCharacter,SecondDie.ConnectedCharacter)

    ShowPagesClashBetweenPages(FirstDie)
    
    FirstDieResult = RollDie(FirstDie.HeldPage.DiceList[0],FirstDie.ConnectedCharacter)
    #FirstDieType = FirstDie.HeldPage.DiceList[0].type
    SecondDieResult = RollDie(SecondDie.HeldPage.DiceList[0],SecondDie.ConnectedCharacter)
    #SecondDieType = SecondDie.HeldPage.DiceList[0].type
    
    if FirstDieResult > SecondDieResult:
        
        AddEmotion(FirstDie.ConnectedCharacter,True)
        AddEmotion(SecondDie.ConnectedCharacter,False)

        WinningDieResult = FirstDieResult
        WinningDieType = FirstDie.HeldPage.DiceList[0].type
        WinningDie = FirstDie
        LosingDieResult = SecondDieResult
        LosingDieType = SecondDie.HeldPage.DiceList[0].type
        LosingDie = SecondDie
    elif SecondDieResult > FirstDieResult:
        
        AddEmotion(FirstDie.ConnectedCharacter,False)
        AddEmotion(SecondDie.ConnectedCharacter,True)

        WinningDieResult = SecondDieResult
        WinningDieType = SecondDie.HeldPage.DiceList[0].type
        WinningDie = SecondDie
        LosingDieResult = FirstDieResult
        LosingDieType = FirstDie.HeldPage.DiceList[0].type
        LosingDie = FirstDie
        
        
    if SecondDieResult == FirstDieResult:
        ResolveAndRemoveDie(FirstDie)
        ResolveAndRemoveDie(SecondDie)
        print("Equal results no damage")
        AddEmotion(FirstDie.ConnectedCharacter,True)
        AddEmotion(SecondDie.ConnectedCharacter,True)
    else:
        
        if WinningDie.HeldPage.DiceList[0].Trigger == "Clash Win":
            TriggerDieEffect(WinningDie.HeldPage.DiceList[0],WinningDie.ConnectedCharacter,LosingDie.ConnectedCharacter)
            
        if LosingDie.HeldPage.DiceList[0].Trigger == "Clash Lose":
            TriggerDieEffect(LosingDie.HeldPage.DiceList[0],LosingDie.ConnectedCharacter,WinningDie.ConnectedCharacter)
        
        if WinningDieType == "slash" or WinningDieType == "pierce" or WinningDieType == "blunt":
            
            AttackAnimation(WinningDieType,WinningDie.ConnectedCharacter)
            if WinningDie.HeldPage.DiceList[0].Trigger == "On Hit":
                TriggerDieEffect(WinningDie.HeldPage.DiceList[0],WinningDie.ConnectedCharacter,LosingDie.ConnectedCharacter)
            
            if LosingDieType == "block":
                TakeDamage(LosingDie.ConnectedCharacter,WinningDie.ConnectedCharacter,WinningDieResult-LosingDieResult,WinningDieType)
                print(("First won but blocked and Dealt: ") + str(WinningDieResult) + " damage")
            else:
                TakeDamage(LosingDie.ConnectedCharacter,WinningDie.ConnectedCharacter,WinningDieResult,WinningDieType)
                print(("First won and Dealt: ") + str(WinningDieResult) + " damage")
            
            ResolveAndRemoveDie(WinningDie)
            ResolveAndRemoveDie(LosingDie)
            
        elif WinningDieType == "block":
            print("Blocked")
            LosingDie.ConnectedCharacter.Stagger -= WinningDieResult-LosingDieResult
            UpdateBars(LosingDie.ConnectedCharacter)
            for count in range(WinningDieResult-LosingDieResult):
                CreateParticle(LosingDie.ConnectedCharacter.CharacterSprite.centerX,LosingDie.ConnectedCharacter.CharacterSprite.centerY,5,"yellow")
            AttackAnimation("block",LosingDie.ConnectedCharacter)
            ResolveAndRemoveDie(WinningDie)
            ResolveAndRemoveDie(LosingDie)
            
            
        elif WinningDieType == "evade":
            print("Evaded")
            WinningDie.ConnectedCharacter.Stagger += WinningDieResult-LosingDieResult
            AttackAnimation("evade",WinningDie.ConnectedCharacter)
            if WinningDie.ConnectedCharacter.Stagger > WinningDie.ConnectedCharacter.MaxStagger:
                WinningDie.ConnectedCharacter.Stagger = WinningDie.ConnectedCharacter.MaxStagger
                
            UpdateBars(WinningDie.ConnectedCharacter)
                
            if LosingDieType == "block" or LosingDieType == "evade":
                ResolveAndRemoveDie(WinningDie)
            ResolveAndRemoveDie(LosingDie)
            
            
            
    if FirstDie.HeldPage != None and len(FirstDie.HeldPage.DiceList) == 0: #first die's page runs out of dice
        ResolveAndRemovePage(FirstDie)
        ClearActingDice()
        if SecondDie.HeldPage != None and len(SecondDie.HeldPage.DiceList) > 0: #switches the acting die to the second die
            
            AddEmotion(SecondDie.ConnectedCharacter,True)
            app.ActingDice.append(SecondDie)
        else:
            app.PausedForClash = False
            
    if SecondDie.HeldPage != None and len(SecondDie.HeldPage.DiceList) == 0: #second die's page runs out of dice
        
        if len(app.ActingDice) > 0: #makes sure the other page still exists for the overrun emotion bonus
            
            AddEmotion(FirstDie.ConnectedCharacter,True)
            
        ResolveAndRemovePage(SecondDie)

def OneSidedRolling(FirstDie,SecondDie):
    
    print("One sided attack")
    DiceType = FirstDie.HeldPage.DiceList[0].type
    ShowOneSidedAttackPage(FirstDie)
    
    if SecondDie.ConnectedCharacter.Health <= 0:
        print("Stopped attack bc beating up a corpse :(")

    else:
        if DiceType == "slash" or DiceType == "pierce" or DiceType == "blunt":
            if FirstDie.HeldPage.DiceList[0].Trigger == "On Hit":
                TriggerDieEffect(FirstDie.HeldPage.DiceList[0],FirstDie.ConnectedCharacter,SecondDie.ConnectedCharacter)
            
            AttackAnimation(DiceType,FirstDie.ConnectedCharacter)
            Damage = RollDie(FirstDie.HeldPage.DiceList[0],FirstDie.ConnectedCharacter)
            
            if Damage == FirstDie.HeldPage.DiceList[0].max + FirstDie.HeldPage.DiceList[0].MaxModifier:#check for a max roll
                AddEmotion(FirstDie.ConnectedCharacter,True)
                
            elif Damage == FirstDie.HeldPage.DiceList[0].min + FirstDie.HeldPage.DiceList[0].MinModifier:#check for a min roll
                AddEmotion(FirstDie.ConnectedCharacter,False)
            
            print(("Dealt: ") + str(Damage) + " damage")
            TakeDamage(SecondDie.ConnectedCharacter,FirstDie.ConnectedCharacter,Damage,FirstDie.HeldPage.DiceList[0].type)

    if DiceType == "block" or DiceType == "evade":
        
        CardDie = FirstDie.HeldPage.DiceList[0]
        ConstructingUnusedDice = []
        CreateDie(CardDie.min,CardDie.max,CardDie.type,ConstructingUnusedDice,CardDie.Effect,CardDie.Trigger,CardDie.Target,CardDie.Counter)
        UnusedBox = Rect(180,185,60,25)
        UnusedDie = ConstructingUnusedDice[0] 
        UnusedDie.IconCircle.centerX = 200
        UnusedDie.IconCircle.centerY = 200
        UnusedDie.TypeSprite.centerX = 200
        UnusedDie.TypeSprite.centerY = 200
        UnusedDie.DamageRangeText.centerX = 220
        UnusedDie.DamageRangeText.centerY = 200
        if UnusedDie.AddEffectDescription != None:
            StartY = 190 - 6
            for line in UnusedDie.AddEffectDescription:
                StartY += 7
                line.left = 183
                line.centerY = StartY
            StartY -= 6

        FullUnusedDieVisual = Group(UnusedBox,UnusedDie.IconCircle,UnusedDie.TypeSprite,UnusedDie.DamageRangeText)
        if UnusedDie.AddEffectDescription != None:
            for line in UnusedDie.AddEffectDescription:
                FullUnusedDieVisual.add(line)
        FullUnusedDieVisual.TrueDie = UnusedDie
        FirstDie.ConnectedCharacter.UnusedDice.append(FullUnusedDieVisual)
        
        #FirstDie.ConnectedCharacter.UnusedDice.append(FirstDie.HeldPage.DiceList[0])
        #Die.color = "lightBlue"

    
    ResolveAndRemoveDie(FirstDie)
    
    if len(FirstDie.HeldPage.DiceList) == 0:
        ResolveAndRemovePage(FirstDie)
        app.PausedForClash = False
        ClearActingDice()
    
def ResolveAndRemoveDie(Die):
    
    if Die.HeldPage != None:
        Die.HeldPage.UsedDiceList.append(Die.HeldPage.DiceList[0])
        
        Die.HeldPage.DiceList[0].TypeSprite.opacity = 0
        Die.HeldPage.DiceList[0].IconCircle.opacity = 0
        Die.HeldPage.DiceList[0].DamageRangeText.opacity = 0
        Die.HeldPage.DiceList.remove(Die.HeldPage.DiceList[0])
        
        index = len(Die.HeldPage.UsedDiceList) - 1
    
def ResolveAndRemoveExtraDie(ExtraDieList):
    
    print(ExtraDieList)
    #ExtraDieList[0].fill = "red"
    ExtraDieList[0].visible = False
    ExtraDieList.remove(ExtraDieList[0])
    
def RestorePage(Page):
    Page.Used = False
    if len(Page.DiceList) == 0:
        Page.DiceList = list(Page.UsedDiceList)
    else:
        NewList = []
        for Die in list(Page.UsedDiceList):
            NewList.append(Die)
        for Die in list(Page.DiceList):
            NewList.append(Die)
        Page.DiceList = NewList
        
    for Dice in Page.DiceList:
        
        Dice.TypeSprite.opacity = 100
        Dice.IconCircle.opacity = 100
        Dice.DamageRangeText.opacity = 100
        Dice.MaxModifier = 0
        Dice.MinModifier = 0
        UpdateDamageRange(Dice)
        
    Page.UsedDiceList.clear()
    
def ResolveAndRemovePage(Die):
    
    if Die.HeldPage != None:
        RestorePage(Die.HeldPage)
        Die.HeldPage.visible = False
        RemoveClashLine(Die)
        
        #Die.ConnectedCharacter.Library.append(Die.HeldPage)
        Die.ConnectedCharacter.Graveyard.append(Die.HeldPage)
        
        Die.HeldPage = None
        
def AddEmotion(Character,Positive):
    #print("wip")
    if Character.ControlledByPlayer:
        if Character.EmotionLevel < app.CurrentEmotionLevelCap:#check if at max level already
            if len(Character.EmotionCoins) < len(Character.EmotionBarList) - 1: #checks if at max coins in bar
                Character.EmotionCoins.append(Positive)
                UpdateEmotionBar(Character)
    else:
        if Character.EmotionLevel < app.CurrentBattle.EmotionLevelCap:#check if at max level already
            if len(Character.EmotionCoins) < len(Character.EmotionBarList) - 1: #checks if at max coins per turn
                Character.EmotionCoins.append(Positive)
                UpdateEmotionBar(Character)

    
def EmotionLevelUp(Character):
    Character.EmotionLevel += 1
    Character.MaxLight += 1
    for Coin in Character.EmotionCoins:
        Character.BankedEmotionCoins.append(Coin)
    Character.EmotionCoins.clear()
    Character.Light = Character.MaxLight - 1
    GainLight(Character)
    ResetEmotionBar(Character)
    
def RollDie(Die,RollingCharacter):
    if Die.Trigger == "On Use":
        TriggerDieEffect(Die,RollingCharacter,None)
    
    if Die.max + Die.MaxModifier < Die.min + Die.MinModifier: #lower min to max
        if Die.max + Die.MaxModifier < 0: #absolute min 0
            Roll = 0
        else:
            Roll = Die.max + Die.MaxModifier
    else:
        if Die.min + Die.MinModifier < 0: #absolute min 0
            if Die.max + Die.MaxModifier < 0: #absolute min 0
                Roll = 0
            else:
                Roll = random.randint(0, Die.max + Die.MaxModifier)
        else:
            Roll = random.randint(Die.min + Die.MinModifier, Die.max + Die.MaxModifier)
    
    for Effect in RollingCharacter.StatusEffects:
        if Die.type == "Slash" or Die.type == "Blunt" or Die.type == "Pierce":
            if Effect.name == "Bleed":
                RollingCharacter.Health -= Effect.Count
                UpdateBars(RollingCharacter)
                for count in range(Effect.Count):
                    CreateParticle(RollingCharacter.CharacterSprite.centerX,RollingCharacter.CharacterSprite.centerY,5,"darkred")
                Effect.Count = int((2/3) * Effect.Count)
            elif Effect.name == "Fairy":
                RollingCharacter.Health -= Effect.Count
                UpdateBars(RollingCharacter)

    return Roll
    
def ResolveDieValueChanges(SpeedDie):
    for Die in SpeedDie.HeldPage.DiceList:
        Modifier = 0
        for Effect in SpeedDie.ConnectedCharacter.StatusEffects:
            if Effect.BaseEffect:
                if Die.type == "slash" or Die.type == "blunt" or Die.type == "pierce":
                    if Effect.name == "Strength":
                        Modifier += Effect.Count
                    elif Effect.name == "Feeble":
                        Modifier -= Effect.Count
                        
                elif Die.type == "evade" or Die.type == "block":
                    if Effect.name == "Endurance":
                        Modifier += Effect.Count
                    elif Effect.name == "Disarm":
                        Modifier -= Effect.Count
                        
            elif Effect.Trigger == "Rolled":
                print("trying to Activate rolled passive")
                ActivatePassive = False
                if Effect.Type == "All":
                    ActivatePassive = True
                elif Effect.Type == "Offensive":
                    if Die.type == "slash" or Die.type == "blunt" or Die.type == "pierce":
                        ActivatePassive = True
                elif Effect.Type == "Defensive":
                    print(Die.type)
                    if Die.type == "evade" or Die.type == "block":
                        print("how about this")
                        ActivatePassive = True
                elif Effect.Type == "Slash":
                    if Die.type == "slash":
                        ActivatePassive = True
                elif Effect.Type == "Blunt":
                    if Die.type == "blunt":
                        ActivatePassive = True
                elif Effect.Type == "Pierce":
                    if Die.type == "pierce":
                        ActivatePassive = True
                elif Effect.Type == "Block":
                    if Die.type == "block":
                        ActivatePassive = True
                elif Effect.Type == "Evade":
                    if Die.type == "evade":
                        ActivatePassive = True
                        
                if ActivatePassive:
                    print("Activating rolled passive")
                    Chance2 = random.randint(Effect.Min, Effect.Max)
                    Chance2 *= Effect.Modifier
                    Modifier += Chance2

                if Effect.name == "Matchlight":
                    if len(Effect.UsedCards) == 0 or not Contains(Effect.UsedCards,SpeedDie.HeldPage): #makes sure it only runs once per page
                        #if you dont have 1,2 add them
                        if len(Effect.TrackedCards) == 0:
                            Effect.TrackedCards.append(SpeedDie.HeldPage)
                            SpeedDie.HeldPage.CardBox.border = "orange"
                        elif len(Effect.TrackedCards) == 1:
                            if SpeedDie.HeldPage != Effect.TrackedCards[0]:
                                Effect.TrackedCards.append(SpeedDie.HeldPage)
                                SpeedDie.HeldPage.CardBox.border = "orange"

                        if Contains(Effect.TrackedCards,SpeedDie.HeldPage):
                            #check if the page is a matchlight page
                            Found = None
                            for SearchEffect in SpeedDie.ConnectedCharacter.StatusEffects:
                                if not SearchEffect.BaseEffect and SearchEffect.name == "Ember": 
                                    #look for ember
                                    Found = SearchEffect
                            if Found == None:
                                #if none create it
                                AddPassiveEffect(SpeedDie.ConnectedCharacter,"Ember")
                                UpdateStatusEffects(SpeedDie.ConnectedCharacter)
                            else:
                                Die.MaxModifier += Found.Count
                                print("ember increasing die max by " + str(Found.Count))
                                UpdateDamageRange(Die)
                                #otherwise raise max of this die by it
                                if Found.Count >= 4:
                                    #also check for 4+ to see if damage
                                    Chance2 = random.randint(1,4)
                                    if Chance2 == 4:
                                        SpeedDie.ConnectedCharacter.Health -= Found.Count
                                        Sprite = SpeedDie.ConnectedCharacter.CharacterSprite
                                        CreateParticle(Sprite.centerX,Sprite.centerY,30,"orange")
                                    #25% chance to explode
                                #and finally increment ember
                                Found.Count += 1

                            Effect.UsedCards.append(SpeedDie.HeldPage)                    
                               
        if Modifier != 0:
            Die.MinModifier += Modifier
            Die.MaxModifier += Modifier
            UpdateDamageRange(Die)
            
    #resolve paralysis
    for Effect in SpeedDie.ConnectedCharacter.StatusEffects:
        if Effect.name == "Paralysis":
            TargetList = list(SpeedDie.HeldPage.DiceList)
            for count in range(Effect.Count):
                if len(TargetList) > 0:
                    chance = random.randint(0, len(TargetList) - 1)
                    TargetList[chance].MaxModifier -= 3
                    UpdateDamageRange(TargetList[chance])
                    TargetList.remove(TargetList[chance])
                
    
def TriggerDieEffect(CombatDie,TriggerCharacter,EnemyCharacter):
    #Example effect 3Bleed
    print("triggering additional effect")
    AdditionalEffect = CombatDie.Effect
    EffectTarget = CombatDie.Target
    Potency = 1
    SelfSpeedDie = None
    AlterVal = False
    if len(app.ActingDice) > 0 and app.ActingDice[0].HeldPage != None and len(app.ActingDice[0].HeldPage.DiceList) > 0 and app.ActingDice[0].HeldPage.DiceList[0] == CombatDie:
        SelfSpeedDie = app.ActingDice[0]
    elif len(app.ActingDice) > 0 and app.ActingDice[0].TargetDie != None:
        SelfSpeedDie = app.ActingDice[0].TargetDie
        
    StartChar = AdditionalEffect[0:1]
    if StartChar.isdigit():
        Potency = int(StartChar)
        AdditionalEffect = AdditionalEffect[1:]
        
    elif StartChar == "X":
        print("lol this is complex so WIP")
        #remove expected X=
        AdditionalEffect = AdditionalEffect[2:]
        AnalyzedCharacter = None
        if AdditionalEffect.startswith("Self"):
            AnalyzedCharacter = TriggerCharacter
        else:
            AnalyzedCharacter = EnemyCharacter
        X = 0
        for StatusEffect in AnalyzedCharacter.StatusEffects:
            if AdditionalEffect.startswith(StatusEffect.name):
                X = StatusEffect.Count
        Potency = X


        
    NextTurnActivate = False
    if AdditionalEffect.startswith("Next"):
        NextTurnActivate = True
        AdditionalEffect = AdditionalEffect[4:]
        
    if AdditionalEffect.startswith("Reduce"):
        AlterVal = True
        Potency *= -1
    elif AdditionalEffect.startswith("Increase"):
        AlterVal = True

    print("adding additional effect " + AdditionalEffect + " with potency " + str(Potency))
    
    Target = None
    if AlterVal:
        if EffectTarget == "FollowingSelfDie" and len(SelfSpeedDie.HeldPage.DiceList) >= 2:
            Target = SelfSpeedDie.HeldPage.DiceList[1]
        elif EffectTarget == "LastSelfDie" and len(SelfSpeedDie.HeldPage.DiceList) != 0:
            Last = len(SelfSpeedDie.HeldPage.DiceList) - 1
            Target = SelfSpeedDie.HeldPage.DiceList[Last]
        elif SelfSpeedDie.TargetDie != None and SelfSpeedDie.TargetDie.HeldPage != None:
            if EffectTarget == "FollowingOpponentDie" and len(SelfSpeedDie.TargetDie.HeldPage.DiceList) >= 2:
                Target = SelfSpeedDie.TargetDie.HeldPage.DiceList[1]
            if EffectTarget == "LastOpponentDie" and len(SelfSpeedDie.TargetDie.HeldPage.DiceList) != 0:
                Last = len(SelfSpeedDie.HeldPage.DiceList) - 1
                Target = SelfSpeedDie.TargetDie.HeldPage.DiceList[Last]
    else:
        if EffectTarget == "Enemy":
            Target = EnemyCharacter
            print("putting on enemy")
        elif EffectTarget == "Self":
            Target = TriggerCharacter
            print("putting on self?")
    
    if Target != None:    
        if AdditionalEffect == "Gain Light":
            for count in range(Potency):
                GainLight(TriggerCharacter)
        elif AdditionalEffect == "Regain Health":
            HealCharacter(TriggerCharacter,Potency)
        elif AdditionalEffect == "Increase" or AdditionalEffect == "Reduce":
            Target.MinModifier += Potency
            Target.MaxModifier += Potency
            UpdateDamageRange(Target)
        else:
            for count in range(Potency):
                AddStatusEffect(Target,AdditionalEffect,NextTurnActivate)
            
def ActivateCardAbility(Effect,Die):
    
    AdditionalEffect = Effect
    EffectTarget = "Self"
    Potency = 1
    IsStatusEffect = False
    
    if AdditionalEffect.startswith("Effect"):
        IsStatusEffect = True
        AdditionalEffect = AdditionalEffect[6:]
        
        
    StartChar = AdditionalEffect[0:1]
    
    if StartChar.isdigit():
        Potency = int(StartChar)
        AdditionalEffect = AdditionalEffect[1:]
        
    elif StartChar == "X":
        print("lol this is complex so WIP")
        
    if AdditionalEffect.startswith("All"):
        AdditionalEffect = AdditionalEffect[3:]
        if AdditionalEffect.startswith("Players"):
            AdditionalEffect = AdditionalEffect[7:]
            if Die.ConnectedCharacter.ControlledByPlayer:
                EffectTarget = "AllPlayers"
            else:
                EffectTarget = "AllEnemies"
        elif AdditionalEffect.startswith("Enemies"):
            AdditionalEffect = AdditionalEffect[7:]
            if Die.ConnectedCharacter.ControlledByPlayer:
                EffectTarget = "AllEnemies"
            else:
                EffectTarget = "AllPlayers"
        
    NextTurnActivate = False
    if AdditionalEffect.startswith("Next"):
        NextTurnActivate = True
        AdditionalEffect = AdditionalEffect[4:]
        
    print("adding additional effect " + AdditionalEffect + " with potency " + str(Potency))
    
    if EffectTarget == "Self":
        EffectTarget = Die.ConnectedCharacter
        if AdditionalEffect == "Gain Light":
            for count in range(Potency):
                GainLight(EffectTarget)
        elif AdditionalEffect == "Regain Health":
            HealCharacter(EffectTarget,Potency)
                
        elif IsStatusEffect:
            for count in range(Potency):
                AddStatusEffect(EffectTarget,AdditionalEffect,NextTurnActivate)
    elif EffectTarget == "AllPlayers":
        for Character in PlayerCharacters:
            if AdditionalEffect == "Gain Light":
                for count in range(Potency):
                    GainLight(Character)
            elif AdditionalEffect == "Regain Health":
                HealCharacter(Character,Potency)
            
            elif IsStatusEffect:
                for count in range(Potency):
                    AddStatusEffect(Character,AdditionalEffect,NextTurnActivate)
                    
    elif EffectTarget == "AllEnemies":
        print("wip")
        EnemyList = list(AllFightingCharacters)
        for Character in PlayerCharacters:
            if Contains(EnemyList,Character):
                EnemyList.remove(Character)
        for Character in EnemyList:
            if AdditionalEffect == "Gain Light":
                for count in range(Potency):
                    GainLight(Character)
            
            elif IsStatusEffect:
                for count in range(Potency):
                    AddStatusEffect(Character,AdditionalEffect,NextTurnActivate)
      
def CreateAbnormailyPage(name,Level,Positive,SingleTarget,Description,Effect,List):
    
    AbnormailyPage = Group()
    AbnormailyPage.name = name
    AbnormailyPage.Level = Level
    AbnormailyPage.Positive = Positive
    AbnormailyPage.SingleTarget = SingleTarget
    AbnormailyPage.Description = Description
    AbnormailyPage.Effect = Effect
    List.append(AbnormailyPage)

#brick
#turn into the actual passive for character
def AddPassiveEffect(Character,Passive):
    PassiveEffect = Group()
    effect = Passive
    PassiveEffect.Trigger = None
    PassiveEffect.Type = None
    PassiveEffect.Modifier = 0
    PassiveEffect.Min = 0
    PassiveEffect.Max = 0
    PassiveEffect.DamageTypeStagger = False
    PassiveEffect.StatusEffect = None
    PassiveEffect.StatusEffectToSelf = False
    PassiveEffect.StatusNext = False
    
    PassiveEffect.RemovalTrigger = None
    PassiveEffect.Removal = "Full"
    PassiveEffect.name = effect
    PassiveEffect.Count = 1
    PassiveEffect.BaseEffect = False
    #PassiveEffect.Exceptional = True
    PassiveEffect.Icon = None
    
    CreatePassive = False
    if effect.startswith("Create Passive"):
        effect = effect[14:]
        #PassiveEffect.Exceptional = True
        
    elif Passive == "Pale Hands":
        PassiveEffect.Trigger = "Dealt"
        PassiveEffect.Type = "All"
    elif Passive == "Scars":
        PassiveEffect.Trigger = "Recieved"
        PassiveEffect.Type = "All"
    elif Passive == "Scorched Girl Mourn":
        PassiveEffect.Trigger = "Death"
        PassiveEffect.Type = "Ally"
    elif Passive == "Scorched Girl Clumsy":
        PassiveEffect.Trigger = "Staggered"
    elif Passive == "Footfalls":
        PassiveEffect.Trigger = "Clash"
        PassiveEffect.Type = "All"
    elif Passive == "Ashes":
        PassiveEffect.Trigger = "Dealt"
        PassiveEffect.Type = "All"
        #40% chance to gain non stackable Offensive dice inflict 1 burn
    elif Passive == "Dormant Ash Boost":
        PassiveEffect.Trigger = "Dealt"
        PassiveEffect.Type = "All"
        PassiveEffect.RemovalTrigger = "EndTurn"
        PassiveEffect.Removal = "Dormant Ash"
        PassiveEffect.Icon = Rect(0,0,15,15,fill="orange",border = "grey")
        PassiveEffect.add(PassiveEffect.Icon)
    elif Passive == "Matchlight":
        PassiveEffect.Trigger = "Rolled"
        PassiveEffect.RemovalTrigger = "EndTurn"
        PassiveEffect.Removal = "Matchlight Reset"
        PassiveEffect.TrackedCards = []
        PassiveEffect.UsedCards = []
    elif Passive == "Ember":
        PassiveEffect.Icon = Rect(0,0,15,15,fill="darkGrey",border = "orange")
        PassiveEffect.add(PassiveEffect.Icon)
        
    if PassiveEffect.Icon == None:
        PassiveEffect.Icon = Circle(0,0,10,fill = "yellow",border = "red")
        PassiveEffect.add(PassiveEffect.Icon)
        
    PassiveEffect.Text = Label("1",10,10)
    PassiveEffect.add(PassiveEffect.Text)
    
    PassiveEffect.visible = False
    
    if effect.startswith("Dealt"):
        PassiveEffect.Trigger = "Dealt"
        effect = effect[5:]
    elif effect.startswith("Rolled"):
        PassiveEffect.Trigger = "Rolled"
        effect = effect[6:]
    elif effect.startswith("Recieved"):
        PassiveEffect.Trigger = "Recieved"
        effect = effect[8:]
    if PassiveEffect.Trigger == None:
        print("Things are breaking? no trigger?")
        
    if effect.startswith("Defensive"):
        PassiveEffect.Type = "Defensive"
        effect = effect[9:]
    elif effect.startswith("Offensive"):
        PassiveEffect.Type = "Offensive"
        effect = effect[9:]
    elif effect.startswith("All"):
        PassiveEffect.Type = "All"
        effect = effect[3:]
    elif effect.startswith("Pierce"):
        PassiveEffect.Type = "Pierce"
        effect = effect[6:]
    elif effect.startswith("Slash"):
        PassiveEffect.Type = "Slash"
        effect = effect[5:]
    elif effect.startswith("Blunt"):
        PassiveEffect.Type = "Blunt"
        effect = effect[5:]
    elif effect.startswith("Block"):
        PassiveEffect.Type = "Block"
        effect = effect[5:]
    elif effect.startswith("Evade"):
        PassiveEffect.Type = "Evade"
        effect = effect[5:]
        
    if effect.startswith("Num"):
        effect = effect[3:]
        if PassiveEffect.Trigger == "Rolled":
            if effect.startswith("-"):
                PassiveEffect.Modifier = -1
                
            elif effect.startswith("+"):
                PassiveEffect.Modifier = 1
             
            effect = effect[1:]
    
            StartChar = effect[0:1]
            if StartChar.isdigit():
                PassiveEffect.Min = int(StartChar)
                effect = effect[2:]
            StartChar = effect[0:1]
            if StartChar.isdigit():
                PassiveEffect.Max = int(StartChar)
                effect = effect[1:]
        elif PassiveEffect.Trigger == "Dealt" or PassiveEffect.Trigger == "Recieved":
            if effect.startswith("Stagger"):
                PassiveEffect.DamageTypeStagger = True
                effect = effect[7:]
            elif effect.startswith("Damage"):
                PassiveEffect.DamageTypeStagger = False
                effect = effect[6:]
    if effect.startswith("Create Status"):
        effect = effect[13:]
        if effect.startswith("Self"):
            PassiveEffect.StatusEffectToSelf = True
            effect = effect[4:]
        if effect.startswith("Next"):
            PassiveEffect.StatusNext = True
            effect = effect[4:]

        StartChar = effect[0:1]
        if StartChar.isdigit():
            PassiveEffect.Min = int(StartChar)
            effect = effect[2:] #skips the dash ex: 1-3
        StartChar = effect[0:1]
        if StartChar.isdigit():
            PassiveEffect.Max = int(StartChar)
            effect = effect[1:]
        PassiveEffect.StatusEffect = effect
        print("Passive Status creator will inflict:" + effect)



    #EffectIcon.Trigger = None
    Character.StatusEffects.append(PassiveEffect)
    Character.add(PassiveEffect)
    UpdateStatusEffects(Character)
    
def AddStatusEffect(Target,Effect,NextTurnActivate):
    #First check if contains, otherwise create
    Found = None
    if NextTurnActivate:
        for ExistingEffect in Target.NextTurnStatusEffects:
            if ExistingEffect.name == Effect:
                Found = ExistingEffect
    else:
        for ExistingEffect in Target.StatusEffects:
            if ExistingEffect.name == Effect:
                Found = ExistingEffect
            

    if Found != None:
        
        Found.Count += 1
        if Found.name == "Smoke" and Found.Count > 10:
            Found.Count = 10
    else:
        EffectIcon = Group()
        EffectIcon.Trigger = None
        EffectIcon.RemovalTrigger = "EndTurn"
        EffectIcon.Removal = "Full"
        EffectIcon.name = Effect
        EffectIcon.Count = 1
        EffectIcon.BaseEffect = True
        Symbol = None
        Symbol1 = None
        Symbol2 = None
        Symbol3 = None
        print("applying " + Effect)
        
        if Effect == "Burn":
            Symbol = Circle(0,0,10,fill = "yellow",border = "red")
            EffectIcon.Trigger = "EndTurn"
            EffectIcon.Removal = "1/3"
            #switch to triple arc black red yellow
        if Effect == "Bleed":
            Symbol = Circle(0,0,10,fill = "red",border = "black")
            EffectIcon.Trigger = "RollDie"
        if Effect == "Smoke":
            Symbol = Circle(0,0,10,fill = "grey",border = "black")
            EffectIcon.Trigger = "TakeDamage"
            EffectIcon.Removal = "-1"
        if Effect == "Paralysis":
            Symbol = Circle(0,0,10,fill = "yellow",border = "black")
            EffectIcon.Trigger = "RollDie"
        if Effect == "Fairy":
            Symbol = Circle(0,0,10,fill = "pink",border = "blue")
            EffectIcon.Trigger = "RollDie"
            EffectIcon.Removal = "Fairy"
        if Effect == "Charge":
            Symbol = Circle(0,0,10,fill = "yellow",border = "blue")
            EffectIcon.Trigger = None
            EffectIcon.RemovalTrigger = None
            EffectIcon.Removal = None
        if Effect == "Feeble":
            Symbol = Polygon(0,0,10,20,20,0,fill="red",border = "black")
            EffectIcon.Trigger = "RollDie"
        if Effect == "Strength":
            Symbol = Polygon(0,0,10,-20,20,0,fill="red",border = "black")
            EffectIcon.Trigger = "RollDie"
        if Effect == "Disarm":
            Symbol = Polygon(0,0,10,20,20,0,fill="lightblue",border = "black")
            EffectIcon.Trigger = "RollDie"
        if Effect == "Endurance":
            Symbol = Polygon(0,0,10,-20,20,0,fill="lightblue",border = "black")
            EffectIcon.Trigger = "RollDie"
        if Effect == "Bind":
            Symbol = Polygon(0,0,10,20,20,0,fill="lightyellow",border = "black")
            EffectIcon.Trigger = "RollSpeedDice"

        if Effect == "Haste":
            Symbol = Polygon(0,0,10,-20,20,0,fill="lightyellow",border = "black")
            EffectIcon.Trigger = "RollSpeedDice"
        if Effect == "Fragile":
            Symbol = Rect(0,0,15,15,fill="lightblue",border = "black")
            Symbol1 = Line(0,0,15,15)
            Symbol2 = Line(15,0,0,15)
            EffectIcon.Trigger = "TakeDamage"
        if Effect == "Protection":
            Symbol = Rect(0,0,15,15,fill="lightblue",border = "black")
            EffectIcon.Trigger = "TakeDamage"
        if Effect == "Stagger Protection":
            Symbol = Rect(0,0,15,15,fill="lightyellow",border = "black")
            EffectIcon.Trigger = "TakeDamage"

        if Symbol != None:
            EffectIcon.add(Symbol)
        else:
            print("wtf no symbol")
            
        if Symbol1 != None:
            EffectIcon.add(Symbol1)
        if Symbol2 != None:
            EffectIcon.add(Symbol2)
        if Symbol3 != None:
            EffectIcon.add(Symbol3)
        
        EffectIcon.Text = Label("1",10,10)
        EffectIcon.add(EffectIcon.Text)
            
        EffectIcon.IsNextTurn = False
        if NextTurnActivate:
            EffectIcon.opacity = 50
            #EffectIcon.Effect = "AddEffect" + Effect
            #EffectIcon.IsNextTurn = True
            
            Target.NextTurnStatusEffects.append(EffectIcon)
        else:
            Target.StatusEffects.append(EffectIcon)
        
        Target.add(EffectIcon)
            
    
    UpdateStatusEffects(Target)

def HealCharacter(RecievingCharacter,Potency):
    if RecievingCharacter.Health + Potency >= RecievingCharacter.MaxHealth:
        RecievingCharacter.Health = RecievingCharacter.MaxHealth
    else:
        RecievingCharacter.Health += Potency

def TakeDamage(RecievingCharacter,DealingCharacter,Damage,type):
    
    if Damage <= 0:
        Damage = 0
    
    HealthResModifier = CalculatePhysResistence(RecievingCharacter,type,False)
    StaggerResModifier = CalculatePhysResistence(RecievingCharacter,type,True)
    
    HealthEffectModifier = 0
    StaggerEffectModifier = 0
    SmokeModifier = 1
    for Effect in RecievingCharacter.StatusEffects:
        if Effect.BaseEffect:
            if Effect.name == "Protection":
                HealthEffectModifier -= Effect.Count
            elif Effect.name == "Stagger Protection":
                StaggerEffectModifier -= Effect.Count
            elif Effect.name == "Fragile":
                HealthEffectModifier += Effect.Count
            elif Effect.name == "Smoke":
                SmokeModifier = 1 + (Effect.Count/10)
        elif Effect.Trigger == "Recieved":
            
            ActivatePassive = False
            if Effect.Type == "All":
                ActivatePassive = True
            elif Effect.Type == "Offensive":
                if type == "slash" or type == "blunt" or type == "pierce":
                    ActivatePassive = True
            elif Effect.Type == "Defensive":
                if type == "evade" or type == "block":
                    ActivatePassive = True
            elif Effect.Type == "Slash":
                if type == "slash":
                    ActivatePassive = True
            elif Effect.Type == "Blunt":
                if type == "blunt":
                    ActivatePassive = True
            elif Effect.Type == "Pierce":
                if type == "pierce":
                    ActivatePassive = True
            elif Effect.Type == "Block":
                if type == "block":
                    ActivatePassive = True
            elif Effect.Type == "Evade":
                if type == "evade":
                    ActivatePassive = True
                        
            if ActivatePassive:
                Chance2 = random.randint(Effect.Min, Effect.Max)
                
                if Effect.StatusEffect != None:
                    for Count in range(Chance2):
                        if Effect.StatusEffectToSelf:
                            AddStatusEffect(RecievingCharacter,Effect.StatusEffect,Effect.StatusNext)
                        else:
                            AddStatusEffect(DealingCharacter,Effect.StatusEffect,Effect.StatusNext)
                else:
                    Chance2 *= Effect.Modifier
                    if Effect.DamageTypeStagger == True:
                        StaggerEffectModifier += Chance2
                    else:
                        HealthEffectModifier += Chance2
                    
            #exceptions, shouldnt break with 0 min 0 max 0 mod
            if Effect.name == "Scars":
                Chance2 = random.randint(1, 5)
                if Chance2 == 5:
                    SmokeModifier = 0 #a way to do negation but works
                    
                #20% negation chance
                    
    for Effect in DealingCharacter.StatusEffects:  
        if Effect.Trigger == "Dealt":
            ActivatePassive = False
            if Effect.Type == "All":
                ActivatePassive = True
            elif Effect.Type == "Offensive":
                if type == "slash" or type == "blunt" or type == "pierce":
                    ActivatePassive = True
            elif Effect.Type == "Defensive":
                if type == "evade" or type == "block":
                    ActivatePassive = True
            elif Effect.Type == "Slash":
                if type == "slash":
                    ActivatePassive = True
            elif Effect.Type == "Blunt":
                if type == "blunt":
                    ActivatePassive = True
            elif Effect.Type == "Pierce":
                if type == "pierce":
                    ActivatePassive = True
            elif Effect.Type == "Block":
                if type == "block":
                    ActivatePassive = True
            elif Effect.Type == "Evade":
                if type == "evade":
                    ActivatePassive = True
                        
            if ActivatePassive:
                print("triggering dealt passive " + Effect.name)
                Chance2 = random.randint(Effect.Min, Effect.Max)
                
                if Effect.StatusEffect != None:
                    print("Passive Status creator is inflicting in combat:" + str(Chance2) + Effect.StatusEffect)
                    for Count in range(Chance2):
                        if Effect.StatusEffectToSelf:
                            AddStatusEffect(DealingCharacter,Effect.StatusEffect,Effect.StatusNext)
                        else:
                            AddStatusEffect(RecievingCharacter,Effect.StatusEffect,Effect.StatusNext)
                else:
                    Chance2 *= Effect.Modifier
                    if Effect.DamageTypeStagger == True:
                        StaggerEffectModifier += Chance2
                    else:
                        HealthEffectModifier += Chance2
                    
            #exceptions, shouldnt break with 0 min 0 max 0 mod  
            if Effect.name == "Ashes":
                #40% chance to gain non stackable Offensive dice inflict 1 burn 
                Chance = random.randint(1, 10)    
                if Chance <= 4:
                    FoundAshBoost = False
                    for Suspect in DealingCharacter.StatusEffects: #non stackable check for already present
                        if Suspect.name == "Dormant Ash Boost":
                            FoundAshBoost = True
                    if FoundAshBoost == False:
                        print("adding Dormant ash boost") #I would love to use addpassive but this needs to be impermanent
                        AddPassiveEffect(DealingCharacter,"Dormant Ash Boost")

                        UpdateStatusEffects(DealingCharacter)

            elif Effect.name == "Ash Boost":
                print("burning with ash boost")
                AddStatusEffect(RecievingCharacter,"Burn",False)
                
            elif Effect.name == "Pale Hands":
                #adds effect and removals all from all else, 3 stax = 3-10 stagger 
                for Character in AllFightingCharacters:
                    if Character != RecievingCharacter: #dont check me
                        for Suspect in Character.StatusEffects: #custom contains bc they are not actually the same across all
                            if Suspect.name == "Pale Combo":
                                RemoveStatusEffect(Suspect,Character.StatusEffects)
                FoundCombo = None
                print("length of status to look through is: " + str(len(RecievingCharacter.StatusEffects)))
                for FindIt in RecievingCharacter.StatusEffects:
                    print("Findit is: " + FindIt.name)
                    if FindIt.name == "Pale Combo":
                        FoundCombo = FindIt
                        
                if FoundCombo != None:
                    print("increased pale combo")
                    FoundCombo.Count += 1
                    UpdateStatusEffects(RecievingCharacter)
                    if FoundCombo.Count >= 3:
                        Chance2 = random.randint(3, 10)
                        StaggerEffectModifier += Chance2
                        RemoveStatusEffect(FoundCombo,RecievingCharacter.StatusEffects)
                        UpdateStatusEffects(RecievingCharacter)
                        
                else:
                    print("added pale combo")
                    EffectIcon = Group()
                    EffectIcon.Trigger = None
                    EffectIcon.RemovalTrigger = None
                    EffectIcon.Removal = "Full"
                    EffectIcon.name = "Pale Combo"
                    EffectIcon.Count = 1
                    EffectIcon.BaseEffect = False
                    Symbol = Rect(0,0,15,15,fill="white",border = "black")
                    EffectIcon.add(Symbol)
                    EffectIcon.Text = Label("1",10,10)
                    EffectIcon.add(EffectIcon.Text)
                    RecievingCharacter.StatusEffects.append(EffectIcon)
                    print("length of status is now: " + str(len(RecievingCharacter.StatusEffects)))
                    RecievingCharacter.add(EffectIcon)
                    UpdateStatusEffects(RecievingCharacter)
    
    FinalPhysDamage = int(((Damage * HealthResModifier) + HealthEffectModifier) * SmokeModifier)
    FinalStaggerDamage = int(Damage * StaggerResModifier) + StaggerEffectModifier
    
    if FinalPhysDamage <= 0:
        print("Fully negated phys dmg")
    else:
        RecievingCharacter.Health -= FinalPhysDamage
        if RecievingCharacter.Health <= 0:
            for Count in range(3):
                AddEmotion(DealingCharacter,True)
        for count in range(FinalPhysDamage):
            CreateParticle(RecievingCharacter.CharacterSprite.centerX,RecievingCharacter.CharacterSprite.centerY,5,"red")
        
    if FinalStaggerDamage <= 0:
        print("Fully negated stagger dmg")
    else:
        RecievingCharacter.Stagger -= FinalStaggerDamage
        for count in range(FinalStaggerDamage):
            CreateParticle(RecievingCharacter.CharacterSprite.centerX,RecievingCharacter.CharacterSprite.centerY,5,"yellow")
    
    if RecievingCharacter.Stagger <= 0 and RecievingCharacter.Staggered != True:
        RecievingCharacter.Stagger = 0
        GainLight(DealingCharacter)
    HitDirection = 0
    Displacement = RecievingCharacter.centerX - DealingCharacter.centerX
    if Displacement > 0:
        HitDirection = 1
    else: 
        HitDirection = -1
    RecievingCharacter.centerX += HitDirection * Damage * 10
    UpdateBars(RecievingCharacter)

def CalculatePhysResistence(Character,type,IsStagger):
    ModifierNumber = 0
    if not IsStagger:
        if type == "slash":
            ModifierNumber = Character.ResistanceList[0]
        elif type == "pierce":
            ModifierNumber = Character.ResistanceList[1]
        elif type == "blunt":
            ModifierNumber = Character.ResistanceList[2]
    else:
        if type == "slash":
            ModifierNumber = Character.ResistanceList[3]
        elif type == "pierce":
            ModifierNumber = Character.ResistanceList[4]
        elif type == "blunt":
            ModifierNumber = Character.ResistanceList[5]
        
    if ModifierNumber == 2:
        ModifierValue = 2
    elif ModifierNumber == 1:
        ModifierValue = 1.5
    elif ModifierNumber == 0:
        ModifierValue = 1
    elif ModifierNumber == -1:
        ModifierValue = .5
    elif ModifierNumber == -2:
        ModifierValue = .25
    elif ModifierNumber == -3:
        ModifierValue = 0
    
    if Character.Staggered:
        ModifierValue = 2
        
    return ModifierValue
    
def Stagger(Character):
    for Effect in Character.StatusEffects:
        if Effect.BaseEffect == False and Effect.Trigger == "Staggered":
            print("triggering a stagger passive: " + Effect.name)
            if Effect.name == "Scorched Girl Clumsy":
                Character.Light = 0
                FixLightSpritePositions(Character)

    for Die in Character.SpeedDice:
        if Die.HeldPage != None:
            #RestorePage(Die.HeldPage)
            Die.HeldPage.visible = False
            #UntargetSpeedDie(Die)
            Die.ConnectedCharacter.Light += Die.HeldPage.cost
            ResolveAndRemovePage(Die)
            
            if Die.TargettingLine != None:
                Die.TargettingLine.visible = False
        Die.TargetDie = None
    Character.Staggered = True
        
def KillCharacter(Character):
    print("killing: " + Character.name)
    
    DissapearCharacter(Character, True)
    
    #hides the hand library and graveyard
    for Card in (Character.Library + Character.Hand + Character.Graveyard):
        Card.visible = False
    
    #removes dice from their ally list for targetting
    for DeadDie in Character.SpeedDice:
        DeadSpeedDice.append(DeadDie)
        
        if Character.ControlledByPlayer:
            PlayerSpeedDice.remove(DeadDie)
            print("removing a player die")
        else:
            EnemySpeedDice.remove(DeadDie)
    
    #removed from fight
    AllFightingCharacters.remove(Character)
    
    #hides the info board
    Character.AdditionalInfoBoard.visible = False
    
    #death particles
    for count in range(30):
        CreateParticle(Character.CharacterSprite.centerX,Character.CharacterSprite.centerY,8,"red")
    
    #adds emotions to allies
    for FightCharacter in AllFightingCharacters:
        if Character.ControlledByPlayer == FightCharacter.ControlledByPlayer:
            for Count in range(3):
                AddEmotion(FightCharacter,False)

    #resolves death trigger passives
    for EachCharacter in AllFightingCharacters:
        if EachCharacter != Character:
            for Effect in EachCharacter.StatusEffects:
                if Effect.BaseEffect == False and Effect.Trigger == "Death":
                    if Effect.Type == "All" or (Effect.Type == "Ally" and EachCharacter.ControlledByPlayer == Character.ControlledByPlayer) or Effect.Type == "Enemy" and EachCharacter.ControlledByPlayer != Character.ControlledByPlayer:
                        print("Death trigger passive activating: " + Effect.name)
                        if Effect.name == "Scorched Girl Mourn":
                            EachCharacter.Health -= EachCharacter.MaxHealth / 2
                            EachCharacter.Stagger = 0
                            UpdateBars(EachCharacter)

                
    
    #adds to dead
    DeadCharacters.append(Character)
    #removes cards from hand and graveyard to put in library
    ResetCharacterLibrary(Character)
    #checks if all of one side died
    if len(PlayerSpeedDice) == 0:
        FightEnd(False)
    elif len(EnemySpeedDice) == 0:
        FightEnd(True)

def UpdateBars(Character):
    
    MaxHealth = Character.MaxHealth
    MaxStagger = Character.MaxStagger

        
    if Character.Health > 0:
        Character.HealthBar.width = Character.Health / MaxHealth * 40
        Character.HealthBar.opacity = 100
        Character.HealthBarText.opacity = 100
    else:
        Character.HealthBar.opacity = 0
        Character.HealthBarText.opacity = 0
    
    Character.HealthBar.right = Character.CharacterSprite.centerX
    Character.HealthBar.centerY = Character.CharacterSprite.centerY + 40
    
    Character.HealthBarText.value = Character.Health
    Character.HealthBarText.centerY = Character.HealthBar.centerY
    Character.HealthBarText.centerX = Character.HealthBar.centerX

    if Character.Stagger > 0:
        Character.StaggerBar.width = Character.Stagger / MaxStagger * 40
        Character.StaggerBar.opacity = 100
        Character.StaggerBarText.opacity = 100
    else:
        #stagger <= 0
        Character.StaggerBar.opacity = 0
        Character.StaggerBarText.opacity = 0
        Stagger(Character)
        for Die in Character.SpeedDice:
            Die.TargetDie = None
        for Card in (Character.Library + Character.Hand + Character.Graveyard):
            Card.visible = False
        
        print(Character.name + " was Staggered")
                
        
    Character.StaggerBar.left = Character.CharacterSprite.centerX
    Character.StaggerBar.centerY = Character.CharacterSprite.centerY + 40

    Character.StaggerBarText.value = Character.Stagger
    Character.StaggerBarText.centerY = Character.StaggerBar.centerY
    Character.StaggerBarText.centerX = Character.StaggerBar.centerX

def UpdateStatusEffects(Character):
    AllStatusEffects = Character.StatusEffects + Character.NextTurnStatusEffects
    StartX = Character.CharacterSprite.centerX - (10 * len(AllStatusEffects))
    StartY = Character.CharacterSprite.centerY + 60
    for Effect in AllStatusEffects:
        Effect.centerX = StartX
        Effect.centerY = StartY
        Effect.Text.value = str(Effect.Count)
        StartX += 20
        
def UpdateDamageRange(Die):
    
    if Die.min + Die.MinModifier > Die.max + Die.MaxModifier:
        if Die.max + Die.MaxModifier < 0:
            Die.DamageRangeText.value = str(0) + "-" + str(0)
        else:
            Die.DamageRangeText.value = str(Die.max + Die.MaxModifier) + "-" + str(Die.max + Die.MaxModifier)
    else:
        if Die.max + Die.MaxModifier < 0:

            Die.DamageRangeText.value = str(0) + "-" + str(0)
        else:
            if Die.min + Die.MinModifier < 0:
                Die.DamageRangeText.value = str(0) + "-" + str(Die.max + Die.MaxModifier)
            else:
                Die.DamageRangeText.value = str(Die.min + Die.MinModifier) + "-" + str(Die.max + Die.MaxModifier)

def ParseForDescription(String,Trigger,Target):
    
    OriginalText = String
    Description = ""
    Potency = 1
    NextTurnActivate = False
    Description += Trigger
    
    if OriginalText.startswith("Effect"):
        OriginalText = OriginalText[6:]
        
    if OriginalText.startswith("Reduce"):
        OriginalText = OriginalText[6:]

    StartChar = OriginalText[0:1]
    if StartChar.isdigit():
        Potency = int(StartChar)
        OriginalText = OriginalText[1:]
        
    if OriginalText.startswith("All"):
        OriginalText = OriginalText[3:]
        if OriginalText.startswith("Players"):
            OriginalText = OriginalText[7:]
            Target = "AllPlayers"
        if OriginalText.startswith("Enemies"):
            OriginalText = OriginalText[7:]
            Target = "AllEnemies"
        
    
    if OriginalText.startswith("Next"):
        NextTurnActivate = True
        OriginalText = OriginalText[4:]

    if Target == "Enemy":
        Description += " Inflict"
    elif Target == "Self":
        Description += " Gain"
    elif Target == "AllPlayers":
        Description += " Give all Allies"
        
    if OriginalText == "Gain Light":
        Description += " " + str(Potency) + " Light"
    else:
        Description += " " + str(Potency) + " " + OriginalText
    if NextTurnActivate:
        Description += " Next Turn"
    else:
        Description += " This Turn"
    
    return Description
    
def CardPartition(String):
    PartitionedDescription = []
    if len(String) > 14:

        PrevSentence = ""
        NextWord = ""
        while len(String) > 0: #this needs to change so we stop losing final word / sentence
            NextWord = ""
            while not String.startswith(" ") and len(String) > 0:
                NextWord = NextWord + String[0:1]
                String = String[1:]
            #print(len(PrevSentence))
            if len(PrevSentence + NextWord) < 14:
                if len(PrevSentence) > 0:
                    #print("adding a word to the sentence: ")
                    PrevSentence = PrevSentence + " " + NextWord
                else:
                    PrevSentence = NextWord

                String = String[1:]
            else:
                Piece = Label(PrevSentence,0,0,fill = "yellow",size = 8) #sentence is full so finish it and start a new one
                PartitionedDescription.append(Piece)
                #print("Overflowing into next sentence with " + NextWord +"fin")
                PrevSentence = NextWord
        
        Piece = Label(PrevSentence,0,0,fill = "yellow",size = 8) #final sentence bc we were losing words
        PartitionedDescription.append(Piece)

    else:
        FinalPiece = Label(String,0,0,fill = "yellow",size = 8)
        PartitionedDescription.append(FinalPiece)
        
    return PartitionedDescription

def RefreshResistances(Character):
    
    index = 0
    for Text in Character.AdditionalInfoBoard.TextList:
        ResValue = Character.ResistanceList[index]
        ResTextVal = ""
        if ResValue == 2:
            ResTextVal = "Fatal"
        elif ResValue == 1:
            ResTextVal = "Weak"
        elif ResValue == 0:
            ResTextVal = "Normal"
        elif ResValue == -1:
            ResTextVal = "Endured"
        elif ResValue == -2:
            ResTextVal = "Ineffective"
        elif ResValue == -3:
            ResTextVal = "Immune"
        else:
            print("MASSIVE ERROR failed to find type sprite resistance 2")
        
        Text.value = ResTextVal
        
        index += 1

def ResetAllCharacterPositions():
    print("resetting characters")
    for Character in AllFightingCharacters:
        Character.centerX = Character.StartX
        Character.centerY = Character.StartY
        
        if Character.ClearStaggered == True:
            Character.Staggered = False
            Character.ClearStaggered = False
            Character.Stagger = Character.MaxStagger
            UpdateBars(Character)
        elif Character.Stagger <= 0:
            Character.ClearStaggered = True
            
        CheckForEmotionLevelup(Character)
            
        ShowCharacterUI(Character)
        if Character.Staggered != True and app.RoundNum != 0 and app.PlayerConfirmStage != 7:
            GainLight(Character)
            FixLightSpritePositions(Character)
        
        for Die in Character.SpeedDice:
            NewDiceText = str(Die.min) + "-" + str(Die.max)
            Die.ConnectedText.value = NewDiceText
            Die.TargetDie = None
            if Die.HeldPage != None:
                print("why the heck are there still pages")
                UntargetSpeedDie(Die)
        
        if len(Character.UnusedDice) > 0:
            print("I have extra dice")
            ClearExtraDice(Character)
            
        RemovalList = []
        
        for StatusEffect in Character.StatusEffects: #end of turn resolving effects
            if StatusEffect.Trigger == "EndTurn":
                print("EOT trigger: " + StatusEffect.name + " for " + str(StatusEffect.Count))
                Character.Health -= StatusEffect.Count
                UpdateBars(Character)
            if StatusEffect.RemovalTrigger == "EndTurn":
                if StatusEffect.Removal == "Full":
                    StatusEffect.Count = 0
                elif StatusEffect.Removal == "1/3":
                    StatusEffect.Count = int((2/3) * StatusEffect.Count)
                elif StatusEffect.Removal == "-1":
                    StatusEffect.Count -= 1
                elif StatusEffect.Removal == "Fairy":
                    Character.Health -= StatusEffect.Count
                    StatusEffect.Count = int((1/2) * StatusEffect.Count)
                elif StatusEffect.Removal == "Dormant Ash":
                    if StatusEffect.name == "Dormant Ash Boost":
                        StatusEffect.name = "Ash Boost"
                        StatusEffect.fill = "red"
                    else:
                        StatusEffect.Count = 0
                elif StatusEffect.Removal == "Matchlight Reset":
                    StatusEffect.UsedCards.clear()

            if StatusEffect.Count == 0:
                RemovalList.append(StatusEffect)
                
        for GoneEffect in RemovalList:
            RemoveStatusEffect(GoneEffect,Character.StatusEffects)
            
        for StatusEffect in Character.NextTurnStatusEffects:
            for count in range(StatusEffect.Count):
                AddStatusEffect(Character,StatusEffect.name,False)
        
        RemovalList = list(Character.NextTurnStatusEffects)
        
        for GoneEffect in RemovalList:
            RemoveStatusEffect(GoneEffect,Character.NextTurnStatusEffects)
        UpdateStatusEffects(Character)
                
        FixUpCharacter(Character)
        
    #check for team level ups
    NumOfCharacters = 0
    TotalPositive = 0
    TotalNegative = 0
    for Character in AllFightingCharacters:
        if Character.ControlledByPlayer:
            NumOfCharacters += 1
            AllCoins = Character.EmotionCoins + Character.BankedEmotionCoins
            for Coin in AllCoins:
                if Coin == True:#checks if the coins is positive
                    TotalPositive += 1
                else:
                    TotalNegative += 1
    
    EmotionalRequirement = 3 * NumOfCharacters
    index = 1
    for Count in range(app.CurrentTeamEmotionLevel): #adds additional req accounting for banked
        EmotionalRequirement += NumOfCharacters * (3 + 2 * index)
        index += 1
    print("emotional req for team level is " + str(EmotionalRequirement))
    if TotalPositive + TotalNegative >= EmotionalRequirement:
        print("Team emotional level up to " + str(app.CurrentTeamEmotionLevel + 1))
        LevelUpTeamEmotionLevel(TotalPositive,TotalNegative)
    

def CheckForEmotionLevelup(Character):
    
    #print (str(len(Character.EmotionCoins)) + " coins vs possible: " + str(len(Character.EmotionBarList)))
    if len(Character.EmotionCoins) >= len(Character.EmotionBarList) - 1: #-1 bc the text is included in length
        EmotionLevelUp(Character)
        if Character.EmotionLevel == 3 or Character.EmotionLevel == 4:
            print("add a die from emotion level up")
            #add a die
        #at emotion 5 draw extra card

        
def LevelUpTeamEmotionLevel(TotalPositive,TotalNegative):
    #it is actually 3 levels not 5 with 1-2 = level 1  3-4 = level 2 5 = level3
    if app.CurrentTeamEmotionLevel == 0 or app.CurrentTeamEmotionLevel == 1:
        EmotionOptions = app.CurrentFloor.EmotionPayoffs[0]
    elif app.CurrentTeamEmotionLevel == 2 or app.CurrentTeamEmotionLevel == 3:
        EmotionOptions = app.CurrentFloor.EmotionPayoffs[1]
    elif app.CurrentTeamEmotionLevel == 5:
        EmotionOptions = app.CurrentFloor.EmotionPayoffs[2]
    
    if TotalPositive + TotalNegative > 0:

        Chance = random.randint(0,TotalPositive + TotalNegative)

        if len(EmotionOptions) > 0:
            DisplayedOptions = []
            PositiveList = []
            NegativeList = []
            for Option in EmotionOptions:
                if not Contains(app.ChosenAbnoPages,Option):
                    if Option.Positive:
                        PositiveList.append(Option)
                    else:
                        NegativeList.append(Option)
                        

            for RunItThrice in range(3):
                if len(PositiveList) <= 0 and len(NegativeList) <= 0:
                    print("failed to find abno")
                elif (Chance <= TotalPositive and len(PositiveList) >= 0) or len(NegativeList) <= 0: #checks if positive or a list is running out
                    print("positive abno")
                    Chance2 = random.randint(0,len(PositiveList) - 1)
                    DisplayedOptions.append(PositiveList[Chance2])
                    PositiveList.remove(PositiveList[Chance2])
                    
                else:
                    print("negative abno")
                    Chance2 = random.randint(0,len(NegativeList) - 1)
                    DisplayedOptions.append(NegativeList[Chance2])
                    NegativeList.remove(NegativeList[Chance2])
            
            DisplayAbnoOptions(DisplayedOptions)
            
    app.CurrentTeamEmotionLevel += 1

def DisplayAbnoOptions(ListedOptions):
    NumOfOptions = len(ListedOptions)
    print("this many options of abno pages: " + str(NumOfOptions))
    app.PlayerConfirmStage = 7
    PageWidth = 400 * app.XScreenDialation / NumOfOptions
    StartX = 0
    Background = Rect(0,0,400 * app.XScreenDialation,400 * app.YScreenDialation)
    Background.Text = Label("",0,0)
    Background.Type = "Locked"
    app.TemporaryButtons.append(Background)

    for AbnoPage in ListedOptions:
        Page = Group()
        Outline = Rect(StartX,50 * app.YScreenDialation,PageWidth,300 * app.YScreenDialation)
        if AbnoPage.Positive:
            Outline.fill = "green"
            Outline.border = "darkGreen"
        else:
            Outline.fill = "red"
            Outline.border = "darkRed"
        Outline.borderWidth = 8
        Page.add(Outline)
        Title = Label(AbnoPage.name,Outline.centerX,100 * app.YScreenDialation,size = 20 * app.XScreenDialation)
        Page.add(Title)
        TargetTitle = Label("Idk Target",Outline.centerX,130 * app.YScreenDialation,size = 18 * app.XScreenDialation)
        if AbnoPage.SingleTarget:
            TargetTitle.value = "Single target"
        else:
            TargetTitle.value = "World Effect"
        Outline.Text = Group(Title,TargetTitle)
        PartitionedText = CardPartition(AbnoPage.Description)
        StartY = 160 * app.YScreenDialation
        for Line in PartitionedText:
            #Textline = Label(Line,Outline.centerX,StartY)
            Line.size = 16 * app.YScreenDialation
            Line.centerX = Outline.centerX
            Line.centerY = StartY
            StartY += 12 * app.YScreenDialation
            Page.add(Line)
            Outline.Text.add(Line)
        
        Outline.Type = "Page"
        Outline.ConnectedPage = AbnoPage
        app.TemporaryButtons.append(Outline)
        StartX += PageWidth


def RemoveStatusEffect(Effect,List):
    Effect.visible = False
    List.remove(Effect)
                
def ResetCharacterLibrary(Character):
    for Die in Character.SpeedDice:
        if Die.HeldPage != None:
            UntargetSpeedDie(Die)
    for Card in Character.Hand:
        Character.Library.append(Card)
    Character.Hand.clear()
    
    GraveyardToLibrary(Character)
    
def Contains(List,Item):
    Result = False
    for Element in List:
        if Element == Item:
            Result = True
    return Result
    
def AttackAnimation(Action, Character):
    Particle = None
    if Action == "slash":
        Particle = Arc(0,0,80,20,0,180)
        Particle.centerX = Character.centerX
        Particle.centerY = Character.centerY
    if Action == "blunt":
        Particle = Star(0,0,15,8)
        Particle.centerX = Character.centerX
        Particle.centerY = Character.centerY
    if Action == "pierce":
        Particle = Polygon(0,0,40,10,0,20)
        Particle.centerX = Character.centerX
        Particle.centerY = Character.centerY
    if Action == "block":
        Particle = Rect(0,0,16,80)
        if Character.FacingLeft:
            Particle.right = Character.left
        else:
            Particle.left = Character.right
            
        Particle.centerY = Character.centerY
    if Action == "evade":
        if Character.FacingLeft:
            Character.centerX += 15
        else:
            Character.centerX -= 15
           
    if Particle != None:
        if Character.FacingLeft == True:
            Particle.rotateAngle += 180
            Particle.XVel = -1
        else:
            Particle.XVel = 1
            
        Particle.Fade = 20
        Particle.YVel = 0
        Particle.Rotation = 0
        Particle.fill = "white"
        app.FadingParticles.append(Particle)
    
def CreateParticle(x,y,size,color):
    Particle = Rect(0,0,size,size,fill = color)
    Particle.centerX = x
    Particle.centerY = y
    Particle.Rotation = random.randint(-10, 10)
    Particle.XVel = random.randint(-10, 10)
    Particle.YVel = random.randint(-10, 10)
    Particle.Fade = 2
    app.FadingParticles.append(Particle)
    
def UpdateResolution():
    Background = Rect(0,0,app.width,app.height,fill="burlywood")
    app.XScreenDialation = app.width / 400
    app.YScreenDialation = app.height / 400
    app.BlackScreen = Rect(0,0,app.width,app.height,visible = False)
    app.GamoverText = Label("Game Over",app.width/2,app.height/2, fill = "white",visible = False, size = 20)
    app.WinText = Label("You Win",app.width/2,app.height/2, fill = "white",visible = False, size =20)
    app.ContinueText = Label("Press Space To Continue",app.width/2,app.height/2 + 50 * app.YScreenDialation, fill = "white",visible = False)

#right now things;
#make sprites for brothers, chefs, hooks, matches, scorched girl
#make scroll in progression tree
#next stages are chef office, into forsaken murderer and lulu office

# also fix random target to be smarter and Chef officers to have their actual decks

#far off
#have character's page be clickable to go into attribution

#polish
#also maybe new card / new fight reminder icons for main menu
#add instructions, make set positions template
#fix fixupcharacter is an acceptable bug for now
#also add a rules page, and maybe eventually a save code system
#wording for regain health die effects is kinda wacky so fix later?

#also cards can be found easily on https://projectmoon.miraheze.org/wiki/Cards_(Library_of_Ruina)
# type: python LibraryOfRuin.py to run
cmu_graphics.run() #runs fine without on home comp but needed for school comp