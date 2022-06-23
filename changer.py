import json
import uuid
from helpers import *

#go through the whole menu and generate menu ids if there isnt one alr
def item_id_gen( menu ):
    #for all cateogries
    for category in menu["Categories"]:
        #for all menu items in category
        for item in category["MenuItems"]:
            #check if there is not a Id, if true then gen id
            if "Id" not in item or item["Id"] == "":
                item["Id"] = menu["RestaurantId"] + "-" + str(uuid.uuid4())


#this function will also add the restaurant to map
def gen_rest_id( name ):
    id = str( uuid.uuid4() )
    open("map.txt", "a").write( name + " | " + id + "\n" )
    return id