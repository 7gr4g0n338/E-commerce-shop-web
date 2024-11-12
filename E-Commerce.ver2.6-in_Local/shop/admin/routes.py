import os
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import login_user
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Product, Brand, Category
from shop.customers.models import RegisterModel, CustomerOrder
from shop.admin.utils import admin_required
from flask_login import logout_user
from datetime import datetime, timedelta

@app.route('/admin')
@admin_required
def admin():
    if 'email' not in session:
        flash('Vui lòng đăng nhập!', 'danger')
        return redirect(url_for('login'))
    
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=10)
    return render_template('admin/index.html', title='Admin Page', products=products)



@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.role == 'admin':
            password = form.password.data.encode('utf-8')
            if bcrypt.check_password_hash(user.password.encode('utf-8'), password):
                login_user(user)
                session['email'] = form.email.data
                session['admin'] = True
                flash(f'Welcome {user.name}', 'success')
                return redirect(url_for('admin'))
        flash('Sai email hoặc password!', 'danger')
        return redirect(url_for('admin_login'))
    return render_template('admin/login.html', form=form, title='Login Page', CustomerOrder=CustomerOrder)

@app.route('/admin/logout')
def admin_logout():
    logout_user()
    session.pop('email', None)
    session.pop('admin', None)
    flash('Bạn đã đăng xuất thành công!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/search', methods=['GET'])
@admin_required
def admin_search():
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('q')
    search_type = request.args.get('type', 'products')
    
    if not keyword:
        return redirect(url_for('admin'))

    if search_type == 'users':
        # Search users with pagination
        users_pagination = RegisterModel.query.filter(
            db.or_(
                RegisterModel.name.ilike(f'%{keyword}%'),
                RegisterModel.email.ilike(f'%{keyword}%'),
                RegisterModel.username.ilike(f'%{keyword}%')
            )
        ).paginate(page=page, per_page=10)
        
        if not users_pagination.items:
            flash(f'Không tìm thấy người dùng nào liên quan tới từ khóa: {keyword}', 'info')
            return redirect(url_for('admin_users'))
            
        # Get cart information for found users
        user_carts = {}
        week_ago = datetime.now() - timedelta(days=7)
        new_users = RegisterModel.query.filter(RegisterModel.date_created >= week_ago).all()
        
        for user in users_pagination.items:
            cart_items = CustomerOrder.query.filter_by(customer_id=user.id).order_by(CustomerOrder.date_added.desc()).limit(3).all()
            user_carts[user.id] = cart_items
            
        return render_template('admin/users.html', 
                             users=users_pagination.items,
                             pagination=users_pagination,
                             new_users=new_users,
                             user_carts=user_carts,
                             title=f'User Search Results: {keyword}')
    else:
        # Product search remains unchanged
        products = Product.query.join(Brand).join(Category).filter(
            db.or_(
                Product.name.ilike(f'%{keyword}%'),
                Brand.name.ilike(f'%{keyword}%'),
                Category.name.ilike(f'%{keyword}%')
            )
        ).paginate(page=page, per_page=10)

        if not products.items:
            flash(f'Không tìm thấy sản phẩm nào liên quan tới từ khóa: {keyword}', 'info')
            return redirect(url_for('admin'))

        return render_template('admin/index.html',
                             products=products,
                             brands=Brand.query.all(),
                             categories=Category.query.all(),
                             title=f'Product Search Results: {keyword}')


@app.route('/admin/brands')
@admin_required
def admin_brands():
    if "email" not in session:
        flash(f"Vui lòng đăng nhập!", "danger")
        return redirect(url_for("admin_login"))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('products/brand.html', title="Brands Page", brands=brands)

@app.route('/admin/categories')
@admin_required
def admin_categories():
    if "email" not in session:
        flash(f"Vui lòng đăng nhập!", "danger")
        return redirect(url_for("admin_login"))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('products/categories.html', title="Categories Page", categories=categories)

@app.route('/admin/users')
@admin_required
def admin_users():
    if "email" not in session:
        flash(f"Vui lòng đăng nhập!", "danger")
        return redirect(url_for("admin_login"))
        
    users = RegisterModel.query.order_by(RegisterModel.date_created.desc()).all()
    week_ago = datetime.now() - timedelta(days=7)
    new_users = RegisterModel.query.filter(RegisterModel.date_created >= week_ago).all()
    
    user_carts = {}
    for user in users:
        # First get recently added items (in_cart)
        added_items = CustomerOrder.query.filter_by(
            customer_id=user.id, 
            status='in_cart'
        ).order_by(CustomerOrder.date_added.desc()).limit(5).all()
        
        # Then get recently removed items if needed
        remaining_slots = 5 - len(added_items)
        removed_items = []
        if remaining_slots > 0:
            removed_items = CustomerOrder.query.filter_by(
                customer_id=user.id,
                status='removed'
            ).order_by(CustomerOrder.date_added.desc()).limit(remaining_slots).all()
            
        # Combine and sort by date
        user_carts[user.id] = sorted(
            added_items + removed_items,
            key=lambda x: x.date_added,
            reverse=True
        )
    
    return render_template('admin/users.html', users=users, new_users=new_users, user_carts=user_carts)

@app.route('/admin/delete_user/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    if "email" not in session:
        flash(f"Vui lòng đăng nhập!", "danger")
        return redirect(url_for("admin_login"))
        
    user = RegisterModel.query.get_or_404(id)
    try:
        # First delete all orders associated with this user
        CustomerOrder.query.filter_by(customer_id=id).delete()
        # Then delete the user
        db.session.delete(user)
        db.session.commit()
        flash(f'Đã xóa người dùng {user.name}', 'success')
    except:
        flash('Có lỗi xảy ra khi xóa người dùng', 'danger')
        
    return redirect(url_for('admin_users'))


@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    import re
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Validate email format and existence
        if not re.match(r"[^@]+@[^@]+\.[^@]+", form.email.data):
            flash('Sai định dạng email!', 'danger')
            return redirect(url_for('register'))
            
        # Validate password strength
        if len(form.password.data) < 8:
            flash('Mật khẩu phải chứa ít nhất 8 kí tự', 'danger')
            return redirect(url_for('register'))
            
        # Check username length and characters
        if not re.match("^[A-Za-z0-9_-]*$", form.username.data):
            flash('Tên người dùng chỉ có thể chứa chữ cái, số, dấu gạch dưới và dấu gạch ngang!', 'danger')
            return redirect(url_for('register'))
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email đã được đăng ký. Vui lòng sử dụng email khác!', 'danger')
            return render_template('admin/register.html', form=form, title="Registration page")
            
        # If email doesn't exist, proceed with registration
        password = form.password.data.encode('utf-8')
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(
            name=form.name.data,
            username=form.username.data, 
            email=form.email.data,
            password=hash_password,
            role='admin'
        )
        db.session.add(user)
        db.session.commit()
        flash('Đăng kí thành công. Xin mời đăng nhập!', 'success')
        return redirect(url_for('admin_login'))
        
    return render_template('admin/register.html', form=form, title="Registration page")


