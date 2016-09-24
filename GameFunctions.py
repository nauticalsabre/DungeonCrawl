from Item import *


def createItem(character, item_name, amount=1):
    item_to_create_category = getVarInFile('[' + item_name + ']', 'category=', search_file='.\GameTextFiles\Items') # store what type of item we are going to create from finding it's name in the Items.txt file
    
    if item_to_create_category == 'common':
        createCommonItem(character, item_name, amount)
        
    elif item_to_create_category == 'consumable':
        createConsumableItem(character, item_name, amount)

    elif item_to_create_category == 'crafting':
        createCommonItem(character, item_name, amount)
        
    elif item_to_create_category == 'equipment':
        for i in range(amount):
            createEquipmentItem(character, item_name)

    elif item_to_create_category == 'quest':
        createCommonItem(character, item_name, amount)


def createCommonItem(character, item_name, amount):
    new_item = Item(getVarInFile('[' + item_name + ']', 'name=', search_file='.\GameTextFiles\Items'),
                    getVarInFile('[' + item_name + ']', 'category=', search_file='.\GameTextFiles\Items'),
                    float(getVarInFile('[' + item_name + ']', 'weight=', search_file='.\GameTextFiles\Items')),
                    amount,
                    int(getVarInFile('[' + item_name + ']', 'value=', search_file='.\GameTextFiles\Items')))

    character.addToInventory(new_item)


def createConsumableItem(character, item_name, amount):
    new_item = ConsumableItem(getVarInFile('[' + item_name + ']', 'name=', search_file='.\GameTextFiles\Items'),
                              getVarInFile('[' + item_name + ']', 'category=', search_file='.\GameTextFiles\Items'),
                              float(getVarInFile('[' + item_name + ']', 'weight=', search_file='.\GameTextFiles\Items')),
                              amount,
                              int(getVarInFile('[' + item_name + ']', 'value=', search_file='.\GameTextFiles\Items')),
                              getVarInFile('[' + item_name + ']', 'stat_to_nourish=', search_file='.\GameTextFiles\Items'),
                              int(getVarInFile('[' + item_name + ']', 'nourish_amount=', search_file='.\GameTextFiles\Items')))

    character.addToInventory(new_item)

def createEquipmentItem(character, item_name):
    new_item = EquipmentItem(getVarInFile('[' + item_name + ']', 'name=', search_file='.\GameTextFiles\Items'),
                             getVarInFile('[' + item_name + ']', 'category=', search_file='.\GameTextFiles\Items'),
                             float(getVarInFile('[' + item_name + ']', 'weight=', search_file='.\GameTextFiles\Items')),
                             1, # stack will always be 1, but gotta have it like this or things won't line up with the arguments
                             int(getVarInFile('[' + item_name + ']', 'value=', search_file='.\GameTextFiles\Items')),
                             getVarInFile('[' + item_name + ']', 'equipment_type=', search_file='.\GameTextFiles\Items'),
                             int(getVarInFile('[' + item_name + ']', 'damage=', search_file='.\GameTextFiles\Items')),
                             int(getVarInFile('[' + item_name + ']', 'defence=', search_file='.\GameTextFiles\Items')),
                             getVarInFile('[' + item_name + ']', 'material=', search_file='.\GameTextFiles\Items'),
                             int(getVarInFile('[' + item_name + ']', 'durability=', search_file='.\GameTextFiles\Items')))

    character.addToInventory(new_item)

def createProgressBar(current_amount, max_amount, scale, fill_char='»', empty_char='-', end_caps='[]'): # progress bar creator, returns progress bar string
    progress_bar_fill = int((current_amount / max_amount) * scale)
    progress_bar_left = scale - progress_bar_fill
    progress_bar = end_caps[:1]
    for i in range(int(progress_bar_fill)):
        progress_bar += fill_char
    if progress_bar_left != 0:
        for i in range(int(progress_bar_left)):
            progress_bar += empty_char
    progress_bar += end_caps[-1:]
    return progress_bar

def gameFormatPrint(string, string_length=65):
    string_to_format = string
    if len(string_to_format) < string_length:
        length_of_string = len(string_to_format)
        length_left = (string_length - 2) - length_of_string
        for i in range(length_left):
            string_to_format += ' '
        string_to_format += '||'
    print(string_to_format)

def printContentToCommandLine(startKeyWord, endKeyWord='[', search_file='.\GameTextFiles\GameInfo'): # file - name of file without extension, startKeyWord - word to look for to start reading from, endKeyWord - word to look for to stop reading
    foundStart = False
    with open(search_file +'.txt') as file:
        for line in file: # search lines for starting point
            if line.strip('\n') == startKeyWord.upper(): # if we found the start continue
                foundStart = True
            elif foundStart == True and line[0] != endKeyWord and line[0] != '@' and line.strip('\n') != '': # if we found the start and haven't found the end keep printing lines
                print(line.strip('\n'))
            elif foundStart == True and line[0] == endKeyWord: # if we found the start and have reached the end stop reading/printing lines
                break

def getVarInFile(startKeyWord, varName, endKeyWord='[', search_file='.\GameTextFiles\GameInfo'):
    foundStart = False
    temp_string = ''
    with open(search_file + '.txt') as file:
        for line in file: # search lines for starting point

            if line.strip('\n') == startKeyWord.upper(): # if we found the start continue
                foundStart = True
            elif foundStart == True and line[0] != endKeyWord and line[0] != '@' and line.strip('\n') != '': # if we found the start and haven't found the end or a designated comment char check line for var
                if varName in line:
                    temp_string = line.strip('\n')
                    temp_string = temp_string.replace(varName, '')
                    break
            elif foundStart == True and line[0] == endKeyWord: # if we found the start and have reached the end stop reading/printing lines
                break
    return temp_string

def getVarInSaveFile(var_name, save_name):
    format_string = ''
    save_contents = open('.\Saves\SaveFile_' + save_name + '.txt')
    for line in save_contents:
        if var_name in line:
            format_string = line.strip('\n')
            format_string = format_string.replace(var_name, '')
            break
    save_contents.close()
    return format_string


def saveCharacterFile(player): # TODO flesh out function better with more necessary variables, maybe create for statement to reduce code
    saveFile = open('.\Saves\SaveFile_' + player.name + '.txt', 'w')
    saveFile.write('[VARS]\n')
    saveFile.write('name=' + player.name + '\n')
    saveFile.write('characterhp=' + str(player.hp) + '\n')
    saveFile.write('ability_resource_amount=' + str(player.ability_resource_amount) + '\n')
    saveFile.write('vitality=' + str(player.vitality) + '\n')
    saveFile.write('vitality_total=' + str(player.vitality_max) + '\n')
    saveFile.write('dexterity=' + str(player.dexterity) + '\n')
    saveFile.write('dexterity_total=' + str(player.dexterity_max) + '\n')
    saveFile.write('speed=' + str(player.speed) + '\n')
    saveFile.write('speed_total=' + str(player.speed_max) + '\n')
    saveFile.write('intelligence=' + str(player.intelligence) + '\n')
    saveFile.write('intelligence_total=' + str(player.intelligence_max) + '\n')
    saveFile.write('luck=' + str(player.luck) + '\n')
    saveFile.write('luck_total=' + str(player.luck_max) + '\n')
    saveFile.write('experience=' + str(player.experience) + '\n')
    saveFile.write('experience_needed=' + str(player.experience_needed) + '\n')
    saveFile.write('class=' + player.class_type + '\n')
    saveFile.write('level=' + str(player.level) + '\n')
    for item in player.inventory_items: # TODO figure out way to store player items in save
        pass
    saveFile.write('[END]')
    print('Game saved...')
    saveFile.close()

def loadCharacterFile(character_name): # TODO figure out where to place this function. Needs to be able to access the Player variables to set its stats
    """
    :param character_name: the character name to search for, in the Saves directory, that's in the file name.
    :type character_name: string
    :return: none
    :rtype: string
    """
    global Player
    Player.setName(getVarInSaveFile('name=', character_name))
    Player.setHp(int(getVarInSaveFile('characterhp=', character_name)))
    Player.setVitality(int(getVarInSaveFile('vitality=', character_name)))
    Player.setDexterity(int(getVarInSaveFile('dexterity=', character_name)))
    Player.setSpeed(int(getVarInSaveFile('speed=', character_name)))
    Player.setIntelligence(int(getVarInSaveFile('intelligence=', character_name)))
    Player.setLuck(int(getVarInSaveFile('luck=', character_name)))
    Player.setExperience(int(getVarInSaveFile('experience=', character_name)))
    Player.setClassType(getVarInSaveFile('class=', character_name))
    print('Game loaded..')

def quitGameConfirmation():
    print('QuitGameConfirmation')
    printContentToCommandLine('[QUIT_CONFIRMATION]')
    valid_responses = {'y', 'yes', 'n', 'no'}
    while True:
        print('QuitConfirmation')
        print('CHOICE::> ', end='')
        response = input().lower()

        if response in valid_responses:
            if response == 'y' or response == 'yes':
                exit()
            elif response == 'n' or response == 'no':
                print('')
                break
        else:
            print('Please try again..')
