import json, os, random, time, random

currentRoom = None


#Inventory Class
class Inventory:

  def __init__(self, inventory):
    self.inventory = inventory


#Load in a new game from an existing game file
def loadNewGame(fileName):
  directoryPath = os.getcwd()

  #Delete the current unsaved game files
  delDir = f"{directoryPath}/running_game_data/rooms"
  for f in os.listdir(delDir):
    os.remove(os.path.join(delDir, f))

  delDir = f"{directoryPath}/running_game_data/items"
  for f in os.listdir(delDir):
    os.remove(os.path.join(delDir, f))

  #Grab the game file and start copying over files into the active game
  #Open the room file for looping and copying
  roomDirectory = os.listdir(
    f"{directoryPath}/games/{fileName}/resources/rooms")
  print(roomDirectory)

  #create the new room data by transcribing the json files from the base save in the main game file
  for item in roomDirectory:
    appendFile = open(f"{directoryPath}/running_game_data/rooms/{item}", "w")
    copyFile = open(f"{directoryPath}/games/{fileName}/resources/rooms/{item}",
                    "r")
    appendFile.write("")
    appendFile.write(copyFile.read())
    appendFile.close()
    copyFile.close()

  #Transcribing Item Data
  itemDirectory = os.listdir(
    f"{directoryPath}/games/{fileName}/resources/items")
  print(itemDirectory)

  #create the new item data by transcribing the json files from the base save in the main game file
  for item in itemDirectory:
    appendFile = open(f"{directoryPath}/running_game_data/items/{item}", "w")
    copyFile = open(f"{directoryPath}/games/{fileName}/resources/items/{item}",
                    "r")
    appendFile.write("")
    appendFile.write(copyFile.read())
    appendFile.close()
    copyFile.close()

  #Transcribing Cutscene Data
  itemDirectory = os.listdir(
    f"{directoryPath}/games/{fileName}/resources/cutscenes")
  print(itemDirectory)

  #create the new cutscene data by transcribing the json files from the base save in the main game file
  for item in itemDirectory:
    appendFile = open(f"{directoryPath}/running_game_data/cutscenes/{item}",
                      "w")
    copyFile = open(
      f"{directoryPath}/games/{fileName}/resources/cutscenes/{item}", "r")
    appendFile.write("")
    appendFile.write(copyFile.read())
    appendFile.close()
    copyFile.close()
  #for item in


#testing loading in new games
loadNewGame("test_game")

#Item list
itemlist = []
#Cutscene list
cutscenelist = []

#Setting up player inventory
playerInventory = Inventory([])
itemPickedUp = False


class Item():

  def __init__(self, name, description, type, usemessages):
    self.name = name
    self.description = description
    self.type = type
    self.usemessages = usemessages

  def type():
    return (type)


class Cutscene():

  def __init__(self, scenes, trigger, attr, chance, waitTime, doOnce,
               timesRan):
    self.scenes = scenes
    self.trigger = trigger
    self.attr = attr
    self.chance = chance
    self.waitTime = waitTime
    self.doOnce = doOnce
    self.timesRan = timesRan

  def runScenes(self):
    for item in self.scenes:
      if item.split("-")[0] == "player_give:":
        playerInventory.inventory.append(int(item.split("-")[1]))
      elif item.split("-")[0] == "player_remove:":
        if int(item.split("-")[1]) in playerInventory.inventory:
          playerInventory.inventory.pop(int(item.split("-")[1]))
      elif item.split("-")[0] == "room_exit_append:":
        currentRoom["exits"].append([item.split("-")[1], item.split("-")[2]])
      elif item.split("-")[0] == "player_moveto:":
        currentRoom = loadRoom(item.split("-")[1])
        roomfilename = item.split("-")[1]
      else:
        print(self.scenes[self.scenes.index(item)])
      time.sleep(self.waitTime)


#Load in cutscenes from a cutscene set
def loadCutscenes(cutsceneSet):
  print(f"Initiating the loading of the cutscene set {cutsceneSet}")
  #Get the filepath of the cutscene set
  directoryPath = os.getcwd()
  cutsceneDirectory = open(
    f"{directoryPath}/running_game_data/cutscenes/{cutsceneSet}.json", "r")
  cutsceneListDic = json.load(cutsceneDirectory)
  print(cutsceneListDic)
  #Load all the cutscenes from the set of cutscenes
  for item in cutsceneListDic["cutscenelist"]:
    cutsceneFile = open(
      f"{directoryPath}/running_game_data/cutscenes/{item}.json")
    cutsceneJson = json.load(cutsceneFile)
    cutscenelist.append(
      Cutscene(cutsceneJson["scenes"], cutsceneJson["trigger"],
               cutsceneJson["attr"], cutsceneJson["chance"],
               cutsceneJson["waitTime"], cutsceneJson["doOnce?"], 0))
  return cutscenelist


#Grabs the json file of a wanted room from the rooms directory and transform that into a dic object for further use
def loadRoom(roomName):
  #Grab the file path of the directory so the function can function in all computers
  directoryPath = os.getcwd()
  roomFileName = roomName
  #Open the file in the predetermined file path
  roomFile = open(
    f"{directoryPath}/running_game_data/rooms/{roomFileName}.json", "r")
  #Transcribe the json file in the secondary memory to the main memory in the form of a dic object
  roomJson = json.load(roomFile)
  roomFile.close()
  #Return the dic object
  return (roomJson)


#Loading in items from the item directory
def loadItems(itemSet):
  print(f"Initiating the loading of item set {itemSet}")
  #Get the file path to the itemset
  directoryPath = os.getcwd()
  itemDirectory = open(
    f"{directoryPath}/running_game_data/items/{itemSet}.json", "r")
  itemListDic = json.load(itemDirectory)
  print(itemListDic)
  #Load all the item in from the item set.
  for item in itemListDic['itemlist']:
    itemFile = open(f"{directoryPath}/running_game_data/items/{item}.json")
    itemJson = json.load(itemFile)
    itemlist.append(
      Item(itemJson["name"], itemJson["description"], itemJson["type"],
           itemJson["usemessages"]))
  return (itemlist)


#Load in all the cutscenes from a set of cutscenes
#def loadCutScenes()

itemlist = loadItems("main_itemset")
cutscenelist = loadCutscenes("main_cutsceneset")

#Settup main vars
currentRoom = loadRoom("bloodied_street")
roomfilename = "bloodied_street"
playerconsoleinput = ""
playerinventory = []
playerconsoleinterpation = []
roomexitkeys = []
roomexitlist = []

#Credits
print("---Interperated by IntFic---")
#Main Game Loop
while True:
  textcutscenedone = 0
  #Cycle through the list of cutscenes and run any cutscenes if possible
  for item in cutscenelist:
    chance = random.randint(1,
                            int(cutscenelist[cutscenelist.index(item)].chance))
    if chance == 1:
      if cutscenelist[cutscenelist.index(item)].trigger == "entry":
        if cutscenelist[cutscenelist.index(item)].attr == roomfilename:
          if cutscenelist[cutscenelist.index(item)].doOnce == 1:
            if cutscenelist[cutscenelist.index(item)].timesRan == 0:
              cutscenelist[cutscenelist.index(item)].runScenes()
              cutscenelist[cutscenelist.index(item)].timesRan += 1
          else:
            cutscenelist[cutscenelist.index(item)].runScenes()
            cutscenelist[cutscenelist.index(item)].timesRan += 1

      if cutscenelist[cutscenelist.index(item)].trigger == "item":
        if cutscenelist[cutscenelist.index(
            item)].attr in playerInventory.inventory:
          if cutscenelist[cutscenelist.index(item)].doOnce == 1:
            if cutscenelist[cutscenelist.index(item)].timesRan == 0:
              cutscenelist[cutscenelist.index(item)].runScenes()
              cutscenelist[cutscenelist.index(item)].timesRan += 1
          else:
            cutscenelist[cutscenelist.index(item)].runScenes()
            cutscenelist[cutscenelist.index(item)].timesRan += 1

  #Grab and parse player console input
  playerconsoleinput = input(">> ")
  playerconsoleinterpation = playerconsoleinput.split(" ")

  #Cycle through all the cutscenes in search of certain ones that need player input
  for item in cutscenelist:
    chance = random.randint(1,
                            int(cutscenelist[cutscenelist.index(item)].chance))
    if chance == 1:
      if cutscenelist[cutscenelist.index(item)].trigger == "player_input":
        if cutscenelist[cutscenelist.index(item)].attr == playerconsoleinput:
          if cutscenelist[cutscenelist.index(item)].doOnce == 1:
            if cutscenelist[cutscenelist.index(item)].timesRan == 0:
              cutscenelist[cutscenelist.index(item)].runScenes()
              cutscenelist[cutscenelist.index(item)].timesRan += 1
              textcutscenedone = 1
          else:
            cutscenelist[cutscenelist.index(item)].runScenes()
            cutscenelist[cutscenelist.index(item)].timesRan += 1
            textcutscenedone = 1

  #movement function
  if playerconsoleinterpation[0] == "move":
    #Grab the keys in currentRoom exits just do grab the exits
    roomexitkeys = []
    if len(playerconsoleinterpation) >= 2:
      #Get an ordered list of the dictionary inputs
      for item in currentRoom["exits"]:
        roomexitlist = list(item)
        roomexitkeys.append(roomexitlist[0])

      #Join together rest of interpation
      playerconsoleinterpation.pop(0)
      itemtargetstring = " ".join(playerconsoleinterpation)
      #Check if the exit the player wants is available
      if itemtargetstring in roomexitkeys:
        #Load the next room after printing the move message associated with the path
        roomfilename = currentRoom["exits"][roomexitkeys.index(
          itemtargetstring)][roomexitkeys[roomexitkeys.index(
            itemtargetstring)]]
        print(currentRoom["exits"][roomexitkeys.index(itemtargetstring)]
              ["message"])
        currentRoom = loadRoom(
          currentRoom["exits"][roomexitkeys.index(itemtargetstring)][
            roomexitkeys[roomexitkeys.index(itemtargetstring)]])
      else:
        print(f"{itemtargetstring} is not a valid exit.")
    else:
      print(f"You need to move somewhere!")

  #Use item function
  elif playerconsoleinterpation[0] == "use":
    if len(playerconsoleinterpation) >= 2:
      del playerconsoleinterpation[0]
      playerItemUseTarget = " ".join(playerconsoleinterpation)
      playerItemUseTarget = playerItemUseTarget.title()
      itemused = False
      for item in cutscenelist:
        chance = random.randint(
          1, int(cutscenelist[cutscenelist.index(item)].chance))
        if cutscenelist[cutscenelist.index(item)].trigger == "use_item":
          if cutscenelist[cutscenelist.index(
              item)].attr in playerInventory.inventory or cutscenelist[
                cutscenelist.index(item)].attr in currentRoom["objects"]:
            if itemlist[cutscenelist[cutscenelist.index(
                item)].attr].name == playerItemUseTarget:
              if cutscenelist[cutscenelist.index(item)].doOnce == 1:
                if cutscenelist[cutscenelist.index(item)].timesRan == 0:
                  cutscenelist[cutscenelist.index(item)].runScenes()
                  cutscenelist[cutscenelist.index(item)].timesRan += 1
                  itemused = True
              else:
                cutscenelist[cutscenelist.index(item)].runScenes()
                cutscenelist[cutscenelist.index(item)].timesRan += 1
                itemused = True
      if itemused == False:
        print("I can't use this item")
    else:
      print("You need an item to use.")

  #Look Function
  elif playerconsoleinterpation[0] == "look":
    if len(playerconsoleinterpation) >= 2:
      if playerconsoleinterpation[1] == "around":
        print(
          f"You are in {currentRoom['name']}. {currentRoom['description']}")
        if len(currentRoom["objects"]) >= 1:
          print(f"On the floor you see:")
          for item in currentRoom['objects']:
            print(f"  {itemlist[item].name}")
        else:
          print("There is nothing on the floor.")
        if len(currentRoom['exits']) >= 1:
          print(f"Exits: ")
          for item in currentRoom["exits"]:
            print(item)
        else:
          print("There are no exits to your knowledge.")
      if playerconsoleinterpation[1] == "inventory":
        if len(playerInventory.inventory) > 0:
          playerInventory.inventory.sort()
          print("In your inventory you see:")
          for item in playerInventory.inventory:
            print(f"  {itemlist[item].name}")
        else:
          print("There is nothing in your inventory.")
    else:
      print("Enter a valid thing to look at.")

  #Pickup Item Function
  elif playerconsoleinterpation[0] == "get":
    itemPickedUp = False
    if len(playerconsoleinterpation) >= 2:
      #Get a string name for an item
      playerconsoleinterpation.pop(0)
      playerItemGetTarget = " ".join(playerconsoleinterpation)
      playerItemGetTarget = playerItemGetTarget.title()
      for item in itemlist:
        if item.name == playerItemGetTarget:
          if itemlist.index(item) in currentRoom["objects"]:
            itemPickedUp = True
            print(f"You pick up the {item.name}.")
            currentRoom["objects"].pop(itemlist.index(item))
            playerInventory.inventory.append(itemlist.index(item))
            break
      if itemPickedUp == False:
        print(f"{playerItemGetTarget} is not an available item to pick up.")
    else:
      print(f"You need to have a target item to grab.")

  #Drop Item Function
  elif playerconsoleinterpation[0] == "drop":
    itemDropped = False
    if len(playerconsoleinterpation) >= 2:
      #Get string name
      playerconsoleinterpation.pop(0)
      playerItemDropTarget = " ".join(playerconsoleinterpation)
      playerItemDropTarget = playerItemDropTarget.title()
      for item in itemlist:
        if item.name == playerItemDropTarget:
          if itemlist.index(item) in playerInventory.inventory:
            itemDropped = True
            print(f"You drop the {item.name}.")
            playerInventory.inventory.pop(itemlist.index(item))
            currentRoom["objects"].append(itemlist.index(item))
            break
      if itemDropped == False:
        print(f"{playerItemGetTarget} is not an available item to drop.")
    else:
      print("You need an item to drop.")

  #Clear Console Command
  elif playerconsoleinterpation[0] == "clear":
    os.system('clear')

  #Reaction if no action is put in
  else:
    if textcutscenedone == 0:
      list = ["What?", "Huh?", "Hm?", "Wie bitte?!"]
      randomNum = random.randint(0, len(list) - 1)
      print(list[randomNum])

  #Return the dictionary room to the file room and reload it to save room updates
  directoryPath = os.getcwd()
  returnRoomFile = open(
    f"{directoryPath}/running_game_data/rooms/{roomfilename}.json", "w")
  json.dump(currentRoom, returnRoomFile)
  returnRoomFile.close()
  currentRoom = loadRoom(roomfilename)
