import tflite_runtime.interpreter as tflite
from flask import request,url_for, jsonify, json,Flask,render_template, make_response
from flask_cors import CORS, cross_origin
#from flask_restplus import Api, Resource
import numpy as np
from PIL import Image
from io import BytesIO
import requests
import os
import boto3
import botocore
import base64
import io
import zipfile

BUCKET_NAME = 'nsfw-inceptionv3'
MODEL_FILE_NAME ='converted_nsfw_model.tflite.zip'
MODEL_LOCAL_PATH=  MODEL_FILE_NAME

def download_model():
    print("Downloading model...")
    s3=boto3.resource('s3')
    try:
        s3.Bucket(BUCKET_NAME).download_file(MODEL_FILE_NAME,MODEL_FILE_NAME)
        with zipfile.ZipFile(MODEL_FILE_NAME, 'r') as zip_ref:
            zip_ref.extractall(APP_ROOT)
        os.remove(MODEL_FILE_NAME)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The Object doesnot exist")
        else:
            raise


app=Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/upload": {"origins": "http://localhost:port"}})
#app=Api(app=flask_app)
#name_space=app.namespace('main', description='Main APIs')
APP_ROOT=os.path.dirname(os.path.abspath(__file__))


if not os.path.exists(APP_ROOT + '/converted_nsfw_model.tflite'):
    print("model not present")
    download_model()



@app.route('/')
def index():
    return render_template("index.html")

#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
#    return send_from_directory("static/images",
#                            filename)

@app.route("/upload",methods=['GET','POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def upload():
    if request.method== 'POST' and 'file' in request.files:
        upload=request.files.getlist("file")[0]
        filename=upload.filename
        target=os.path.join(APP_ROOT, 'static/images/')
        destination="/".join([target,filename])
        upload.save(destination)
        print("File saved to:", destination)
    if request.method== 'GET':
        data=request.args.get('text')
        if "http" in data:
            response=requests.get(data, stream=True)
            upload=Image.open(io.BytesIO(response.content))
            #byteImg = Image.open(response)
            #byteImg = byteImgIO.read()
            if "jpeg" in data:
                filename="nsfw.jpeg"
            elif "jpg" in data:
                filename="nsfw.jpg"
            elif "png" in data:
                filename="nsfw.png"
            elif "gif" in data:
                return("The File not supported"),400
            else:
                filename="nsfw.jpeg"
            target=os.path.join(APP_ROOT, 'static/images/')
            destination="/".join([target,filename])
            upload.save(destination)
            print("File saved to:", destination)
        elif "base64" in data:
            name=data.split(',')
            name0=name[0]
            name1=name[1]
            print(name0)
            name1=name1.replace(' ','+')
            imgdata= base64.b64decode(name1)
            if "jpeg" in name0:
                filename="nsfw.jpeg"
            elif "jpg" in name0:
                filename="nsfw.jpg"
            elif "png" in name0:
                filename="nsfw.png"
            elif "gif" in data:
            	return("The File not supported"),400
            else:
            	filename="nsfw.jpeg"
                
            target=os.path.join(APP_ROOT, 'static/images/')
            destination="/".join([target,filename]) 
            with open(destination, "wb") as f:
                f.write(imgdata)
            print("File saved to:", destination)
        else:
            return("The File is not supported"),400
            
            

        
        

    if request.method=='POST' and 'file' not in request.files:
       # data=request.form['text']
        data=request.args.get('text')
        if "http" in data:
            response=requests.get(data)
            upload=Image.open(BytesIO(response.content))
            if "jpeg" in data:
                filename="nsfw.jpeg"
            elif "jpg" in data:
                filename="nsfw.jpg"
            elif "png" in data:
                filename="nsfw.png"
            elif "gif" in data:
                return("The File not supported"),400
            else:
                filename="nsfw.jpeg"
            target=os.path.join(APP_ROOT, 'static/images/')
            destination="/".join([target,filename])
            upload.save(destination)
            print("File saved to:", destination)
        elif "base64" in data:
            name=data.split(',')
            name0=name[0]
            name1=name[1]
            print(name0)
            name1=name1.replace(' ','+')
            imgdata= base64.b64decode(name1)
            if "jpeg" in name0:
                filename="nsfw.jpeg"
            elif "jpg" in name0:
                filename="nsfw.jpg"
            elif "png" in name0:
                filename="nsfw.png"
            elif "gif" in data:
                return("The File not supported"),400
            else:
                filename="nsfw.jpeg"
            target=os.path.join(APP_ROOT, 'static/images/')
            destination="/".join([target,filename]) 
            with open(destination, "wb") as f:
                f.write(imgdata)
            print("File saved to:", destination)
        else:
            return("The File is not supported"),400
            
       # filename=name.rsplit('/',1)
       # filename=filename[1]
       # response=requests.get(data)
       # upload=Image.open(BytesIO(response.content))
        
        
    # target=os.path.join(APP_ROOT, 'static/images/')
    # filename="nsfw.jpeg"
    # #create image directory if not found
    # if not os.path.isdir(target):
    #     os.mkdir(target)
    # print("File name: {}".format(filename))
        
    # ext=os.path.splitext(filename)[1]
    # if(ext==".jpg")or (ext==".png") or(ext==".bmp") or (ext==".jpeg"):
    #     print("File accepted")
    # else:
    #     filename+=".jpg"
    #     return("The file is not supported"),400
#
#     save file
#    
    # destination="/".join([target,filename]) 
    # print("File saved to:", destination)
    # upload.save(destination)
    interpreter = tflite.Interpreter(model_path="converted_nsfw_model.tflite")
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_shape=input_details[0]['shape']
    img=Image.open(destination)
    upload1 = img.resize((input_shape[1],input_shape[2]))
    
    im_array=np.array(upload1)
    im_array =im_array / 255
    # x_test=np.array(im_array,dtype=np.float32)
    x_test=np.array(im_array).astype(np.float32)
    x_test = np.expand_dims(x_test, axis=0)
    interpreter.set_tensor(input_details[0]['index'], x_test)
    interpreter.invoke()
#    model_load()
#    load_model()
    pred = interpreter.get_tensor(output_details[0]['index'])
    print(pred)
    dict={'Drawing':'0','Hentai':'0','Neutral':'0','Porn':'0','Sexy':'0'}
#    print(dict)
#    max_key=max(dict, key=dict.get)
#    print(max_key)
    dict['Drawing']=str(round(pred[0][0],3))
    dict['Hentai']=str(round(pred[0][1],3))
    dict['Neutral']=str(round(pred[0][2],3))
    dict['Porn']=str(round(pred[0][3],3))
    dict['Sexy']=str(round(pred[0][4],3))
    second_max=list(sorted(dict.values()))[-2]
    maxi=list(sorted(dict.values()))[-1]
    for key,val in dict.items():
        if val == second_max:
            print("second max:",key," ")
            print(val)
        if val == maxi:
            print("max:",key," ")
            print(val)
    if os.path.exists(destination):
    	os.remove(destination)
    r=make_response( dict )
    r.mimetype = 'text/html'
    return r, 200


if __name__ == '__main__':
    app.run(debug=True)
