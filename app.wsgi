import sys

sys.path.insert(0,'/web/ubmdfl/deepfake-o-meter/web/')

python_home = '/data/web/ubmdfl/deepfake-o-meter/venv-dfom'

activate_this = python_home + '/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


from run import app as application
