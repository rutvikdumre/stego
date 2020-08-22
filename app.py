import numpy
from numpy import asarray
from PIL import Image,ImageOps
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template,send_file
from werkzeug.utils import secure_filename







def hide(pixel,msg):
    bno='{:08b}'.format(pixel)
    #print(bno)
    no=bno[:-1]+msg
    #print(no)
    ans= int(no,2)
    #print(ans)
    return ans

def unhide(pixel):
    #bno='{:08b}'.format(pixel)
    bno= bin(pixel)
    return bno[-1]


    
def BinaryToDecimal(binary):  
         
    binary1 = binary  
    decimal, i, n = 0, 0, 0
    while(binary != 0):  
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)  
        binary = binary//10
        i += 1
    return (decimal)     
    

def encode(image1,msg):
    mywidth = 256

    wpercent = (mywidth/float(image1.size[0]))
    hsize = int((float(image1.size[1])*float(wpercent)))
    image1 = image1.resize((mywidth,hsize))
    
    r,c=image1.size[0],image1.size[1]
    image2=ImageOps.grayscale(image1)
    #print(image2.size)
    data=asarray(image2)
    #print(data)
    data1=data.tolist()
    #print(data1)
    #image2.show()
    
    msg = "wearempstmemomoteam"+msg+"$$$"
    x=''
    for i in msg:
        x+=format(ord(i), '08b')

    #x= ' '.join(format(ord(i), 'b') for i in msg) 
    #print(x)
    x=str(x)
    #print(x)
    arr = data1
    ctr=0
    for i in range(r):
        for j in range(c):
            if ctr<len(x):
                arr[i][j]=hide(data1[i][j],x[ctr])
                ctr+=1


    #print(arr)

    image_arr=numpy.array(arr)
    #print(image_arr)

    image_arr2=Image.fromarray(image_arr)
    #image_arr2=image_arr2.save('imgdemo.png')
    #image_arr2.show()
    return image_arr2

#--------------------------Decryption-------------------------#


def decode(img):

    r,c=img.size[0],img.size[1]
    data=asarray(img)
    data1=data.tolist()
    #print(r,c)
    output=''
    y=''
    for i in 'wearempstmemomoteam':
        y+=format(ord(i), '08b')
    n=len(y)
    ctr=0
    flag= 'encrypted'
    
    for i in range(r):
        if flag!='encrypted':
            break
        for j in range(c):
            if c<n:
                if data1[i][j]!= int(y[ctr]):
                    flag='not enc'
                    break
            elif ctr==n:
                flag='enc'
                break
            
            ctr+=1
            

    if(flag=='encrypted' or flag=='enc'):
        #print(output)
        y=''
        for i in '$$$':
            y+=format(ord(i), '08b')
        for i in range(r):
            for j in range(c):
                if y in output:
                    flag=True
                    break
                else:
                    output+=unhide(data1[i][j])
        
        #print(output)

        str_data =' '
           

        for i in range(0, len(output), 8): 
              
           
            temp_data = int(output[i:i + 8]) 
            decimal_data = BinaryToDecimal(temp_data) 
            str_data = str_data + chr(decimal_data)  

          
        return str_data[(len("wearempstmemomoteam")+1):-3]
    else:
        return "There is no message in the image or the image has been modified"
def decrypt(img):
    return decode(ImageOps.grayscale(img))
    

    
'''image1 = Image.open('download.jpg')
x=encode(image1, input())
x.show()
x.convert('RGB').save('new1.png')
img=Image.open('new1.png')
print(decrypt(img))'''
























UPLOAD_FOLDER = 'C:/Users/rutvik/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'No selected file'
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],'download.jpg'))
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







