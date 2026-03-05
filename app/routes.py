from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Transaction
from app import db

main = Blueprint('main', __name__)

# --- ระบบสมาชิก (โจทย์ข้อ 1) ---
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') # แบบง่ายๆ ก่อนส่งอาจารย์
        new_user = User(username=username, password=password)
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
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --- ระบบจัดการเงิน CRUD (โจทย์ข้อ 3 & 4) ---
@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        amount = request.form.get('amount')
        new_tx = Transaction(title=title, amount=float(amount), owner=current_user)
        db.session.add(new_tx)
        db.session.commit()
        return redirect(url_for('main.index'))
    
    # ดึงข้อมูลมาแสดง (Read)
    user_txs = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', transactions=user_txs)

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    tx = Transaction.query.get(id)
    if tx.owner == current_user:
        db.session.delete(tx)
        db.session.commit()
    return redirect(url_for('main.index'))