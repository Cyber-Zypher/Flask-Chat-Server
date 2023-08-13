import csv

from flask import Flask, render_template, request, session, redirect, jsonify, Response, send_file
import pymysql.cursors
import bcrypt
import io

app = Flask(__name__, template_folder='templates')
app.secret_key = "51c485a293ee32d79b8700db67b69243759cb9adfbd60009"

# MySQL configurations
db_host = 'localhost'
db_user = 'UNAME'
db_password = 'PASSWD'
db_name = 'DB_NAME'


def create_connection():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name, charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def home():
    if 'username' in session:
        return redirect('/chat')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        connection = create_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                user = cursor.fetchone()

                if user:
                    error = 'Username already exists'
                    return render_template('register.html', error=error)

                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(sql, (username, hashed_password))
                connection.commit()

                session['username'] = username
                return redirect('/chat')

        finally:
            connection.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        connection = create_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                user = cursor.fetchone()

                if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
                    session['username'] = username
                    return redirect('/chat')
                else:
                    error = 'Invalid username or password'
                    return render_template('login.html', error=error)

        finally:
            connection.close()

    return render_template('login.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect('/')

    if request.method == 'POST':
        message = request.form['message']
        username = session['username']

        connection = create_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO chat (username, message) VALUES (%s, %s)"
                cursor.execute(sql, (username, message))
                connection.commit()

        finally:
            connection.close()

    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM chat"
            cursor.execute(sql)
            messages = cursor.fetchall()

    finally:
        connection.close()

    return render_template('chat.html', messages=messages)


@app.route('/export-chats')
def export_chats():
    # if 'username' not in session or session['username'] != 'admin':
    #     return redirect('/')

    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM chat"
            cursor.execute(sql)
            chats = cursor.fetchall()

        # Create a CSV file in memory
        csv_data = io.StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(['Username', 'Message'])
        for chat in chats:
            csv_writer.writerow([chat['username'], chat['message']])

        # Create a Flask Response with the CSV data
        response = send_file(
            io.BytesIO(csv_data.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name="chats.csv"
            # attachment_filename='chats.csv'
        )

        return response

    finally:
        connection.close()


@app.route('/clear-chats', methods=['GET', 'POST'])
def clear_chats():
    # if 'username' not in session or session['username'] != 'admin':
    #     return redirect('/')

    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM chat"
            cursor.execute(sql)
            connection.commit()

    finally:
        connection.close()

    return redirect('/chat')


@app.route('/get-messages')
def get_messages():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM chat"
            cursor.execute(sql)
            messages = cursor.fetchall()
    finally:
        connection.close()

    return render_template('chat-messages.html', messages=messages)



@app.route('/export')
def export():
    if 'username' not in session or session['username'] != 'admin':
        return redirect('/')

    return render_template('export.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
