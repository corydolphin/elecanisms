import sys

from flask import Flask, render_template
from flask_frozen import Freezer
import os
import shutil
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['FREEZER_DESTINATION'] = "_build"
freezer = Freezer(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mechanical.html')
def mechanical():
    return render_template('mechanical.html')



def copy_files(src, dest, ignore=None):
    for f in os.listdir(src):
        if not os.path.isdir(f):
            shutil.copy(os.path.join(src,f),dest)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
        copy_files("./_build", "./")

    else:
        app.run(port=5000)

