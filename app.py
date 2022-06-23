#DOMAIN: http://54.145.44.208:5000/
#HELP WEBSITE: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

#flask import
from flask import Flask, request, render_template

#helpful imports
from helpers import *
import time 
import json

#app setup
app = Flask( __name__ )
app.secret_key = "what is a good secret" #maybe change in the future

#send menu data correlating to specific id
#add case where ID doesnt match
@app.route("/menu/<id>")
def get_menu(id):
    return retreiveMenu(id)

#post order
#rn generates a new order everytime, in the future we should check if preexist order
@app.route("/order", methods=["POST"])
def post_order():
    print( request.data )
    orderInfo = json.loads(request.data)
    #check if there is pre-exisiting order id
    if "OrderId" in orderInfo and orderInfo["OrderId"] != "":
        #update the order in db (only need to give the OrderItem list)
        updateOrder( orderInfo["OrderId"],  orderInfo["OrderItems"] )
    else:
        #generate OrderId 
        orderId = "-".join( [ orderInfo[x] for x in ["RestaurantId", "TableId", "Time"] ] )
        #add it to orderInfo
        orderInfo["OrderId"] = orderId
        #add the order to db
        addOrder(orderInfo)
    #always return the OrderId
    return orderInfo["OrderId"] 

#remove order from Order table and into History table
#and return receipt
@app.route("/close/<id>")
def close_order(id):
    return closeOrder(id)

#returns the current state of the reciept of an open order
@app.route("/receipt/<id>")
def get_current_receipt(id):
    return getReceipt(id)

#FOR TESTING PURPOSES:

#temp kitchen endpoint
@app.route("/kitchen")
def see_kitchen():
    return render_template( "kitchen.html", orders=getOrders() )

#list of restaurants w/ their ids
@app.route("/restaurants")
def see_restaurants():
    arr = open("map.txt").read().splitlines()
    return render_template("table.html", arr=arr)

#run the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

#to run with gunicorn:
#$ gunicorn -b 0.0.0.0:5000 app:app
