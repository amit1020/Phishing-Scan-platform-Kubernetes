from flask import Blueprint, render_template



#Define the blueprint: 'product', set its url prefix: app.url/product
Main_page_bp = Blueprint(
    'Main_page', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/Main_page/static'
)






@Main_page_bp.route('/')
def product_home():
    return render_template('index.html')
    