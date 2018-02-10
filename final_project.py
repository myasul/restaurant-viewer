## import Flask library for web related functions ##
import os
from flask import Flask, render_template, url_for, request, redirect, jsonify, send_from_directory

## import sqlalchemy libarary for database functions ##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Base

## Create session and database connection ##
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# Set upload folder location
UPLOAD_FOLDER = os.path.dirname('static/images/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    try:
        restaurants = session.query(Restaurant).all()
    except:
        restaurants = []
    return jsonify(Restaurants=[res.serialize for res in restaurants])


@app.route('/restaurant/<int:restaurant_id>/JSON')
def showMenuJSON(restaurant_id):
    try:
        menu = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id).all()
    except:
        restaurants = []
    return jsonify(MenuItems=[item.serialize for item in menu])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuItemJSON(restaurant_id, menu_id):
    try:
        menu = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id, id=menu_id).all()
    except:
        restaurants = []
    return jsonify(MenuItem=[item.serialize for item in menu])


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    try:
        restaurants = session.query(Restaurant).all()
    except:
        restaurants = []
    return render_template("restaurants.html", restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == "POST":
        file = request.files['image']

        # save the new restaurant details in the database
        new_restaurant = Restaurant(
            name=request.form["restaurant-name"], description=request.form["description"],
            image_filename=file.filename)
        session.add(new_restaurant)
        session.commit()

        # save file in upload folder
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(f)

        return redirect(url_for("showRestaurants"))
    else:
        return render_template("newRestaurant.html")


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['POST', 'GET'])
def editRestaurant(restaurant_id):
    restaurant = getRestaurant(restaurant_id)

    if request.method == 'POST':

        restaurant.name = request.form["restaurant-name"]
        restaurant.description = request.form["description"]

        if 'image' in request.files:
            file = request.files['image']
            restaurant.image_filename = file.filename
            f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(f)
            print("hello!")

        session.add(restaurant)
        session.commit()

        return redirect(url_for("showRestaurants"))
    else:
        return render_template("editRestaurant.html", restaurant_name=restaurant.name,
                               restaurant_id=restaurant.id, description=restaurant.description)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['POST'])
def deleteRestaurant(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    restaurant_name = restaurant.name
    session.delete(restaurant)
    session.flush()
    session.commit()

    result = "{} has been successfully deleted".format(restaurant_name)
    return jsonify(result=result)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template("menu.html", menu=menu, restaurant_name=restaurant.name, restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['POST', 'GET'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        new_menu = MenuItem(
            name=request.form["restaurant-name"],
            description=request.form["description"],
            price=request.form["price"],
            course=request.form["course"],
            restaurant_id=restaurant_id
        )
        session.add(new_menu)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template("newMenuItem.html", restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['POST', 'GET'])
def editMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_id).one()

    if request.method == 'POST':
        menu_item.name = request.form["menu-name"]
        menu_item.description = request.form["description"]
        menu_item.price = request.form["price"]
        menu_item.course = request.form["course"]
        session.add(menu_item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))

    else:
        return render_template("editMenuItem.html", menu_name=menu_item.name,
                               description=menu_item.description, price=menu_item.price,
                               course=menu_item.course, restaurant_id=restaurant_id,
                               menu_id=menu_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_id).one()

    if request.method == 'POST':
        session.delete(menu_item)
        session.flush()
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))

    else:
        return render_template("deleteMenuItem.html", restaurant_id=restaurant_id, menu_id=menu_item.id, menu_name=menu_item.name)


def getRestaurant(restaurant_id):
    return session.query(Restaurant).filter_by(id=restaurant_id).one()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
