from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import User, Transaction
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# สร้างตัวแปร main เป็น Blueprint แทนการใช้ app ตรงๆ
main = Blueprint('main', __name__)

# เปลี่ยนจาก @app เป็น @main ให้หมดทั้งไฟล์
@main.route('/')
@login_required
def index():
    search = request.args.get('search')
    if search:
        items = Transaction.query.filter(
            Transaction.user_id == current_user.id,
            Transaction.title.ilike(f'%{search}%')
        ).all()
    else:
        items = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', items=items)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        return "ขออภัย คุณไม่มีสิทธิ์เข้าถึงหรือแก้ไขรายการนี้", 403
    
    if request.method == 'POST':
        transaction.title = request.form.get('title')
        transaction.amount = request.form.get('amount')
        transaction.type = request.form.get('type')
        db.session.commit()
        return redirect(url_for('main.index')) # ต้องแก้เป็น main.index
    
    return render_template('edit.html', transaction=transaction)

@main.route('/delete/<int:id>')
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id == current_user.id:
        db.session.delete(transaction)
        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('ชื่อผู้ใช้นี้ถูกใช้ไปแล้ว')
            return redirect(url_for('main.register'))
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/add', methods=['POST'])
@login_required
def add_transaction():
    title = request.form.get('title')
    amount = request.form.get('amount')
    
    if title and amount:
        # สร้างรายการใหม่ผูกกับ ID ของคนที่ล็อกอินอยู่
        new_item = Transaction(
            title=title, 
            amount=float(amount), 
            user_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        
    return redirect(url_for('main.index'))