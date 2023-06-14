from flask import request, render_template, jsonify
import flask
import psycopg2

app = flask.Flask(__name__)

# Configurez une connexion de base de données
# en utilisant psycopg2
# et les identifiants ElephantSQL.
def connect() :
    DB_host ='horton.db.elephantsql.com'
    DB_name ='pbhzmfgg'
    DB_user ='pbhzmfgg'
    DB_pass ='wjCQRWxJ6o7m4tS8-nlOvj8L9JQiI9Lr'
    conn = psycopg2.connect(dbname=DB_name, user=DB_user, password=DB_pass,host=DB_host)
    return conn

# Créez une fonction pour récupérer toutes les données de la base de données
# et les retourner sous forme de réponse JSON.
@app.route('/afficher', methods=['GET'])
def getall() :
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM data")
    db = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(db)

# Créez une fonction pour récupérer un seul élément de données par son ID
# et le retourner sous forme de réponse JSON.
@app.route("/afficher/<int:id>", methods=['GET'])
def getone(id) :
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM data WHERE id = %s", (id,))
    db = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if db is not None:
        return jsonify(db)
    else:
        return jsonify({'error': 'L\'élément avec l\'ID spécifié n\'existe pas.'}), 404
    
# Créez une fonction pour ajouter un nouvel élément de données à la base de données
# et retourner une réponse JSON indiquant le succès ou l'échec.    
@app.route('/ajouter', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        data = request.form
        conn = connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO data (name, value) VALUES (%s, %s)", (data['name'], data['age']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Nouvel élément ajouté avec succès.'}), 200
    else:
        return render_template('add_data.html')


# Créez une fonction pour mettre à jour un élément de données existant dans la base de données
# et retourner une réponse JSON indiquant le succès ou l'échec.
@app.route('/maj/<nom>/<valeur>', methods=['GET', 'PUT'])
def update(nom, valeur):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE data SET value = %s WHERE name = %s", (valeur, nom))
    message = f"{cur.rowcount} record modified."
    conn.commit()
    cur.close()
    conn.close()
    return message

# Créez une fonction pour supprimer un élément de données existant de la base de données
# et retourner une réponse JSON indiquant le succès ou l'échec.
@app.route('/supp', methods=['GET', 'POST', 'DELETE'])
def supp():
    if request.method == 'DELETE':
        data = request.form
        print(data['name'])
        conn = connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM data WHERE name = %s", data['name'])
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Élément supprimé avec succès.'}), 200
    else:
        return render_template('del_data.html')    
    
# Configurez des routes pour chacune des fonctions ci-dessus
# en utilisant le décorateur route() de Flask.

# Exécutez l'application Flask et testez chacune des routes à l'aide de Postman.

if __name__ == '__main__':
    app.run(debug=True)