#!/usr/bin/env python3

from app import create_app
from models import db, Restaurant, Pizza, RestaurantPizza

app = create_app()

with app.app_context():
    # Clear existing data to avoid duplicates
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="123 Pizza Lane")
    bistro = Restaurant(name="Sanjay's Pizza Bistro", address="456 Bistro Blvd")
    palace = Restaurant(name="Kiki's Pizza Palace", address="789 Palace Rd")
    restaurants = [shack, bistro, palace]

    print("Creating pizzas...")
    cheese = Pizza(name="Cheese Pizza", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Pepperoni Pizza", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="California Pizza", ingredients="Dough, Sauce, Ricotta, Red Peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    print("Creating RestaurantPizza relationships...")
    pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=10)
    pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=12)
    pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=15)
    restaurant_pizzas = [pr1, pr2, pr3]

    # Add everything to the session and commit
    db.session.add_all(restaurants)
    db.session.add_all(pizzas)
    db.session.add_all(restaurant_pizzas)
    db.session.commit()

    print("Seeding done!")
