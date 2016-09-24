import random
import time
from GameFunctions import *
from Character import *
import os


# default naming scheme
#    Functions/Methods are camel case starting on second word(doSomethingFunction, doSomethingMethod, etc)
#    Variables are underscore spaced and all lower case ( variable_one, variable_two, etc)
#    ONLY GAME PHASE VARIABLE IS ALL UPPERCASE

def DEBUG_PRINT_INVENTORY(character):
    print('%s INVENTORY' % character.name)
    for item in character.inventory_items:
        print(item.__dict__)
        print('')
    print('%s EQUIPMENT' % character.name)
    for slot in character.equipment_items:
        print(slot + ': ' + str(character.equipment_items[slot].__dict__))

"""----------------------------------------------------------------------------------------------------------------------------------
    GLOBAL VARIABLES
----------------------------------------------------------------------------------------------------------------------------------"""
current_game_phase = "INTRO" # game phase, used to determine what game loop you will be in. [ INTRO, ACTION, BATTLE ]
current_dungeon_floor = 1 # TODO create actual map for navigating floors and have use for floor variable
current_dungeon_floor_type = "Cave" # TODO create actual impact from floor type in battle or stat buffs/nerfs due to environment

Player = PlayerCharacter('player_name')
Player_Companions = [] # TODO maybe change Player into an array and just have the player's main character as always index 1 and remove this array to store companions

player_game_records = {'monsters_killed'      : 0,
                       'items_used'           : 0,
                       'items_crafted'        : 0,
                       'damage_dealt'         : 0,
                       'damage_received'      : 0,
                       'battles_fought'       : 0,
                       'battles_fled'         : 0,
                       'companions_recruited' : 0,
                       'companions_died'      : 0,}

enemy_holder_one   = Character()
enemy_holder_two   = Character()
enemy_holder_three = Character()
Enemy = [enemy_holder_one, enemy_holder_two, enemy_holder_three] # TODO make Enemy into an array of EnemyCharacter's, allowing for more group on group battling, remember to go through code and change to reflect that Enemy would be an array of EnemyCharacter's



battle_time_delay = 2 # time the console pauses during battle sequences

Turn = 1 # turn 

current_player_turn = '' # current characters turn in battle
starting_player_turn = '' # who's the first character to engage

"""----------------------------------------------------------------------------------------------------------------------
    DISPLAY PLAYER STATS / EXAMINE ITEM / DISPLAY INVENTORY CATEGORY / MANAGE INVENTORY MENU
---------------------------------------------------------------------------------------------------------------------"""
def displayPlayerStats():  # Display player's character stats # TODO create better interface to show player stats, think about what is important to show and what would just be clutter which would be better somewhere else
    """
    When called, will print the stats block for the player character. Will show all major attributes, level, name, class specific
    debuffs and buffs.
    """
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('||    Name: %s' % Player.name)
    gameFormatPrint('||        Hp: %i / %i ' % (Player.hp['current'], Player.hp['max']))
    gameFormatPrint('||        %s: %i / %i' % (Player.ability_resource_name, Player.ability_resource_amount, Player.ability_resource_amount_max))
    gameFormatPrint('||    Combat Stats:')
    gameFormatPrint('||        Defence: %i' % Player.defence['current'])
    gameFormatPrint('||        Damage:  %i (Weapon: %s)' % (Player.equipment_items['primary'].damage, Player.equipment_items['primary'].name))
    gameFormatPrint('\|_____________________________________________________________|/')
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('||')
    gameFormatPrint('||    Class: %s' % Player.class_type)

    # Check if attributes have been reduced below their respective max value if so, show current value and max value, else just show current value # TODO reduce to for statement to reduce code and increase readability
    if Player.attributes['vitality']['current'] != Player.attributes['vitality']['max']:
        gameFormatPrint('||        > Vitality:     %i / %i' % (Player.attributes['vitality']['current'], Player.attributes['vitality']['max']))
    else:
        gameFormatPrint('||        > Vitality:     %i' % Player.attributes['vitality']['current'])

    if Player.attributes['strength']['current'] != Player.attributes['strength']['max']:
        gameFormatPrint('||        > Strength:     %i / %i' % (Player.attributes['strength']['current'], Player.attributes['strength']['max']))
    else:
        gameFormatPrint('||        > Strength:     %i' % Player.attributes['strength']['current'])

    if Player.attributes['perception']['current'] != Player.attributes['perception']['max']:
        gameFormatPrint('||        > Perception:   %i / %i' % (Player.attributes['perception']['current'], Player.attributes['perception']['max']))
    else:
        gameFormatPrint('||        > Perception:   %i' % Player.attributes['perception']['current'])

    if Player.attributes['endurance']['current'] != Player.attributes['endurance']['max']:
        gameFormatPrint('||        > Endurance:    %i / %i' % (Player.attributes['endurance']['current'], Player.attributes['endurance']['max']))
    else:
        gameFormatPrint('||        > Endurance:    %i' % Player.attributes['endurance']['current'])

    if Player.attributes['intelligence']['current'] != Player.attributes['intelligence']['max']:
        gameFormatPrint('||        > Intelligence: %i / %i' % (Player.attributes['intelligence']['current'], Player.attributes['intelligence']['max']))
    else:
        gameFormatPrint('||        > Intelligence: %i' % Player.attributes['intelligence']['current'])

    if Player.attributes['speed']['current'] != Player.attributes['speed']['max']:
        gameFormatPrint('||        > Speed:        %i / %i' % (Player.attributes['speed']['current'], Player.attributes['speed']['max']))
    else:
        gameFormatPrint('||        > Speed:        %i' % Player.attributes['speed']['current'])

    if Player.attributes['dexterity']['current'] != Player.attributes['dexterity']['max']:
        gameFormatPrint('||        > Dexterity:    %i / %i' % (Player.attributes['dexterity']['current'], Player.attributes['dexterity']['max']))
    else:
        gameFormatPrint('||        > Dexterity:    %i' % Player.attributes['dexterity']['current'])

        gameFormatPrint('||')
        gameFormatPrint('||    Primary:    %s' % Player.main_attribute)
        gameFormatPrint('||    Diminished: %s' % Player.nerf_attribute)
        gameFormatPrint('||')
        gameFormatPrint('||    Level: %i' % Player.level)
        gameFormatPrint('||    Experience: %i / %i' % (Player.experience['current'], Player.experience['needed']))
        gameFormatPrint('||     ' + createProgressBar(Player.experience['current'], Player.experience['needed'], 50))
        gameFormatPrint('\|_____________________________________________________________|/')


def examineItem(item):
    print('')
    printContentToCommandLine('[EXAMINE_HEADER]')
    gameFormatPrint('||    Name: %s' % item.name)
    gameFormatPrint('||    Category: %s' % item.category)
    gameFormatPrint('||    Weight: ' + '{:.2f}'.format(item.weight) + ' lbs')
    gameFormatPrint('||    Value: %i' % item.value)
    gameFormatPrint('||')
    if item.category == 'consumable':
        gameFormatPrint('||    Affects: %s' % item.stat_to_nourish)
        gameFormatPrint('||    Amount Restored: %i' % item.nourish_amount)
    elif item.category == 'equipment':
        if item.equipment_type == 'weapon':
            gameFormatPrint('||    Type: %s' % item.equipment_type)
            gameFormatPrint('||    Damage: %i' % item.damage)
            gameFormatPrint('||    Durability: %i' % item.durability)
            gameFormatPrint('||     ' + createProgressBar(item.durability, item.durability_max, 50))
            gameFormatPrint('||    Is Two Handed: ' + str(item.is_two_handed))
        else:
            gameFormatPrint('||    Slot: %s' % item.equipment_type)
            gameFormatPrint('||    Defence: %i' % item.defence)
        gameFormatPrint('||    Material: %s' % item.material)
        gameFormatPrint('||    Durability: %i' % item.durability)
    gameFormatPrint('||')
    name_to_file_name = item.name.upper()
    name_to_file_name = name_to_file_name.replace(' ', '_')
    printContentToCommandLine('[' + name_to_file_name + '_EXAMINE]', search_file='.\GameTextFiles\ItemDesc')


def displayItemCategory(category):
    """
        When called, will search through the player's inventory for all items that have their category set to the 'category' argument and print the info block
        containing them all.
    """
    item_count = 0  # get amount of items in player inventory that are of the type 'category'
    for item in Player.inventory_items:
        if item.category == category:
            item_count += 1

    if item_count > 0:  # if there is at least 1 item that is of the 'category' type in player inventory print segment
        printContentToCommandLine('[' + category.upper() + '_HEADER]')
        for item in Player.inventory_items:
            if item.category == category:
                if category == 'equipment':
                    item_equipment_type = item.equipment_type

                    if item.is_equipped:
                        gameFormatPrint('||   > ' + item.name + ' :: >-EQUIPPED-<')
                    else:
                        gameFormatPrint('||   > ' + item.name)

                    if item_equipment_type == 'weapon':
                        gameFormatPrint('||        > Damage   - ' + '{:,}'.format(item.damage))
                    gameFormatPrint('||        > Defence  - ' + '{:,}'.format(item.defence))
                    gameFormatPrint('||        > Durability - ' + '{:,}'.format(item.durability))
                    gameFormatPrint('||        > Material - %s' % item.material)
                    gameFormatPrint('||        > Type - %s' % item.equipment_type)
                    gameFormatPrint('||        > Two Handed - %s' % item.is_two_handed)
                    gameFormatPrint('||        > Is Equipped - ' + str(item.is_equipped))
                else:
                    gameFormatPrint('||    ' + item.name + ' :: Amount > ' + '{:,}'.format(item.stack))

                total_item_weight = item.weight * item.stack
                if total_item_weight != 0:
                    gameFormatPrint('||        > Weight - ' + '{:.2f}'.format(total_item_weight) + ' lbs')
        gameFormatPrint('\|_____________________________________________________________|/')


def managePlayerInventory():
    while True: # Keep looping through a players input til they input something we can use

        displayItemCategory('common')
        # -----------------------------------------------------------------------------------------------------------------
        displayItemCategory('consumable')
        # -----------------------------------------------------------------------------------------------------------------
        displayItemCategory('crafting')
        # -----------------------------------------------------------------------------------------------------------------
        displayItemCategory('equipment')
        # -----------------------------------------------------------------------------------------------------------------
        displayItemCategory('quest')
        # ----------------------------------------------------------------------------------------------------------------
        printContentToCommandLine('[INVENTORY_STATS]')
        Player.updateInventoryWeight() # update 'current' and 'max' player inventory weight
        gameFormatPrint('||    Total Weight: ' + '{:.2f}'.format(Player.inventory_weight['current']) + ' lbs')
        gameFormatPrint('||    Max Carry Weight: ' + '{:.2f}'.format(Player.inventory_weight['max']) + ' lbs')
        gameFormatPrint('\|_____________________________________________________________|/')
        print('')
        printContentToCommandLine('[MANAGE]')
        print('CHOICE::> ', end='')
        response = input().lower()
        print(response[:7])
        print(response[8:])
        print('')
        if response == 'use': # TODO create use function for items
            print('do stuff \ WIP')
            break
        elif response[:5] == 'equip' or response[:7] == 'unequip':
            if response == 'equip':
                displayItemCategory('equipment')
                printContentToCommandLine('[CHOOSE_EQUIP]')
                print('CHOICE::> ', end='')
                response = input().lower()
                Player.equipItem(Player.getItem(response))
            else:
                Player.equipItem(Player.getItem(response[6:]))
            if response == 'unequip': # TODO make dialog sequence for slow uneequip
                print('stuff happens')
            else:
                Player.unequipItem(Player.getItem(response[8:]))
        elif response == 'craft': # TODO create crafting system
            print('do stuff \ WIP')
            break
        elif response[:7] == 'examine':
            if len(response) == 7: # if the response was just 'examine' go through full examine dialog
                printContentToCommandLine('[EXAMINE_CHOICE]')
                print('CHOICE::> ', end='')
                response = input().lower()
                for item in Player.inventory_items:
                    if response == item.name.lower():
                         
                        examineItem(item)
                        print('')
                        printContentToCommandLine('[MANAGE]')
            else: # else if response was more than just 'examine' such as 'examine leather legs' get string after 'examine' and try looking for it in inventory and displaying its info
                for item in Player.inventory_items:
                    if response[8:] == item.name.lower():
                         
                        examineItem(item)
                        print('')
                        printContentToCommandLine('[MANAGE]')

        elif response == 'return':
             
            break
        else:
            print('Please try again...')


def createMultipleItems(character, item_names, item_amounts): # using 2 lists, 1 for item names and 1 for amounts
    for name, amount in zip(item_names, item_amounts):
        createItem(character, name, amount)


def saveGameConfirmation():
    print('SaveGameConfirmation')
    printContentToCommandLine('[SAVE_CONFIRMATION]')
    valid_responses = {'y', 'yes', 'n', 'no'}
    while True:
        print('CHOICE::> ', end='')
        response = input().lower()
        if response in valid_responses:
            if response == 'y' or response == 'yes':
                saveCharacterFile(Player)
                break
            elif response == 'n' or response == 'no':
                break
        else:
            print('Please try again...')

def quitToMenu():
    global current_game_phase

     
    print('QuitToMenu')
    printContentToCommandLine('[QUIT_TO_MENU_CONFIRMATION]')
    valid_responses = {'y', 'yes', 'n', 'no'}
    while True:
        print('CHOICE::> ', end='')
        response = input().lower()
        if response in valid_responses:
            if response == 'y' or response == 'yes':
                current_game_phase = 'INTRO'
                print('')
                saveGameConfirmation()
                break
            elif response == 'n' or response == 'no':
                current_game_phase = 'INTRO'
                print('')
                break
        else:
            print('Please try again..')

"""----------------------------------------------------------------------------------------------------------------------------------
    MAIN MENU / GET PLAYER NAME / CLASS SELECTION
----------------------------------------------------------------------------------------------------------------------------------"""
# menu method call for new game creation: mainMenu() -> newGameSetup() -> classSelection()
# once in classSelection() will change next game phase to 'ACTION', so after classSelection() game goes into 'ACTION' phase

def mainMenu():
    global current_game_phase
    global battle_time_delay
    global Player # TODO remove this line after game near completion, only hear to allow player creation for test game starts

     
    printContentToCommandLine('[GAME_INFO]')
    acceptable_responses = {'new game', 'load game', 'options', 'exit', 'quit'}
    while True:
        printContentToCommandLine('[INTRO_MENU]')
        print('CHOICE::> ', end='')
        response = input().lower()
        if response in acceptable_responses or response[:11] == 'setup::game': # TODO maybe remove 'or response[:11]' choice after game near completion, only used for quick starting a game with certain conditions for ease sake
            if response == 'new game': # start new game
                newGameSetup()
                break
            elif response == 'load game': # load a game # TODO allow the possibility of actually seeing save games to choose from, need to learn OS module to get save files names
                current_game_phase = 'ACTION'
                print('Still in early stage...not possible to see directory file names yet...for me...')
                print('Type name of character in save you want (case sensitive)')
                response = input()
                loadCharacterFile(response)
                break
            elif response == 'options': # go to options # TODO create options menu, maybe allow different battle speeds, or game difficulty options
                print('current time delay: ' + str(battle_time_delay))
                print('what do you want the time delay at? (1-10 seconds)')
                new_delay = input()
                setGameDelayTime(battle_time_delay, int(new_delay))
                print('show options that will be available')
                print('no options right now...')
                break
            elif response == 'quit' or response == 'exit': # quit game
                quitGameConfirmation()
            elif response[:11] == 'setup::game': # TODO maybe remove this choice after game near completion, only used for quick starting a game with certain conditions for ease sake
                class_choice = response[12:]
                Player = PlayerCharacter('Test_Game_' + response[12:].upper())
                createMultipleItems(Player, ['WOODEN_SHORT_SWORD', 'GOLD_COIN', 'WOOD', 'COAL', 'LEATHER_BODY', 'LEATHER_LEGS', 'TEST_WEAPON'], [1,365,8,12,1,1,1])
                Player.equipItem(Player.getItem('wooden short sword'))
                Player.equipItem(Player.getItem('leather body'))
                Player.class_type = getVarInFile('[' + class_choice + '_ATTRIBUTES]', 'class=')

                attribute_list = Player.attributes.keys() # ['vitality', 'strength', 'perception', 'endurance', 'intelligence', 'speed', 'dexterity']
                for att in attribute_list:
                    Player.setAttribute(att, int(getVarInFile('[' + class_choice + '_ATTRIBUTES]', att + '=')))

                Player.main_attribute = getVarInFile('[' + class_choice + '_ATTRIBUTES]', 'main_attribute=')
                Player.nerf_attribute = getVarInFile('[' + class_choice + '_ATTRIBUTES]', 'nerf_attribute=')

                Player.ability_resource_name = getVarInFile('[' + class_choice + '_ATTRIBUTES]', 'ability_resource_name=')
                Player.ability_resource_amount = Player.attributes[Player.main_attribute]['current'] * 5
                Player.ability_resource_amount_max = Player.ability_resource_amount

                Player.setHp(int(((Player.attributes['vitality']['max'] * .36) * 8) + 50))
                current_game_phase = 'ACTION'
                break
        else:
            print('Please try again..')


def newGameSetup():
    global current_game_phase
    global Player

     
    while True:
        printContentToCommandLine('[INTRO_NAME]')
        print('CHOICE::> ', end='')
        response = input() # don't need to worry about case sensitivity for player names
        name_holder = response

         
        print('/:>------------------------------------------------------------|\\')
        gameFormatPrint('| |    Your name is: ' + response)
        gameFormatPrint('| |    is this correct?')
        print('\|_____________________________________________________________|/')

        print('CHOICE::> ', end='')
        response = input().lower()
        print('')

        if response == 'y' or response == 'yes':
            Player = PlayerCharacter(name_holder) # reinitialize Player character to default status
            current_game_phase = 'ACTION'
            classSelection()
            break


def classSelection():
    global current_game_phase

     
    createMultipleItems(Player, ['GOLD_COIN', 'WOODEN_SHORT_SWORD', 'TEST_WEAPON', 'WOOD'], [200, 2, 1 ,4])


    """
    Here we will create a list of strings to hold the classes the player is able to choose from.
    We will keep looping over the GameInfo.txt file finding all the class names until we run out.
    """
    accepted_responses = [] # will hold all the class names for the player to choose from
    class_number = 1
    while True:
        class_to_add = getVarInFile('[CLASS_CHOICES]', 'class' + str(class_number) + '=')
        if class_to_add != '':
            accepted_responses.append(class_to_add.lower())
            class_number += 1
        else:
            break
    
    # Keep looping through a players input til they input something acceptable
    while True:
        printContentToCommandLine('[CLASS_CHOICE_HEADER]')
        for class_name in accepted_responses:
            printContentToCommandLine('[' + class_name.replace(' ', '_').upper() + '_DESC]')

        print('CHOICE::> ' , end='')
        class_choice = input().lower()

        if class_choice in accepted_responses:

            class_choice_formatted = class_choice.replace(' ', '_').upper() # format class choice string to replace spaces with underscores
                                                                            # since that is the format for headers in GameInfo.txt

            Player.class_type = getVarInFile('[' + class_choice_formatted + '_ATTRIBUTES]', 'class=')
            attribute_list = Player.attributes.keys() # ['vitality', 'strength', 'perception', 'endurance', 'intelligence', 'speed', 'dexterity']

            for att in attribute_list:
                Player.setAttribute(att, int(getVarInFile('[' + class_choice_formatted + '_ATTRIBUTES]', att + '=')))

            Player.main_attribute = getVarInFile('[' + class_choice_formatted + '_ATTRIBUTES]', 'main_attribute=')
            Player.nerf_attribute = getVarInFile('[' + class_choice_formatted + '_ATTRIBUTES]', 'nerf_attribute=')

            Player.ability_resource_name = getVarInFile('[' + class_choice_formatted + '_ATTRIBUTES]', 'ability_resource_name=')
            Player.ability_resource_amount = Player.attributes[Player.main_attribute]['current'] * 5
            Player.ability_resource_amount_max = Player.ability_resource_amount

            Player.setHp(int(((Player.attributes['vitality']['max'] * .36) * 8) + 50))
            break
        else:
             
            print('That is not a a class, try again...')
     

"""----------------------------------------------------------------------------------------------------------------------------------
    MAIN GAME LOOP
----------------------------------------------------------------------------------------------------------------------------------"""

def mainChoiceMenu():
    printContentToCommandLine('[ACTION_PHASE]')
    gameFormatPrint('||    Current floor: ' + str(current_dungeon_floor))
    gameFormatPrint('||    Current floor environment: ' + str(current_dungeon_floor_type))
    print(' \\____________________________________________________________//')
    acceptable_responses = {'stats', 'inventory', 'manage', 'roam', 'down', 'go down', 'up', 'go up', 'save',
                            'save game', 'menu', 'exit', 'quit', 'menu'}
    while True:  # Keep looping through a players input til they input something acceptable
        print('CHOICE::> ', end='')
        response = input().lower()
        print('')
        if response in acceptable_responses:
            if response == 'stats':
                 
                displayPlayerStats()
                break
            elif response == 'inventory' or response == 'manage':
                managePlayerInventory()
                break
            elif response == 'roam':
                print('Roaming..........')
                roamRoom()
                break
            elif response == 'save' or response == 'save game':
                saveGameConfirmation()
            elif response == 'exit' or response == 'quit' or response == 'menu':
                quitToMenu()
                break
            else:
                print('Please try again..')

"""---------------------------------------------------------------------------------------------------------------------------------------------
    INTRO PHASE - LOOP
---------------------------------------------------------------------------------------------------------------------------------------------"""


def introPhase():
    mainMenu()
    print('')


"""---------------------------------------------------------------------------------------------------------------------------------------------
    ACTION PHASE - LOOP
---------------------------------------------------------------------------------------------------------------------------------------------"""


def actionPhase():
    mainChoiceMenu()
    print('')


"""---------------------------------------------------------------------------------------------------------------------------------------------
    BATTLE PHASE - LOOP
---------------------------------------------------------------------------------------------------------------------------------------------"""

def battlePhase(): # TODO figure out way to maybe clean up the attack order
    global Turn
     
    print('TURN:: ' + str(Turn) + ' :: ' + str(current_player_turn) + '\'s turn.')
    if current_player_turn == 'player':
        battleInfoDetailed()
        battlePhasePlayerTurn()
        battlePhaseEnemyTurn()
    else:
        battleInfoDetailed()
        time.sleep(battle_time_delay)
        battlePhaseEnemyTurn()
        battlePhasePlayerTurn()
    Turn += 1

"""---------------------------------------------------------------------------------------------------------------------------------------------
    PLAYER BATTLE TURN / BATTLE CHOICE MENU / ENEMY BATTLE TURN / PLAYER BATTLE INFO / ENEMY BATTLE INFO / BATTLE INFO DETAILED / END BATTLE INFO
---------------------------------------------------------------------------------------------------------------------------------------------"""
def battlePhasePlayerTurn():
    battleChoiceMenu()


def battleChoiceMenu(): # TODO create a cleaner more intuitive interface layout for battle screen
    global Turn
    global current_game_phase
    global current_player_turn
    global Player
    global Enemy

     
    battleInfoDetailed()
    acceptable_responses = {'attack', 'use', 'use item', 'flee', 'run'}
    while True:  # Keep looping through a players input til they input something acceptable

        printContentToCommandLine('[BATTLE_ACTION]')
        print('CHOICE::> ', end='')
        response = input().lower()
        print('')
        if response in acceptable_responses:
            if response == 'attack':
                 
                battleInfoDetailed()
                damage_dealt_by_player = max(int(Player.equipment_items['primary'].damage) - int(Enemy[0].defence['current']), 0)  # simple damage dealt, replace with method to calculate damage once formula made
                player_game_records['damage_dealt'] += damage_dealt_by_player # Add damage dealt this turn to player records
                Enemy[0].hp['current'] = max(Enemy[0].hp['current'] - damage_dealt_by_player, 0)
                print('You attack! >> You deal: ' + str(damage_dealt_by_player) + ' damage!')
                Player.equipment_items['primary'].durability -= Enemy[0].defence['current'] # TODO maybe change the way durability is reduced from attacking an enemy
                if Enemy[0].hp['current'] <= 0:  # player kills enemy
                    print(str(Enemy[0].name) + ' has died!')
                    player_game_records['monsters_killed'] += 1 # Add 1 kill to player records
                    player_game_records['battle_fought'] += 1 # Add 1 battle fought to player records
                    Player.addExperience(Enemy[0].experience_worth)
                    endBattleInfo(Enemy[0].name, Enemy[0].experience_worth)  # call EndBattleInfo
                    Turn = 1
                    current_game_phase = 'ACTION'
                    Enemy[0] = Character() # reinitialize Enemy to default
                else:  # enemy doesn't die from attack
                    current_player_turn = 'enemy'
                    Player.ability_resource_amount = min(Player.ability_resource_amount + (Player.attributes['intelligence']['max'] * .25), Player.ability_resource_amount_max)
                time.sleep(battle_time_delay)
                break
            elif response == 'flee' or response == 'run':  # player attempts to flee
                print('You attempt to flee!') # TODO replace with function that calculates chance of escape
                player_game_records['battles_fled'] += 1 # Add 1 to battles fled in player records
                Enemy[0].wipeInventory()
                print('It was successful!')
                Turn = 1
                current_game_phase = 'ACTION'
                break
        else:
            print('Please try again..')


def battlePhaseEnemyTurn():
    global current_game_phase
    global current_player_turn
    global Turn
     
    if Enemy[0].hp['current'] > 0 and Enemy[0].name != 'character_default':
        battleInfoDetailed()
        damage_dealt_by_enemy =  max(Enemy[0].equipment_items['primary'].damage - Player.defence['current'], 0)
        player_game_records['damage_received'] += damage_dealt_by_enemy # Add damage dealt by enemy this turn to player records
        Player.hp['current'] = max(Player.hp['current'] - damage_dealt_by_enemy, 0)
        print(Enemy[0].name + ' attacks! >> ' + Enemy[0].name + ' deals: ' + str(damage_dealt_by_enemy) + ' damage!')

        if Player.hp['current'] <= 0:
            print('You have Died!')
            playerDiesEndScreen(Enemy[0])
            Turn = 1
            current_game_phase = 'INTRO'
        else:
            current_player_turn = 'player'
        time.sleep(battle_time_delay)


def battleInfoPlayer(): # TODO create better visual/readability to battle information text displayed
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('||    ' + str(Player.name))
    gameFormatPrint('\|_____________________________________________________________|/')
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('||    Hp: %i / %i    Defence: %i' % (Player.hp['current'], Player.hp['max'], Player.defence['current']))
    gameFormatPrint('||    ' + createProgressBar(Player.hp['current'], Player.hp['max'], 50))
    gameFormatPrint('\|_____________________________________________________________|/')
    print('')


def battleInfoEnemy():
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('| |    ' + str(Enemy[0].name))
    gameFormatPrint('\|_____________________________________________________________|/')
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('| |    Hp: %i / %i    Defence: %i' % (Enemy[0].hp['current'], Enemy[0].hp['max'], Enemy[0].defence['current']))
    gameFormatPrint('| |    ' + createProgressBar(Enemy[0].hp['current'], Enemy[0].hp['max'], 50))
    gameFormatPrint('\|_____________________________________________________________|/')
    print('')


def battleInfoDetailed():
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('||    ' + str(Player.name))
    gameFormatPrint('\|_____________________________________________________________|/')
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('||    Hp: %i / %i    Defence: %i' % (Player.hp['current'], Player.hp['max'], Player.defence['current']))
    gameFormatPrint('||    ' + createProgressBar(Player.hp['current'], Player.hp['max'], 50))
    gameFormatPrint('||    Weapon: %s / %i' % (Player.equipment_items['primary'].name, Player.equipment_items['primary'].damage))
    gameFormatPrint('||')
    gameFormatPrint('||    ' + Player.ability_resource_name + ': ' + str(Player.ability_resource_amount) + ' / ' + str(Player.ability_resource_amount_max))
    gameFormatPrint('||    ' + createProgressBar(Player.ability_resource_amount, Player.ability_resource_amount_max, 50))
    gameFormatPrint('\|_____________________________________________________________|/')
    print('')
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('||    ' + str(Enemy[0].name))
    gameFormatPrint('\|_____________________________________________________________|/')
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('||    Hp: ' + str(Enemy[0].hp['current']) + ' / ' + str(Enemy[0].hp['max']))
    gameFormatPrint('||    ' + createProgressBar(Enemy[0].hp['current'], Enemy[0].hp['max'], 50))
    gameFormatPrint('||    Weapon: %s' % Enemy[0].equipment_items['primary'].name)
    gameFormatPrint('\|_____________________________________________________________|/')
    print('')


def endBattleInfo(enemy_defeated, exp_gained):
     
    gameFormatPrint('/:>------------------------------------------------------------|\\')
    gameFormatPrint('||    Enemy killed: ' + enemy_defeated)
    gameFormatPrint('||    Experienced gained: ' + str(exp_gained))
    gameFormatPrint('||    Total experience: ' + str(Player.experience['current']) + ' / ' + str(Player.experience['needed']))
    gameFormatPrint('||     ' + createProgressBar(Player.experience['current'], Player.experience['needed'], 50))
    print('\|_____________________________________________________________|/')

"""---------------------------------------------------------------------------------------------------------------------------------------------
    PLAYER DIES
---------------------------------------------------------------------------------------------------------------------------------------------"""
def playerDiesEndScreen(killing_enemy):
    global current_game_phase
     
    printContentToCommandLine('[GAME_OVER_HEADER]')
    gameFormatPrint('||    %s was killed by level %i %s using %s' % (Player.name, killing_enemy.level, killing_enemy.name, killing_enemy.equipment_items['primary'].name))
    gameFormatPrint('||    Game Statistics:')
    gameFormatPrint('||')
    gameFormatPrint('||        Monsters Killed: %s' % player_game_records['monsters_killed'])
    gameFormatPrint('||        Battles Fought: %s' % player_game_records['battles_fought'])
    gameFormatPrint('||        Battles Fled: %s' % player_game_records['battles_fled'])
    gameFormatPrint('||')
    gameFormatPrint('||        Damage Dealt: %s' % player_game_records['damage_dealt'])
    gameFormatPrint('||        Damage Received: %s' % player_game_records['damage_received'])
    gameFormatPrint('||')
    gameFormatPrint('||        Items Used: %s' % player_game_records['items_used'])
    gameFormatPrint('||')
    gameFormatPrint('||    Do you wish to return to the menu?')
    print('\|_____________________________________________________________|/')
    positive_responses = ['y', 'sure', 'maybe', 'ya', 'okay', 'yes']
    negative_responses = ['n', 'nah', 'no', 'never']
    while True: # Keep looping through a players input til they input something acceptable
        print('CHOICE::> ', end='')
        response = input().lower()
        if response in positive_responses or response in negative_responses:
            if response in positive_responses:
                current_game_phase = 'INTRO'
                break
            elif response in negative_responses:
                quitGameConfirmation()
    else:
        print('Please try again..')

"""---------------------------------------------------------------------------------------------------------------------------------------
    GENERATE ENEMY / ROAM ROOM
---------------------------------------------------------------------------------------------------------------------------------------"""


def generateEnemy(): # TODO flesh out generateEnemy() to take into account dungeon_floor and dungeon_floor_type
    enemy_choice = random.randint(1,3)

    if enemy_choice == 1:
        Enemy[0].name = 'ghoul'
        Enemy[0].species = 'undead'
        Enemy[0].experience_worth = 25
        Enemy[0].setHp(65)
        Enemy[0].setDefence(2)
        Enemy[0].setAttribute('speed', 35)

        """ Create enemy weapon equipment / equip newly created weapon """
        createMultipleItems(Enemy[0], ['FERAL_CLAWS', 'GOLD_COIN'],[1, random.randint(25,75)])
        Enemy[0].equipItem(Enemy[0].getItem('Feral Claws'))
    elif enemy_choice == 2:
        Enemy[0].name = 'bandit'
        Enemy[0].species = 'human'
        Enemy[0].experience_worth = 40
        Enemy[0].setHp(105)
        Enemy[0].setDefence(4)
        Enemy[0].setAttribute('speed', 45)

        """ Create enemy weapon equipment / equip newly created weapon """
        createMultipleItems(Enemy[0], ['WOODEN_SHORT_SWORD', 'GOLD_COIN'],[1, random.randint(50,200)])
        Enemy[0].equipItem(Enemy[0].getItem('Wooden Short Sword'))
    elif enemy_choice == 3:
        Enemy[0].name = 'slime'
        Enemy[0].species = 'monster'
        Enemy[0].experience_worth = 10
        Enemy[0].setHp(15)
        Enemy[0].setDefence(0)
        Enemy[0].setAttribute('speed', 15)

        """ Create enemy weapon equipment / equip newly created weapon """
        createMultipleItems(Enemy[0], ['GEL', 'GOLD_COIN'],[1, random.randint(5,10)])
        Enemy[0].equipItem(Enemy[0].getItem('GEL'))


def roamRoom():
    global current_game_phase
    global current_player_turn
    global starting_player_turn
    encounter_chance = 100 - Player.luck['current'] # percentage an encounter can happen (simple formula: 100 - player's luck stats) # TODO maybe change encounter_chance to rely on more then just the player's luck stat
    encounter_roll = random.randint(1,100)
    if encounter_roll <= encounter_chance: # if we run into an enemy
        print('Enemy encountered!')
        time.sleep(battle_time_delay)
        generateEnemy()  # GenerateEnemy()
        if Player.attributes['speed']['current'] <= Enemy[0].attributes['speed']['current']: # figure out who gets the first turn # TODO maybe change way first turn is given to take into account more then just speed
            current_player_turn = 'enemy'
            starting_player_turn = 'enemy'
        else:
            current_player_turn = 'player'
            starting_player_turn = 'player'
        current_game_phase = "BATTLE"
    else:  # if we don't run into an enemy or find a random encounter # TODO create other events if enemy not found, perhaps finding a secret room, or a chest
        print('Nothing was found.')

        
"""-------------------------------------------------------------------------------------------------------------------------------------------
    HANDLING PHASES
-------------------------------------------------------------------------------------------------------------------------------------------"""
while True:
    while current_game_phase == 'INTRO':
        introPhase()

    while current_game_phase == 'ACTION':
        actionPhase()

    while current_game_phase == 'BATTLE':
        battlePhase()
