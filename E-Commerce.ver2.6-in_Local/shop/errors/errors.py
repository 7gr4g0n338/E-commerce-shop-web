from flask import render_template, redirect, url_for, flash
from shop import app
from shop.products.routes import get_all_brands, get_all_categories

@app.errorhandler(404)
def page_not_found(error):
    flash('Trang bạn đang tìm kiếm không tồn tại', 'danger')
    return render_template('errors/404.html', 
                         brands=get_all_brands(),
                         categories=get_all_categories()), 404

@app.errorhandler(500) 
def internal_error(error):
    flash('Đã xảy ra lỗi máy chủ', 'danger')
    return render_template('errors/500.html',
                         brands=get_all_brands(), 
                         categories=get_all_categories()), 500
