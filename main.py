from flask import Flask, session, redirect, url_for, escape, request, json, render_template

from backend import funcs
from backend.api.black_rock_api import BlackRock
from backend.api.nasdaq_api import simulate_data


app = Flask(__name__, template_folder='html/', static_folder='static/', static_url_path='')

# Create instance of MongoDB client.
mongo = funcs.connect_db()


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('groups'))

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


@app.route('/proposal', methods=['POST'])
def proposal():
    if 'username' in session:
        # mongo.add_proposal(request.form.to_dict())
        return redirect(url_for('proposals'))

    return 'You must login in order to propose a trade.'


@app.route('/proposals', methods=['GET'])
def proposals():
    return render_template('proposals.html')

@app.route('/groups', methods=['GET'])
def groups():
    return render_template('groups.html')

@app.route('/vote/<stock_id>/<buy>/<approve>', methods=['GET', 'POST'])
def vote(stock_id, buy, approve):
    return mongo.vote(stock_id, buy, approve)

@app.route('/votes/<stock_id>', methods=['GET', 'POST'])
def votes(stock_id):
    return mongo.vote_count(stock_id)

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

@app.route('/nasdaq', methods=['GET', 'POST'])
def nasdaq():
    return simulate_data('GOOG')

@app.route('/live', methods=['GET', 'POST'])
def live():
    return render_template('stock_live.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# SHHHHHH it's a secret
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
    app.run()
