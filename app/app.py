from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


def db_connection():
    connection = psycopg2.connect(
        database="database_flask",
        user="postgres",
        password="postgres",
        host="db"
    )
    return connection


def db_create_table():
    connection = db_connection()
    cur = connection.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        last_name VARCHAR(50)
    )'''
    cur.execute(create_table_query)
    connection.commit()
    cur.close()
    connection.close()


@app.route('/')
def home():
    db_create_table()
    return jsonify(message="Created a table with id, name, last_name. Welcome to the home page!")


@app.route('/add_user', methods=['POST'])
def add_user():
    # Получение данных из запроса
    data = request.get_json()
    name = data.get('name')
    last_name = data.get('last_name')

    # Проверка данных
    if not name or not last_name:
        return jsonify({"error": "The name and last_name fields are required"}), 400

    # Добавление записи в базу данных
    conn = db_connection()
    cur = conn.cursor()
    insert_query = 'INSERT INTO users (name, last_name) VALUES (%s, %s)'
    cur.execute(insert_query, (name, last_name))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Entry added successfully"}), 201


@app.route('/get_users', methods=['GET'])
def get_users():
    conn = db_connection()
    cur = conn.cursor()
    select_query = 'SELECT * FROM users'
    cur.execute(select_query)
    users = cur.fetchall()
    cur.close()
    conn.close()

    # Преобразуем данные в JSON-формат
    users_list = [{"id": user[0], "name": user[1], "last_name": user[2]} for user in users]
    return jsonify(users=users_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
