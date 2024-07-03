from flask import Flask, render_template,request,redirect,url_for,send_file
import os
from werkzeug.utils import secure_filename

import main

UPLOAD_FOLDER = 'D:/projects/Internship_frontend/uploads'
images=os.path.join('static','images')
upload=os.path.join('uploads')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['icons'] = images
fav_icon = os.path.join(app.config['icons'], 'logo.png')

uploaded_files=[]
folder_path=''




@app.route('/')
def index():
    uploaded_files=main.read_from_file()
    return render_template("index.html",fav_icon=fav_icon,uploaded_files=uploaded_files)

@app.route('/about')
def about():
    return render_template("about.html",fav_icon=fav_icon)

@app.route('/download')
def download():
    file_path = request.args.get('file_path')
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        status= "File error"
        message="File Not Found !!"
        return render_template('error.html', error_title=status, error_message=message,fav_icon=fav_icon), 404



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    try:
        global folder_path
        if request.method == 'POST':
            
            # Getting the inputs from the frontend.
            file = request.files['file']
            folder_path = request.form['folderpath']
            option = request.form['option'] 

            # Check for the path given is correct or wrong.
            if os.path.exists(folder_path):
                # call the main function for processing .....
                result=main.main_function(file,folder_path,option)
                
                if(result[0]=="translated" or result[0]=="transcribed"):
                    return render_template("index.html",message=result[0],filepath=result[1],fav_icon=fav_icon, uploaded_files=result[2]) 
                else:
                    return render_template('error.html', error_title="error", error_message=result[0],fav_icon=fav_icon), 500

            else:
                message="invalid folder path!."
                return render_template('error.html', error_title="patherror", error_message=message,fav_icon=fav_icon)


        return render_template("index.html",message="none",fav_icon=fav_icon)
    
    except Exception as e:
        print(e)
        status= "updation error"
        message=e   
        return render_template('error.html', error_title=status, error_message=message,fav_icon=fav_icon), 500


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
