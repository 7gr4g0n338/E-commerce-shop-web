from flask import redirect, url_for, request, flash, render_template, session, current_app
from shop import db, app, photos
from shop import bcrypt
from shop.products.routes import get_all_brands, get_all_categories
from .forms import CustomerRegistrationForm, CustomerLoginForm, CustomerUpdateForm
from .models import RegisterModel
import secrets, os
from shop import login_manager
from flask_login import current_user, logout_user, login_user, login_required
from shop.customers.models import CustomerOrder

@app.route('/customer/register', methods=["POST", "GET"])
def register_customer():
        form = CustomerRegistrationForm()
        if form.validate_on_submit():
            # Validate contact number
            if not form.contact.data.isdigit() or len(form.contact.data) < 10:
                flash('Số điện thoại không hợp lệ!', 'danger')
                return redirect(url_for('register_customer'))
            
            # Validate address length
            if len(form.address.data) < 2:
                flash('Độ dài địa chỉ lơn hơn 2', 'danger')
                return redirect(url_for('register_customer'))
            
            # Validate city and state names
            if not all(c.isalnum() or c.isspace() for c in form.state.data):
                flash('Thành Phố, Huyện chỉ gồm các chữ, số và khoảng trắng', 'danger')
                return redirect(url_for('register_customer'))


            hash_password = bcrypt.generate_password_hash(form.password.data)
            register = RegisterModel(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password, country=form.country.data, state=form.state.data,city=form.city.data,
                    address=form.address.data, contact=form.contact.data)
            db.session.add(register)
            db.session.commit()
            flash(f"{form.name.data} đã đăng kí thành công, Mời đăng nhập tài khoản", 'success')
            return redirect(url_for('customerLogin'))
        return render_template('customers/register.html', form=form, title='Register Page',
                             brands=get_all_brands(),
                             categories=get_all_categories(), name=form.name.data,
                             username=form.username.data,
                             email=form.email.data,
                             contact=form.contact.data,
                             address=form.address.data,
                             city=form.city.data,
                             state=form.state.data,
                             country=form.country.data)

@app.route('/customer/login', methods=['GET', "POST"])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = RegisterModel.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash("Sai email hoặc password!", 'danger')
        return redirect(url_for('customerLogin'))
    return render_template('customers/login.html', form=form, title='Login Page',
                         brands=get_all_brands(),
                         categories=get_all_categories())

@app.route('/customer/logout')
def customerLogout():
    logout_user()
    return redirect(url_for('customerLogin'))

@app.route('/customer/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = CustomerUpdateForm()
    if form.validate_on_submit():
        # Validate contact number
        if not form.contact.data.isdigit() or len(form.contact.data) < 10:
            flash('Số điện thoại không hợp lệ!', 'danger')
            return redirect(url_for('user_profile'))
        
        # Validate address length
        if len(form.address.data) < 2:
            flash('Địa chỉ không hợp lệ!', 'danger')
            return redirect(url_for('user_profile'))
        
        # Validate city and state names
        if not all(c.isalpha() or c.isspace() for c in form.city.data) or not all(c.isalpha() or c.isspace() for c in form.state.data):
            flash('Thành Phố, Huyện chỉ gồm các chữ, số và khoảng trắng.', 'danger')
            return redirect(url_for('user_profile'))

        # Check if email already exists for other users
        existing_email = RegisterModel.query.filter(RegisterModel.email == form.email.data, RegisterModel.id != current_user.id).first()
        if existing_email:
            flash('Email này đã được sử dụng', 'danger')
            return redirect(url_for('user_profile'))

        # Check if username already exists for other users
        existing_username = RegisterModel.query.filter(RegisterModel.username == form.username.data, RegisterModel.id != current_user.id).first()
        if existing_username:
            flash('Username này đã được sử dụng', 'danger')
            return redirect(url_for('user_profile'))

        # Update user information
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.contact = form.contact.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.country = form.country.data
        db.session.commit()
        flash('Thông tin cá nhân của bạn đã được cập nhật!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.contact.data = current_user.contact
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.country.data = current_user.country
    return render_template('customers/profile.html', title='Profile', form=form, brands=get_all_brands(), categories=get_all_categories(), CustomerOrder=CustomerOrder)
