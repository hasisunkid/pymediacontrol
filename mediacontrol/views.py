from mediacontrol import log,app
from flask import render_template
import os
import json

@app.route("/info")
def index():
    path = os.path.join(app.static_folder,'info.json')
    with open(path) as data_file:    
        data = json.load(data_file)
        
    return render_template('musicinfo.html',meta=data)
