from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with your secret key
app.permanent_session_lifetime = timedelta(minutes=5)

# Dummy users (in a real app, use a database)
users = {'admin': 'password'}

# Dummy movie data
movies = [
    {'title': 'Inception', 'rating': '8.8', 'logo': 'https://via.placeholder.com/50x75'},
    {'title': 'The Dark Knight', 'rating': '9.0', 'logo': 'https://via.placeholder.com/50x75'},
    # Add more movies here
]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if users.get(username) == password:
        session['username'] = username
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/intermediate')
def intermediate():
    if 'username' in session:
        return render_template('intermediate.html')
    return redirect(url_for('home'))

@app.route('/movies')
def movie_list():
    if 'username' in session:
        return render_template('movies.html', movies=movies)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
