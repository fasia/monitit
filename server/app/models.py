from flask import g
from flask_wtf import FlaskForm
import email_validator
from sqlalchemy.orm import relationship
from wtforms.validators import Email
from flask_sqlalchemy import SQLAlchemy
from app.server import db, flask_bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, info={'validators': Email()})
    password = db.Column(db.String(80), nullable=False)
    recipes = db.relationship('Recipe', backref='user', lazy ='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.email


items_in_recipe = db.Table('items_in_recipe', 
                db.Column('recipe_id',db.Integer, db.ForeignKey('recipe.id')),
                db.Column('item_id',db.Integer, db.ForeignKey('recipe_item.id'))
)

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    price = db.Column(db.Float, nullable=False)
    recipeitems = db.relationship('RecipeItem', secondary=items_in_recipe, backref=db.backref('recipes', lazy ='dynamic'))    
    
    def __init__(self, title, instruction, price, owner_id, recipeitems):
        self.title = title
        self.instruction = instruction
        self.price = price
        self.owner_id = g.user.id
        self.recipeitems = recipeitems
    
    def __repr__(self):
        return '<Recipe %r>' % self.title


class RecipeItem(db.Model):
    __tablename__ = 'recipe_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    qty = db.Column(db.String, nullable=False)

    #unit = db.relationship('Unit', backref= db.backref('recipe_item', uselist=False))
    #recipeid = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    #ingredient = db.relationship('Ingredient', backref= db.backref('recipeitem', uselist= False))
    
    def __init__(self, name, qty):
        self.name = name
        self.qty = qty

    def __repr__(self):
        return '<recipe_item %r>' % self.name


"""class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200), nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    def __init__(self, content, post_id):
        self.content = content
        self.user_id = g.user.id
        self.post_id = post_id

    def __repr__(self):
        return '<Comment %r>' % self.content """


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.relationship('Category', backref=db.backref('ingredient', uselist=False))
    recipeitem_id = db.Column(db.Integer, db.ForeignKey('recipe_item.id'))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Ingredient %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

""" class Unit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    recipeitem_id = db.Column(db.Integer, db.ForeignKey('recipe_item.id'))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Unit %r>' % self.name
 """
