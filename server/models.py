from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates

# Metadata with naming conventions for migrations
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

# Initialize SQLAlchemy with custom metadata
db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # Relationship to RestaurantPizza
    restaurant_pizzas = db.relationship(
        "RestaurantPizza",
        backref="restaurant",
        cascade="all, delete-orphan",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "restaurant_pizzas": [rp.to_dict(exclude_restaurant=True) for rp in self.restaurant_pizzas]
        }

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Restaurant name cannot be empty.")
        return value.strip()

    @validates("address")
    def validate_address(self, key, value):
        if not value or not value.strip():
            raise ValueError("Address cannot be empty.")
        return value.strip()


class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # Relationship to RestaurantPizza
    restaurant_pizzas = db.relationship(
        "RestaurantPizza",
        backref="pizza",
        cascade="all, delete-orphan",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients
        }

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Pizza name cannot be empty.")
        return value.strip()


class RestaurantPizza(db.Model):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"), nullable=False)

    def to_dict(self, exclude_restaurant=False, exclude_pizza=False):
        """Convert to dictionary, with options to exclude relationships to avoid cyclic references."""
        data = {
            "id": self.id,
            "price": self.price,
            "restaurant_id": self.restaurant_id,
            "pizza_id": self.pizza_id
        }
        if not exclude_restaurant:
            data["restaurant"] = self.restaurant.to_dict()
        if not exclude_pizza:
            data["pizza"] = self.pizza.to_dict()
        return data

    @validates("price")
    def validate_price(self, key, value):
        if not (1 <= value <= 30):
            raise ValueError("Price must be between 1 and 30.")
        return value
