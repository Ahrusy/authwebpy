from app import app, db
from app.models import User
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash  # Добавлен импорт


def initialize_database():
    with app.app_context():
        try:
            print("🔄 Начало инициализации базы данных...")

            # Удаляем все таблицы (осторожно - это удалит все данные!)
            db.drop_all()
            print("🗑️ Старые таблицы удалены")

            # Создаем таблицы заново
            db.create_all()
            print("🛠️ Создание новых таблиц...")

            # Проверяем создание таблицы user
            inspector = inspect(db.engine)
            table_names = inspector.get_table_names()

            if 'user' in table_names:
                print("✅ Таблица 'user' успешно создана!")

                # Создаем тестового пользователя для проверки
                try:
                    test_user = User(
                        username='test',
                        email='test@example.com',
                        password_hash=generate_password_hash('testpassword')
                    )
                    db.session.add(test_user)
                    db.session.commit()
                    print("👤 Тестовый пользователь создан:")
                    print(f"Username: test\nPassword: testpassword")
                except Exception as user_error:
                    db.session.rollback()
                    print(f"⚠️ Ошибка при создании тестового пользователя: {user_error}")
            else:
                print("❌ Ошибка: таблица 'user' не создана")

        except Exception as e:
            print(f"❌ Критическая ошибка: {str(e)}")
            db.session.rollback()
        finally:
            db.session.close()


if __name__ == '__main__':
    initialize_database()
    print("🏁 Завершено!")