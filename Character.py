from Item import *

class Character(object):
    # TODO create nerf/buff effects for characters
    def __init__(self):
        self.name = 'character_default'

        self.hp      = {'current' : 1,
                        'max'     : 1}

        self.defence = {'current' : 0,
                        'max'     : 0}

        self.evasion = {'current' : 0,
                        'max'     : 0}

        self.luck    = {'current' : 1,
                        'max'     : 1}

        self.level = 1

        self.experience_worth = 0
        self.species = 'none'

        self.attributes = { 'vitality'     : {'current' : 1,
                                              'max'     : 1},
                            'strength'     : {'current' : 1,
                                              'max'     : 1},
                            'perception'   : {'current' : 1,
                                              'max'     : 1},
                            'endurance'    : {'current' : 1,
                                              'max'     : 1},
                            'intelligence' : {'current' : 1,
                                              'max'     : 1},
                            'speed'        : {'current' : 1,
                                              'max'     : 1},
                            'dexterity'    : {'current' : 1,
                                              'max'     : 1}}

        self.inventory_weight = {'current' : 0,
                                 'max'     : 0}
        
        self.inventory_items = []

        self.abilities = [] # TODO create abilites
        self.effects = []   # TODO create effects
        
        """
        We first initialize all equipment items for the character.

        then we create a dictionary containing slot names and assign
        the characters equipment items to the slots.
        """
        primary    = EquipmentItem()
        secondary  = EquipmentItem()
        helmet     = EquipmentItem()
        body       = EquipmentItem()
        legs       = EquipmentItem()
        boots      = EquipmentItem()
        gloves     = EquipmentItem()
        back       = EquipmentItem()
        
        self.equipment_items = {'primary'   : primary,
                                'secondary' : secondary,
                                'helmet'    : helmet,
                                'back'      : back,
                                'body'      : helmet,
                                'gloves'    : gloves,
                                'legs'      : legs,
                                'boots'     : boots}

    """
    >> Use these setter methods to make sure the 'max' value is always higher or equal
    >> to the 'current' value you set it to.
    """
    def setHp(self, new_hp):
        self.hp['current'] = new_hp
        if self.hp['current'] > self.hp['max']:
            self.hp['max'] = self.hp['current']

    def setDefence(self, new_defence):
        self.defence['current'] = new_defence
        if self.defence['current'] > self.defence['max']:
            self.defence['max'] = self.defence['current']


    def setEvasion(self, new_evasion):
        self.evasion['current'] = new_evasion
        if self.evasion['current'] > self.evasion['max']:
            self.evasion['max'] = self.evasion['current']

    def setAttribute(self, attribute, new_value):
        self.attributes[attribute]['current'] = new_value
        if self.attributes[attribute]['current'] > self.attributes[attribute]['max']:
            self.attributes[attribute]['max'] = self.attributes[attribute]['current']

    def setLuck(self, new_luck):
        self.luck['current'] = new_luck
        if self.luck['current'] > self.luck['max']:
            self.luck['max'] = self.luck['current']

    def setLevel(self, new_level):
        self.level = new_level

    def wipeInventory(self):
        self.inventory_items = []
        
    # item_to_add is a reference to an item object
    def addToInventory(self, item_to_add, amount_to_add=1):
        item_found = False
        """
            If the item belongs to the 'equipment' category just append the item to
        the inventory_items list.
        
            If it DOESN'T belong to the 'equipment' category look to see if we already
        have an item like it in the inventory. If so just at amount to that items
        stack.
        
            If the item isn't found in the inventory at all. append it to the
        inventory_items list
        """
        if item_to_add.category == 'equipment':
            self.inventory_items.append(item_to_add)
        else:
            for item in self.inventory_items:
                if item.name == item_to_add.name:
                    item_found = True
                    item.Set_Stack(item.stack + amount_to_add)
                    break
            if not item_found:
                self.inventory_items.append(item_to_add)

    def getItem(self, item_name):
        for item in self.inventory_items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def equipItem(self, item_to_equip): # TODO continue working on equipping items. Right now it tests items using the built in id() function of python which basically allows all objects to have a unique identifier since it uses memory addresses
        if item_to_equip != None:
            for item in self.inventory_items:
                if id(item) == id(item_to_equip): # Check if item_to_equip is in the character inventory
                    for slot in self.equipment_items:
                        if slot == item_to_equip.equipment_type:
                            self.equipment_items[slot].is_equipped = False

                            self.equipment_items[slot] = item_to_equip
                            self.equipment_items[slot].is_equipped = True
        else:
            print('<That item is not in your inventory>')

    def unequipItem(self, item_to_unequip):
        if item_to_unequip != None:
            for item in self.inventory_items:
                if item.category == 'equipment':
                    if item.is_equipped:
                        for slot in self.equipment_items:
                            if slot == item_to_unequip.equipment_type:
                                self.equipment_items[slot].is_equipped = False
                                blank_equipment_item = EquipmentItem()
                                self.equipment_items[slot] = blank_equipment_item
    
    def updateInventoryWeight(self):
        """
        First update the max amount of weight the character can hold

        Then go through inventory_items list and add up all the items
        weights.

        Then set the characters current inventory_weight
        """
        self.inventory_weight['max'] = (self.attributes['strength']['current'] * 10) + 40

        current_weight = 0
        for item in self.inventory_items:
            current_weight += item.weight
                            
        self.inventory_weight['current'] = current_weight



class PlayerCharacter(Character):
    def __init__(self, new_name):
        super().__init__() # call parent class __init__ to initialize needed vars
        self.name = new_name
                            
        self.main_attribute = 'none'
        self.nerf_attribute = 'none'
        self.ability_resource_name = 'none'
                            
        self.ability_resource = {'current' : 1,
                                 'max'     : 1}
                            
        self.experience = {'current' : 0,
                           'needed'  : round( 100 + ((self.level * 75) * (self.level / 4)), -1)}
        self.class_type = 'none'
                            
        # Constants
        self.CONST_ATT_POINT_GAIN = 5
        self.CONST_ATT_MAIN_GAIN = 3
        self.CONST_ATT_AVER_GAIN = 2
        self.CONST_ATT_DIMM_GAIN = 1

        self.attribute_points = 0

    def addExperience(self, amount):
        self.experience['current'] += amount

        if self.experience['current'] >= self.experience['needed']:  # if we have enough experience to level up then call levelUp() and pass the amount of experience left
                                                       # over if we had more then enough to level up.
            experience_leftover = max(self.experience['current'] - self.experience['needed'], 0)
            self.levelUp(experience_leftover)

    def levelUp(self, leftover_exp):
        self.level += 1
        self.experience['current'] = 0
        self.experience['needed'] = round( 100 + ((self.level * 75) * (self.level / 4)), -1)

        self.addExperience(leftover_exp)
        self.attribute_points += self.CONST_ATT_POINT_GAIN

        for index in self.attributes:
            self.setAttribute(index, self.attributes[index]['current'] + self.CONST_ATT_AVER_GAIN)
