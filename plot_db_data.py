import mysql.connector
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Crear una función que seleccione todos los datos de tu tabla y los regrese.
def select_data():
    try:
        # Crear una conexión a la base de datos
        cnx = mysql.connector.connect(user='root', database='Iot_Situacion_Problema', password='', host='localhost', port='3306')
        cursor = cnx.cursor()

        # Consultar la base de datos
        query = ("SELECT * FROM dht_data")

        # Ejecutar la consulta
        cursor.execute(query)

        # Obtener los datos
        data = cursor.fetchall()

        # Cerrar la conexión
        cnx.close()
        cursor.close()

        # Devolver los datos
        return data

    except mysql.connector.Error as err:
        """Handle possible errors"""
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

# Crear una función que reciba los datos de la base de datos, los convierta a un dataframe, 
# y regrese una gráfica de línea con los datos de humedad y temperatura. Por ahora, 
# utiliza los ids de los datos en el eje X, y los datos de humedad y temperatura en el eje Y.
def plot_data():
    try:
        # Obtener los datos de la base de datos
        data = select_data()

        # Verificar si se obtuvieron datos
        if data:
            # Convertir los datos en un DataFrame
            df = pd.DataFrame(data, columns=['id', 'humidity', 'temperature', 'date_time'])

            # Crear una gráfica de línea con Plotly Express
            fig = px.line(df, x='id', y=['humidity', 'temperature'], labels={'humidity': 'Humedad', 'temperature': 'Temperatura'})
            fig.update_layout(
                title='Gráfica de Humedad y Temperatura',
                xaxis_title='ID Datos',
                yaxis_title='>Valores de Humedad y Temperatura '
            )

            return fig

        else:
            print("No se encontraron datos en la base de datos.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Define the layout of the web application
app.layout = html.Div([
    # A div is a container for other HTML elements. These are usually stored in the children property.
    html.Div(
        # The children property is used to define the elements that will be displayed inside the div.
        children=[
            # The html.H1 component is used to display a heading. The style property is used to give the heading styling properties.
            # In this case, the style is used to center the heading.
            html.H1("Humedad vs Temperatura", style={'text-align': 'center'}),
            html.P("Aquí se puede observar una gráfica de línea con datos de humedad y temperatura generados con un código de python generando 100 datos entre 0 y 100 para temperatura como para humedad."),
            

            # The dcc.Graph component is used to display a plotly graph.
            dcc.Graph(figure=plot_data())
        ])
])


app.run_server(debug=True)