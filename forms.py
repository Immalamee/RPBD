from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange
from models import Car, Driver, Client

class CarForm(FlaskForm):
    brand = StringField('Марка', validators=[DataRequired(), Length(max=50)])
    registration_number = StringField('Номер регистрации', validators=[DataRequired(), Length(max=20)])
    load_capacity = DecimalField('Грузоподъемность', validators=[DataRequired()])
    cargo_type = StringField('Назначение', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Сохранить')

class DriverForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(max=50)])
    qualification_level = IntegerField('Классность', validators=[DataRequired(), NumberRange(min=1)])
    experience_years = IntegerField('Стаж', validators=[DataRequired(), NumberRange(min=0)])
    car_id = SelectField('Автомобиль', coerce=int)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        self.car_id.choices = [(0, 'Нет')] + [(car.id, car.brand) for car in Car.query.all()]

class ClientForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(max=50)])
    address = StringField('Адрес', validators=[DataRequired(), Length(max=150)])
    phone = StringField('Телефон', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Сохранить')

class OrderForm(FlaskForm):
    cargo = StringField('Груз', validators=[DataRequired(), Length(max=100)])
    from_address = StringField('Адрес отправления', validators=[DataRequired(), Length(max=150)])
    to_address = StringField('Адрес назначения', validators=[DataRequired(), Length(max=150)])
    completion_date = DateTimeField('Дата и время выполнения', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    cost = DecimalField('Стоимость', validators=[DataRequired()])
    car_id = SelectField('Автомобиль', coerce=int)
    driver_id = SelectField('Водитель', coerce=int)
    client_id = SelectField('Клиент', coerce=int)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.car_id.choices = [(car.id, car.brand) for car in Car.query.all()]
        self.driver_id.choices = [(driver.id, driver.last_name) for driver in Driver.query.all()]
        self.client_id.choices = [(client.id, client.last_name) for client in Client.query.all()]