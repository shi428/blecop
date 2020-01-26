from flask import Flask, request, redirect, url_for, render_template, flash
import os
import thread
from concurrent.futures import ThreadPoolExecutor
import raw_to_times

app = Flask(__name__)
app.secret_key = 'super secret key'

UPLOAD_PATH = "../uploads"
ALLOWED_EXTENSIONS = ["mp4"]
STATIC_FILE_DIR = "./static/converted"

executor = ThreadPoolExecutor(2)

def do_convert(filename):
	raw_to_times.convert_mp4(filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print file.filename
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print file.filename.split(".")[1]
        if file and file.filename.split(".")[1] in ALLOWED_EXTENSIONS:
            filename = file.filename
            file.save(os.path.join(UPLOAD_PATH, filename))
            executor.submit(do_convert, filename)
            flash("Uploaded and converting")
            return redirect(request.url)
        flash("An error occurred")
        return redirect(request.url)
    return render_template("upload.html")

@app.route("/dir", methods=["GET"])
def view():
  files = os.listdir(STATIC_FILE_DIR)
  return render_template("listdir.html", len=len(files), files=files)

@app.route("/watch", methods=["GET"])
def watch():
	path = "/static/converted/" + request.args.get("fname")
	print(path)
	return render_template("video.html", path=path)

@app.route("/chart", methods=["GET"])
def graphs():
	return render_template("chart.html")

@app.route("/", methods=["GET"])
def home():
	return render_template("index.html")

app.run(debug=True, host="127.0.0.1", port=8081)
