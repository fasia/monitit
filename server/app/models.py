from flask import g

from wtforms.validators import Email

from server import db, flask_bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, info={'validators': Email()})
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.email


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    post_comments = db.relationship('Comment', backref='post', lazy='dynamic')



    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.user_id = g.user.id

    def __repr__(self):
        return '<Post %r>' % self.title

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200), nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))


    def __init__(self, content, post_id):
        self.content = content
        self.user_id = g.user.id
        self.post_id = post_id

    def __repr__(self):
        return '<Comment %r>' % self.content
