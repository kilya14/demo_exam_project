from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
import re

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(), 
        Length(min=6, message='Логин должен содержать минимум 6 символов'),
        Regexp('^[a-zA-Z0-9]+$', message='Логин должен содержать только латинские буквы и цифры')
    ])
    full_name = StringField('ФИО', validators=[DataRequired(), Length(min=3, max=200)])
    phone = StringField('Контактный номер телефона', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, message='Пароль должен содержать минимум 8 символов')])
    submit = SubmitField('Регистрация')

class OrderForm(FlaskForm):
    service_type = SelectField('Тип услуги', choices=[
        ('Зал', 'Зал'),
        ('Ресторан', 'Ресторан'),
        ('Летняя веранда', 'Летняя веранда'),
        ('Закрытая веранда', 'Закрытая веранда')
    ], validators=[DataRequired()])
    service_date = StringField('Дата услуги (ДД.ММ.ГГГГ)', validators=[
        DataRequired(),
        Regexp(r'^\d{2}\.\d{2}\.\d{4}$', message='Формат даты должен быть ДД.ММ.ГГГГ')
    ])
    payment_method = SelectField('Способ оплаты', choices=[
        ('Наличные', 'Наличные'),
        ('Банковская карта', 'Банковская карта'),
        ('Онлайн-перевод', 'Онлайн-перевод')
    ], validators=[DataRequired()])
    submit = SubmitField('Создать заявку')

class ReviewForm(FlaskForm):
    text = TextAreaField('Отзыв', validators=[DataRequired(), Length(min=10, max=500)])
    rating = SelectField('Оценка', choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')], validators=[DataRequired()])
    submit = SubmitField('Оставить отзыв')
