#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_migrate import Migrate
import os
from models import db, Restaurant, RestaurantPizza, Pizza

# Base directory and database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Initialize Flask application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Routes
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    try:
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant_by_id(id):
    try:
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return jsonify(restaurant.to_dict()), 200
        return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    try:
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return "", 204
        return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    try:
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict() for pizza in pizzas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/restaurant_pizzas", methods=["POST"])
def add_restaurant_pizza():
    data = request.get_json()

    required_keys = ["price", "restaurant_id", "pizza_id"]
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return jsonify({"error": f"Missing keys: {', '.join(missing_keys)}"}), 400

    try:
        # Validate the price
        price = data["price"]
        if not (1 <= price <= 30):
            return jsonify({"errors": ["validation errors"]}), 400

        # Check if restaurant_id and pizza_id exist
        restaurant = Restaurant.query.get(data["restaurant_id"])
        pizza = Pizza.query.get(data["pizza_id"])
        if not restaurant or not pizza:
            return jsonify({"error": "Invalid restaurant_id or pizza_id"}), 400

        # Create and save the RestaurantPizza
        restaurant_pizza = RestaurantPizza(
            price=price,
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"],
        )
        db.session.add(restaurant_pizza)
        db.session.commit()
        return jsonify(restaurant_pizza.to_dict()), 201

    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# Run the application
if __name__ == "__main__":
    app.run(port=5555, debug=True)
