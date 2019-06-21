from app import db

class users(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(255), unique=True)
    password = db.Column(db.VARCHAR(255))
    useremail = db.Column(db.VARCHAR(255), unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class students(db.Model):
    studentid = db.Column(db.Integer, primary_key=True)
    studentname = db.Column(db.VARCHAR(255), unique=True)
    studentcode = db.Column(db.VARCHAR(255), unique=True)

    def __repr__(self):
        return '<Student {}'.format(self.studentname)

#class is a keyword so I've added an extra 's'
class classs(db.Model):
    classid = db.Column(db.Integer, primary_key=True)
    teacherid = db.Column(db.Integer)
    classcode = db.Column(db.VARCHAR(255))
    
    def __repr__(self):
        return '<Class {}'.format(self.classid)

class enrolment(db.Model):
    eid = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer, db.ForeignKey('students.studentid'))
    cid = db.Column(db.Integer, db.ForeignKey('classs.clasid'))

    def __repr__(self):
        return '<Student {}'.format(self.studentname)


def init_db():
    db.create_all()

    new_user = users(username='johnt07', password='bigfish09', useremail='johntron@gmail.com')
    db.session.add(new_user)
    db.session.commit();
