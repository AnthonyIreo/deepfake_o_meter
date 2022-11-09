import flask, os, time, re, you_get, sys, shutil
import numpy as np
from datetime import datetime
from flask import  render_template, url_for, redirect, request, Flask, send_from_directory
from email_utils import SendEmail, validateEmail
import time
from concurrent.futures import ThreadPoolExecutor

# create threads
executor = ThreadPoolExecutor(2)

# Flask App
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024


@app.route("/")
def hello_world():
    return render_template('index.html')    

@app.route('/message', methods=['POST', 'GET'])
def submitmessage():
    name = request.values["message_name"]
    email = request.values["message_email"]
    subject = request.values["message_subject"]
    messages = request.values["message_message"]

    # if some inputs are empty
    if name == "":
        return render_template("error_new.html", sentence1 = "Please enter your name.", sentence2 ="")
    elif email == "":
        return render_template("error_new.html", sentence1 = "Please enter your email address.", sentence2 ="")
    elif subject == "":
        return render_template("error_new.html", sentence1 = "Please enter the subject of the message.", sentence2 ="")
    elif messages == "":
        return render_template("error_new.html", sentence1 = "Please enter some messages.", sentence2 ="")

    # record the time and create a file
    timerecord = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    save_path = '/data/web/ubmdfl/deepfake-o-meter-sync-received/a_received_messages/'
    save_path = os.path.join(save_path, timerecord)
    save_path = os.path.join(save_path, email)
    received_message = ""
    received_message = name + "(" + email + "):\n" + subject + "\n" + messages

    # create file firstly
    os.makedirs(save_path)

    # add the txt file into the path and create the txt file
    save_path = os.path.join(save_path, "message.txt")
    with open(save_path, 'w') as f:
        f.write(received_message)
        f.close

    return render_template('submit_message.html', name = name)

#the submit website
@app.route('/submit', methods=['POST', 'GET'])
def submitpadge():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':

            # Get the submision information
            f = request.files['file']
            methods = request.values.getlist("method")
            email = request.values.getlist("input_email")[0]
            # fileurl = request.values.getlist("input_file")[0]
            # timerecord = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            print('submit', methods, email)

            

            # check if the submission information is right
            isEmail = validateEmail(email)
            if isEmail == 0:
                return render_template("error_new.html", sentence1 = "Please enter your email address.", sentence2 ="")
            elif not f.filename:
                return render_template("error_new.html", sentence1 = "Please upload your file.", sentence2 ="")
            elif len(methods) == 0:
                return render_template("error_new.html", sentence1 = "Please select a detection method.", sentence2 ="")

            else:
                check_path = '/data/web/ubmdfl/deepfake-o-meter-sync-result/' # check duplicated file
                check_upload_path = os.path.join(check_path, email)
                if os.path.exists(check_upload_path):
                    return render_template("error_new.html", sentence1 = "File already exists.", sentence2 = "Please use another email address to receive the result.") #return the page that tell user the email have already exist

                basepath = '/data/web/ubmdfl/deepfake-o-meter-sync-received/'  #os.path.dirname(__file__)
                # emailDir = os.path.join(basepath, 'tmp', email)
                upload_path = os.path.join(basepath, email)
                #if not os.path.isdir(emailDir):
                    #os.mkdir(emailDir)
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                # upload_path = os.path.join(basepath, 'tmp', email, timerecord)
                
                    
                # save the video and pin code
                np.save(upload_path+'/methods', methods)
                if f.filename:
                    f.save(os.path.join(upload_path, f.filename))
                    with open(os.path.join(upload_path, (f.filename).split('.')[0]+'.csv'), 'w') as f:
                        f.writelines('Finish Save!')
                # else:
                #     sys.argv = ['you-get', '-o', upload_path, '-O', 'tmp', fileurl]
                #     you_get.main()
                #     with open(os.path.join(upload_path, 'tmp.csv'), 'w') as f:
                #         f.writelines('Finish Save!')
                
                # return render_template('succeed.html')
                sleep = 0
                # check_path = '/data/web/ubmdfl/deepfake-o-meter-sync-result/' 
                # check_upload_path = os.path.join(check_path, email)
                # check_upload_path = '/data/web/ubmdfl/deepfake-o-meter-sync-result/' + email + '/result.png'
                # check if the path of txt file exists
                check_txt_path = '/data/web/ubmdfl/deepfake-o-meter-sync-result/' + email + '/result.txt'

                # orginal while
                while (not os.path.exists(check_txt_path))and sleep < 300:
                        sleep = sleep + 1
                        time.sleep(1)

                # if the path of file does not exist, while means the file is too large to analysis
                if not os.path.exists(check_txt_path):
                    return render_template("error_new.html", sentence1 = "The size of uploaded file is too large.", sentence2 = "Please upload another file with a smaller size") #return the page that tell user the email have already exist
                # if result exists
                else:
#                     check_upload_path = '../deepfake-o-meter-sync-result/' + email + '/result.png'
                    # check_upload_path = '../deepfake-o-meter-sync-result/' + email + '/result.png'
                    # read the data of result.txt
                    _true = ''
                    _false = ''
                    with open(check_txt_path, "r") as f:
                        all_content = f.read()
                        all_content_list = all_content.split("\n", 1)
                        content_true = all_content_list[0].split(":")
                        content_false = all_content_list[1].split(":")
                        _true += content_true[1]
                        _false += content_false[1]
                        f.close()


                    return render_template('result.html', true_for_result=_true, false_for_result=_false)
                    # return render_template('result.html', image=check_upload_path)

        # created comment on 10/17
        # if click the Check Status button and it would return the result page
#         elif request.form['submit_button'] == 'Check Status':
            

#             # Get the submision information
#             f = request.files['file']
#             methods = request.values.getlist("method")
#             email = request.values.getlist("input_email")[0]
#             fileurl = request.values.getlist("input_file")[0]
#             timerecord = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
#             print('Check Status', methods, email)

#             # check if the submission information is right
#             isEmail = validateEmail(email)
#             if isEmail == 0:
#                 return redirect(url_for('error',type='Email'))
            
#             else:
#                 check_path = '/data/web/ubmdfl/deepfake-o-meter-sync-result/' # check duplicated file
#                 check_upload_path = os.path.join(check_path, email)
#                 if not os.path.exists(check_upload_path):
#                     return redirect(url_for('error', type='Input')) #return the page that tell user the email have already exist
#                 # if result exists
#                 else:
# #                     check_upload_path = '../deepfake-o-meter-sync-result/' + email + '/result.png'
#                     check_upload_path = '../deepfake-o-meter-sync-result/' + email + '/result.png'
#                     return render_template('result.html', image=check_upload_path)




# edited on 10/30/2022
# test, edited on 09/29/2022
            time.sleep(2)
            return render_template('result.html', image="./static/images/result.jpg")
            # test end

            # original code for the check status button
            email = request.values.getlist("input_email")[0]
            isEmail = validateEmail(email)
            if isEmail == 0:
                return redirect(url_for('error', type='Email'))

            # if email is validated, we need to check if the email file exists
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
                    time_folder=foldername

                if not pin_flag:
                    return redirect(url_for('error', type='PIN'))

                #input_folder = basepath+email+'/'+time_folder+'/'
                result_folder = '/data/web/ubmdfl/deepfake-o-meter-sync-result/' + email + '/' + time_folder + '/'
                #result_folder=input_folder
                if os.path.isfile(result_folder+'result.zip'):
                    return render_template('status.html', status = 'complete')
                    # changed ('status.html', status = 'complete')
                else:
                    return render_template(url_for('result'), status='Running')

# 09/29/2022 edited
@app.route("/result")
def result_web():
    return render_template('result.html')



@app.route('/error/<string:type>')
def error(type):
    if type=='Email':
        error = 'email address'
    
    # for the message form input
    elif type=='Name':
        error = 'name'
    elif type=='Subject':
        error = 'subject'
    elif type=='Message':
        error = 'message'

    elif type=='Input2':
        error = 'email repeatedly'
    elif type=='Method':
        error = 'selected methods'
    elif type == 'PIN':
        error = 'PIN code'
    elif type == 'Download':
        error = 'download URL'
    elif type == 'File already exists':
        error = 'Latest result is ready, please hit the check status button.'
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
    date = subfolders[1]
    # Check if email and date are matched with PIN
    received_folder = '/data/web/ubmdfl/deepfake-o-meter-sync-received/{}/{}'.format(email, date)

    directory = os.path.join('/data/web/ubmdfl/deepfake-o-meter-sync-result/{}/{}/'.format(email, date))
    
    fn = 'result.zip'
    if os.path.isfile(os.path.join(directory, fn)):
        return send_from_directory(directory, fn, as_attachment=True)
    raise exceptions.MyHttpNotFound('not found file')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)

    # automatic updated(09/28/2022 edited)
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.run(debug=True, host='0.0.0.0')

    app.run()