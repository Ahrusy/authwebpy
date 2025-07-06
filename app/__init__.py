# Импорт необходимых модулей
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # Для хеширования паролей
from flask_login import LoginManager  # Для управления аутентификацией пользователей

# Создание экземпляра приложения Flask
app = Flask(__name__)

# Конфигурация приложения
app.config['SECRET_KEY'] = 'вашсекретныйключ'  # Ключ для защиты от CSRF-атак
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Путь к базе данных SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем уведомления об изменениях

# Инициализация расширений
db = SQLAlchemy(app)  # Работа с базой данных
bcrypt = Bcrypt(app)  # Хеширование паролей

# Настройка менеджера авторизации
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Маршрут для входа (будет перенаправлять неавторизованных пользователей)
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'  # Сообщение при перенаправлении
login_manager.login_message_category = 'info'  # Категория сообщения (для стилизации)

# Импорт маршрутов в конце, чтобы избежать циклических импортов
from app import routes