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
history = dynamo.Table('History') #for closed order


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
def retrieveMenu(key):
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
#!#in the future we need a solution for multiple of the same item
def updateOrder( orderInfo ):
    #get the key
    key={
        'OrderId': orderInfo['OrderId']
    }
    #get the old OrderItems
    items = order.get_item(Key=key)["Item"]["OrderItems"]
    #add the new OrderItems
    items += orderInfo["OrderItems"] 
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
def retrieveOrder( orderId ):
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
    order = retrieveOrder( orderId )
    removeOrder( orderId )    
    addHistory( order )
    #generate receipt code
    return "receipts are still a work in progress"

