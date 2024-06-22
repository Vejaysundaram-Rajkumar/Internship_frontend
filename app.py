from flask import Flask, render_template,request,redirect,url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:\\projects\\Internship_frontend\\uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate')
def generate():
    return render_template("generate.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            print("hi1")
            # check if the post request has the file part
            if 'file' not in request.files:
                return redirect(request.url)
            print("hi2")
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template('generate.html', message="successful")
            
        return render_template("generate.html",message="none")
    except:
        status= "updation error"
        message="Upload failure!"
        return render_template('error.html', error_title=status, error_message=message), 500


if __name__ == '__main__':
    app.run()
