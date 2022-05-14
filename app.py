#DOMAIN: http://54.145.44.208:5000/
#HELP WEBSITE: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

#flask import
from flask import Flask, request, render_template

#helpful imports
from helpers import *
import time 

#app setup
app = Flask( __name__ )
app.secret_key = "what is a good secret" #maybe change in the future

#send menu data correlating to specific id
#add case where ID doesnt match
@app.route("/menu/<id>")
def get_menu(id):
    return retrieveMenu(id)

#post order
#rn generates a new order everytime, in the future we should check if preexist order
@app.route("/order", methods=["POST"])
def post_order():
    orderInfo = json.loads(request.data)
    print(orderInfo)
    #check if there is pre-exisiting order id
    if "OrderId" in orderInfo:
        #update the order in db (taken care of in helper)
        updateOrder( orderInfo )
    else:
        #generate OrderId 
        orderId = "-".join( [ orderInfo[x] for x in ["RestaurantId", "TableId", "Time"] ] )
        #add it to orderInfo
        orderInfo["OrderId"] = orderId
        #add the order to db
        addOrder(orderInfo)
    #always return the OrderId
    return orderId 

#remove order from Order table and into History table
@app.route("/close/<id>")
def close_order(id):
    return closeOrder(id)


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