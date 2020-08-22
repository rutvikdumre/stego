from Backend import encode,decrypt
import numpy
from numpy import asarray
from PIL import Image,ImageOps
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template,send_file
from werkzeug.utils import secure_filename




UPLOAD_FOLDER = 'e:\\Stego\\'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        file = Image.open(UPLOAD_FOLDER+'download.jpg')
        
        
        if request.form['go']=='encrypt':
            return redirect(url_for('image'))
        return redirect(url_for('decode1'))
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        image1 = Image.open(UPLOAD_FOLDER+'download.jpg')
        msg=request.form['msg']
        x=encode(image1, msg)
        x.convert('RGB').save(UPLOAD_FOLDER+'new1.png')
        return send_file(UPLOAD_FOLDER+'new1.png', as_attachment=True)
    return render_template('encodepage.html')


@app.route('/decode')
def decode1():
    image1 = Image.open('download.jpg')
    msg1= decrypt(image1)
    return render_template('rutwik.html',msg=msg1)

if __name__ == '__main__':
   app.run(debug = True)







