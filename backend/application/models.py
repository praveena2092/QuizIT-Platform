from .database import db
from flask_security import UserMixin,RoleMixin
from sqlalchemy import Column, DateTime, Interval, func,Date
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    username=db.Column(db.String,unique=False,nullable =False)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String(255))
    active=db.Column(db.Boolean())
    dob=db.Column(db.String)
    fs_uniquifier=db.Column(db.String(255),unique=True,nullable=False) #token
    roles=db.relationship("Role",backref="bearer", secondary = "user_roles")
    score=db.relationship("Scores",backref="taker",cascade='all, delete-orphan')
    
    

class Role(db.Model,RoleMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    description=db.Column(db.String(255))
    
class UserRoles(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))
    
    
class Subject(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    name=db.Column(db.String,unique=False)
    description=db.Column(db.String,unique=True)
    chapters = db.relationship('Chapter', backref='subject', cascade='all, delete-orphan')
    
    
    
class Chapter(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    name=db.Column(db.String,unique=True)
    description=db.Column(db.String,unique=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    quizs=db.relationship("Quiz", backref="chapter" , cascade='all, delete-orphan')
    
class Quiz(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    date_of_quiz = db.Column(Date, server_default=func.date('now'))
    time_duration = db.Column(Interval)  # Stores time duration correctly
    remarks=db.Column(db.String)
    chapter_id=db.Column(db.Integer,db.ForeignKey("chapter.id"))
    questions=db.relationship("Question",backref='question',cascade='all, delete-orphan')
    scores=db.relationship("Scores",backref="scores",cascade='all, delete-orphan')
    internal_status=db.Column(db.String)
    
class Question(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    question_statement=db.Column(db.String,unique=True)
    option_1=db.Column(db.String)
    option_2=db.Column(db.String)
    option_3=db.Column(db.String)
    option_4=db.Column(db.String)
    user_answer=db.Column(db.String)
    quiz_id=db.Column(db.Integer,db.ForeignKey("quiz.id"))
    correct_answer=db.Column(db.String)
    
    
class Scores(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    time_stamp_of_attempt=db.Column(db.DateTime, server_default=db.func.now())
    total_score=db.Column(db.Integer)
    quiz_id=db.Column(db.Integer,db.ForeignKey("quiz.id"))
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    
    