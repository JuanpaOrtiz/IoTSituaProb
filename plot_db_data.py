from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import mysql.connector
from dash.dependencies import Input, Output

def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(user=user_name, database=database_name,
                                  password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

def select_data():
    try:
        cnx, cursor = createConnection('sql10652556', 'sql10652556', 'ISIN2KjPvu', 'sql10.freemysqlhosting.net', '3306')
        query = ("SELECT * FROM dht_sensor_data")
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or 'cursor' in globals()):
            cnx.close()
            cursor.close()

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Sensor Data", style={'text-align': 'center'}),
    dcc.Graph(id='sensor-graph', figure=px.line(title="Sensor Data over Time")),
    html.H2("Proximity Data", style={'text-align': 'center'}),
    dcc.Graph(id='proximity-graph', figure=px.line(title="Proximity over Time")),
    dcc.Interval(
            id='interval-component',
            interval=3*1000,  # 3 segundos
            n_intervals=0
    )
])

@app.callback(
    [Output('sensor-graph', 'figure'),
     Output('proximity-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    data = pd.DataFrame(select_data(), columns=["id_data", "date_time", "temperature", "humidity", "mq135Value", "proximity"])

    # Convert data types
    data["humidity"] = data["humidity"].astype(int)
    data["temperature"] = data["temperature"].astype(int)
    data["mq135Value"] = data["mq135Value"].astype(int)
    data["proximity"] = data["proximity"].astype(int)
    data["date_time"] = pd.to_datetime(data["date_time"])

    # Drop NaN values
    data = data.dropna(subset=["humidity", "temperature", "mq135Value", "proximity", "date_time"])

    # Ordenar datos
    data = data.sort_values(by="date_time")

    fig1 = px.line(data, x='date_time', y=["humidity", "temperature", "mq135Value"], title="Sensor Data over Time")
    fig2 = px.line(data, x='date_time', y=["proximity"], title="Proximity over Time")

    return fig1, fig2

if __name__ == "__main__":
    app.run_server(debug=True, port=5001)
