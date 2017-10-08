from flask import Flask, session, redirect, url_for, escape, request, json, render_template

from backend import funcs
from backend.api.black_rock_api import BlackRock

app = Flask(__name__, template_folder='html/', static_folder='static/', static_url_path='')

# Create instance of MongoDB client.
mongo = funcs.connect_db()


@app.route('/')
def index():
    if 'username' in session:
        return ('<p>Logged in as {}</p>'.format(escape(session['username']))
                + "<a href='/propose'><input type=button value='Propose a trade'></a>")

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        redirect(url_for('groups'))

    if request.method == 'POST':
        if mongo.find_user(request.form['username']):
            session['username'] = request.form['username']
        else:
            return "Invalid Username"

        return redirect(url_for('groups'))

    return redirect(url_for('index'))


@app.route('/signup', methods=['POST'])
def signup():

    user_data = request.form.to_dict()
    user_data.pop('password')
    mongo.add_user(user_data)
    session['username'] = request.form['username']

    return redirect(url_for('groups'))


@app.route('/propose', methods=['GET', 'POST'])
def propose():
    if 'username' in session:
        if request.method == 'POST':
            return ("You proposed the following trade to the group:\n"
                    "<p>Symbol: {ticker}\n"
                    "<p>Action: {action}\n"
                    "<p>Type: {type}\n"
                    "<p>Price: {action}\n"
                    "<p>Shares: {shares}\n</p>"
                    "<a href='/'><input type=button value=Home></a>"
                    "".format(**request.form.to_dict()))

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


@app.route('/proposals', methods=['GET'])
def proposals():
    return render_template('proposals.html')

@app.route('/groups', methods=['GET'])
def groups():
    return render_template('groups.html')

@app.route('/vote/<stock_id>/<buy>/<approve>', methods=['GET', 'POST'])
def vote(stock_id, buy, approve):
    return 1
    if request.method == 'POST':

        return mongo.vote(stock_id, buy, approve)

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html')

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        ticker = 'aapl'
        info = BlackRock.get_historical_prices(ticker)
        return json.dumps({
            'ticker': ticker,
            'info': info
        })

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# SHHHHHH it's a secret
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
    app.run(threaded=True)
