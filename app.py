from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Dropped')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='mercury', planet_type='Class D', home_star='sun', mass=3.258e23, radius=1516,
                     distance=35.98e6)
    venus = Planet(planet_name='venus', planet_type='Class K', home_star='sun', mass=4.867e24, radius=3760,
                   distance=67.24e6)
    earth = Planet(planet_name='earth', planet_type='Class M', home_star='sun', mass=5.972e24, radius=3959,
                   distance=92.96e6)
    db.session.add(mercury)
    db.session.add(earth)
    db.session.add(venus)

    test_user = User(first_name='William', last_name='Herschel', email='test@test.com', password='4rgentin4')

    db.session.add(test_user)
    db.session.commit()
    print('Database Seeded!')


@app.route('/')
def hello_world():
    return 'Hello World!'


# Database Models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


if __name__ == '__main__':
    app.run()
