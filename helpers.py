#database import 
import boto3
#database setup
dynamo = boto3.resource("dynamodb")
#TABLES:
menu = dynamo.Table('Menu')
order = dynamo.Table('Order') #for open orders
history = dynamo.Table('History') #for receipts (old order)
info = dynamo.Table('Info')

#MENU TABLE
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
#retreive from database
def retreiveMenu(key):
    return menu.get_item(
        Key={
            'RestaurantId': key
        }
    )["Item"]


#ORDER TABLE
#add an order to processing queue
def addOrder( orderInfo ):
    order.put_item(
        Item=orderInfo
    )
#update an existing order -- in the future we need a solution for multiple of the same item
def updateOrder( orderId, orderItems ):
    key={'OrderId': orderId}
    #get the old OrderItems
    items = order.get_item(Key=key)["Item"]["OrderItems"]
    #create a dictionary to map ItemId : index for every item currently in the order
    name_index = { items[index]["ItemId"]:index for index in range(len(items)) }
    #loop through all the "new" items and merge if possible, else just add
    for item in orderItems:
        name = item["ItemId"] 
        amount = item["Quantity"]
        if name in name_index:
            old_amount = items[ name_index[name]["Quantity"] ]
            items[ name_index[name] ]["Quantity"] = str( old_amount + int(amount) )
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
#return all orders in the Order table (processing queue) (in the future come up with an order)
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
#returns the current state of receipt
def getReceipt( orderId ):
    receipt = retreiveOrder( orderId )    
    menu = retreiveMenu( receipt["RestaurantId"] )
    zipCode = retreiveInfo( receipt["RestaurantId"] )["ZipCode"]
    #build a dict to keep track of {itemId : price}  
    item_map = {}
    for category in menu["Categories"]:
        for item in category["MenuItems"]:
            itemId = item["Id"]
            price = float( item["Price"] )
            item_map[ itemId ] = price
    total = 0.0
    #calculate subtotals for every item
    for item in receipt["OrderItems"]:
        quantity = int( item["Quantity"] )
        price = item_map[ item["ItemId"] ]
        subtotal = quantity * price 
        total += subtotal
        item["Subtotal"] = str(subtotal)
    from tax import get_tax_rate
    tax_rate = get_tax_rate(zipCode)
    total *= ( 1 + (tax_rate/100) )
    receipt["Total"] = str( round(total, 2) )
    receipt["TaxRate"] = str( tax_rate )
    return receipt


#HISTORY TABLE
#add an item to the history table
def addHistory( order ):
    history.put_item(
        Item=order
    )


#HISTORY AND ORDER
#complete an order (take from processing queue and put it in History)
def closeOrder( orderId ):
    receipt = getReceipt( orderId )     
    addHistory( receipt )
    removeOrder( orderId )    
    return receipt


#FOR THE INFO TABLE
#wouldnt this be better in an sql db?
#add info to database
def addInfo( newInfo ):
    #update the item
    info.add_item( newInfo )
#remove from database
def removeInfo( restaurantId ):
    info.delete_item(
        Key={
            'RestaurantId': restaurantId
        }
    )
#retreive from database
def retreiveInfo( restaurantId ):
    return info.get_item(
        Key={
            'RestaurantId': restaurantId
        }
    )["Item"]
