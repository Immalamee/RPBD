from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange
from models import Car, Driver, Client

class CarForm(FlaskForm):
    brand = StringField('Марка', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Введите марку автомобиля"})
    registration_number = StringField('Номер регистрации', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "А123ВС45"})
    load_capacity = DecimalField('Грузоподъемность (т)', validators=[DataRequired()], render_kw={"placeholder": "Например, 5.5"})
    cargo_type = StringField('Назначение', validators=[DataRequired(), Length(max=100)], render_kw={"placeholder": "Тип перевозимого груза"})
    submit = SubmitField('Сохранить')


class DriverForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Введите фамилию водителя"})
    qualification_level = IntegerField('Классность', validators=[DataRequired(), NumberRange(min=1)], render_kw={"placeholder": "Введите классность"})
    experience_years = IntegerField('Стаж', validators=[DataRequired(), NumberRange(min=0)], render_kw={"placeholder": "Введите стаж водителя"})
    car_id = SelectField('Автомобиль', coerce=int)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        self.car_id.choices = [(0, 'Нет')] + [(car.id, car.brand) for car in Car.query.all()]

class ClientForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Введите фамилию заказчика"})
    address = StringField('Адрес', validators=[DataRequired(), Length(max=150)], render_kw={"placeholder": "Введите адрес в любом формате"})
    phone = StringField('Телефон', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "Введите номер получателя в любом формате - +7/8"})
    submit = SubmitField('Сохранить')

class OrderForm(FlaskForm):
    order_date = DateTimeField('Дата заказа', format='%Y-%m-%d %H:%M', validators=[DataRequired()], render_kw={"placeholder": "Г-М-Д Ч:М"})
    cargo = StringField('Груз', validators=[DataRequired(), Length(max=100)], render_kw={"placeholder": "Введите название груза, например, пиво"})
    from_address = StringField('Адрес отправления', validators=[DataRequired(), Length(max=150)], render_kw={"placeholder": "Введите адрес отправления в любом формате"})
    to_address = StringField('Адрес назначения', validators=[DataRequired(), Length(max=150)], render_kw={"placeholder": "Введите адрес назначения в любом формате"})
    completion_date = DateTimeField('Дата и время выполнения', format='%Y-%m-%d %H:%M', validators=[DataRequired()], render_kw={"placeholder": "Г-М-Д Ч:М"})
    cost = DecimalField('Стоимость', validators=[DataRequired()], render_kw={"placeholder": "Введите стоимость заказа, например, 617.95"})
    car_id = SelectField('Автомобиль', coerce=int)
    driver_id = SelectField('Водитель', coerce=int)
    client_id = SelectField('Клиент', coerce=int)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.car_id.choices = [(car.id, car.brand) for car in Car.query.all()]
        self.driver_id.choices = [(driver.id, driver.last_name) for driver in Driver.query.all()]
        self.client_id.choices = [(client.id, client.last_name) for client in Client.query.all()]