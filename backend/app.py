from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import bcrypt 
from flasgger import Swagger

app = Flask(__name__)  # Nos permite acceder desde una API externa
CORS(app)
Swagger = Swagger(app)

# Función para conectarnos a la base de datos de mysql
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset="utf8mb4")
    return conn

# Ruta para consulta general del baul de contraseñas
@app.route("/", methods=['GET'])
def consulta_general():
    try:
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul")
        datos = cur.fetchall()
        data = []
        for row in datos:
            dato = {
                'id_baul': row[0],
                'Plataforma': row[1],
                'usuario': row[2],
                'clave': row[3]
            }
            data.append(dato)
        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baul de contraseñas'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# Ruta para consulta individual
@app.route("/consulta_Individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM baul WHERE id_baul = '{codigo}'")
        datos = cur.fetchone()
        cur.close()
        conn.close()
        if datos:
            dato = {
                'id_baul': datos[0],
                'Plataforma': datos[1],
                'usuario': datos[2],
                'clave': datos[3]
            }
            return jsonify({'baul': dato, 'mensaje': 'Registro encontrado'})
        else:
            return jsonify({'mensaje': 'Registro no encontrado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para registrar un nuevo registro
@app.route("/registro/", methods=['POST'])
def registro():
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].enconde('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("INSERT INTO baul (plataforma,usuario,claves ) VALUES (%s, %s, %s)",(plataforma, usuario, clave))
        conn.commit()  # Para confirmar la inserción de la información
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para eliminar un registro
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].enconde('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul = %s" , (codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para actualizar un registro
@app.route("/actualizar/<codigo>", methods=["PUT"])
def actualizar(codigo):
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].enconde('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute( "UPDATE baul SET plataforma= %s, usuario= %s, clave= %s  WHERE id_baul= %s", 
                    (plataforma,usuario,clave,codigo))
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro Actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

if __name__ == '__main__':
    app.run(debug=True)
