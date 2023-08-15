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
            beaconA_rssi INTEGER NOT NULL,
            beaconB_rssi INTEGER NOT NULL,
            beaconC_rssi INTEGER NOT NULL,
            beaconD_rssi INTEGER NOT NULL,
            quadrante INTEGER NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api/rssi', methods=['POST'])
def save_rssi_data():
    data = request.get_json()

    beaconA_rssi = data.get('beaconA_rssi')
    beaconB_rssi = data.get('beaconB_rssi')
    beaconC_rssi = data.get('beaconC_rssi')
    beaconD_rssi = data.get('beaconD_rssi')
    quadrante = data.get('quadrante')

    if None in [beaconA_rssi, beaconB_rssi, beaconC_rssi, beaconD_rssi, quadrante]:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    try:
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        cur.execute('INSERT INTO rssi_data (beaconA_rssi, beaconB_rssi, beaconC_rssi, beaconD_rssi, quadrante) VALUES (%s, %s, %s, %s, %s)',
                    (beaconA_rssi, beaconB_rssi, beaconC_rssi, beaconD_rssi, quadrante))

        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Dados salvos com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': 'Erro ao salvar os dados no banco de dados'}), 500


    
if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', debug=True)
