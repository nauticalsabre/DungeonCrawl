class Item(object):
    """
    Base Item class.
    Contains basic Setter functions for base variables of the Item class, (Set_Name, Set_Weight, etc.).
    Also contains basic Use function, which is meant to be overridden by extended Item classes.

    :name: string - item's name.
    :category: string - category the item belongs to, (common, equipment, consumable, etc).
    :weight: decimal - weight of the item.
    :stack: int - how many of the item there is.
    :value: int - how valuable the item is in the game.
    :num_identifier: int - is assigned on creation of item. Used to refer to an item by number in inventory.
    """
    def __init__(self, new_name='none', new_category='none', new_weight=0, new_stack=0, new_value=0):
        # Default item properties
        self.name = new_name
        self.category = new_category
        self.weight = new_weight
        self.stack = new_stack
        self.value = new_value
        self.has_use_action = False

    def Use(self):
        pass



class ConsumableItem(Item):
    def __init__(self, new_name, new_category, new_weight, new_stack, new_value, new_stat_to_nourish, new_nourish_amount):
        super().__init__(new_name, new_category, new_weight, new_stack, new_value)
        self.stat_to_nourish = new_stat_to_nourish
        self.nourish_amount = new_nourish_amount


    def Use(self):
        pass



class EquipmentItem(Item):
    def __init__(self, new_name='none',
                       new_category='equipment',
                       new_weight=0,
                       new_stack=1,
                       new_value=0,
                       new_equipment_type='none',
                       new_damage=0,
                       new_defence=0,
                       new_material='none',
                       new_durability=0,
                       new_is_two_handed=False):
        super().__init__(new_name, new_category, new_weight, new_stack, new_value)
        self.equipment_type = new_equipment_type
        self.damage = new_damage
        self.defence = new_defence
        self.material = new_material
        self.durability = new_durability
        self.durability_max = self.durability
        self.is_two_handed = new_is_two_handed
        self.is_equipped = False


