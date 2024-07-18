from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
import webview

import main

# Set webview settings to allow downloads
webview.settings['ALLOW_DOWNLOADS'] = True

# Define upload folder and static images folder
UPLOAD_FOLDER = 'uploads/'
images = os.path.join('static')
upload = os.path.join('uploads')

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['icons'] = images
fav_icon = os.path.join(app.config['icons'], 'logo.png')

# List to store uploaded files
uploaded_files = []

@app.route('/')
def index():
    uploaded_files = main.read_from_file()
    return render_template("index.html", fav_icon=fav_icon, uploaded_files=uploaded_files)

@app.route('/about')
def about():
    return render_template("about.html", fav_icon=fav_icon)

@app.route('/download')
def download():
    file_path = request.args.get('file_path')
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        status = "File error"
        message = "File Not Found !!"
        return render_template('error.html', error_title=status, error_message=message, fav_icon=fav_icon), 404

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            option = request.form['option']
            target = request.form['translateTo'] if option == 'translate' else ''
            print(target)

            # Call the main function for processing
            result = main.main_function(file, target, option)
            
            if result[0] == "translated" or result[0] == "transcribed":
                return render_template("index.html", message=result[0], filepath=result[1], fav_icon=fav_icon, uploaded_files=result[2])
            else:
                return render_template('error.html', error_title="error", error_message=result[0], fav_icon=fav_icon), 500

        return render_template("index.html", message="none", fav_icon=fav_icon)

    except Exception as e:
        print(e)
        status = "updation error"
        message = str(e)
        return render_template('error.html', error_title=status, error_message=message, fav_icon=fav_icon), 500

if __name__ == '__main__':
    # Create a webview window and start it
    window = webview.create_window('Transcriber', app, width=1100, height=800)
    webview.start()
