from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'tu_secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

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
        
        new_user = Usuario(username=email, password=hashed_password)
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

        if not email or not password:
            flash('Por favor, completa todos los campos.')
            return redirect(url_for('login'))

        user = Usuario.query.filter_by(username=email).first()
        if user is None:
            flash('Usuario no encontrado.')
            return redirect(url_for('login'))

        if not check_password_hash(user.password, password):
            flash('Contraseña incorrecta.')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        flash('Inicio de sesión exitoso!')
        return redirect(url_for('products'))  

    return render_template('login.html')


@app.route('/products')
def products():
    return render_template('products.html') 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)

