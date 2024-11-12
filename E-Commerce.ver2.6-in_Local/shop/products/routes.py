from flask import redirect, url_for, request, flash, render_template, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Product
from .forms import AddProducts
import secrets, os
from shop.customers.models import CustomerOrder
from shop.admin.utils import admin_required


def get_all_brands():
    # Brand.id==Product.brand_id là điều kiện để lấy các brand có trong bảng Product
    brands = Brand.query.join(Product, (Brand.id==Product.brand_id)).all()
    return brands

def get_all_categories():
    return Category.query.join(Product, (Category.id==Product.category_id)).all()

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.stock > 0).paginate(page=page, per_page=8)
    return render_template('products/index.html', title="Store Home", products=products, brands=get_all_brands(), categories=get_all_categories(), CustomerOrder=CustomerOrder)

@app.route('/about')
def about():
    return render_template('about.html', title="About My store", brands=get_all_brands(), categories=get_all_categories(), CustomerOrder=CustomerOrder)


@app.route('/product/<int:id>')
def product_details(id):
    product = Product.query.get_or_404(id)
    brands = Brand.query.join(Product, (Brand.id==Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id==Product.category_id)).all()
    return render_template('products/product_details.html', product=product, title=product.name, brands=brands, categories=categories, CustomerOrder=CustomerOrder)

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    # chọn ra 1 brand có id tương ứng với id truyền vào
    get_b = Brand.query.filter_by(id=id).first_or_404()
    # chọn ra tất cả các sản phẩm có brand_id ăn khớp với id của get_b
    brand = Product.query.filter_by(brand = get_b).paginate(page=page, per_page=8)
    return render_template('products/index.html', brand=brand, title=Brand.query.get(id).name, brands=get_all_brands(), 
    categories=get_all_categories(), get_b=get_b, CustomerOrder=CustomerOrder)

@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    category = Product.query.filter_by(category = get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html', category=category, title=Category.query.get(id).name, 
                            categories=get_all_categories(), brands=get_all_brands(), get_cat=get_cat, CustomerOrder=CustomerOrder)

@app.route('/search', methods=['GET'])
def search():
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('q')
    sort_by = request.args.get('sort', 'default')
    
    # Base search query
    products = Product.query.filter(Product.name.ilike(f'%{keyword}%'))
    brand_results = Product.query.join(Brand).filter(Brand.name.ilike(f'%{keyword}%'))
    category_results = Product.query.join(Category).filter(Category.name.ilike(f'%{keyword}%'))
    
    # Combine results
    search_results = products.union(brand_results, category_results)
    
    # Apply sorting
    if sort_by == 'price_asc':
        search_results = search_results.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        search_results = search_results.order_by(Product.price.desc())
    elif sort_by == 'brand':
        search_results = search_results.join(Brand).order_by(Brand.name.asc())

    if search_results.count() == 0:
        flash(f'Không tìm thấy kết quả cho từ khóa: {keyword}', 'info')
        return redirect(url_for('home'))

    paginated_results = search_results.paginate(page=page, per_page=8)
    
    return render_template('products/index.html',
                         products=paginated_results,
                         brands=get_all_brands(),
                         categories=get_all_categories(),
                         keyword=keyword,
                         sort_by=sort_by,
                         title=f'Search Results for: {keyword}', 
                         CustomerOrder=CustomerOrder)



@app.route('/admin/addbrand', methods=["GET", "POST"])
@admin_required
def admin_addbrand():
    if request.method == "POST":
        brand_name = request.form.get('brand')
        
        # Validate brand name
        if not brand_name or len(brand_name) < 2:
            flash('Brand name must be at least 2 characters', 'danger')
            return redirect(url_for('admin_addbrand'))
            
        # Check for duplicate brand
        if Brand.query.filter_by(name=brand_name).first():
            flash('Brand already exists', 'danger')
            return redirect(url_for('admin_addbrand'))
        
        brand = Brand(name=brand_name)
        db.session.add(brand)
        db.session.commit()
        flash(f'Brand {brand_name} has been added to your database', 'success')
        return redirect(url_for('admin_brands'))

    brands = Brand.query.all()  # Get actual Brand objects
    return render_template('products/addbrand.html', title='Add Brand', brands=brands)

@app.route('/admin/addcategory', methods=["GET", "POST"])
@admin_required
def admin_addcategory():
    if request.method == "POST":
        getCategory = request.form.get('category')
        
        # Kiểm tra category đã tồn tại chưa
        category = Category.query.filter_by(name=getCategory).first()
        if category:
            flash(f'Category {getCategory} already exists', 'danger')
            return redirect(url_for('admin_addcategory'))
            
        # Nếu chưa tồn tại thì thêm mới
        category = Category(name=getCategory)
        db.session.add(category)
        db.session.commit()
        flash(f'Category {getCategory} added successfully', 'success')
        return redirect(url_for('admin_addcategory'))
    return render_template('products/addbrand.html', title='Add Category')


@app.route('/admin/addproduct', methods=["GET", "POST"])
@admin_required
def admin_addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProducts(request.form)
    if request.method == "POST":
        # Validate product name
        name = request.form.get('name')
        if not name or len(name) < 3:
            flash('Tên sản phẩm phải chứa ít nhất 3 kí tự', 'danger')
            return redirect(url_for('admin_addproduct'))
            
        # Validate price
        price = request.form.get('price')
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            flash('Giá không hợp lệ', 'danger')
            return redirect(url_for('admin_addproduct'))
            
        # Validate stock
        stock = request.form.get('stock')
        try:
            stock = int(stock)
            if stock < 0:
                raise ValueError
        except ValueError:
            flash('Số lượng không hợp lệ', 'danger')
            return redirect(url_for('admin_addproduct'))

        desc = form.desc.data
        brand_id = request.form.get('brand')
        category_id = request.form.get('category')
        print(f"ID thương hiệu:{brand_id}, Id danh mục:{category_id}")

        image_1 = photos.save(request.files['image_1'] , name=secrets.token_hex(10) + '.')
        print(f"Tên ảnh 1:{image_1}, Loại của ảnh:{type(image_1)}")
        product = Product(name=name, price=price, stock=stock, desc=desc, brand_id=brand_id, 
        category_id=category_id, image_1=image_1)
        db.session.add(product)
        flash(f"{name} đã được thêm vào database.", 'success')
        db.session.commit()
        return redirect(url_for('admin_addproduct'))
    return render_template('products/addproduct.html', title='Add Product', form=form, brands=brands, categories=categories)

@app.route('/admin/updatebrand/<int:id>', methods=["GET", "POST"])
@admin_required
def admin_updatebrand(id):
    if 'email' not in session:
        flash('Vui lòng đăng nhập!', 'danger')
    
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(f'Thương hiệu của bạn đã được cập nhật', 'success')
        db.session.commit()
        return redirect(url_for('admin_brands'))
    return render_template('products/updatebrand.html', title="Update Brand Info", updatebrand=updatebrand)

@app.route('/admin/updatecategory/<int:id>', methods=["GET", "POST"])
@admin_required
def admin_updatecategory(id):
    if 'email' not in session:
        flash('Vui lòng đăng nhập!', 'danger')
    
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecategory.name = category
        flash(f'Danh mục sản phẩm đã được cập nhật', 'success')
        db.session.commit()
        return redirect(url_for('admin_categories'))
    return render_template('products/updatebrand.html', title="Update category Info", updatecategory=updatecategory)

@app.route('/admin/updateproduct/<int:id>', methods=["GET", "POST"])
@admin_required
def admin_updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    form = AddProducts()

    if request.method == "POST":
        # Get values directly from request.form
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        desc = request.form.get('desc')
        brand = request.form.get('brand')
        category = request.form.get('category')

        # Update product with new values
        product.name = name
        product.price = int(price) if price else product.price
        product.stock = int(stock) if stock else product.stock
        product.desc = desc
        product.brand_id = brand
        product.category_id = category

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + '.')
            except:
                product.image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + '.')

        db.session.commit()
        flash('Sản phẩm đã được cập nhật', 'success')
        return redirect(url_for('admin'))

    # Populate form for GET request
    form.name.data = product.name
    form.price.data = int(product.price)
    form.stock.data = product.stock
    form.desc.data = product.desc

    return render_template('products/updateproduct.html',
                         title="Update Product",
                         form=form,
                         brands=brands,
                         categories=categories,
                         product=product)


@app.route('/admin/deletebrand/<int:id>', methods=["POST"])
@admin_required
def admin_deletebrand(id):
    if 'email' not in session:
        flash('Vui lòng đăng nhập!', 'danger')
    
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'Xóa {brand.name} thành công', 'success')
        return redirect(url_for('admin_brands'))
    flash(f'Không thể xoá {brand.name}!', 'warning')
    return redirect(url_for('admin'))

@app.route('/admin/deletecategory/<int:id>', methods=["POST"])
@admin_required
def admin_deletecategory(id):
    if 'email' not in session:
        flash('Vui lòng đăng nhập!', 'danger')
    
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'Xóa {category.name} thành công', 'success')
        return redirect(url_for('admin_categories'))
    flash(f'Không thể xóa {category.name}', 'warning')
    return redirect(url_for('admin'))

@app.route('/admin/deleteproduct/<int:id>', methods=["POST"])
@admin_required
def admin_deleteproduct(id):
    # Xóa các customer_order liên quan trước
    CustomerOrder.query.filter_by(product_id=id).delete()
    
    # Sau đó mới xóa sản phẩm
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    
    flash(f'Xóa {product.name} thành công!','success')
    return redirect(url_for('admin'))
