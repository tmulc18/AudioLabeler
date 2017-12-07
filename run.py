import glob
import random
import json
import io
import os

from flask import Flask, Response, render_template, request, redirect


app = Flask(__name__)


DATA_PATH = "static/data/"#"static/LJSpeech-1.0/wavs/"
EXT = ".wav"
OUTPUT_FILE = "record.csv"


@app.route('/')
def webpage():
    data = get_settings()
    data['file'] = get_random_file()
    return render_template('labeling.html',**data)


@app.route("/update", methods=["POST"])
def update():
    data = request.form
    file_name = data['file']
    label = data.getlist('label')

    if not os.path.isfile(OUTPUT_FILE):
        f = io.open(OUTPUT_FILE,'a')
        f.write("fname,label\n")
        f.close()
    f = io.open(OUTPUT_FILE,'a')
    f.write(file_name+','+label[0]+'\n')
    f.close()
    return redirect(location='/')


def get_settings():
    return json.load(open("settings/settings.json","rb"))


def get_random_file():
    files = glob.glob(DATA_PATH+"*"+EXT)
    file = files[random.randint(0,len(files)-1)]
    return file
