import json
import uuid
from helpers import *

#TO DO:
#in the future have a better system to create uuid for menuitems
def item_id_gen( json ):
    #for all cateogries
    for category in json["Categories"]:
        #for all menu items in category
        for item in category["MenuItems"]:
            #check if there is not a Id, if true then gen id
            if "Id" not in item:
                item["Id"] = json["RestaurantId"] + "-" + str(uuid.uuid4())

#user input
print("\nWhat would you like to do?\n\t0: Add Menu\n\t1: Change Menu")
choice = input("\nYour Choice: ")
print()

#get the filename
filename = input("Filename: ")

#load the file
content = json.load(open("jsons/"+filename))

#maybe instead of having 2 choices, it can just check if there alr exists 
#a restaurant id... dont matter tho as this is a temporary means

#ADDING MENU
if choice == '0':
    #get the name of the restaurant
    name = content["RestaurantName"]
    #generate a uuid and assign it
    id = str( uuid.uuid4() )
    content["RestaurantId"] = id
    #create a map for item 
    open("map.txt", "a").write( name + " | " + id + "\n" )
    
    #add menu item ids
    item_id_gen(content)
    #load the new file content back
    open("jsons/"+filename, "w").write( json.dumps(content) )
    
    #add the menu to database
    addMenu(content)

#UPDATE MENU
elif choice == '1':
    id = content["RestaurantId"]
    
    #add menu item id for all categories (if not)
    item_id_gen(content)
    #load the new file content back
    open("jsons/"+filename, "w").write( json.dumps(content) )
    
    #only update categories
    newMenu = content["Categories"]
    updateMenu(id, newMenu)
    