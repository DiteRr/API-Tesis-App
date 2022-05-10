
import urllib.parse
from flask import Flask, request, Response, jsonify, redirect, render_template
from flask_mysqldb import MySQL
import requests

import swagger_client
from swagger_client.rest import ApiException

configuration = swagger_client.Configuration()

app = Flask(__name__)
#my sql connection
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'stravadb'

mysql = MySQL(app)

STRAVA_CLIENT_ID = "74995"
STRAVA_CLIENT_SECRET = "d6d2222bb093f8a3117a35aa428c045beac19e67"
REDIRECT_URI = 'http://192.168.0.7:5000/strava_token' #http://146.83.216.251:5000 servidor


def getActivities(access_token):
    configuration.access_token = access_token
    # create an instance of the API class
    api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
    before = 56 # Integer | An epoch timestamp to use for filtering activities that have taken place before a certain time. (optional)
    after = 56 # Integer | An epoch timestamp to use for filtering activities that have taken place after a certain time. (optional)
    page = 56 # Integer | Page number. Defaults to 1. (optional)
    per_page = 56 # Integer | Number of items per page. Defaults to 30. (optional) (default to 30)

    try: 
        # List Athlete Activities
        api_response = api_instance.get_logged_in_athlete_activities()
        return(api_response)
        #pprint(api_response)
    except ApiException as e:
        #print("Exception when calling ActivitiesApi->getLoggedInAthleteActivities: %s\n" % e)
        return(e)

#Validación de IDUsuario y contraseña.
@app.route('/login', methods=['POST'])
def login():   
    data = request.json
    cur = mysql.connection.cursor()
    print(data)
    
    cur.execute("SELECT  * from Usuario where id = %d" %int(data['id']))
    result = {'data':[dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]}
  
    if(result['data'] == []):
        #ID no valida o no registrada.
        msg = {'message': 0}
    else:
        if(data['password'] == result['data'][0]['refresh_token']):
            #Usuario valido
            msg = {'message': 2}
        else:
            #Refresh_token invalido
            msg = {'message': 1}

    return jsonify(msg)


#Actualizar el access_token y obtener la lista de actividades
@app.route('/update_token', methods=['POST'])
def update_accessToken():
    data = request.json
    print(data)
    user_refresh_token = data['refresh_token']

    strava_request = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "refresh_token": user_refresh_token,
            "grant_type": "refresh_token",
        },
    ).json()

    access_token  = strava_request['access_token']
    
    #Actualizar access_token en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Usuario SET access_token = '{}' WHERE refresh_token = '{}' ".format(access_token, user_refresh_token))
    mysql.connection.commit()

    #Luego de obtener el token actualizado, se procede a llamar las actividades del usuario.
    response = getActivities(access_token)
    res = []
    for i in range(0, len(response)):
        id_actividad = response[i].id
        distance = response[i].distance
        average_speed = response[i].average_speed
        elapsed_time = response[i].elapsed_time
        elev_high = response[i].elev_high
        elev_low = response[i].elev_low
        name = response[i].name
        type = response[i].type

        data = {"id_actividad": id_actividad, "distance": distance, "average_speed": average_speed, 
                "elapsed_time": elapsed_time, "elev_high": elev_high, "elev_low": elev_low,
                 "name":name, "type": type}
        res.append(data)
    return jsonify({'activities': res})

#Actividades realizadas por usuario
@app.route('/activities_user', methods=['POST'])
def get_activities():
    data = request.json
    access_token = data['access_token']

    response = getActivities(access_token)

    res = []
    for i in range(0, len(response)):
        id_actividad = response[i].id
        distance = response[i].distance
        average_speed = response[i].average_speed
        elapsed_time = response[i].elapsed_time
        elev_high = response[i].elev_high
        elev_low = response[i].elev_low
        name = response[i].name
        type = response[i].type

        data = {"id_actividad": id_actividad, "distance": distance, "average_speed": average_speed, 
                "elapsed_time": elapsed_time, "elev_high": elev_high, "elev_low": elev_low,
                 "name":name, "type": type}
        res.append(data)

    return jsonify({'activities': res})

#Verificar si el usuario se conecta por primera vez
def new_user(data):
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * from Usuario where id = %d" %int(data['ID']))
    
    result = {'data':[dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]}

    #Verificar si el usuario no existe
    if(result['data'] == []):
        cur.execute("insert into Usuario values ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                                data['ID'],
                                data['username'],
                                data['firstname'],
                                data['lastname'],
                                data['access_token'],
                                data['refresh_token']))
        mysql.connection.commit()

#Obtener y guardar los datos de usuario cuando autorize los permisos de la aplicación.
def exchange_token(code):
    strava_request = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': STRAVA_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
    ).json()
    #print(strava_request.json()['access_token'])

    #Save user data 
    id_user  = strava_request['athlete']['id']
    username  = strava_request['athlete']['username']
    firstname  = strava_request['athlete']['firstname']
    lastname  = strava_request['athlete']['lastname']
    access_token  = strava_request['access_token']
    refresh_token  = strava_request['refresh_token']

    data = {"ID": id_user, "username": username, "firstname": firstname, 
            "lastname": lastname, "access_token": access_token, "refresh_token":refresh_token}
    
    new_user(data) #save data user

    
    data = {'id': id_user, 'refresh_token': refresh_token}
    return render_template('layout.html', datos = data)
    #return jsonify({'ID': id_user, 'refresh_token': refresh_token})

#URL de solicitud de permisos de la aplicación
@app.route('/strava_authorize', methods=['GET'])
def strava_authorize():
    params = {
        'client_id': STRAVA_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'activity:read_all'
    }
    return redirect('{}?{}'.format(
        'https://www.strava.com/oauth/authorize',
        urllib.parse.urlencode(params)
    ))

#Verificar si el usuario acepto los permisos de la aplicación
@app.route('/strava_token', methods=['GET'])
def strava_token():
    code = request.args.get('code')
    if not code:
        return Response('Error: Missing code param', status=400)
    return exchange_token(code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)