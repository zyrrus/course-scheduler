import json

from flask import Flask, flash, render_template, request, redirect, url_for, make_response
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TimeField, BooleanField, SubmitField

from schedule.manage import Manager, Week

# ===============================================
# TODO: 
# - Clean up css and anything else that 
# could use some help
# - Fix secret key and remove dev mode
# - Add flashes for courses added
# ===============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-that-no-one-knows'


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
    app.run(debug=True)

''' Generic course info 
[{"name":"CSC 2362","start":"15:00","end":"16:20","days":["M", "W"]},{"name":"CSC 3200","start":"10:30","end":"11:20","days":["W"]},{"name":"CSC 3380","start":"16:30","end":"17:50","days":["T", "Th"]},{"name":"CSC 4330","start":"15:00","end":"16:20","days":["T", "Th"]},{"name":"CSC 3501","start":"13:30","end":"14:50","days":["T", "Th"]},{"name":"CSC 3730","start":"09:00","end":"10:20","days":["T", "Th"]},{"name":"CSC 4101","start":"12:00","end":"13:20","days":["M", "W"]},{"name":"CSC 4103","start":"13:30","end":"14:50","days":["M", "W"]},{"name":"CSC 4444","start":"15:30","end":"16:50","days":["M", "W"]},{"name":"MATH 2060","start":"12:30","end":"13:20","days":["T", "Th"]},{"name":"MATH 4020","start":"13:30","end":"14:50","days":["T", "Th"]},{"name":"MATH 4031","start":"09:30","end":"10:20","days":["M", "W", "F"]},{"name":"MATH 4065","start":"10:30","end":"11:50","days":["T", "Th"]},{"name":"MATH 4153","start":"15:00","end":"16:20","days":["T", "Th"]},{"name":"MATH 4200","start":"08:30","end":"09:20","days":["M", "W", "F"]},
'''
