from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Enrolment(db.Model):
    __tablename__ = 'enrolment'
    eid = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer, db.ForeignKey('students.studentid'))
    cid = db.Column (db.Integer, db.ForeignKey('classs.classid'))


class Users(UserMixin, db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(255), unique=True)
    password = db.Column(db.VARCHAR(255))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    def get_id(self):
        return (self.uid)
        

class Students(db.Model):
    __tablename__ = 'students'
    studentid = db.Column(db.Integer, primary_key=True)
    studentname = db.Column(db.VARCHAR(255), unique=True)
    studentcode = db.Column(db.VARCHAR(255), unique=True)
    classes = db.relationship('Classs', secondary = "enrolment", backref="students")
    def __repr__(self):
        return '<Student {}'.format(self.studentname)

#class is a keyword so I've added an extra 's'
class Classs(db.Model):
    __tablename__ = 'classs'
    classid = db.Column(db.Integer, primary_key=True)
    teacherid = db.Column(db.Integer)
    classcode = db.Column(db.VARCHAR(255), unique=True)
    
    def __repr__(self):
        return '<Class {}'.format(self.classid)

class StudentData(db.Model):
    __tablename__ = 'studentdata'
    dataid = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.Integer)
    gameid = db.Column(db.Integer)
    score = db.Column(db.Integer)
    areamost = db.Column(db.String)
    arealeast = db.Column(db.String)
    improvementrate = db.Column(db.Integer)
    studentname = db.Column(db.String)
    classid = db.Column(db.Integer)

    def __repr__(self):
        return '<Class {}'.format(self.dataid)

@login.user_loader
def load_user(uid):

    return Users.query.get(int(uid))
