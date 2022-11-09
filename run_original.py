import flask, os, time, re, you_get, sys, shutil
import numpy as np
from datetime import datetime
from flask import  render_template, url_for, redirect, request, Flask, send_from_directory
from email_utils import SendEmail, validateEmail


# Flask App
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024


@app.route("/")
def hello_world():
    return render_template('index.html')


#the submit website
@app.route('/submit', methods=['POST', 'GET'])
def submitpadge():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
            # Get the submision information
            f = request.files['file']
            methods = request.values.getlist("method")
            email = request.values.getlist("input_email")[0]
            fileurl = request.values.getlist("input_file")[0]
            pin = request.values.getlist("input_pin")[0]
            timerecord = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            print('submit', methods, email)

            # check if the submission information is right
            isEmail = validateEmail(email)
            if isEmail == 0:
                return redirect(url_for('error',type='Email'))
            elif not f.filename and len(fileurl)==0:
                return redirect(url_for('error',type='Input'))
            elif len(methods) == 0:
                return redirect(url_for('error',type='Method'))
            elif not pin.isdigit() or len(pin) < 4 or len(pin) > 6:
                return redirect(url_for('error',type='PIN'))
            else:
                basepath = '/data/web/ubmdfl/deepfake-o-meter-sync-received/'  #os.path.dirname(__file__)
                # emailDir = os.path.join(basepath, 'tmp', email)
                upload_path = os.path.join(basepath, email, timerecord)
                #if not os.path.isdir(emailDir):
                    #os.mkdir(emailDir)
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                # upload_path = os.path.join(basepath, 'tmp', email, timerecord)

                # save the video and pin code
                np.save(upload_path+'/methods', methods)
                np.save(upload_path+'/pin', pin)
                if f.filename:
                    f.save(os.path.join(upload_path, f.filename))
                    with open(os.path.join(upload_path, (f.filename).split('.')[0]+'.csv'), 'w') as f:
                        f.writelines('Finish Save!')
                else:
                    sys.argv = ['you-get', '-o', upload_path, '-O', 'tmp', fileurl]
                    you_get.main()
                    with open(os.path.join(upload_path, 'tmp.csv'), 'w') as f:
                        f.writelines('Finish Save!')


                # send the email
                title = 'DeepFake-o-meter received your submission'
                content = 'We have received your submission. The result will be send to your email later. \n' + \
                'Please remeber your pin code:' + pin + '\n' + \
                'If you don not receive the results in 2 days, Pleasse contact us via deepfakeometer@gmail.com.'
                
                # SendEmail(email, title, content)
            return render_template('succeed.html')
            
        elif request.form['submit_button'] == 'Check Status':
            email = request.values.getlist("input_email")[0]
            pin = request.values.getlist("input_pin")[0]
            isEmail = validateEmail(email)
            if isEmail == 0:
                return redirect(url_for('error', type='Email'))
            elif not pin.isdigit() or len(pin) < 4 or len(pin) > 6:
                return redirect(url_for('error', type='PIN'))
            else:
                basepath='/data/web/ubmdfl/deepfake-o-meter-sync-received/'
                #print('PIN:', type(pin), pin)

                #basepath='./'
                user_foldername_list=os.listdir(basepath)
                #print(user_foldername_list)

                if not email in user_foldername_list:
                    return redirect(url_for('error', type='Email'))

                #np.save(basepath+email+'/123/pin', pin)
                user_time_foldername_list = os.listdir(basepath+email+'/')
                pin_flag=True
                for foldername in user_time_foldername_list:
                    try:
                        saved_pin=np.load(basepath+email+'/'+foldername+'/pin.npy')
                        #print('saved:', type(saved_pin), saved_pin)
                        #print('PIN:', type(pin), pin)
                        if saved_pin==pin:
                            pin_flag=True
                            time_folder=foldername
                            break
                    except:
                        continue

                if not pin_flag:
                    return redirect(url_for('error', type='PIN'))

                #input_folder = basepath+email+'/'+time_folder+'/'
                result_folder = '/data/web/ubmdfl/deepfake-o-meter-sync-result/' + email + '/' + time_folder + '/'
                #result_folder=input_folder
                if os.path.isfile(result_folder+'result.zip'):
                    return render_template(url_for(result_folder+'result.zip'))
                    # changed ('status.html', status = 'complete')
                else:
                    return render_template('status.html', status='Running')






@app.route('/error/<string:type>')
def error(type):
    if type=='Email':
        error = 'email address'
    elif type=='Input':
        error = 'input video'
    elif type=='Method':
        error = 'selected methods'
    elif type == 'PIN':
        error = 'PIN code'
    elif type == 'Download':
        error = 'download URL'
    return render_template('error.html', error=error, type=type)


#the reference website
@app.route('/reference')
def index():
    return render_template('reference.html')
    
@app.route('/terms')
def terms():
    return render_template('terms.html')
    
    
# Downloading results    
@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    # filename = email address _ PIN code _ date
    subfolders = filename.split('_')
    email = subfolders[0]
    pin = subfolders[1]
    date = subfolders[2]
    # Check if email and date are matched with PIN
    received_folder = '/data/web/ubmdfl/deepfake-o-meter-sync-received/{}/{}'.format(email, date)
    pin_ = np.load(os.path.join(received_folder, 'pin.npy'))
    if pin_ != pin:
        return redirect(url_for('error',type='Download'))
    else:
        directory = os.path.join('/data/web/ubmdfl/deepfake-o-meter-sync-result/{}/{}/'.format(email, date))
        fn = 'result.zip'
        if os.path.isfile(os.path.join(directory, fn)):
            return send_from_directory(directory, fn, as_attachment=True)
        raise exceptions.MyHttpNotFound('not found file')
    

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, port=5006)
    app.run()
