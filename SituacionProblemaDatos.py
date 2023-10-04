from datetime import date, datetime
import random
import mysql.connector

# TODO: Call the createConnection() function and store the connection and cursor in variables. 
def createConnection(user_name, database_name, user_password, host, port):
    """Creates a connection to the mysql database
    
    Parameters
    -----------
        user_name {string} -- The username to the database
        database_name {string} -- The name of the database
        user_password {string} -- The password to the database
        host {string} -- The host of the database
        port {string} -- The port of the database

    Returns
    --------
        tuple -- A tuple containing the connection and the cursor
    """
    cnx = mysql.connector.connect(user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

def select_data():
    """Selects all the data from the database"""
    try:
        # Create a connection to the database - # Dont forget to pass in the correct parameters
        cnx, cursor = createConnection('root', 'Iot_Situacion_Problema', '56KLD.22!!a', 'localhost', '3306')

        # Query the database
        query = ("SELECT * FROM dht_data")

        # Execute the query
        cursor.execute(query)

        # Get the data
        data = cursor.fetchall()

        # Return the data
        return data
    
    except mysql.connector.Error as err:
        """Handle possible errors"""
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        """Close the connection"""
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or 'cursor' in globals()):
            cnx.close()
            cursor.close()

def create_data():
    
    """Inserts random sensor data into the database"""
    # For the float values, use the random.uniform() function.
    # Humidity: 0 to 100%, +-5%.
    humidity = float(random.uniform(0, 100) * random.uniform(0.95, 1.05))
    
    # Temperature: 0 to 100%, +-5%.
    temperature = random.uniform(0, 100) * random.uniform(0.95, 1.05)
    
    # Date/Time: Current date and time. Check the datetime module for help.
    current_datetime = datetime.now()
    
    # When you have the data, print it out to the console. 
    print(f"Random Sensor Data - Humidity: {humidity}%, Temperature: {temperature}°C, Timestamp: {current_datetime}")
    return humidity, temperature, current_datetime

def insert_data(H, T, D, cnx, cursor):
    try:
        # Create a connection to the database - # Dont forget to pass in the correct parameters
        cnx, cursor = createConnection('root', 'Iot_Situacion_Problema', '56KLD.22!!a', 'localhost', '3306')

        results = str(str(H)+','+str(T)+','+"'"+str(D)+"'")
        print(results)

        # Query the database
        query = ("INSERT INTO dht_data(humidity, temperature, date_time) VALUES("+results+")")

        # Execute the query
        cursor.execute(query)

        # Commit the changes
        cnx.commit()

        print("Data inserted successfully")

    except mysql.connector.Error as err:
        """Handle possible errors"""
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        """Close the connection"""
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or 'cursor' in globals()):
            cnx.close()
            cursor.close()
        
    return 0
    
#####################################################################################################################################################
#####################################################################################################################################################

#FUNCTIONS

# Create a connection to the database
cnx, cursor = createConnection('root', 'Iot_Situacion_Problema', '56KLD.22!!a', 'localhost', '3306')
select_data()

for i in range(100):
    hum, temp, dat = create_data() 

    # Insert the data into the database
    insert_data(hum, temp, dat, cnx, cursor) 

        # TODO: Create the query string that inserts the data you created into the database
        # The query string should be an insert statement that inserts the data into the dht_sensor_data table

        # Insert the data into the database
        # TODO: Execute the query string you created

if __name__ =='main_':
    # TODO: Call the insert_data() function 100 times to insert 100 rows of data into the database
    # Dont forget to delete the pass keyword
    pass