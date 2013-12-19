import sys

from flask import Flask, render_template
from flask_frozen import Freezer
import os
import shutil
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['FREEZER_DESTINATION'] = "_build"
app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def index(path):
    return render_template(path)

@freezer.register_generator
def default_generator():
    yield 'index', {'path':'index.html' }
def copy_files(src, dest, ignore=None):
    for f in os.listdir(src):
        if not os.path.isdir(f):
            shutil.copy(os.path.join(src,f),dest)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
        copy_files("./_build", "./")

    else:
        extra_dirs = ['./templates']
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in os.walk(extra_dir):
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    if os.path.isfile(filename):
                        extra_files.append(filename)

        app.run(port=5000, extra_files=extra_files)

