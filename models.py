from flask import jsonify;
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate

db = SQLAlchemy()

database_name = "postgram"
DATABASE_URL = "postgresql://postgres:root@{}/{}".format('localhost:5432', database_name)

def setup_db(app):
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    migrate = Migrate(app, db)
    db.create_all()

    return app, migrate


class Authors(db.Model,UserMixin): # Post authors
    __tablename__='authors'
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    username=db.Column(db.String)
    email = db.Column(db.String,nullable=True)
    password=db.Column(db.String, nullable=True)
   
    author_profile = db.relationship('Profiles', backref='authors', lazy=True)

    posts = db.relationship('Posts', backref='authors', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Profiles(db.Model): # Post authors
    __tablename__='profiles'
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    first_name=db.Column(db.String)
    last_name=db.Column(db.String)
    bio = db.Column(db.String)
    author_id = db.Column(db.ForeignKey("authors.id"))


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    
class Comments(db.Model): # Comment on Posts
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    post_id = db.Column(db.ForeignKey("posts.id"))
    post_comment = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

class Posts(db.Model): # Blog posts Models
    __tablename__ ="posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    author = db.Column(db.ForeignKey("authors.id"))
    comment_id = db.relationship('Comments', backref='posts', lazy=True)
    status = db.Column(db.Boolean, default=False)
 
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_post(self):
        return jsonify({
            "id": self.id,
            "title":self.title,
            "body":self.body,
            "post_date": self.post_date,
            "author": self.author,
            "comment": self.comment,
            "status": self.status,
            "likes":self.likes
        })

