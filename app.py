from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'tu_secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)  
    apellido = db.Column(db.String(150), nullable=False) 
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@app.route('/')
def index():
    user_id = session.get('user_id') 
    user = Usuario.query.get(user_id) if user_id else None 
    return render_template('index.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    flash('Has cerrado sesión exitosamente.')  
    return redirect(url_for('index')) 



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not nombre or not apellido or not email or not password or not confirm_password:
            flash('Por favor, completa todos los campos.')
            return redirect(url_for('register'))

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Por favor, ingresa un correo electrónico válido.')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden.')
            return redirect(url_for('register'))

        if Usuario.query.filter_by(username=email).first():
            flash('El correo electrónico ya está registrado.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = Usuario(nombre=nombre, apellido=apellido, username=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito! Por favor, inicia sesión.')
        return redirect(url_for('login'))  

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        errors = {}

        if not email:
            errors['email_error'] = 'Por favor, ingresa tu correo electrónico.'
        elif not Usuario.query.filter_by(username=email).first():
            errors['email_error'] = 'El correo electrónico no está registrado.'

        if not password:
            errors['password_error'] = 'Por favor, ingresa tu contraseña.'
        else:
            user = Usuario.query.filter_by(username=email).first()
            if user and not check_password_hash(user.password, password):
                errors['password_error'] = 'La contraseña es incorrecta.'

        if errors:
            session['errors'] = errors
            return redirect(url_for('login'))

        session.pop('errors', None)
        session['user_id'] = user.id
        flash('Inicio de sesión exitoso!')
        return redirect(url_for('index'))

    return render_template('login.html')

@app.after_request
def clear_errors(response):
    session.pop('errors', None)
    return response


@app.route('/products')
def products():
    return render_template('products.html') 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)

