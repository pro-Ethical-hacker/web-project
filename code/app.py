import mysql.connector
from flask import Flask, render_template, request, redirect, jsonify, session, url_for
import json
from flask_cors import CORS
from flask_mail import Mail


from utils import get_filter_options, get_full_info, apply_filter

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'  # Make sure to set a secure secret key in a production environment

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'soahmed.bese21seecs@seecs.edu.pk',
    MAIL_PASSWORD = 'baloch2004',
    # MAIL_DEFAULT_SENDER = 'sohaibahmed1070@gmail.com'

)

mail = Mail(app)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="project2"
)
mycursor = mydb.cursor()


# Decorator for the before_request function
@app.before_request
def before_request():
    # Check if the user is not logged in and the current request is not to the login page

    print(request.endpoint)
    if 'user' not in session and request.endpoint in ['filter','home']:
        return redirect(url_for('signin'))

@app.route('/', methods=['GET'])
def before():
    return redirect('/signin')


@app.route('/get_filter_options', methods=['GET'])
def end_point_1():
    return json.dumps(get_filter_options(mycursor))


@app.route("/get_course_info", methods=['POST'])
def end_point_2():
    id = request.json.get("course_id")
    return json.dumps(get_full_info(mycursor, id))


@app.route("/apply_filter", methods=['POST'])
def end_point_3():
    body = {
        "search": request.json.get("search"),
        "limit": request.json.get("limit"),
        "Country": request.json.get("country"),
        "Duration (years)": request.json.get("duration"),
        "Degree Level": request.json.get("degree_level"),
        "Discipline": request.json.get("discipline"),
        "Fee": request.json.get("fee"),
        "Institute": request.json.get("institute"),
        "Language": request.json.get("language"),
    }
    return json.dumps(apply_filter(mycursor, body))


@app.route('/filter', methods=['GET', 'POST'])
def filter():
    return render_template('filter.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    key = True
    if request.method == "POST":
        sql = "select count(*) from user_login where username=%s"
        username = request.form.get('username')
        passw = request.form.get('password')
        passw = passw[::-1]
        password = ""
        for i in passw:
            password += str(ord(i))
        data = ([username])
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        result = mycursor.fetchall()
        mydb.commit()
        print(password)
        if result[0][0] > 0:
            # return jsonify({"message": "failure"})
            return redirect('/signup/1')

        sql = "insert into user_login values(%s,%s)"
        data = (username, password)
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        mydb.commit()
        # return jsonify({"message": "success"})
        return render_template('second.html', key=True)
    return render_template('second.html', key=key)
    # return jsonify({"message": "failure"})


@app.route('/signup/<id>', methods=['GET','POST'])
def signup(id):
    if id == "1":
        key = False
        return render_template('second.html', key=key, error=True)
    key = False
    return render_template('second.html', key=key)


@app.route('/adminfront/<frompage>', methods=['GET', 'POST'])
def afteradminlogin(frompage):
    if request.method == 'POST':
        c_id = request.form.get('id')
        new = request.form.get('new')
        sql = 'select count(*) from courses where course_id=%s'
        data = ([c_id])
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        result = mycursor.fetchall()
        mydb.commit()
        if result[0][0] <= 0:
            return render_template('error.html')

        if frompage == 'fee':
            sql = 'update fee set pkr_value=%s where course_id=%s'
        if frompage == 'duration':
            sql1='''  (select dur_id from complete_data where course_id=%s)'''
            sql2 = '''update course_duration set dur_year=%s where dur_id = %s'''
        if frompage == 'discipline':
            sql1=''' (select disc_id from complete_data where course_id=%s)'''
            sql2 = '''update discipline set disc_name=%s where disc_id = %s'''
        if frompage == 'description':
            sql1 = '''(select disc_id from complete_data where course_id=%s)'''
            sql2 = '''update discipline set description=%s where disc_id = %s'''
        if frompage == "course":
            sql = "delete from courses where course_id=%s"
            data = ([c_id])
            mycursor = mydb.cursor()
            mycursor.execute(sql, data)
            result = mycursor.fetchall()
            mydb.commit()
        if frompage == "fee":
            data = (new, c_id)
            mycursor = mydb.cursor()
            print(sql)
            mycursor.execute(sql, data)
            mydb.commit()
            
        if frompage != "fee" and frompage != "course":
            mycursor = mydb.cursor()
            mycursor.execute(sql1, [c_id])
            descriptions = mycursor.fetchall()
            descriptions=tuple(descriptions)
            data = descriptions[0][0]
            print("following is description \n",data)
            print("follwoing is new",new)
            result=mycursor.execute(sql2,(new, data))
            print(result)
            mydb.commit()

    return render_template('admin.html')


@app.route('/admin/<page>', methods=['GET'])
def updationpages(page):
    if page == "FEE":
        return render_template('update.html', key="FEE", key_lower="fee")
    if page == "DISCIPLINE":
        return render_template('update.html', key="DISCIPLINE", key_lower="discipline")
    if page == "DURATION":
        return render_template('update.html', key="DURATION", key_lower="duration")
    if page == "DESCRIPTION":
        return render_template('update.html', key="DESCRIPTION", key_lower="description")
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')



@app.route('/deletecourse', methods=['GET'])
def deletecourse():
    return render_template('delete.html')


@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method=='POST':
       name=request.form.get('name')
       email=request.form.get('email')
       message=request.form.get('message')
       print(email)
       mail.send_message("This is a mail from blog",sender=email,recipients=['sohaibahmed1070@gmail.com'],body=message)
       return redirect('/home')
    return render_template('contact.html')



@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/frontuser', methods=['GET', 'POST'])
def afteruserlogin():
    if request.method == "POST":
        sql = "select count(*) from admin_login where username=%s and password=%s"
        username = request.form.get('username')
        passw = request.form.get('password')
        passw = passw[::-1]
        password = ""
        for i in passw:
            password += str(ord(i))
        data = (username, password)
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        result = mycursor.fetchall()
        mydb.commit()
        print(result[0][0])
        if result[0][0] > 0:
            return redirect('/adminfront/none')
        sql = "select count(*) from user_login where username=%s and password=%s"
        username = request.form.get('username')
        passw = request.form.get('password')
        passw = passw[::-1]
        password = ""
        for i in passw:
            password += str(ord(i))
        data = (username, password)
        mycursor = mydb.cursor()
        mycursor.execute(sql, data)
        result = mycursor.fetchall()
        mydb.commit()
        print(result[0][0])
        if result[0][0] > 0:
            session['user'] = username
            return redirect('/home')
            # return jsonify({"message": "success"})
        else:
            return redirect('/signin')
            # return jsonify({"message": "failure"})
    return redirect('/home')
    # return jsonify({"message": "success"})


app.run(debug=True)
