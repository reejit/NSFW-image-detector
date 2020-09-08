import tflite_runtime.interpreter as tflite
from flask import jsonify, json, Flask, request, render_template, make_response

#from flask_restplus import Api, Resource
import numpy as np
from PIL import Image
from nsfw_api import app
from io import BytesIO
import requests
import os
#import boto3
#import botocore
import base64
import zipfile


#BUCKET_NAME = 'nsfwimages-inceptionv3'
#MODEL_FILE_NAME ='converted_nsfw_model.tflite.zip'
#MODEL_LOCAL_PATH=  MODEL_FILE_NAME
#
# def download_model():
#     print("Downloading model...")
#     s3=boto3.resource('s3')
#     try:
#         s3.Bucket(BUCKET_NAME).download_file(MODEL_FILE_NAME,MODEL_FILE_NAME)
#         with zipfile.ZipFile(MODEL_FILE_NAME, 'r') as zip_ref:
#             zip_ref.extractall(APP_ROOT)
#         os.remove(MODEL_FILE_NAME)
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == "404":
#             print("The Object doesnot exist")
#         else:
#             raise



if not os.path.exists('nsfw_api/resources/saved_model.tflite'):
    print("model not present")
    # download_model()

interpreter = tflite.Interpreter(model_path="nsfw_api/resources/saved_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

@app.route('/')
def hello_world():
#    return 'Hello, World!'
    return render_template("index.html")

@app.route("/pred",methods=['GET','POST'])
def predict():
    try:
        if request.method== 'POST' and 'file' in request.files:
            upload=request.files.getlist("file")[0]
            filename=upload.filename
            target=os.path.join('nsfw_api/static/images/')
            destination="/".join([target,filename])
            upload.save(destination)
#            print("File saved to:", destination)
            input_shape=input_details[0]['shape']
            img=Image.open(destination)
            upload1 = img.resize((input_shape[1], input_shape[2]))
            im_array=np.array(upload1)
            im_array =im_array / 255
            # x_test=np.array(im_array,dtype=np.float32)
            x_test=np.array(im_array).astype(np.float32)
            x_test = np.expand_dims(x_test, axis=0)
            interpreter.set_tensor(input_details[0]['index'], x_test)
            interpreter.invoke()

            pred = interpreter.get_tensor(output_details[0]['index'])
        #    print(pred)
            dict={'Drawing':'0','Hentai':'0','Neutral':'0','Porn':'0','Sexy':'0'}
        #    print(dict)
            dict['Drawing']=str(round(pred[0][0],3))
            dict['Hentai']=str(round(pred[0][1],3))
            dict['Neutral']=str(round(pred[0][2],3))
            dict['Porn']=str(round(pred[0][3],3))
            dict['Sexy']=str(round(pred[0][4],3))
            if os.path.exists(destination):
            	os.remove(destination)
            kk=dict
        if request.method== 'GET':
            data=request.args.get('text')
            kk=score(data)
        if request.method=='POST' and 'file' not in request.files:
            data=request.form['text']
            kk=score(data)
        
#        print(type(kk))
#        print(kk)
        return jsonify(kk), 200

    except AssertionError as error:
        app.logger.error('API called for string: ' + data + 'Error: '+ error)

def score(data):
    if "http" in data:
        response=requests.get(data)
        upload=Image.open(BytesIO(response.content))
        
        if "jpg" in data:
            filename="nsfw.jpg"
        elif "png" or "gif" not in data:
            filename="nsfw.jpeg"
#        elif "png" in data:
#            filename="nsfw.png"
#        elif "gif" in data:
#            return("The File not supported"),400
        target=os.path.join('nsfw_api/static/images/')
        destination="/".join([target, filename])
        upload.save(destination)
#        print("File saved to:", destination)
    elif "base64" in data:
        name=data.split(',')
        name0=name[0]
        name1=name[1]
#        print(name0)
        name1=name1.replace(' ','+')
        imgdata= base64.b64decode(name1)
        if "jpg" in name0:
            filename="nsfw.jpg"
        elif "png" or "gif" not in data:
            filename="nsfw.jpeg"
        
        target=os.path.join('nsfw_api/static/images/')
        destination="/".join([target,filename]) 
        with open(destination, "wb") as f:
            f.write(imgdata)
#        print("File saved to:", destination)


    input_shape=input_details[0]['shape']
    img=Image.open(destination)
    upload1 = img.resize((input_shape[1], input_shape[2]))
    
    im_array=np.array(upload1)
    im_array =im_array / 255
    # x_test=np.array(im_array,dtype=np.float32)
    x_test=np.array(im_array).astype(np.float32)
    x_test = np.expand_dims(x_test, axis=0)
    interpreter.set_tensor(input_details[0]['index'], x_test)
    interpreter.invoke()

    pred = interpreter.get_tensor(output_details[0]['index'])
#    print(pred)
    dict={'Drawing':'0','Hentai':'0','Neutral':'0','Porn':'0','Sexy':'0'}
#    print(dict)
    dict['Drawing']=str(round(pred[0][0],3))
    dict['Hentai']=str(round(pred[0][1],3))
    dict['Neutral']=str(round(pred[0][2],3))
    dict['Porn']=str(round(pred[0][3],3))
    dict['Sexy']=str(round(pred[0][4],3))
    if os.path.exists(destination):
    	os.remove(destination)
    return dict

