from flask import Flask
from flask_pymongo import PyMongo
import urllib.parse

app = Flask(__name__)
username = 'your_username'
password = 'your_password'
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Forming the URI
uri = f"mongodb+srv://chandureddy:Sekhar@2003@chandrasekhardb.s9r5nu8.mongodb.net/"

# Setting up PyMongo with the escaped URI
app.config["MONGO_URI"] = uri
mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = mongo.db.users.find_one({'email': email, 'password': password})
        if user_data:
            firstname = user_data['first_name']
            session['email'] = email
            session['name'] = firstname
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = {
            'first_name': request.form.get('firstname'),
            'last_name': request.form.get('lastname'),
            'email': request.form.get('email'),
            'password': request.form.get('password')
        }
        mongo.db.users.insert_one(user_data)
        flash('SIGN UP SUCCESSFUL...YOU CAN NOW LOGIN HERE...', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/intermediate')
def home():
    top_picks = mongo.db.Movies.find({"Rating": {"$gt": "8.5"}})
    ultratop = mongo.db.Movies.find({"Rating": {"$gt": "9"}})
    allmovies = mongo.db.Movies.find()
    watchlist = []
    if 'email' in session:
        watchlist = list(mongo.db.Watchlist.find({"email": session['email']}))
    return render_template('home.html', top_picks=top_picks, ultratop=ultratop, watchlist=watchlist, allmovies=allmovies)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        movies = list(mongo.db.Movies.find({
            "$or": [
                {"movie_name": {"$regex": query, "$options": "i"}},
                {"cast": {"$regex": query, "$options": "i"}},
                {"year": {"$regex": query, "$options": "i"}}
            ]
        }))
        return render_template('search_results.html', movies=movies, query=query)
    else:
        flash('Please enter a search query', 'warning')
        return redirect(url_for('home'))

@app.route('/search_results')
def search_results():
    avmovies = mongo.db.Movies.find()
    return render_template('search_results.html', avmovies=avmovies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)