from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Order, Review
from app.forms import LoginForm, RegisterForm, OrderForm, ReviewForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('main.admin'))
            return redirect(url_for('main.profile'))
        flash('Неверный логин или пароль', 'error')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Логин уже занят', 'error')
            return render_template('register.html', form=form)
        
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email уже зарегистрирован', 'error')
            return render_template('register.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/profile')
@login_required
def profile():
    return redirect(url_for('main.orders'))

@bp.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    order_form = OrderForm()
    if order_form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            service_type=order_form.service_type.data,
            service_date=order_form.service_date.data,
            payment_method=order_form.payment_method.data
        )
        db.session.add(order)
        db.session.commit()
        flash('Заявка создана!', 'success')
        return redirect(url_for('main.orders'))

    my_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', order_form=order_form, orders=my_orders)

@bp.route('/review/<int:order_id>', methods=['GET', 'POST'])
@login_required
def review(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Доступ запрещён', 'error')
        return redirect(url_for('main.orders'))
    
    if order.status == 'Новая':
        flash('Отзыв можно оставить только после изменения статуса администратором', 'error')
        return redirect(url_for('main.orders'))
    
    existing_review = Review.query.filter_by(order_id=order_id).first()
    if existing_review:
        flash('Вы уже оставили отзыв для этой заявки', 'error')
        return redirect(url_for('main.orders'))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            order_id=order_id,
            text=form.text.data,
            rating=int(form.rating.data)
        )
        db.session.add(review)
        db.session.commit()
        flash('Отзыв добавлен!', 'success')
        return redirect(url_for('main.orders'))
    
    return render_template('review.html', form=form, order=order)

@bp.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('Доступ запрещён', 'error')
        return redirect(url_for('main.profile'))

    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    status_filter = request.args.get('status', '')
    query = Order.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin.html', orders=pagination.items, pagination=pagination, status_filter=status_filter)

@bp.route('/admin/update_status/<int:order_id>', methods=['POST'])
@login_required
def update_status(order_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Доступ запрещён'}), 403
    
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['Новая', 'Услуга назначена', 'Услуга завершена']:
        order.status = new_status
        db.session.commit()
        flash(f'Статус заявки #{order_id} изменён на "{new_status}"', 'success')
        return jsonify({'success': True, 'message': 'Статус обновлён'})
    
    return jsonify({'success': False, 'message': 'Неверный статус'}), 400

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
