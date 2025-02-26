from flask import Blueprint, render_template, redirect, url_for,flash, session







login_bp = Blueprint(
    'login_page', __name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/login_page/static')




@login_bp.route('/', methods=['GET'])
def PageShowUp():
    return render_template('/login.html') 







@login_bp.route('/UserPage/', methods=['GET'])
def UserPage():
    if 'user' not in session:
        return redirect(url_for('login_bp.PageShowUp'))  # Redirect to login page if not logged in 
    return render_template('/user.html') 



@login_bp.route('/logout') 
def logout():
    session.clear()  # Clear session
    return redirect(url_for('login_bp.PageShowUp'))