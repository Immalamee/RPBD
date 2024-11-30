from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    __tablename__ = 'cars'
    __table_args__ = {'schema': 'avto'}

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    registration_number = db.Column(db.String(20), nullable=False, unique=True)
    load_capacity = db.Column(db.Numeric(10, 2), nullable=False)
    cargo_type = db.Column(db.String(100), nullable=False)
    drivers = db.relationship('Driver', backref='car', lazy=True)
    orders = db.relationship('Order', backref='car', lazy=True)

class Driver(db.Model):
    __tablename__ = 'drivers'
    __table_args__ = {'schema': 'avto'}

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    qualification_level = db.Column(db.Integer, nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('avto.cars.id'), nullable=True)
    orders = db.relationship('Order', backref='driver', lazy=True)

class Client(db.Model):
    __tablename__ = 'clients'
    __table_args__ = {'schema': 'avto'}

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    orders = db.relationship('Order', backref='client', lazy=True)

class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'avto'}

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    cargo = db.Column(db.String(100), nullable=False)
    from_address = db.Column(db.String(150), nullable=False)
    to_address = db.Column(db.String(150), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('avto.cars.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('avto.drivers.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('avto.clients.id'), nullable=False)
