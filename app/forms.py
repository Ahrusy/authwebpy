from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


class RegistrationForm(FlaskForm):
    """Форма регистрации нового пользователя"""

    username = StringField('Имя пользователя',
                           validators=[
                               DataRequired(message='Поле обязательно для заполнения'),
                               Length(min=2, max=20,
                                      message='Длина имени должна быть от 2 до 20 символов')
                           ],
                           render_kw={"placeholder": "Придумайте имя пользователя"})

    email = StringField('Email',
                        validators=[
                            DataRequired(message='Поле обязательно для заполнения'),
                            Email(message='Введите корректный email адрес')
                        ],
                        render_kw={"placeholder": "Ваш email"})

    password = PasswordField('Пароль',
                             validators=[
                                 DataRequired(message='Поле обязательно для заполнения'),
                                 Length(min=8, max=128,
                                        message='Пароль должен быть от 8 до 128 символов')
                             ],
                             render_kw={"placeholder": "Придумайте пароль"})

    confirm_password = PasswordField('Подтверждение пароля',
                                     validators=[
                                         DataRequired(message='Поле обязательно для заполнения'),
                                         EqualTo('password', message='Пароли не совпадают')
                                     ],
                                     render_kw={"placeholder": "Повторите пароль"})

    submit = SubmitField('Создать аккаунт',
                         render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Аккаунт с таким email уже существует.')


class LoginForm(FlaskForm):
    """Форма авторизации пользователя"""

    email = StringField('Email',
                        validators=[
                            DataRequired(message='Поле обязательно для заполнения'),
                            Email(message='Введите корректный email адрес')
                        ],
                        render_kw={"placeholder": "Ваш email"})

    password = PasswordField('Пароль',
                             validators=[
                                 DataRequired(message='Поле обязательно для заполнения')
                             ],
                             render_kw={"placeholder": "Ваш пароль"})

    remember = BooleanField('Запомнить меня',
                            render_kw={"class": "form-check-input"})

    submit = SubmitField('Войти',
                         render_kw={"class": "btn btn-primary"})


class EditProfileForm(FlaskForm):
    """Форма редактирования профиля пользователя"""

    username = StringField('Имя пользователя',
                           validators=[
                               DataRequired(message='Поле обязательно для заполнения'),
                               Length(min=2, max=20,
                                      message='Длина имени должна быть от 2 до 20 символов')
                           ],
                           render_kw={"placeholder": "Ваше имя пользователя"})

    email = StringField('Email',
                        validators=[
                            DataRequired(message='Поле обязательно для заполнения'),
                            Email(message='Введите корректный email адрес')
                        ],
                        render_kw={"placeholder": "Ваш email"})

    current_password = PasswordField('Текущий пароль',
                                     validators=[
                                         DataRequired(message='Необходимо подтвердить текущий пароль')
                                     ],
                                     render_kw={"placeholder": "Ваш текущий пароль"})

    new_password = PasswordField('Новый пароль',
                                 validators=[
                                     Length(min=8, max=128,
                                            message='Пароль должен быть от 8 до 128 символов')
                                 ],
                                 render_kw={"placeholder": "Оставьте пустым, если не нужно менять"})

    confirm_password = PasswordField('Подтвердите новый пароль',
                                     validators=[
                                         EqualTo('new_password', message='Пароли должны совпадать')
                                     ],
                                     render_kw={"placeholder": "Повторите новый пароль"})

    submit = SubmitField('Обновить профиль',
                         render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя уже занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Аккаунт с таким email уже существует.')

    def validate_current_password(self, current_password):
        if not current_user.verify_password(current_password.data):
            raise ValidationError('Неверный текущий пароль')