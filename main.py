from backend import funcs

from flask import Flask, session, redirect, url_for, escape, request
app = Flask(__name__)

# Create instance of MongoDB client.
mongo = funcs.connect_db()


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if mongo.find_user(request.form['username']):
            session['username'] = request.form['username']
        else:
            return "Invalid Username"

        return redirect(url_for('index'))

    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user_data.pop('password')
        mongo.add_user(user_data)

        return "Congrats on signing up {}!".format(user_data['username'])

    return '''
        <form method="post">
            <p><input type=text name=username placeholder=Username>
            <p><input type=password name=password placeholder=Password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/propose', methods=['GET', 'POST'])
def propose():
    if request.method == 'POST':
        return request.form.__dir__

    if 'username' in session:
        return '''
            <form method="post">
                <p><input type=text name=ticker placeholder=Symbol>
                <p><input type=text name=action placeholder=Action>
                <p><input type=text name=type placeholder="Order Type">
                <p><input type=text name=price placeholder="Price">
                <p><input type=text name=shares placeholder="Number of Shares">
                <p><input type=submit value=Propose>
            </form>
        '''

    return 'You must login in order to propose a trade.'


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
####


if __name__ == '__main__':
  app.run()
