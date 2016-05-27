from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'my_secret_key'
database = MySQLConnector(app, 'friendships')

@app.route('/', methods = ['GET'])
def index():
    query = "SELECT * FROM users"
    values = {}
    users = database.query_db(query,values)
    return render_template('index.html', users = users)

@app.route('/add_friend/<int:id>')
def create_friendship(id):

    try:
        session['current_user']
        if id != session['current_user']:
            query = "insert into friendships (friend1_id, friend2_id, created_at, updated_at) VALUES (:friend1_id, :friend2_id, NOW(), NOW())"
            values = {
                'friend1_id' : session['current_user'],
                'friend2_id' : id
            }
            database.query_db(query,values)
            print ("WINNNING")
            # del 'current_user' from session
            session.pop('current_user')
            return redirect('/show_friends')
        else:
            return redirect('/')
    except KeyError:
        session['current_user'] = id
        return redirect('/')

@app.route('/show_friends')
def show_friends():
    query = "SELECT users.first_name as friend1, friend.first_name as friend2 from users JOIN friendships on friendships.friend1_id = users.id LEFT JOIN users as friend on friendships.friend2_id = friend.id"
    values = {}
    friendships = database.query_db(query,values)
    print friendships
    return render_template('friends.html', friends = friendships)

if __name__ == '__main__':
  app.run(debug = True)
