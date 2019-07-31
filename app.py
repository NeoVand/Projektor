# Program by Neo Mohsenvand
from flask import Flask,session, render_template, url_for, flash, request, redirect
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField
from pylsl import StreamInfo, StreamOutlet
import glob
import random
import time
import os
from shutil import copyfile
from datetime import datetime
import json
import argparse

default_folder = "E:\\Dropbox (MIT)\\inSight\\Experiment\\Recordings\\fl_test"
default_fr = 32.0
eeg_exts = ['edf','easy']


info = StreamInfo(name='medialab', type='Markers', channel_count=1,
                  channel_format='int32', source_id='neo')
outlet = StreamOutlet(info)
global VIDPATH
global FRAMERATE

def is_number(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def containsEEG(directory, extensions=eeg_exts):
    files =[]
    for ext in extensions:
        files += [f for f in os.listdir(directory) if f.endswith('.' + ext)]
    return len(files)>0


app = Flask(__name__)

def pathscan(email):
    for entry in os.scandir(VIDPATH):
        check = False
        if entry.is_dir():
            for sub in os.scandir(entry):
                if sub.name==email:
                    if containsEEG(sub.path):
                        check = True
            if check:
                print('folder contained EEG file')
                continue
            else:
                return entry
    return None
    
class RegistrationForm(Form):
    email = StringField('Email', [
        validators.DataRequired(),
        validators.Email(),
        validators.EqualTo('verify', message='Email must match')
    ])
    verify = StringField('Email (verify)')
    howdy = SelectField("How do you feel",choices=[('rr', 'Rested and Ready'), ('abt', 'normal'), ('abt', 'Tired and Sleepy')], validators=[validators.DataRequired()])
    note = StringField('note',[validators.DataRequired()])
    TOA = BooleanField('I have read the experiment description and I agree with all the terms of agreement', [validators.DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        session['email']=form.email.data
        session['note']=form.note.data
        session['howdy']=form.howdy.data
        flash('Setting up the experiment ...')
        return redirect(url_for('experiment'))
    return render_template('start.html', form=form)

@app.route('/log', methods=['POST'])
def log():
    content=request.json
    outlet.push_sample([int(content['current_time'])])
    return 'done'

@app.route('/exp_end', methods=['POST'])
def exp_end():
    print('experiment ended!')
    content=request.json
    session['vidtimes'] = content
    folder = session['folder']
    # os.mkdir(folder)
    with open(os.path.join(folder,'explog_'+session['start_time']+'.json'),'w') as jsf:
        out = {'email':session['email'],'folder':folder,'session_start_time':session['start_time'],'note':session['note'], 'howdy':session['howdy'],'vid_times':session['vidtimes']}
        json.dump(out,jsf)
    flash('Thank you!')
    os.remove(os.path.join(os.curdir,'static','video','v.mp4'))
    return 'done'
@app.route('/experiment')
def experiment():
    session['start_time']= datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    email = session['email']
    path = pathscan(email)
    if path is None:
        return "WOW YOU ARE DONE!!"
    else:
        found = False
        for file in os.listdir(path):
            if file.endswith(".mp4"):
                video = os.path.join(path, file)
                found = True
        if found == False:
            return "The video directory is not set up correctly!"
        copyfile(video,os.path.join(os.curdir,'static','video','v.mp4'))
        print('file transfered.')
        session['folder']= os.path.join(path,email)
        folder = session['folder']
        if not os.path.exists(folder):
            os.mkdir(folder)
        # folder = os.path.join(path,email)

    return render_template('experiment.html',url=os.path.join(path,email), fr=FRAMERATE)

def is_valid_folder(parser, arg):
    if not os.path.exists(arg):
        parser.error("The folder %s does not exist!" % arg)
    else:
        global VIDPATH
        VIDPATH =os.path.normpath(arg)
        print(f"folder {VIDPATH} is chosen") 
def is_valid_fr(parser, arg):
    if not is_number(arg):
        parser.error(f"{arg} is not a float number")
    else:
        global FRAMERATE
        FRAMERATE = float(arg)
        print(f"frame rate {FRAMERATE} is chosen")

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', nargs='?', default=default_folder, type=str
         ,help="path to the folder of folders of videos")
    parser.add_argument('--fr', nargs='?', default=default_fr, type=float, help="video frame rate")

    args = parser.parse_args()
    is_valid_folder(parser,args.path)
    is_valid_fr(parser, args.fr)

    app.run(debug = True)
    
    

