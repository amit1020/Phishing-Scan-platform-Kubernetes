from flask import (
    Blueprint, render_template, request
    )


admin_bp = Blueprint(
    'admin', __name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static'
)







@admin_bp.route('/')
def product_home():
    return render_template('admin_home.html')



    
@admin_bp.route('/add_user', methods=['POST'])
def add_user(data):
    data = request.form
    print(data)
    pass


    
    