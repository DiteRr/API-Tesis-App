
import urllib.parse
from flask import Flask, request, Response, jsonify, redirect, render_template
from flask_mysqldb import MySQL
import requests
import datetime
import time

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
REDIRECT_URI = 'http://192.168.0.20:5000/strava_token' #http://146.83.216.251:5000 servidor


def getActivities(access_token):
    configuration.access_token = access_token
    # create an instance of the API class
    api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
    before = 56 # Integer | An epoch timestamp to use for filtering activities that have taken place before a certain time. (optional)
    after = int(time.time()) - 604800 # Integer | An epoch timestamp to use for filtering activities that have taken place after a certain time. (optional)
    page = 56 # Integer | Page number. Defaults to 1. (optional)
    per_page = 56 # Integer | Number of items per page. Defaults to 30. (optional) (default to 30)

    try: 
        # List Athlete Activities
        api_response = api_instance.get_logged_in_athlete_activities(after=after)
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

    cur.execute("SELECT  * from Usuario where id = %d" %int(data['id']))
    result = {'data':[dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]}
    
    #Verificar si encontro algun usuario guardado con el "id" recibido.
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


@app.route('/Preguntas', methods=['POST'])
def Preguntas():
    data = request.json
    tipo_cuestionario = data['tipo_preg']
    #tipo_cuestionario = 'pl'
    cur = mysql.connection.cursor()

    #Consultar por la preguntas de tipo slider correspondiente al tipo de cuestionario
    cur.execute("SELECT PreguntaSlider.id_pregunta, Pregunta.pregunta, Pregunta.tipo_cuestionario, PreguntaSlider.tipo_preg, PreguntaSlider.valueStringMin, PreguntaSlider.valueStringMax, PreguntaSlider.tipo_respuesta FROM Pregunta INNER JOIN PreguntaSlider ON PreguntaSlider.id_pregunta = Pregunta.ID WHERE Pregunta.tipo_cuestionario = '%s'" %tipo_cuestionario)
    pregs_slider = [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]
    #-----------------------

    #Consultar por las preguntas de tipo dropdown correspondiente al tipo de cuestionario
    cur.execute("SELECT Pregunta.ID, Pregunta.pregunta, PreguntaDropDown.tipo_respuesta FROM Pregunta INNER JOIN PreguntaDropDown ON PreguntaDropDown.id_pregunta = Pregunta.ID WHERE Pregunta.tipo_cuestionario = '%s'" %tipo_cuestionario)
    result = {'preguntas_dropdown':[dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]}
    
    preguntas_dropdown = []
    for preg in result['preguntas_dropdown']:
        cur.execute("SELECT alternativa FROM Alternativas where id_pregunta = %d" %int(preg['ID']))
        alternativas = [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]
        preguntas_dropdown.append({'id_pregunta': preg['ID'], 'pregunta': preg['pregunta'], 'alternativas': alternativas, 'tipo_respuesta' : preg['tipo_respuesta']})
    #-----------------------
    
    return jsonify({'pregs' : {'preguntas_slider' : pregs_slider, 'preguntas_dropdown' : preguntas_dropdown}})

@app.route('/Actividades_registradas', methods=['POST'])
def ActividadesRegistradas():
    data = request.json
    cur = mysql.connection.cursor()

    #Consultar por las actividades que registró el usuario
    cur.execute("SELECT Registro.id_activity FROM Registro INNER JOIN Actividad ON Actividad.ID = Registro.id_activity WHERE Actividad.IDathlete = %s GROUP BY Registro.id_activity;" %data['id_user'])
    result = {'data':[dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]}
    return jsonify(result)


@app.route('/Guardar_datos', methods=['POST'])
def GuardarRespuestas():
    #Guardar los datos principales de la actividad obtenidos por STRAVA + Las respuestas que registró el usuario.
    data = request.json
    cur = mysql.connection.cursor()

    #Guardar los parametros de la actividad.
    cur.execute("insert into Actividad values ('{}', '{}', {}, {}, {}, {}, {}, '{}', '{}', '{}', '{}')".format(
        data["actividad"]["id_actividad"],
        data['id_user'],
        float(data["actividad"]["distance"]),
        float(data["actividad"]["elapsed_time"]),
        float(data["actividad"]["elev_high"]),
        float(data["actividad"]["elev_low"]),
        float(data["actividad"]["average_speed"]),
        data["actividad"]["name"],
        data["actividad"]["type"],
        datetime.datetime.strptime(data["actividad"]["start_date"], '%a, %d %b %Y %H:%M:%S GMT'),
        datetime.datetime.strptime(data["actividad"]["start_date_local"], '%a, %d %b %Y %H:%M:%S GMT'),
    ))
    mysql.connection.commit()

    #Guardar las respuestas asociadas a cada pregunta.
    for preg in data['data']:
        cur.execute("insert into Registro VALUES ('{}', {}, '{}', '{}')".format(
            data["actividad"]["id_actividad"],
            int(preg['id_preg']),
            preg['respuesta'],
            datetime.date.today(),
        ))
    mysql.connection.commit()

    return jsonify({'status': 200})


@app.route('/Registros', methods=['POST'])
def registros2():
    data = request.json
    id_user = data['id_user']
    #id_user = '91213168'
    cur = mysql.connection.cursor()

    #Selecionar solamente las preguntas de tipo slider.
    cur.execute("SELECT Pregunta.ID, Pregunta.pregunta FROM Pregunta INNER JOIN PreguntaSlider ON PreguntaSlider.id_pregunta = Pregunta.ID")
    pregs= [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]

    data = {}
    for preg in pregs:
        data.setdefault(preg['ID'], {'pregunta' : preg['pregunta'], 'labels': [], 'data':[]})
    
    #Selecionar los registros de respuestas asociados a las preguntas de tipo slider del usuario.
    cur.execute("SELECT Registro.id_activity, Registro.id_pregunta, Registro.respuesta, Actividad.start_date_local FROM Registro INNER JOIN Actividad ON Actividad.ID = Registro.id_activity INNER JOIN Pregunta ON Pregunta.ID = Registro.id_pregunta INNER JOIN PreguntaSlider ON PreguntaSlider.id_pregunta = Pregunta.ID WHERE Actividad.IDathlete = '{}'".format(
        id_user
    ))
    registros = {'registros':[dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]}
    
    #Guardar la fecha de la actividad y la respuesta para cada pregunta de tipo slider.
    for registro in registros['registros']:
        data[registro['id_pregunta']]['labels'].append(registro['start_date_local'])
        data[registro['id_pregunta']]['data'].append(int(registro['respuesta']))
    
    pregus = []
    #Cambiar el formato para guardar las preguntas
    for id_preg in data.keys():
        pregus.append({'id_preg': id_preg, 'pregs' : data[id_preg]})

    return jsonify({"registros": pregus})



#Actualizar el access_token y obtener la lista de actividades
@app.route('/update_token', methods=['POST'])
def update_accessToken():
    data = request.json

    user_refresh_token = data['refresh_token']

    #Solicitud actualización del token
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
    expired_at = strava_request['expires_at']
    
    #Actualizar access_token en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Usuario SET access_token = '{}' WHERE refresh_token = '{}' ".format(access_token, user_refresh_token))
    mysql.connection.commit()

    #Luego de obtener el token actualizado, se procede a llamar las actividades del usuario.
    try:
        response = getActivities(access_token)
    except ApiException as e:
        return jsonify({'activities' : 'expired'})

    res = []

    #Guardar los datos de la actividad en un JSON.
    for i in range(0, len(response)):
        id_actividad = response[i].id
        distance = response[i].distance
        average_speed = response[i].average_speed
        elapsed_time = response[i].elapsed_time
        elev_high = response[i].elev_high
        elev_low = response[i].elev_low
        name = response[i].name
        type = response[i].type
        start_date = response[i].start_date
        start_date_local = response[i].start_date_local

        data = {"id_actividad": id_actividad, "distance": distance, "average_speed": average_speed, 
                "elapsed_time": elapsed_time, "elev_high": elev_high, "elev_low": elev_low,
                 "name":name, "type": type, "start_date": start_date, "start_date_local": start_date_local}
        res.append(data)

    return jsonify({'activities': res, "expired_at" : expired_at, "access_token" : access_token})

#Actividades realizadas por usuario
@app.route('/activities_user', methods=['POST'])
def get_activities():
    data = request.json
    access_token = data['access_token']

    #Obtener actividades realizadas por el usuario
    try:
        response = getActivities(access_token)
    except ApiException as e:
        return jsonify({'activities' : 'expired'})
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
        start_date = response[i].start_date
        start_date_local = response[i].start_date_local

        data = {"id_actividad": id_actividad, "distance": distance, "average_speed": average_speed, 
                "elapsed_time": elapsed_time, "elev_high": elev_high, "elev_low": elev_low,
                 "name":name, "type": type, "start_date": start_date, "start_date_local": start_date_local}
        res.append(data)

    return jsonify({'activities': res})

#Verificar si el usuario se conecta por primera vez
#p
def new_user(data):
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * from Usuario where id = %d" %int(data['ID']))
    
    result = {'data':[dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]}

    #Verificar si el usuario no existe
    if(result['data'] == []):
        #Si no existe lo guarda en la base de datos
        cur.execute("insert into Usuario values ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                                data['ID'],
                                data['username'],
                                data['firstname'],
                                data['lastname'],
                                data['access_token'],
                                data['refresh_token']))
        mysql.connection.commit()

#Guardar usuario en la base de datos
@app.route('/save_user', methods=['POST'])
def save_user():
    data = request.json
    user_data = data['access_token']

    new_user(data)

    return jsonify({'status': 200})

#----------------------------------LOGIN ANTIGUO------------------------------------#
#-----------------------------------------------------------------------------------#

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

    id_user  = strava_request['athlete']['id']
    username  = strava_request['athlete']['username']
    firstname  = strava_request['athlete']['firstname']
    lastname  = strava_request['athlete']['lastname']
    access_token  = strava_request['access_token']
    refresh_token  = strava_request['refresh_token']

    data = {"ID": id_user, "username": username, "firstname": firstname, 
            "lastname": lastname, "access_token": access_token, "refresh_token":refresh_token}
    
    #Guardar datos del usuario
    new_user(data)

    
    data = {'id': id_user, 'refresh_token': refresh_token}
    return render_template('layout.html', datos = data)

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

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)