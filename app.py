from flask import Flask, request, jsonify
import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

def create_table():
    conn = psycopg2.connect(host=db_host,port=db_port, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rssi_data (
            id SERIAL PRIMARY KEY,
            beacon1_rssi INTEGER NOT NULL,
            beacon2_rssi INTEGER NOT NULL,
            beacon3_rssi INTEGER NOT NULL,
            beacon4_rssi INTEGER NOT NULL,
            counter INTEGER NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api/rssi', methods=['POST'])
def save_rssi_data():
    data = request.get_json()

    beacon1_rssi = data.get('beacon1_rssi')
    beacon2_rssi = data.get('beacon2_rssi')
    beacon3_rssi = data.get('beacon3_rssi')
    beacon4_rssi = data.get('beacon4_rssi')
    counter = data.get('counter')

    if None in [beacon1_rssi, beacon2_rssi, beacon3_rssi, beacon4_rssi, counter]:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    try:
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        cur.execute('INSERT INTO rssi_data (beacon1_rssi, beacon2_rssi, beacon3_rssi, beacon4_rssi, counter) VALUES (%s, %s, %s, %s, %s)',
                    (beacon1_rssi, beacon2_rssi, beacon3_rssi, beacon4_rssi, counter))

        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Dados salvos com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': 'Erro ao salvar os dados no banco de dados'}), 500

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
