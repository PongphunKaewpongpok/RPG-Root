#-----------------------------------------------------------------------------------#
#                                                                                   #
#           This Function are calculate about upgrading Player's Ability.           #
#                                                                                   #
#-----------------------------------------------------------------------------------#


import json

#Load upgrade datas when starting game.
with open("Data/game_data.txt") as game_data:
    UPGRADE_DATA_DICT = json.loads(game_data.read())
print(UPGRADE_DATA_DICT)

#Set Price For Shop
#This is not real in-game upgrade price.
LENGTH_PRICE_DICT = {6: 300, 7: 500, 8: 1000, 9: 1500, 10: 2000}
SLOT_PRICE_DICT = {4: 300, 5: 500, 6: 1000, 7: 1500, 8: 2000, 9: 2000, 10: 2000}

def choose_upgrade(string):
    if string == "Length of Equation":
        return length_upgrade()
    elif string == "Inventory Slot":
        return slot_upgrade()
    else:
        return "The name of the ability you mentioned is not available in the system."

def length_upgrade():
    #Level up *LENGTH_OF_EQUATION* and changing in-python upgrade data.
    if UPGRADE_DATA_DICT["Length of Equation"]+1 in LENGTH_PRICE_DICT:
        if UPGRADE_DATA_DICT["Coins"] >= LENGTH_PRICE_DICT[UPGRADE_DATA_DICT["Length of Equation"]+1]:
            UPGRADE_DATA_DICT["Coins"] += -LENGTH_PRICE_DICT[UPGRADE_DATA_DICT["Length of Equation"]+1]
            UPGRADE_DATA_DICT["Length of Equation"] += 1
            print(UPGRADE_DATA_DICT["Length of Equation"])
            save_upgrade_data()
            return "Your skill now level " + str(UPGRADE_DATA_DICT["Length of Equation"]) + "."
        else:
            return "You don't have enough coins to upgrade."
    else:
        return "Your skill level has reached its peak."

def slot_upgrade():
    #Level up *INVENTORY SLOT* and changing in-python upgrade data.
    if UPGRADE_DATA_DICT["Inventory Slot"]+1 in SLOT_PRICE_DICT:
        if UPGRADE_DATA_DICT["Coins"] >= SLOT_PRICE_DICT[UPGRADE_DATA_DICT["Inventory Slot"]+1]:
            UPGRADE_DATA_DICT["Coins"] += -SLOT_PRICE_DICT[UPGRADE_DATA_DICT["Inventory Slot"]+1]
            UPGRADE_DATA_DICT["Inventory Slot"] += 1
            print(UPGRADE_DATA_DICT["Inventory Slot"])
            save_upgrade_data()
            return "Your skill now level " + str(UPGRADE_DATA_DICT["Inventory Slot"]) + "."
        else:
            return "You don't have enough coins to upgrade."
    else:
        return "Your skill level has reached its peak."

def save_upgrade_data():
    #Update Upgrade Data
    with open("Data/game_data.txt", "w") as game_data:
        json.dump(UPGRADE_DATA_DICT, game_data)

print('Do you want to upgrade "Length of Equation" or "Inventory Slot"?')
print(choose_upgrade(input("Upgrade: ")))
