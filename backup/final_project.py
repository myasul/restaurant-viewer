from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return "This page will show all my restaurants"


@app.route('/restaurant/new')
def newRestaurant():
    return "This will page will be for making new restaurants"


@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "This will be for editing restaurant {0}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return "This will be for deleting restaurant {0}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return "The page is the menu for restaurant {0}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "This page is for creating a new menu item for restaurant {0}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "This page is for editing menu item {0}".format(menu_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "This page is for deleting menu item {0}".format(menu_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
