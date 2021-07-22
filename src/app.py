import json
import os

from flask import Flask, flash, render_template, request, redirect, url_for, make_response
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TimeField, BooleanField, SubmitField

from schedule.manage import Manager, Week

# ===============================================
# TODO: 
# - Add flash for courses added
# ===============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


class CourseForm(FlaskForm):
    name = TextField('Course name')
    start = TimeField('Start time')
    end = TimeField('End time')
    
    monday = BooleanField('M')
    tuesday = BooleanField('T')
    wednesday = BooleanField('W')
    thursday = BooleanField('Th')
    friday = BooleanField('F')

    submit_course = SubmitField('Submit Course')

class DoneForm(FlaskForm):
    done = SubmitField('Done')


# Non-Flask Functions ----------------------------------
def form_weekdays(form):
    day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    day_letters = ['M', 'T', 'W', 'Th', 'F']
    used = []

    for name, letter in zip(day_names, day_letters):
        if form.get('edit_form-' + name) is not None:
            used.append(letter)

    return used

# Flask Functions --------------------------------------
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/week")
def week():
    courses = Manager.course_dict_from_dict(json.loads(request.cookies.get('courses')))
    schedules = json.loads(request.cookies.get('schedules'))
    index = int(request.cookies.get('index'))
    n = len(schedules)

    if index < 0:
        index += n
    elif index >= n:
        index %= n

    week = Week([courses[name] for name in schedules[index]])
    
    return render_template('week.html', week=week.weekdays, index=index)
    


@app.route("/editor/<courses_json>", methods=["GET", "POST"])
def editor(courses_json):
    edit_form = CourseForm(prefix='edit_form')
    done_form = DoneForm(prefix='done_form')
        
    # Course form
    if edit_form.validate_on_submit() and edit_form.submit_course.data:
        json_obj = {
            'name': request.form['edit_form-name'],
            'start': request.form['edit_form-start'],
            'end': request.form['edit_form-end'],
            'days': form_weekdays(request.form)
        }
        new_url = courses_json + json.dumps(json_obj) + ','
        print("submitted")
        return redirect(url_for('editor', courses_json=new_url))

    # Final submit form
    elif done_form.validate_on_submit() and done_form.done.data:
        if courses_json.endswith('['):
            flash("You need to add at least one course!")
        else:
            # Correct the json list in the url
            if courses_json.endswith(','):
                courses_json = courses_json[:-1]
            courses_json += ']'
            
            m = Manager(courses_json)
            
            # Set cookies
            resp = redirect(url_for('week'))
            resp.set_cookie("courses", json.dumps(m.course_dict))
            resp.set_cookie("schedules", json.dumps(m.get_schedules()))
            resp.set_cookie("index", '0')
            return resp

    return render_template('edit.html', edit_form=edit_form, done_form=done_form)
    

# Redirects
@app.route("/")
def index():
    return redirect(url_for('home'))


@app.route("/editor")
@app.route("/editor/")
def edit_redirect():
    return redirect(url_for('editor', courses_json='['))


@app.route("/set_index/<change>/")
def set_index(change):
    index = int(request.cookies.get("index"))
    index += int(change)

    resp = redirect(url_for('week'))
    resp.set_cookie('index', str(index))
    return resp


if __name__ == '__main__':
    app.run()

