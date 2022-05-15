#helpful imports
import json
from decimal import Decimal

#database import 
import boto3

#database setup
dynamo = boto3.resource("dynamodb")

#TABLES:
menu = dynamo.Table('Menu')
order = dynamo.Table('Order') #for open orders
history = dynamo.Table('History') #for receipts (old order)


#FOR THE MENU
#add json to database
def addMenu(item):
    #put the item in
    menu.put_item(
        Item=item
    )

#remove from database
def removeMenu(key):
    menu.delete_item(
        Key={
            'RestaurantId': key
        }
    )

#update menu item on database
def updateMenu(key, newMenu):
    #update the item
    menu.update_item(
        Key={
            'RestaurantId': key
        },
        UpdateExpression='SET Categories = :val1',
        ExpressionAttributeValues={
            ':val1': newMenu
        }
    )

#retreive from database
def retreiveMenu(key):
    return menu.get_item(
        Key={
            'RestaurantId': key
        }
    )["Item"]



#FOR THE ORDER TABLE (move to another script?)
#add an order (first time)
def addOrder( orderInfo ):
    order.put_item(
        Item=orderInfo
    )

#update an order (append)
#in the future we need a solution for multiple of the same item
def updateOrder( orderId, orderItems ):
    #get the key
    key={
        'OrderId': orderId
    }
    #get the old OrderItems
    items = order.get_item(Key=key)["Item"]["OrderItems"]

    #create a dictionary to map ItemId : index for every item currently in the order
    name_index = { items[index]["ItemId"]:index for index in range(len(items)) }
    #loop through all the "new" items and merge if possible, else just add
    for item in orderItems:
        name = item["ItemId"] 
        amount = item["Quantity"]
        if name in name_index:
            items[ name_index[name] ]["Quantity"] += amount
        else:
            items += [item]

    #update the order
    order.update_item(
        Key=key,
        UpdateExpression='SET OrderItems = :val1',
        ExpressionAttributeValues={
            ':val1': items
        }
    )

#get all the orders in the Order table
#what order should it return items in?
def getOrders():
    response = order.scan()
    data = response["Items"]
    while 'LastEvaluatedKey' in response:
        response = table.scan( ExclusiveStartKey=response["LastEvaluatedKey"] )
        data.extend(response["Items"])
    return data

#retreive an order
def retreiveOrder( orderId ):
    key = {
        "OrderId": orderId
    }
    return order.get_item( Key=key )["Item"]

#to remove an item from order table
def removeOrder( orderId ):
    key = {
        "OrderId": orderId
    }
    order.delete_item( Key=key )



#FOR THE HISTORY TABLE
#add an item to the history table
def addHistory( order ):
    history.put_item(
        Item=order
    )



#USE BOTH HISTORY AND ORDER TABLES
#also ADD RECEIPT GENERATION
#complete an order
def closeOrder( orderId ):
    #make the base for the receipt the order 
    receipt = retreiveOrder( orderId )    

    #get the menu of the restaurant
    menu = retreiveMenu( receipt["RestaurantId"] )
    #build a dict to keep track of itemId : price  
    item_map = {}
    for category in menu["Categories"]:
        for item in category["MenuItems"]:
            itemId = item["Id"]
            price = float( item["Price"] )
            item_map[ itemId ] = price
    
    #in the future make an API call to get the tax rate... for now I am using generic taxrate 
    #state = menu["ZipCode"]
    tax_rate = 8.875 #in percent
    total = 0.0

    #loop through all the OrderItems and add a price field
    for item in receipt["OrderItems"]:
        quantity = int( item["Quantity"] )
        price = item_map[ item["ItemId"] ]
        #calculate subtotal and update total 
        subtotal = quantity * price 
        total += subtotal
        item["Subtotal"] = str(subtotal)
    
    #calculate tax
    total *= ( 1 + (tax_rate/100) )
    #add the price + tax rate into total
    receipt["Total"] = str( round(total, 2) )
    receipt["TaxRate"] = str( tax_rate )

    #update the dbs
    removeOrder( orderId )    
    addHistory( receipt )
    #return the receipt
    return receipt

