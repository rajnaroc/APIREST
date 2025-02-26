from urllib import response
from flask import Flask, Response, request, jsonify
from flask_mysqldb import MySQL
from flask_pymongo import PyMongo
from bson import json_util, ObjectId

app = Flask(__name__)

# Configuración de MongoDB
app.config["MONGO_URI"] = "mongodb+srv://rajnaroc:12345@cluster0.r5gm8.mongodb.net/users"

mongo = PyMongo(app)

# Configuración de MySQL (añade los valores correctos)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "1234567890"
app.config["MYSQL_DB"] = "flask_sql"

mysql = MySQL(app)

@app.route("/addsql", methods=["POST"])
def add_sql():
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    calle = request.json["calle"]
    numero = request.json["numero"]

    if nombre and edad and calle and numero:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users VALUES (null,%s,%s,%s,%s)",(nombre,edad,calle,numero))
        mysql.connection.commit()
        
        return "insertado correctamento"

@app.route("/getsql", methods=["GET"])
def get_sql():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    datos = cur.fetchall()

    return jsonify(datos)

@app.route("/getsql/<id>", methods=["GET"])
def getuser_sql(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,)) 
    datos = cur.fetchall()

    return jsonify(datos),202

@app.route("/updatesql/<id>", methods=["PUT"])
def update_sql(id):
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    calle = request.json["calle"]
    numero = request.json["numero"]

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET nombre = %s, edad = %s, calle = %s, numero = %s WHERE id = %s", (nombre,edad,calle,numero, id))
    mysql.connection.commit()
    
    return jsonify("actualizado correctamente")

@app.route("/deletesql/<id>", methods=["DELETE"])
def delete_sql(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s",(id,))
    mysql.connection.commit()
    return jsonify({"message" : "delete user" + id + "eliminado correctamente"}),200

# Ruta para agregar un usuario a MongoDB
@app.route("/add", methods=["POST"])
def add_mongo():
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    calle = request.json["calle"]
    numero = request.json["numero"]

    print(nombre,edad,calle,numero)
    if nombre and edad and calle and numero:
        result = mongo.db.users.insert_one({
            "nombre": nombre,
            "edad": edad,
            "calle": calle,
            "numero": numero
        })

        response = {
            "id": str(result.inserted_id),
            "nombre": nombre,
            "edad": edad,
            "calle": calle,
            "numero": numero
        }

        return jsonify(response), 201

    return jsonify({"error": "Faltan datos"}), 400



# Ruta para obtener todos los usuarios de MongoDB
@app.route("/users", methods=["GET"])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)

    return Response(response, mimetype="application/json")

# Ruta para obtener un usuario por ID en MongoDB
@app.route("/users/<id>", methods=["GET"])
def get_one_user(id):
    try:
        
        user = mongo.db.users.find_one({"_id": ObjectId(id)})
        if user:
            response = json_util.dumps(user)
            return Response(response, mimetype="application/json")
        
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    except:
        return jsonify({"error": "ID inválido"}), 400

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    mongo.db.users.delete_one({"_id": ObjectId(id)})

    response = (
        {
            "message": "delete" + id + "delete success"
        }
    )
    return jsonify(response), 201

def status_404(error):
    return jsonify({"message": "Recurso no encontrado"}), 404

@app.route("/update/<id>", methods=["PUT"])
def update_mongo(id):
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    calle = request.json["calle"]
    numero = request.json["numero"]

    print(nombre,edad,calle,numero)
    if nombre and edad and calle and numero:
        mongo.db.users.update_one({
            "_id": ObjectId(id)},
            {"$set":{
                "nombre": nombre,
                "edad": edad,
                "calle": calle,
                "numero": numero
            }
        })

        response = {
            "id": str(id),
            "nombre": nombre,
            "edad": edad,
            "calle": calle,
            "numero": numero
        }

        return jsonify(response), 201

    return jsonify({"error": "Faltan datos"}), 400


if __name__ == "__main__":
    app.register_error_handler(404, status_404)
    app.run(debug=True)
