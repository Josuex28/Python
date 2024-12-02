from flask import jsonify, Flask, render_template, request, redirect, url_for, flash
import conexion

app = Flask(__name__)
app.secret_key = 'vacio'  

@app.route('/')
def formulario_registro():
    return render_template('registro.html')

@app.route('/registrar', methods=['POST'])
def registrar_usuario():

    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    email = request.form['email']
    password = request.form['password']

    try:
        conn = conexion.conectar()
        cursor = conn.cursor()

   
        cursor.execute("SELECT * FROM registros WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            return jsonify({"message": "Usuario ya registrado"})

       
        query = """
        INSERT INTO registros (nombre, apellido, telefono, email, password)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, apellido, telefono, email, password)
        cursor.execute(query, valores)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Registro exitoso"})
    except Exception as e:
        print("Error al registrar usuario:", e)
        return jsonify({"message": "Error en el registro"})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        conn = conexion.conectar()
        cursor = conn.cursor()

        
        cursor.execute("SELECT * FROM registros WHERE nombre = %s AND password = %s", (nombre, password))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            return jsonify({"message": "Inicio de sesión exitoso"})
        else:
            return jsonify({"message": "Usuario o contraseña incorrectos"})

    return render_template('login.html')



@app.route('/bienvenida')
def bienvenida():
    return render_template('bienvenida.html')  

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')  

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')  

@app.route('/reseñas')
def reseñas():
    return render_template('reseñas.html')  

@app.route('/portafolio')
def portafolio():
    return render_template('portafolio.html') 

@app.route('/detalles')
def detalles():
    return render_template('detalles.html')  


@app.route('/reservar', methods=['POST'])
def reservar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    fecha = request.form['fecha']
    hora = request.form['hora']
    servicio = request.form['servicio']
    
    # Crear una nueva cita
    nueva_cita = citas(nombre=nombre, correo=correo, fecha=fecha, hora=hora, servicio=servicio)
    db.session.add(nueva_cita)
    db.session.commit()
    
    return jsonify(message="Cita agendada con éxito"), 200

if __name__ == '__main__':
    app.run(debug=True)
