from flask import redirect, render_template, session, url_for, flash, request, current_app
from shop import db, app
from shop.products.models import Product
from shop.products.routes import get_all_brands, get_all_categories
from flask_login import current_user
from shop.customers.models import CustomerOrder
from datetime import datetime



# mục đích là gộp đơn hàng lại, Nếu ở dạng list - mảng, thì gộp lại list dễ - giống kiểu thêm phần tử vào mảng. còn nếu là dạng dict - các key:value, thì phải chuyển nó thành dạng list - mảng => sau dó mới chuyển lại thành dict
def merge_dict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=["POST"])
def add_cart():
    if not current_user.is_authenticated:
        flash('Vui lòng đăng nhập để thêm sản phẩm quan tâm', 'danger')
        return redirect(url_for('customerLogin'))
        
    try:
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        
        # Validate product exists
        product = Product.query.get_or_404(product_id)
        
        # Validate quantity
        if quantity <= 0:
            flash('Số lượng phải lớn hơn 0', 'danger')
            return redirect(request.referrer)
            
        if quantity > product.stock:
            flash(f'Số lượng tối đa có sẵn là {product.stock}', 'danger')
            return redirect(request.referrer)
            
        # Check if product already in cart
        cart_item = CustomerOrder.query.filter_by(
            product_id=product_id,
            customer_id=current_user.id,
            status='in_cart'
        ).first()
        
        if cart_item:
            # Validate total quantity doesn't exceed stock
            if cart_item.quantity + quantity > product.stock:
                flash(f'Không thể thêm. Số lượng tối đa là {product.stock}', 'danger')
                return redirect(request.referrer)
            cart_item.quantity += quantity
        else:
            cart_item = CustomerOrder(
                product_id=product_id,
                quantity=quantity,
                customer_id=current_user.id,
                status='in_cart'
            )
            db.session.add(cart_item)
            
        db.session.commit()
        flash('Đã thêm sản phẩm vào danh sách quan tâm', 'success')
        return redirect(request.referrer)
        
    except (ValueError, TypeError):
        flash('Dữ liệu không hợp lệ', 'danger')
        return redirect(request.referrer)

@app.route('/cart')
def get_cart():
    total_without_tax = 0
    if current_user.is_authenticated:        # Lấy giỏ hàng từ database cho user đã đăng nhập
        cart_items = CustomerOrder.query.filter_by(
            customer_id=current_user.id,
            status='in_cart'
        ).all()
        
        for item in cart_items:
            total_without_tax += item.product.price * item.quantity
            
        return render_template('products/cart.html', 
                             cart_items=cart_items,
                             total_without_tax=total_without_tax,
                             brands=get_all_brands(),
                             categories=get_all_categories(), CustomerOrder=CustomerOrder)
    else:
        flash('Vui lòng đăng nhập để xem sản phẩm quan tâm', 'danger')
        # Lấy giỏ hàng từ session cho user ẩn danh
        if 'shopcart' not in session:
            return redirect(request.referrer)
            
        for key, product in session['shopcart'].items():
            quantity = product['quantity']
            if quantity and str(quantity).strip():
                total_without_tax += product['price'] * int(quantity)
            else:
                total_without_tax += product['price'] * 0
                
        return render_template('products/cart.html',
                             total_without_tax=total_without_tax,
                             brands=get_all_brands(),
                             categories=get_all_categories())

@app.route('/updatecart/<int:code>', methods=["POST"])
def updatecart(code):
    if 'shopcart' not in session and len(session['shopcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['shopcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item Updated', 'success')
                    return redirect(url_for('get_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('get_cart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if current_user.is_authenticated:
        # Handle logged in users - update database
        order = CustomerOrder.query.filter_by(
            customer_id=current_user.id,
            product_id=id,
            status='in_cart'
        ).first()
        if order:
            order.status = 'removed'
            order.date_added = datetime.now()  # Cập nhật thời gian khi xóa
            db.session.commit()
        return redirect(url_for('get_cart'))
    else:
        # Handle anonymous users - update session
        if 'shopcart' not in session or len(session['shopcart']) <= 0:
            return redirect(url_for('home'))
            
        try:
            session.modified = True
            for key, item in session['shopcart'].items():
                if int(key) == id:
                    session['shopcart'].pop(key, None)
                    return redirect(url_for('get_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('get_cart'))


@app.route('/clearcart')
def clearcart():
    try:
        # Update status for all items in cart to 'removed'
        if current_user.is_authenticated:
            cart_items = CustomerOrder.query.filter_by(
                customer_id=current_user.id,
                status='in_cart'
            ).all()
            
            for item in cart_items:
                item.status = 'removed'
            db.session.commit()

        # Clear the cart session
        session.pop('shopcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)