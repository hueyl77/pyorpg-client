import time

from network.database import *
from constants import *
import global_vars as g

########
# CHAT #
########

def addText(text, color):
    g.gameEngine.graphicsEngine.gameGUI.guiContainer.chatCtrl.addText(str(text), color)


def handleMsg(text):
        msg = text.lower()

        ''' global msg '''
        if msg[0] == '"':
            if getPlayerAccess(g.myIndex) >= ADMIN_MAPPER:
                msg = msg[1:len(msg)]

                if len(msg) > 0:
                    g.tcpConn.globalMsg(msg)

                return

        if msg[0] == "/":
            command = msg.split()

            if command[0] == "/help":
                addText("Social Commands:", helpColor)
                addText("  'msghere = Broadcast Message", helpColor)
                addText("  -msghere = Emote Message", helpColor)
                addText("  !namehere msghere = Player Message", helpColor)
                addText("Available Commands: /help, /info, /who, /fps, /inv, /stats, /train, /trade, /party, /join, /leave, /resetui", helpColor)

            if command[0] == "/info":
                if len(command) <= 1:
                    addText("Usage: /info (name)", alertColor)
                    return

                if command[1].isdigit():
                    addText("Usage: /info (name)", alertColor)
                    return

                g.tcpConn.sendInfoRequest(command[1])

            ''' who's online '''
            if command[0] == "/who":
                g.tcpConn.sendWhosOnline()

            ''' show/hide fps '''
            if command[0] == "/fps":
                g.boolFPS = not g.boolFPS

            ''' show inventory '''
            if command[0] == "/inv":
                g.gameEngine.graphicsEngine.gameGUI.setUIState(1)  # GUI_INVENTORY = 1


            #################
            # MONITOR ADMIN #
            #################

            ''' shows a list of admin commands '''
            if command[0] == "/admin":
                if getPlayerAccess(g.myIndex) < ADMIN_MONITOR:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                addText("Social Commands:", helpColor)
                addText('  ""msghere = Global Admin Message', helpColor)
                addText("  =msghere  = Private Admin Message", helpColor)
                addText("  !namehere msghere = Player Message", helpColor)
                addText("Available Commands: /admin, /loc, /mapeditor, /warpmeto, /warptome, /warpto, /setsprite, /giveitem, /mapreport, /kick, /ban, /edititem, /respawn, /editnpc, /motd, /editshop, /editspell, /debug", helpColor)

            if command[0] == "/kick":
                if getPlayerAccess(g.myIndex) < ADMIN_MONITOR:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                if len(command) <= 1:
                    addText("Usage: /kick (name)", alertColor)
                    return

                if command[1].isdigit():
                    addText("Usage: /kick (name)", alertColor)
                    return

                # sendKick

            ################
            # MAPPER ADMIN #
            ################

            ''' displays the current location (x, y, map id) '''
            if command[0] == "/loc":
                if getPlayerAccess(g.myIndex) < ADMIN_MAPPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                g.boolLoc = not g.boolLoc

                # draw location tile

            ''' enables the map editor '''
            if command[0] == "/mapeditor":
                if getPlayerAccess(g.myIndex) < ADMIN_MAPPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                g.tcpConn.sendRequestEditMap()

            if command[0] == "/warpmeto":
                if getPlayerAccess(g.myIndex) < ADMIN_MAPPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                if len(command) <= 1:
                    addText("Usage: /warpmeto (name)", alertColor)
                    return

                if command[1].isdigit():
                    addText("Usage: /warpmeto (name)", alertColor)
                    return

                playerName = command[1]
                g.tcpConn.warpMeTo(playerName)

            if command[0] == "/warptome":
                if getPlayerAccess(g.myIndex) < ADMIN_MAPPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                if len(command) <= 1:
                    addText("Usage: /warptome (name)", alertColor)
                    return

                if command[1].isdigit():
                    addText("Usage: /warptome (name)", alertColor)
                    return

                playerName = command[1]
                g.tcpConn.warpToMe(playerName)

            if command[0] == "/warpto":
                if getPlayerAccess(g.myIndex) < ADMIN_MAPPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                if len(command) <= 1:
                    addText("Usage: /warpto (map #)", alertColor)
                    return

                if not command[1].isdigit():
                    addText("Usage: /warpto (map #)", alertColor)
                    return

                n = int(command[1])

                if n > 0 and n <= MAX_MAPS:
                    # warpTo
                    g.tcpConn.warpTo(n)
                else:
                    addText("Invalid map number.", textColor.RED)

            ''' sets the admin sprite '''
            if command[0] == "/setsprite":
                if getPlayerAccess(g.myIndex) < ADMIN_MAPPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                if len(command) <= 1:
                    addText("Usage: /setsprite (sprite #)", alertColor)
                    return

                if not command[1].isdigit():
                    addText("Usage: /setsprite (sprite #)", alertColor)
                    return

                g.tcpConn.sendSetSprite(int(command[1]))

            if command[0] == "/mapreport":
                if getPlayerAccess(g.myIndex) < ADMIN_MAPPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                g.tcpConn.sendMapReport()

            if command[0] == '/respawn':
                if getPlayerAccess(g.myIndex) < ADMIN_MAPPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                g.tcpConn.sendMapRespawn()

            ###################
            # DEVELOPER ADMIN #
            ###################

            ''' enables the map editor '''
            if command[0] == "/itemeditor":
                if getPlayerAccess(g.myIndex) < ADMIN_DEVELOPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                g.tcpConn.sendRequestEditItem()

            ''' enables the npc editor '''
            if command[0] == '/npceditor':
                if getPlayerAccess(g.myIndex) < ADMIN_DEVELOPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                g.tcpConn.sendRequestEditNpc()

            ''' gives an item to a player '''
            if command[0] == '/giveitem':
                if getPlayerAccess(g.myIndex) < ADMIN_DEVELOPER:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                if len(command) < 2:
                    addText('usage: /giveitem <name> <itemnum>', alertColor)
                    return

                if command[1].isdigit() or not command[2].isdigit():
                    addText('usage: /giveitem <name> <itemnum>', alertColor)
                    return

                g.tcpConn.sendGiveItem(command[1], int(command[2]))

            #################
            # CREATOR ADMIN #
            #################

            if command[0] == '/setaccess':
                if getPlayerAccess(g.myIndex) < ADMIN_CREATOR:
                    addText("You need to be a high enough staff member to do this!", alertColor)
                    return

                if len(command) < 2:
                    addText('usage: /setaccess <name> <access>', alertColor)
                    return

                if command[1].isdigit() or not command[2].isdigit():
                    addText('usage: /setaccess <name> <access>', alertColor)
                    return

                g.tcpConn.sendSetAccess(command[1], int(command[2]))

            return


        ''' say message '''
        if len(text) > 0:
            g.tcpConn.sayMsg(text)

########
# GAME #
########

def processMovement(index):
    ''' checks if Player[index] is walking - if so, move them over '''

    if Player[index].moving == MOVING_WALKING:
        movementSpeed = WALK_SPEED
    elif Player[index].moving == MOVING_RUNNING:
        movementSpeed = RUN_SPEED

    direction = getPlayerDir(index)
    if direction == DIR_UP:
        Player[index].yOffset = Player[index].yOffset - movementSpeed

    elif direction == DIR_DOWN:
        Player[index].yOffset = Player[index].yOffset + movementSpeed

    elif direction == DIR_LEFT:
        Player[index].xOffset = Player[index].xOffset - movementSpeed

    elif direction == DIR_RIGHT:
        Player[index].xOffset = Player[index].xOffset + movementSpeed

    # check if on new tile
    if Player[index].xOffset == 0:
        if Player[index].yOffset == 0:
            Player[index].moving = 0

def processNPCMovement(mapNpcNum):
    ''' check if npc is walking and if so, move them '''
    npcDir = mapNPC[mapNpcNum].dir

    if npcDir == DIR_UP:
        mapNPC[mapNpcNum].yOffset = mapNPC[mapNpcNum].yOffset - WALK_SPEED
    elif npcDir == DIR_DOWN:
        mapNPC[mapNpcNum].yOffset = mapNPC[mapNpcNum].yOffset + WALK_SPEED
    elif npcDir == DIR_LEFT:
        mapNPC[mapNpcNum].xOffset = mapNPC[mapNpcNum].xOffset - WALK_SPEED
    elif npcDir == DIR_RIGHT:
        mapNPC[mapNpcNum].xOffset = mapNPC[mapNpcNum].xOffset + WALK_SPEED

    # check if on new tile
    if mapNPC[mapNpcNum].xOffset == 0:
        if mapNPC[mapNpcNum].yOffset == 0:
            mapNPC[mapNpcNum].moving = False


def isTryingToMove():
    if g.inpDIR_UP or g.inpDIR_DOWN or g.inpDIR_LEFT or g.inpDIR_RIGHT:
        return True
    else:
        return False

def checkAttack():
    if g.inpCTRL == True:
        if Player[g.myIndex].attackTimer + 1 < time.time():
            if Player[g.myIndex].attacking == 0:
                Player[g.myIndex].attacking = 1
                Player[g.myIndex].attackTimer = time.time()

                g.tcpConn.sendPlayerAttack()

def canMove():
    d = getPlayerDir(g.myIndex)

    # make sure they aren't already trying to move
    if Player[g.myIndex].moving != 0:
        return False

    if g.inpDIR_UP:
        setPlayerDir(g.myIndex, DIR_UP)

        # check if out of bounds
        if getPlayerY(g.myIndex) > 0:
            if checkDirection(DIR_UP):
                if d != DIR_UP:
                    g.tcpConn.sendPlayerDir()
                
                return False
        else:
            if Map.up > 0:
                #mapEditorLeaveMap
                g.tcpConn.sendPlayerRequestNewMap()
                g.gettingMap = True
                g.canMoveNow = False

            return False

    if g.inpDIR_DOWN:
        setPlayerDir(g.myIndex, DIR_DOWN)
        
        if getPlayerY(g.myIndex) < MAX_MAPY - 1: #TODO: FIX
            if checkDirection(DIR_DOWN):
                if d != DIR_DOWN:
                    g.tcpConn.sendPlayerDir()
                
                return False
        else:
            if Map.down > 0:
                #mapEditorLeaveMap
                g.tcpConn.sendPlayerRequestNewMap()
                g.gettingMap = True
                g.canMoveNow = False
            return False

    if g.inpDIR_LEFT:
        setPlayerDir(g.myIndex, DIR_LEFT)

        if getPlayerX(g.myIndex) > 0:
            if checkDirection(DIR_LEFT):
                if d != DIR_LEFT:
                    g.tcpConn.sendPlayerDir()
                
                return False
        else:
            if Map.left > 0:
                #mapEditorLeaveMap
                g.tcpConn.sendPlayerRequestNewMap()
                g.gettingMap = True
                g.canMoveNow = False
            return False

    if g.inpDIR_RIGHT:
        setPlayerDir(g.myIndex, DIR_RIGHT)

        if getPlayerX(g.myIndex) < MAX_MAPX - 1: #TODO: FIX
            if checkDirection(DIR_RIGHT):
                if d != DIR_RIGHT:
                    g.tcpConn.sendPlayerDir()
                
                return False
        else:
            if Map.right > 0:
                #mapEditorLeaveMap
                g.tcpConn.sendPlayerRequestNewMap()
                g.gettingMap = True
                g.canMoveNow = False
            return False

    return True

def checkDirection(direction):
    if direction == DIR_UP:
        x = getPlayerX(g.myIndex)
        y = getPlayerY(g.myIndex) - 1

    elif direction == DIR_DOWN:
        x = getPlayerX(g.myIndex)
        y = getPlayerY(g.myIndex) + 1

    elif direction == DIR_LEFT:
        x = getPlayerX(g.myIndex) - 1
        y = getPlayerY(g.myIndex)

    elif direction == DIR_RIGHT:
        x = getPlayerX(g.myIndex) + 1
        y = getPlayerY(g.myIndex)

    # check if map tile is blocked
    if Map.tile[x][y].type == TILE_TYPE_BLOCKED:
        return True

    # check if player is on tile
    for i in range(len(g.playersOnMap)):
        if getPlayerX(g.playersOnMap[i]) == x:
            if getPlayerY(g.playersOnMap[i]) == y:
                return True

    return False

def checkMovement():
    if isTryingToMove():
        if canMove():
            Player[g.myIndex].moving = MOVING_WALKING

            direction = getPlayerDir(g.myIndex)

            if direction == DIR_UP:
                g.tcpConn.sendPlayerMove()
                Player[g.myIndex].yOffset = PIC_Y
                setPlayerY(g.myIndex, getPlayerY(g.myIndex) - 1)

            if direction == DIR_DOWN:
                g.tcpConn.sendPlayerMove()
                Player[g.myIndex].yOffset = -PIC_Y
                setPlayerY(g.myIndex, getPlayerY(g.myIndex) + 1)

            if direction == DIR_LEFT:
                g.tcpConn.sendPlayerMove()
                Player[g.myIndex].xOffset = PIC_X
                setPlayerX(g.myIndex, getPlayerX(g.myIndex) - 1)

            if direction == DIR_RIGHT:
                g.tcpConn.sendPlayerMove()
                Player[g.myIndex].xOffset = -PIC_X
                setPlayerX(g.myIndex, getPlayerX(g.myIndex) + 1)

            if Player[g.myIndex].xOffset == 0:
                if Player[g.myIndex].yOffset == 0:
                    if Map.tile[getPlayerX(g.myIndex)][getPlayerY(g.myIndex)].type == TILE_TYPE_WARP:
                        g.gettingMap = True

    if Map.tile[getPlayerX(g.myIndex)][getPlayerY(g.myIndex)].type == TILE_TYPE_WARP:
        #print "cannot move (todo)"
        g.canMoveNow = False


def checkMapGetItem():
    if time.time() * 1000 > Player[g.myIndex].mapGetTimer + 250:
        # todo: check if chat is empty
        if g.gameEngine.graphicsEngine.gameGUI.guiContainer.chatCtrl.chatMsg.value == '':
            Player[g.myIndex].mapGetTimer = time.time() * 1000
            g.tcpConn.sendMapGetItem()


def updateInventory():
    # redraw the inventory interface
    print "todo"

def getPlayersOnMap():
    g.playersOnMap = []

    for i in range(0, len(Player)):
        if isPlaying(i):
            if getPlayerMap(i) == getPlayerMap(g.myIndex):
                g.playersOnMap.append(i)


def clearTempTile():
    for x in range(MAX_MAPX):
        for y in range(MAX_MAPY):
            TempTile[x][y].doorOpen = 0

def calcTilePositions():
    for x in range(MAX_MAPX):
        for y in range(MAX_MAPY):
            MapTilePosition[x][y].x = x * PIC_X
            MapTilePosition[x][y].y = y * PIC_Y

            if Map.tile[x][y].ground != None:
                MapTilePosition[x][y].ground.top    = (Map.tile[x][y].ground // TILESHEET_WIDTH) * PIC_Y
                MapTilePosition[x][y].ground.left   = (Map.tile[x][y].ground % TILESHEET_WIDTH) * PIC_X
                MapTilePosition[x][y].ground.width  = PIC_X
                MapTilePosition[x][y].ground.height = PIC_Y

            if Map.tile[x][y].fringe != None:
                MapTilePosition[x][y].fringe.top    = (Map.tile[x][y].fringe // TILESHEET_WIDTH) * PIC_Y
                MapTilePosition[x][y].fringe.left   = (Map.tile[x][y].fringe % TILESHEET_WIDTH) * PIC_X
                MapTilePosition[x][y].fringe.width  = PIC_X
                MapTilePosition[x][y].fringe.height = PIC_Y


def initMapData():
    # calculate amount of npcs on map
    g.npcHighIndex = 0
    for i in range(MAX_MAP_NPCS):
        if Map.npc[i] != None:
            g.npcHighIndex += 1

    calcTilePositions()

# should be in clienttcp.bas
def isPlaying(index):
    if len(getPlayerName(index)) > 0:
        return True

# should be in handledata
def needMap():
    g.tcpConn.sendNeedMap()