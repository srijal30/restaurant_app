from helpers import history

#get all the info fro the history table and put in data
response = history.scan()
data = response["Items"]
while 'LastEvaluatedKey' in response:
    response = table.scan( ExclusiveStartKey=response["LastEvaluatedKey"] )
    data.extend(response["Items"])

#filter the restaurants
restaurants = {}

for order in data:
    #there is an issue with the split
    splitted = order["OrderId"].split("-")
    rest_id = "-".join( splitted[0:5] )

    #if we havent seen this restaurant before
    if rest_id not in restaurants:
        restaurants[rest_id] = {}

    #loop through all the order items
    for item in order["OrderItems"]:
        #if we havent seen this item before, add it
        if item["ItemId"] not in restaurants[rest_id]:
            restaurants[rest_id][ item["ItemId"] ] = 1
        else:
            restaurants[rest_id][ item["ItemId"] ] += 1


#put everything in a CSV
from helpers import retreiveMenu
fil = open("data.txt", "w")


#get item from id
def get_name_from_id( menu, id ):
    for cat in menu["Categories"]:
        for item in cat["MenuItems"]:
            if id == item["Id"]:
                return item["Name"]
    raise ValueError("not a valid id for given menu")


print( restaurants )

for id in restaurants:
    print( "current id is", id)
    menu = retreiveMenu( id )
    output = ""
    output += menu["RestaurantName"] + "\n"
    for item_id in restaurants[id]:
        output += get_name_from_id( menu, item_id ) + ": " + str( restaurants[id][item_id] ) + "\n"
    output += "\n"
    fil.write( output )
