from app import create_app, db
from app.models import User, Order

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    admin = User(
        username='Admin26',
        email='admin@portal.local',
        full_name='Администратор Системы',
        phone='+79991234567',
        role='admin'
    )
    admin.set_password('Demo20')
    db.session.add(admin)
    
    test_user = User(
        username='testuser',
        email='test@example.com',
        full_name='Тестовый Пользователь',
        phone='+79991234568'
    )
    test_user.set_password('testpass123')
    db.session.add(test_user)
    
    db.session.commit()
    print('База данных инициализирована!')
    print('Админ: Admin26 / Demo20')
    print('Тестовый пользователь: testuser / testpass123')
