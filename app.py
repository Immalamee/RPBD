from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Car, Driver, Client, Order
from forms import CarForm, DriverForm, ClientForm, OrderForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cars')
def list_cars():
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
        flash('Автомобиль добавлен успешно!')
        return redirect(url_for('list_cars'))
    return render_template('cars/add.html', form=form)

@app.route('/cars/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = CarForm(obj=car)
    if form.validate_on_submit():
        form.populate_obj(car)
        db.session.commit()
        flash('Данные автомобиля обновлены!')
        return redirect(url_for('list_cars'))
    return render_template('cars/edit.html', form=form, car=car)

@app.route('/cars/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Автомобиль удален!')
    return redirect(url_for('list_cars'))

@app.route('/drivers')
def list_drivers():
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
        flash('Водитель добавлен успешно!')
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
        flash('Данные водителя обновлены!')
        return redirect(url_for('list_drivers'))
    return render_template('drivers/edit.html', form=form, driver=driver)

@app.route('/drivers/delete/<int:driver_id>', methods=['POST'])
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    flash('Водитель удален!')
    return redirect(url_for('list_drivers'))

@app.route('/clients')
def list_clients():
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
        flash('Клиент добавлен успешно!')
        return redirect(url_for('list_clients'))
    return render_template('clients/add.html', form=form)

@app.route('/clients/edit/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        form.populate_obj(client)
        db.session.commit()
        flash('Данные клиента обновлены!')
        return redirect(url_for('list_clients'))
    return render_template('clients/edit.html', form=form, client=client)

@app.route('/clients/delete/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Клиент удален!')
    return redirect(url_for('list_clients'))

# Маршруты для заказов
@app.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('orders/list.html', orders=orders)

@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
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
        flash('Заказ добавлен успешно!')
        return redirect(url_for('list_orders'))
    return render_template('orders/add.html', form=form)

@app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    form = OrderForm(obj=order)
    if form.validate_on_submit():
        form.populate_obj(order)
        db.session.commit()
        flash('Данные заказа обновлены!')
        return redirect(url_for('list_orders'))
    return render_template('orders/edit.html', form=form, order=order)

@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Заказ удален!')
    return redirect(url_for('list_orders'))

@app.route('/orders/receipt/<int:order_id>')
def order_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('orders/receipt.html', order=order)

if __name__ == '__main__':
    app.run(debug=True)
