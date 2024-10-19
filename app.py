from flask import Flask, request, jsonify, abort
import mysql.connector


app = Flask(__name__)

config = {
    'user': 'db_user',
    'password': 'db_user_pass',
    'host': '10.49.1.135',
    'database': 'upana'
}

def get_db_connection():
    return mysql.connector.connect(**config)

estudiantes = {}
identificador_esudiane=1

#crea un estudiante
@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    global identificador_estudiante
    body=request.get_json()
    
    id = identificador_estudiante
    
    if not body or 'nombre' not in body or 'apellido' not in body or 'edad' not in body:
        abort(400, 'Datos faltantes en el request')
        
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute(
        "INSERT INTO estudiantes (nombre, apellido, edad) VALUES (%s, %s, %s)",
        (body['nombre'], body['apellido'], body['edad'])
    )
    connection.commit()
    
    # estudiantes[identificador_estudiante]={
    #     'id':identificador_estudiante,
    #     'nombre':body['nombre'],
    #     'apellido':body['apellido'],
    #     'edad':body['edad']
        
    # }
    
    
    #identificador_esudiane+=1
    
    id = cursor.lastrowid
    cursor.close()
    connection.close()
    
    return jsonify({
        'id': id,
        'nombre': body['nombre'],
        'apellido': body['apellido'],
        'edad': body['edad']
    }), 201


@app.route('/estudiante', methods=['GET'])
def obtener_estudiantes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estudiantes")
    estudiantes = cursor.fetchall()
    cursor.close()
    connection.close()

    #return jsonify(list(estudiantes.values())), 200
    return jsonify(estudiantes), 200

    
@app.route('/estudiante/<int:id_estudiante>', methods=['GET'])
def obtener_estudiante(id_estudiante):
   connection = get_db_connection()
   cursor = connection.cursor(dictionary=True)
   
   #estudiante=estudiantes.get(id_estudiante)
  
   cursor.execute("SELECT * FROM estudiantes WHERE id = %s", (id_estudiante,))
   estudiante = cursor.fetchone()
    
   cursor.close()
   connection.close()
   if not estudiante:
     abort(404, "Estudiante no encontrado")
   
   return jsonify(estudiante), 200
   

@app.route('/estudiante/<int:id_estudiante>', methods=['DELETE'])
def eliminar_estudiante(id_estudiante):
    connection = get_db_connection()
    cursor = connection.cursor()
    
     # Eliminar el estudiante
    cursor.execute("DELETE FROM estudiantes WHERE id = %s", (id_estudiante,))
    connection.commit()
  
    cursor.close()
    connection.close()
    
    if id_estudiante not in estudiantes:
        abort(404,"Estudiante no encontrado")
    
    #del estudiantes[id_estudiante]
        
    return '', 204

@app.route('/estudiante/<int:id_estudiante>', methods=['PUT'])
def actualizar_estudiante(id_estudiante):
    body=request.get_json()
    
    #estudiante=estudiantes.get(id_estudiante)

    
    if not body or 'nombre' not in body or 'apellido' not in body or 'edad' not in body:
        abort(400, 'Datos faltantes en el request')
        
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute(
        "UPDATE estudiantes SET nombre = %s, apellido = %s, edad = %s WHERE id = %s",
        (body['nombre'], body['apellido'], body['edad'], id_estudiante)
    )
    connection.commit()
    
    cursor.close()
    connection.close()
    
    # estudiante.update({
    #     'nombre':body['nombre'],
    #     'apellido':body['apellido'],
    #     'edad':body['edad']
    # })
    
    if cursor.rowcount == 0:
        abort(404, "Estudiante no encontrado")
    #if not estudiante:
    #   abort(404,"Estudiante no encontrado")
        
    #return jsonify(estudiante), 200
    return jsonify({
        'id': id_estudiante,
        'nombre': body['nombre'],
        'apellido': body['apellido'],
        'edad': body['edad']
    }), 200
    
if __name__ == '__main__':
    app.run(debug=True)
