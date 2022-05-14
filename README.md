name is a work in progress...

# Restaurant App


## Overview

This is the backend portion of an online menu app. The online menu app will consist of 3 subapps with these core features:

* User App (almost done)
  * Users can access an online menu through a tablet provided by the restaurant.
  * Users can order food from the menu.
  * At the end of their dining session, Users will be sent a receipt.

* Kitchen App (not implemented)
  * User orders will be split amongst cooks to help facilitate food production.
  * Cooks will be able to mark orders as complete and send them back to correct tables.

* Owner App (not implemented)
  * Restaurant owners will be allowed to customize their menu items.
  * Restaurant owners can customize other settings (location, price, stackable-orders).
  * Restaurant owners will be provided with analytics.

## Tools Used

* Flask/Python - Backend
* AWS EC2 - Server Host
* DynamoDB - NoSQL Database


## A Few Things to Note
* The jsons folder is temporary... a backup just in case my AWS server decides to break.
* The /kitchen and /restaurants endpoints are temporary means to help facilitate development. 

## Developers
* Salaj Rijal - Backend
* Abid Talukdeer - Frontend