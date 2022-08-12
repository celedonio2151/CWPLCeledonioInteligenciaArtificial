from flask import Flask, request, render_template as render, Response, jsonify, Blueprint
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS, cross_origin
import os
import time
import numpy as np
import pandas as pd
import json
import onnxruntime as onnxrt
# -------------------- Abecedario ----------------------------------
# classes = pd.read_csv("./modelOnnxA_ZClass.csv",
#                       delimiter=",")['0']   # Classes
# onnx_session = onnxrt.InferenceSession("./modelOnnxA_ZClass.onnx")
# ------------------------------------------------------------------
proba_ = 1
clss_ = ""
ind_ = 0
longitud = 3024
vectorEntrada = []
# -------------------- Palabras ------------------------------------
onnx_session = onnxrt.InferenceSession("./modelOnnx7Class.onnx")
classes = pd.read_csv("./modelOnnx7Class.csv", delimiter=",")['0']   # Classes


def predecirClaseOnnixF(x):
    onnx_inputs = {onnx_session.get_inputs()[0].name: [x]}
    onnx_output = onnx_session.run(['output'], onnx_inputs)
    img_label = onnx_output[0][0]
    f_x = np.exp(img_label)/np.sum(np.exp(img_label))
    index = np.argmax(f_x)
    return f_x[index], classes[index], index


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    return render('index.html')


@app.route('/webCam')
def webCam():
    return render('webCam.html')


@app.route('/pointss', methods=['POST'])
def keyPointss():
    global vectorEntrada
    global proba_
    global clss_
    global ind_
    filaInput = []
    for i in request.json['data']:
        filaInput.append(i['x'])
        filaInput.append(i['y'])
        filaInput.append(i['z'])
    if(len(filaInput) == 126):
        # proba_, clss_, ind_ = predecirClaseOnnixF(filaInput)
        # print("Clase: ", clss_)
        # print("Se detecto las dos manos")
        vectorEntrada = np.append(vectorEntrada, filaInput, axis=0)
        # print(len(filaInput))
    else:
        rowZeros = np.zeros(63)
        filaInput = np.append(filaInput, rowZeros, axis=0)
        vectorEntrada = np.append(vectorEntrada, filaInput, axis=0)
        # print("Se detecto solo una mano")
    if(len(vectorEntrada) == longitud):
        proba_, clss_, ind_ = predecirClaseOnnixF(vectorEntrada)
        if(proba_ > 0.80):
            print("Clase: ", clss_, " Proba: ", proba_)
        print("Entrada Completa: ", len(vectorEntrada))
        vectorEntrada = vectorEntrada[126:]
    elif len(vectorEntrada) > longitud:
        print("Entrada fuera de rango ", len(vectorEntrada))
        vectorEntrada = []
    return jsonify({'data': clss_})


# ---------------------Para enviar mensajes
@socketio.on('myEventJson')
def handle_my_custom_event(json):
    emit('myJsonClient', {'data': 'Hola desde el server'})
    print("click: "+str(json))
    # send("Hola desde el server:", broadcast=True)


# ---------------------Para recibir mensajes
@socketio.on('myEventPoints')
def handleMessage(points):
    # print('Message: ', points)
    global vectorEntrada
    global proba_
    global clss_
    global ind_
    filaInput = []
    # print("Points:", str(points))
    if points:  # si existe puntos enviados
        # print("longitud: ", len(points['points']))
        # print(points)
        # print(type(points))
        for point in points['points']:
            # print(point)
            filaInput.append(point['x'])
            filaInput.append(point['y'])
            filaInput.append(point['z'])
        if(len(filaInput) == 126):
            # proba_, clss_, ind_ = predecirClaseOnnixF(filaInput)
            # print("Clase: ", clss_)
            vectorEntrada = np.append(vectorEntrada, filaInput, axis=0)
        else:
            rowZeros = np.zeros(63)
            filaInput = np.append(filaInput, rowZeros, axis=0)
            vectorEntrada = np.append(vectorEntrada, filaInput, axis=0)
        if(len(vectorEntrada) == longitud):
            proba_, clss_, ind_ = predecirClaseOnnixF(vectorEntrada)
            if(proba_ > 0.80):
                print("Clase: ", clss_, " Proba: ", proba_)
                emit('textClassClient', {'classText': clss_})
            # print("Entrada Completa: ", len(vectorEntrada))
            vectorEntrada = vectorEntrada[126:]  # vaciamos en anterior frame
        elif len(vectorEntrada) > longitud:
            print("Entrada fuera de rango ", len(vectorEntrada))
            vectorEntrada = []


@socketio.on('connect')
def test_connect():
    emit('myJsonClient', {'data': 'Connected'})
    print('Client connected')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))


if(__name__ == '__main__'):
    # app.run(debug=True, host="0.0.0.0")   # IP local
    # socketio.run(app, host="0.0.0.0", port=5000)
    #socketio.run(app)
    app.run(debug=True, host="127.0.0.1")
