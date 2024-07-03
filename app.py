from flask import Flask, render_template,request,redirect,url_for,send_file
import os
from werkzeug.utils import secure_filename
import functions
import Translate
UPLOAD_FOLDER = 'D:/projects/Internship_frontend/uploads'
images=os.path.join('static','images')
upload=os.path.join('uploads')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['icons'] = images
fav_icon = os.path.join(app.config['icons'], 'logo.png')

uploaded_files=[]
genfile_path=''
folder_path=''




@app.route('/')
def index():
    uploaded_files=functions.read_from_file()
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
        global genfile_path,folder_path
        if request.method == 'POST':
            file = request.files['file']
            folder_path = request.form['folderpath']
            option = request.form['option'] 
            #print(option) 
            if file:
                filename = secure_filename(file.filename)
                filepath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(filepath)
                file.save(filepath)
                audioname=functions.converter(filepath,filename)
                print("uploaded")
                os.remove(filepath)
                fname=functions.text_generation(audioname)
                genfile_path=fname
                os.remove(audioname)
                if(option):
                    tran_path=Translate.translate_subtitles(genfile_path)
                    uploaded_files=functions.save_file(tran_path,folder_path)
                    os.remove(genfile_path)
                else:
                    uploaded_files=functions.save_file(genfile_path,folder_path)
                return render_template("index.html",message="successful",filepath=genfile_path,fav_icon=fav_icon, uploaded_files=uploaded_files)                
        return render_template("index.html",message="none",fav_icon=fav_icon)
    except Exception as e:
        print(e)
        status= "updation error"
        message=e   
        return render_template('error.html', error_title=status, error_message=message,fav_icon=fav_icon), 500


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
