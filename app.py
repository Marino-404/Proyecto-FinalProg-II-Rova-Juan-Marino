from flask import Flask, request, jsonify, session, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Configuración básica de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'tu_secreto'  # Clave secreta para manejar sesiones de usuario
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'  # Ruta de la base de datos
app.config['DEBUG'] = True  # Activa el modo de depuración para ver errores en detalle

# Inicializa la base de datos
db = SQLAlchemy(app)

# Definición de la tabla de usuarios en la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    nombre = db.Column(db.String(150), nullable=False)  
    apellido = db.Column(db.String(150), nullable=False) 
    username = db.Column(db.String(150), unique=True, nullable=False) 
    password = db.Column(db.String(150), nullable=False) 

# Ruta principal (index.html)
@app.route('/')
def index():
    user_id = session.get('user_id')  # Obtiene el ID del usuario de la sesión
    user = Usuario.query.get(user_id) if user_id else None  # Busca al usuario en la base de datos si está en sesión
    return render_template('index.html', user=user)  # Renderiza la página de inicio con o sin usuario

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Elimina el ID del usuario de la sesión
    return redirect(url_for('index'))  # Redirige a la página de inicio

# Ruta de registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Si el formulario se envía (método POST)
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validaciones del formulario de registro
        if not nombre or not apellido or not email or not password or not confirm_password:
            flash('Por favor, completa todos los campos.')  # Avisa si falta algún campo
            return redirect(url_for('register'))

        # Valida el formato del correo electrónico
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Por favor, ingresa un correo electrónico válido.')
            return redirect(url_for('register'))

        # Verifica que la contraseña tenga al menos 6 caracteres
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.')
            return redirect(url_for('register'))

        # Verifica que las contraseñas coincidan
        if password != confirm_password:
            flash('Las contraseñas no coinciden.')
            return redirect(url_for('register'))

        # Verifica si el correo ya está registrado
        if Usuario.query.filter_by(username=email).first():
            flash('El correo electrónico ya está registrado.')
            return redirect(url_for('register'))

        # Cifra la contraseña antes de guardarla
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Crea un nuevo usuario y lo guarda en la base de datos
        new_user = Usuario(nombre=nombre, apellido=apellido, username=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()  # Confirma los cambios en la base de datos
        flash('Usuario registrado con éxito! Por favor, inicia sesión.')  # Muestra un mensaje de éxito
        return redirect(url_for('login'))  # Redirige a la página de login

    # Renderiza el formulario de registro
    return render_template('register.html')

# Ruta de API para verificar si el correo ya está registrado (usada en el frontend)
@app.route('/api/check_register', methods=['POST'])
def check_register():
    data = request.json  # Obtiene los datos JSON del frontend
    email = data.get('email')
    errors = {}

    # Verifica si el correo ya está en la base de datos
    if Usuario.query.filter_by(username=email).first():
        errors['email'] = 'Este correo electrónico ya está registrado.'

    # Si hay errores, los devuelve al frontend
    if errors:
        return jsonify({'success': False, 'errors': errors})

    # Si no hay errores, confirma que el correo está disponible
    return jsonify({'success': True})

# Ruta de login de usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Si el formulario de login se envía
        email = request.form['email']
        password = request.form['password']
        errors = {}

        # Busca al usuario en la base de datos
        user = Usuario.query.filter_by(username=email).first()

        # Validaciones del login
        if not email:
            errors['email'] = 'Por favor, ingresa tu correo electrónico.'
        elif not user:
            errors['email'] = 'El correo electrónico no está registrado.'

        if not password:
            errors['password'] = 'Por favor, ingresa tu contraseña.'
        elif user and not check_password_hash(user.password, password):
            errors['password'] = 'La contraseña es incorrecta.'

        # Si hay errores, los devuelve al frontend
        if errors:
            return jsonify({'success': False, 'errors': errors})

        # Si todo está correcto, inicia sesión guardando el ID de usuario
        session['user_id'] = user.id
        flash('Inicio de sesión exitoso!')
        return jsonify({'success': True, 'redirect_url': url_for('index')})  # Envía la URL de redirección al frontend

    # Renderiza la página de login
    return render_template('login.html')

# Ruta de API para verificar las credenciales de login
@app.route('/api/check_credentials', methods=['POST'])
def check_credentials():
    data = request.get_json()  # Obtiene los datos JSON del frontend
    email = data.get('email')
    password = data.get('password')
    errors = {}

    # Busca al usuario y valida sus credenciales
    user = Usuario.query.filter_by(username=email).first()
    if not email:
        errors['email'] = 'Por favor, ingresa tu correo electrónico.'
    elif not user:
        errors['email'] = 'El correo electrónico no está registrado.'

    if not password:
        errors['password'] = 'Por favor, ingresa tu contraseña.'
    elif user and not check_password_hash(user.password, password):
        errors['password'] = 'La contraseña es incorrecta.'

    # Si hay errores, los devuelve al frontend
    if errors:
        return jsonify({'success': False, 'errors': errors})

    # Si las credenciales son correctas, inicia sesión y devuelve la URL de redirección
    session['user_id'] = user.id
    return jsonify({'success': True, 'redirect_url': url_for('index')})

# Función para limpiar errores después de cada respuesta
@app.after_request
def clear_errors(response):
    session.pop('errors', None)
    return response

# Ruta para ver productos (requiere estar logueado)
@app.route('/products')
def products():
    if 'user_id' not in session:  # Si no está en sesión, redirige al login
        return redirect(url_for('login'))
    return render_template('products.html')  # Muestra la página de productos

# Configuración para crear la base de datos y ejecutar la app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea todas las tablas si no existen
    app.run(debug=True)  # Ejecuta la app en modo de depuración

