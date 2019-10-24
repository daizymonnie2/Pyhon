from flask import Flask, render_template, request, session
import pymysql

app = Flask(__name__)
app.secret_key = "monnie0708068740daizy"


# you can generate random key


@app.route('/', methods=['GET', 'POST'])
def login():
    # A default browser uses GET method by default
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "" or password == "":
            return render_template('login.html', msg1="* Empty credentials!!")

        con = pymysql.connect("localhost", "root", "", "guestbook")
        cursor = con.cursor()

        sql = "SELECT * FROM  `users` WHERE username = %s AND password =%s"

        data = (username, password)

        cursor.execute(sql, data)
        # fetch data found
        if cursor.rowcount == 0:
            return render_template('login.html', msg1="*Login failed!")
        elif cursor.rowcount == 1:
            results = cursor.fetchall()
            session['x'] = username
            # store username in a session

            return render_template('checkin.html', msg9="WELCOME TO GRAND REGENCY HOTEL:", results=results)
        else:
            return render_template('login.html', msg1="*Error: Kindly Contact the Admin")

    else:
        return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if 'x' in session:
        user = session['x']  # retrieves session 'x'
        # check if there is any session 'x'

        # A default browser uses GET method by default
        if request.method == 'POST':

            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            room = request.form['room']
            mobile = request.form['mobile']
            timein = request.form['timein']

            if fname == "":
                return render_template('checkin.html', msg1="* please enter your first name")
            if lname == "":
                return render_template('checkin.html', msg2="* please enter your last name")
            if email == "":
                return render_template('checkin.html', msg3="* please enter your email")
            if room == "":
                return render_template('checkin.html', msg4="* please enter your allocated room")
            if mobile == "":
                return render_template('checkin.html', msg5="* please enter your phone number")
            if timein == "":
                return render_template('checkin.html', msg6="* please enter time in")

            # connect to host and db

            con = pymysql.connect("localhost", "root", "", "guestbook")
            # cursor to excecute

            cursor = con.cursor()

            sql = "INSERT INTO `clients`(`fname`, `lname`, `email`, `room`, `mobile`, `timein`,`user`) VALUES (%s,%s,%s,%s,%s,%s,%s)"

            # put values in a turple
            data = (fname, lname, email, room, mobile, timein, user)

            # append your data to sql
            cursor.execute(sql, data)
            con.commit()  # commit changes
            return render_template('checkin.html', msg="SAVED SUCCESSFULLY")


        else:
            return render_template('checkin.html')
    else:
        return 'You are not logged in <a href = "/"> LOGIN HERE'


@app.route('/register', methods=['GET', 'POST'])
def register():
    # A default browser uses GET method by default
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        level = request.form['level']

        if username == "":
            return render_template('register.html', msg7="* please enter your username")
        if password == "":
            return render_template('register.html', msg8="* please enter your password")
        if level== "":
            return render_template('register.html', msg9="* please enter your Role")

        # connect to host and db

        con = pymysql.connect("localhost", "root", "", "guestbook")
        # cursor to excecute

        cursor = con.cursor()

        sql = "INSERT INTO `users`(`username`,`password`, `level`) VALUES (%s,%s,%s)"

        # put values in a turple
        data = (username, password, level)

        # append your data to sql
        cursor.execute(sql, data)
        con.commit()  # commit changes
        return render_template('register.html', msg="SAVED SUCCESSFULLY")


    else:
        return render_template('register.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'x' in session:
    # A default browser uses GET method by default
        if request.method == 'POST':

            mobile = request.form['mobile']

            if mobile == "":
                return render_template('search.html', msg5="* please enter a phone number")

            con = pymysql.connect("localhost", "root", "", "guestbook")
            cursor = con.cursor()

            sql = "SELECT * FROM  `clients` WHERE mobile = %s AND flag =%s"

            data = (mobile, "yes")

            cursor.execute(sql, data)
            # fetch data found
            if cursor.rowcount < 1:
                return render_template('search.html', error="No Records Found")

            results = cursor.fetchall()

            return render_template('search.html', results=results)


        else:
            return render_template('search.html')
    else:
        return 'You are not logged in <a href = "/"> LOGIN HERE'

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'x' in session:
    # A default browser uses GET method by default
        if request.method == 'POST':

            room = request.form['room']

            if room == "":
                return render_template('checkout.html', msg4="* please enter a room number")

            con = pymysql.connect("localhost", "root", "", "guestbook")
            cursor = con.cursor()

            sql = "SELECT * FROM  `clients` WHERE room = %s AND flag =%s "

            data = (room, "yes")

            cursor.execute(sql, data)
            # fetch data found
            if cursor.rowcount < 1:
                return render_template('checkout.html', error="No Records Found")

            results = cursor.fetchall()

            return render_template('checkout.html', results=results)


        else:
            return render_template('checkout.html')
    else:
        return 'You are not logged in <a href = "/"> LOGIN HERE'

@app.route('/clientcheckout/<room>', methods=['POST', 'GET'])
def clientcheckout(room):
    if 'x' in session:
        if request.method == "GET":
            con = pymysql.connect("localhost", "root", "", "guestbook")

            cursor = con.cursor()

            sql = "UPDATE `clients` SET `flag`=%s WHERE room = %s"

            data = ("no", room)

            cursor.execute(sql, data)
            con.commit()
        return render_template('checkout.html', msg8="CHECKED OUT")

    else:
        return 'You are not logged in <a href = "/"> LOGIN HERE'
@app.route('/delete', methods=['GET', 'POST'])  # every root is attached to a fuction
def delete():
    if 'x' in session:
        if request.method == 'POST':
            mobile = request.form['mobile']

            if mobile == "":
                return render_template('delete.html', msg3="Please enter no")

            con = pymysql.connect("localhost", "root", "", "guestbook")
            cursor = con.cursor()

            sql = " DELETE FROM clients WHERE mobile = %s AND flag =%s"
            # We first put valaues in a turple
            data = (mobile, "no")
            # Append data to sql
            cursor.execute(sql, data)
            con.commit()

            if cursor.rowcount > 0:
                return render_template('delete.html', msg3="deleted succesfully!")
            else:
                return render_template('delete.html', msg3="failed to delete!!")

        else:
            # return template
            return render_template('delete.html')
    else:
        return 'You are not logged in <a href = "/"> LOGIN HERE'
@app.route('/logout')
def logout():
     session.pop('x',None) # clear session 'x'
     return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=
            'true')
