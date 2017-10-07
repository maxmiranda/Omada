from flask import Flask, session, redirect, url_for, escape, request

from backend import funcs
# from backend.api.black_rock_api import BlackRock

app = Flask(__name__)

# Create instance of MongoDB client.
mongo = funcs.connect_db()


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as {}'.format(escape(session['username']))
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
            <p><input type=text name=username placeholder=Username>
            <p><input type=password name=password placeholder=Password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user_data.pop('password')
        mongo.add_user(user_data)
        session['username'] = request.form['username']

        return ("<p>Congrats on signing up {}!</p>".format(user_data['username'])
                + "<a href='/login'><input type=button value='Login'></a>")

    return '''
        <form method="post">
            <p><input type=text name=username placeholder=Username>
            <p><input type=password name=password placeholder=Password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/propose', methods=['GET', 'POST'])
def propose():
    if 'username' in session:

        if request.method == 'POST':
            return ("You proposed the following trade to the group:\n"
                    "<p>Symbol: {ticker}\n"
                    "<p>Action: {action}\n"
                    "<p>Type: {type}\n"
                    "<p>Price: {action}\n"
                    "<p>Shares: {shares}\n".format(**request.form.to_dict()))

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
        
    

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if 'username' in session:
        if request.method == 'POST':
            ticker = str(request.form.to_dict()["ticker"])
            return ("You requested the following information:\n"
                    "<p>Symbol: " + ticker + "\n"
                    "<p>Value: " + str(BlackRock.get_stock_performance_key_val(ticker)))

        return '''
            <form method="post">
                <p><input type=text name=ticker placeholder=Symbol>
                <p><input type=submit value=Info>
            </form>
        '''

    return 'You must login in order to request stock info.'



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
