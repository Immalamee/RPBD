from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Car, Driver, Client, Order
from forms import CarForm, DriverForm, ClientForm, OrderForm
from flask import make_response
from weasyprint import HTML
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal

app = Flask(__name__)
app.config.from_object(Config)
app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False,
}
db.init_app(app)

api = Api(app)

car_fields = {
    'id': fields.Integer,
    'brand': fields.String,
    'registration_number': fields.String,
    'load_capacity': fields.Float,
    'cargo_type': fields.String
}

driver_fields = {
    'id': fields.Integer,
    'last_name': fields.String,
    'qualification_level': fields.Integer,
    'experience_years': fields.Integer,
    'car_id': fields.Integer
}

client_fields = {
    'id': fields.Integer,
    'last_name': fields.String,
    'address': fields.String,
    'phone': fields.String
}

order_fields = {
    'id': fields.Integer,
    'order_date': fields.DateTime(dt_format='iso8601'),
    'cargo': fields.String,
    'from_address': fields.String,
    'to_address': fields.String,
    'completion_date': fields.DateTime(dt_format='iso8601'),
    'cost': fields.Float,
    'car_id': fields.Integer,
    'driver_id': fields.Integer,
    'client_id': fields.Integer
}

class CarListResource(Resource):
    @marshal_with(car_fields)
    def get(self):
        cars = Car.query.all()
        return cars

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('brand', required=True, help="Brand is required")
        parser.add_argument('registration_number', required=True, help="Registration number is required")
        parser.add_argument('load_capacity', type=float, required=True, help="Load capacity is required")
        parser.add_argument('cargo_type', required=True, help="Cargo type is required")
        args = parser.parse_args()

        car = Car(
            brand=args['brand'],
            registration_number=args['registration_number'],
            load_capacity=args['load_capacity'],
            cargo_type=args['cargo_type']
        )
        db.session.add(car)
        db.session.commit()
        return marshal(car, car_fields), 201

class CarResource(Resource):
    @marshal_with(car_fields)
    def get(self, car_id):
        car = Car.query.get_or_404(car_id)
        return car

    def put(self, car_id):
        parser = reqparse.RequestParser()
        parser.add_argument('brand')
        parser.add_argument('registration_number')
        parser.add_argument('load_capacity', type=float)
        parser.add_argument('cargo_type')
        args = parser.parse_args()

        car = Car.query.get_or_404(car_id)

        if args['brand']:
            car.brand = args['brand']
        if args['registration_number']:
            car.registration_number = args['registration_number']
        if args['load_capacity'] is not None:
            car.load_capacity = args['load_capacity']
        if args['cargo_type']:
            car.cargo_type = args['cargo_type']

        db.session.commit()
        return marshal(car, car_fields), 200

    def delete(self, car_id):
        car = Car.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        return '', 204

class DriverListResource(Resource):
    @marshal_with(driver_fields)
    def get(self):
        drivers = Driver.query.all()
        return drivers

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('last_name', required=True, help="Last name is required")
        parser.add_argument('qualification_level', type=int, required=True, help="Qualification level is required")
        parser.add_argument('experience_years', type=int, required=True, help="Experience years are required")
        parser.add_argument('car_id', type=int)
        args = parser.parse_args()

        driver = Driver(
            last_name=args['last_name'],
            qualification_level=args['qualification_level'],
            experience_years=args['experience_years'],
            car_id=args.get('car_id')
        )
        db.session.add(driver)
        db.session.commit()
        return marshal(driver, driver_fields), 201

class DriverResource(Resource):
    @marshal_with(driver_fields)
    def get(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        return driver

    def put(self, driver_id):
        parser = reqparse.RequestParser()
        parser.add_argument('last_name')
        parser.add_argument('qualification_level', type=int)
        parser.add_argument('experience_years', type=int)
        parser.add_argument('car_id', type=int)
        args = parser.parse_args()

        driver = Driver.query.get_or_404(driver_id)

        if args['last_name']:
            driver.last_name = args['last_name']
        if args['qualification_level'] is not None:
            driver.qualification_level = args['qualification_level']
        if args['experience_years'] is not None:
            driver.experience_years = args['experience_years']
        if args['car_id'] is not None:
            driver.car_id = args['car_id']

        db.session.commit()
        return marshal(driver, driver_fields), 200

    def delete(self, driver_id):
        driver = Driver.query.get_or_404(driver_id)
        db.session.delete(driver)
        db.session.commit()
        return '', 204

class ClientListResource(Resource):
    @marshal_with(client_fields)
    def get(self):
        clients = Client.query.all()
        return clients

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('last_name', required=True, help="Last name is required")
        parser.add_argument('address', required=True, help="Address is required")
        parser.add_argument('phone', required=True, help="Phone number is required")
        args = parser.parse_args()

        client = Client(
            last_name=args['last_name'],
            address=args['address'],
            phone=args['phone']
        )
        db.session.add(client)
        db.session.commit()
        return marshal(client, client_fields), 201

class ClientResource(Resource):
    @marshal_with(client_fields)
    def get(self, client_id):
        client = Client.query.get_or_404(client_id)
        return client

    def put(self, client_id):
        parser = reqparse.RequestParser()
        parser.add_argument('last_name')
        parser.add_argument('address')
        parser.add_argument('phone')
        args = parser.parse_args()

        client = Client.query.get_or_404(client_id)

        if args['last_name']:
            client.last_name = args['last_name']
        if args['address']:
            client.address = args['address']
        if args['phone']:
            client.phone = args['phone']

        db.session.commit()
        return marshal(client, client_fields), 200

    def delete(self, client_id):
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        return '', 204

class OrderListResource(Resource):
    @marshal_with(order_fields)
    def get(self):
        orders = Order.query.all()
        return orders

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order_date', required=True, help="Order date is required")
        parser.add_argument('cargo', required=True, help="Cargo is required")
        parser.add_argument('from_address', required=True, help="From address is required")
        parser.add_argument('to_address', required=True, help="To address is required")
        parser.add_argument('completion_date', required=True, help="Completion date is required")
        parser.add_argument('cost', type=float, required=True, help="Cost is required")
        parser.add_argument('car_id', type=int, required=True, help="Car ID is required")
        parser.add_argument('driver_id', type=int, required=True, help="Driver ID is required")
        parser.add_argument('client_id', type=int, required=True, help="Client ID is required")
        args = parser.parse_args()

        order = Order(
            order_date=args['order_date'],
            cargo=args['cargo'],
            from_address=args['from_address'],
            to_address=args['to_address'],
            completion_date=args['completion_date'],
            cost=args['cost'],
            car_id=args['car_id'],
            driver_id=args['driver_id'],
            client_id=args['client_id']
        )
        db.session.add(order)
        db.session.commit()
        return marshal(order, order_fields), 201

class OrderResource(Resource):
    @marshal_with(order_fields)
    def get(self, order_id):
        order = Order.query.get_or_404(order_id)
        return order

    def put(self, order_id):
        parser = reqparse.RequestParser()
        parser.add_argument('order_date')
        parser.add_argument('cargo')
        parser.add_argument('from_address')
        parser.add_argument('to_address')
        parser.add_argument('completion_date')
        parser.add_argument('cost', type=float)
        parser.add_argument('car_id', type=int)
        parser.add_argument('driver_id', type=int)
        parser.add_argument('client_id', type=int)
        args = parser.parse_args()

        order = Order.query.get_or_404(order_id)

        if args['order_date']:
            order.order_date = args['order_date']
        if args['cargo']:
            order.cargo = args['cargo']
        if args['from_address']:
            order.from_address = args['from_address']
        if args['to_address']:
            order.to_address = args['to_address']
        if args['completion_date']:
            order.completion_date = args['completion_date']
        if args['cost'] is not None:
            order.cost = args['cost']
        if args['car_id'] is not None:
            order.car_id = args['car_id']
        if args['driver_id'] is not None:
            order.driver_id = args['driver_id']
        if args['client_id'] is not None:
            order.client_id = args['client_id']

        db.session.commit()
        return marshal(order, order_fields), 200

    def delete(self, order_id):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return '', 204

api.add_resource(CarListResource, '/api/cars')
api.add_resource(CarResource, '/api/cars/<int:car_id>')
api.add_resource(DriverListResource, '/api/drivers')
api.add_resource(DriverResource, '/api/drivers/<int:driver_id>')
api.add_resource(ClientListResource, '/api/clients')
api.add_resource(ClientResource, '/api/clients/<int:client_id>')
api.add_resource(OrderListResource, '/api/orders')
api.add_resource(OrderResource, '/api/orders/<int:order_id>')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cars')
def list_cars():
    search = request.args.get('search')
    if search:
        cars = Car.query.filter(Car.registration_number.ilike(f'%{search}%')).all()
    else:
        cars = Car.query.all()
    return render_template('cars/list.html', cars=cars)
    
    cars = Car.query.all()
    return render_template('cars/list.html', cars=cars)

@app.route('/cars/add', methods=['GET', 'POST'])
def add_car():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(
            brand=form.brand.data,
            registration_number=form.registration_number.data,
            load_capacity=form.load_capacity.data,
            cargo_type=form.cargo_type.data
        )
        db.session.add(car)
        db.session.commit()
        flash('Автомобиль добавлен успешно!', 'success')
        return redirect(url_for('list_cars'))
    return render_template('cars/add.html', form=form)

@app.route('/cars/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = CarForm(obj=car)
    if form.validate_on_submit():
        form.populate_obj(car)
        db.session.commit()
        flash('Данные автомобиля обновлены!', 'success')
        return redirect(url_for('list_cars'))
    return render_template('cars/edit.html', form=form, car=car)

@app.route('/cars/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Автомобиль удален!', 'success')
    return redirect(url_for('list_cars'))

@app.route('/drivers')
def list_drivers():
    search = request.args.get('search')
    if search:
        drivers = Driver.query.filter(Driver.last_name.ilike(f'%{search}%')).all()
    else:
        drivers = Driver.query.all()
    return render_template('drivers/list.html', drivers=drivers)
    
@app.route('/drivers/add', methods=['GET', 'POST'])
def add_driver():
    form = DriverForm()
    if form.validate_on_submit():
        driver = Driver(
            last_name=form.last_name.data,
            qualification_level=form.qualification_level.data,
            experience_years=form.experience_years.data,
            car_id=form.car_id.data if form.car_id.data != 0 else None
        )
        db.session.add(driver)
        db.session.commit()
        flash('Водитель добавлен успешно!', 'success')
        return redirect(url_for('list_drivers'))
    return render_template('drivers/add.html', form=form)

@app.route('/drivers/edit/<int:driver_id>', methods=['GET', 'POST'])
def edit_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    form = DriverForm(obj=driver)
    if form.validate_on_submit():
        form.populate_obj(driver)
        driver.car_id = form.car_id.data if form.car_id.data != 0 else None
        db.session.commit()
        flash('Данные водителя обновлены!', 'success')
        return redirect(url_for('list_drivers'))
    return render_template('drivers/edit.html', form=form, driver=driver)

@app.route('/drivers/delete/<int:driver_id>', methods=['POST'])
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    flash('Водитель удален!', 'success')
    return redirect(url_for('list_drivers'))

@app.route('/clients')
def list_clients():
    search = request.args.get('search')
    if search:
        clients = Client.query.filter(Client.last_name.ilike(f'%{search}%')).all()
    else:
        clients = Client.query.all()
    return render_template('clients/list.html', clients=clients)

@app.route('/clients/add', methods=['GET', 'POST'])
def add_client():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(
            last_name=form.last_name.data,
            address=form.address.data,
            phone=form.phone.data
        )
        db.session.add(client)
        db.session.commit()
        flash('Клиент добавлен успешно!', 'success')
        return redirect(url_for('list_clients'))
    return render_template('clients/add.html', form=form)

@app.route('/clients/edit/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        form.populate_obj(client)
        db.session.commit()
        flash('Данные клиента обновлены!', 'success')
        return redirect(url_for('list_clients'))
    return render_template('clients/edit.html', form=form, client=client)

@app.route('/clients/delete/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Клиент удален!', 'success')
    return redirect(url_for('list_clients'))

@app.route('/orders')
def list_orders():
    search = request.args.get('search')
    if search:
        orders = Order.query.filter(Order.cargo.ilike(f'%{search}%')).all()
    else:
        orders = Order.query.all()
    return render_template('orders/list.html', orders=orders)

@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            order_date=form.order_date.data,
            cargo=form.cargo.data,
            from_address=form.from_address.data,
            to_address=form.to_address.data,
            completion_date=form.completion_date.data,
            cost=form.cost.data,
            car_id=form.car_id.data,
            driver_id=form.driver_id.data,
            client_id=form.client_id.data
        )
        db.session.add(order)
        db.session.commit()
        flash('Заказ добавлен успешно!', 'success')
        return redirect(url_for('list_orders'))
    return render_template('orders/add.html', form=form)

@app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    form = OrderForm(obj=order)
    if form.validate_on_submit():
        form.populate_obj(order)
        db.session.commit()
        flash('Данные заказа обновлены!', 'success')
        return redirect(url_for('list_orders'))
    return render_template('orders/edit.html', form=form, order=order)

@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Заказ удален!', 'success')
    return redirect(url_for('list_orders'))

@app.route('/orders/receipt/<int:order_id>')
def order_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('orders/receipt.html', order=order)

@app.route('/orders/receipt/<int:order_id>/pdf')
def order_receipt_pdf(order_id):
    order = Order.query.get_or_404(order_id)
    rendered = render_template('orders/receipt_pdf.html', order=order)
    pdf = HTML(string=rendered).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=receipt_{order.id}.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
