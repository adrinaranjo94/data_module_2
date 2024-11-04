from flask import Flask, render_template, redirect, url_for, request, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from utils.decorators import role_required  # Decorador para verificación de roles
from models import db, User, Recipe  # Modelos de la base de datos

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)

# Rutas públicas
@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # No se hashea
        role = request.form['role']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        
        # Guardar la contraseña en texto plano
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            access_token = create_access_token(identity={"username": user.username, "role": user.role})
            response = make_response(redirect(url_for('profile')))
            set_access_cookies(response, access_token)
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful.', 'success')
            return response
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)  # Elimina el token de la cookie
    session.pop('username', None)  # Limpia la sesión
    flash('Logged out successfully.', 'info')
    return response

# Rutas protegidas
@app.route('/profile')
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    return render_template('profile.html', user=user)

@app.route('/recipe/add', methods=['GET', 'POST'])
@jwt_required()
@role_required('admin')
def add_recipe():
    if request.method == 'POST':
        new_recipe = Recipe(
            name=request.form['name'],
            ingredients=request.form['ingredients'],
            steps=request.form['steps'],
            prep_time=request.form['prep_time'],
            difficulty=request.form['difficulty']
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

@app.route('/recipe/edit/<int:recipe_id>', methods=['GET', 'POST'])
@jwt_required()
@role_required('admin')
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == 'POST':
        recipe.name = request.form['name']
        recipe.ingredients = request.form['ingredients']
        recipe.steps = request.form['steps']
        recipe.prep_time = request.form['prep_time']
        recipe.difficulty = request.form['difficulty']
        db.session.commit()
        return redirect(url_for('recipe_detail', recipe_id=recipe.id))
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipe/delete/<int:recipe_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index'))

# Para probar decorador y otras vistas sin proteger
@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)
