from flask import Flask, request
import mysql.connector

app = Flask(__name__)

def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(
        user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        humidity = data.get('humidity')
        temperature = data.get('temperature')
        date_time = data.get('date_time')
        mq135Value = data.get('mq135Value')
        proximity = data.get('proximity')

        print("Received humidity:", humidity)
        print("Received temperature:", temperature)
        print("Received mq135Value:", mq135Value)
        print("Received proximity:", proximity)
        print("Received date_time:", date_time)

        cnx, cursor = createConnection('sql10652556', 'sql10652556', 'ISIN2KjPvu', 'sql10.freemysqlhosting.net', '3306')

        add_data = (
            "INSERT INTO dht_sensor_data (date_time, temperature, humidity, mq135Value, proximity) VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(add_data, ( date_time, temperature, humidity, mq135Value, proximity))
        cnx.commit()
        cursor.close()
        cnx.close()

        return 'Data received successfully.', 200

    else:
        return 'Invalid content type. Expected application/json.', 400

if __name__ == "__main__":
    app.run(debug=True)
