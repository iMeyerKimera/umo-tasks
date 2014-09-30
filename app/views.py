# -*- coding: utf-8 -*-
from flask import Flask, flash, redirect, render_template, \
    request, session, url_for, g
from functools import wraps
import sqlite3
from forms import AddTaskForm

app = Flask(__name__)
app.config.from_object('config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Functools is a module used for extending the capabilities of functions with other
# functions, which is exactly what decorators accomplish.
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
# This tests to see if logged_in is in the session. If it is, then we call
# the appropriate function (e.g., the function that the decorator is
# applied to), and if not, the user is redirected back to the login screen
# with a message stating that a login is required. Add the decorator to the
# top of the main() function:

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
# The logout() function uses the pop() method to reset the session key to the
# default value when the user logs out. The user is then redirected back to
# the login screen and a message is flashed indicating that they were logged out.

# sessions and login required decorators
# Now that users are able to login and logout, we need to protect main.html from
# unauthorized access.
#
# To prevent unauthorized access to main.html ,
# we need to set up sessions, as well as utilize the login_required decorator.
# Sessions store user information in a secure manner, usually as a token,
# within a cookie. In this case, when the session key, logged_in , is set to True ,
# the user has the rights to view the main.html page.
#
# The login_required decorator, meanwhile, checks to make sure that a user is
# authorized (e.g.,logged_in ) before allowing access to certain pages.

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect(url_for('tasks'))
    if request.method == 'GET':
        return render_template('login.html')
# This function compares the username and password entered against those from
# the configuration section. If the correct username and password are entered,
# the user is redirected to the main page and the session key, logged_in ,
# is set to True . If the wrong information is entered, an error message
# is flashed to the user.
# The url_for() function generates an endpoint for the provided method.

# Making the task view. on the tasks.html, the user will have full CRUD
# access the ability to delete tasks (delete) and mark tasks as complete
# (update) rather than just being able to add new tasks (create) to the
# database table and view (read) such tasks.
@app.route('/tasks')
@login_required
def tasks():
    g.db = connect_db()
    cur = g.db.execute(
        'select name, due_date, priority, task_id from tasks where status=1'
    )

    open_tasks = [dict(name=row[0], due_date=row[1], priority=row[2],
                       task_id=row[3]) for row in cur.fetchall()]
    cur = g.db.execute(
        'select name, due_date, priority, task_id from tasks where status=0'
    )

    closed_tasks = [dict(name=row[0], due_date=row[1], priority=row[2],
                         task_id=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks
    )
# make sure to add g to the imports
# We’re querying the database for open and closed tasks, assigning the
#  results to two variables,open_tasks and closed tasks ,  and then
# passing those variables to the tasks.html page.These variables will
#  then be used to populate the open and closed task lists, respectively.
# Make sense? Also, you may have noticed this line
# form=AddTaskForm(request.form), AddTaskForm() will be the name of
# a form used to, well, add tasks. This has not been created yet

# Add, Update, and Delete Tasks
@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    g.db = connect_db()
    name = request.form['name']
    date = request.form['due_date']
    priority = request.form['priority']
    if not name or not date or not priority:
        flash("All fields are required. Please try again.")
        return redirect(url_for('tasks'))
    else:
        g.db.execute('insert into tasks (name, due_date, priority, '
                     'status)values (?, ?, ?, 1)',
                     [request.form['name'], request.form['due_date'],
                      request.form['priority']])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted. Thanks.')
        return redirect(url_for('tasks'))

# Mark tasks as complete:
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    g.db = connect_db()
    g.db.execute(
    'update tasks set status = 0 where task_id='+str(task_id)
    )
    g.db.commit()
    g.db.close()
    flash('The task was marked as complete.')
    return redirect(url_for('tasks'))

# Delete Tasks:
@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
    g.db = connect_db()
    g.db.execute('delete from tasks where task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('The task was deleted.')
    return redirect(url_for('tasks'))

"""
1. The last two functions pass in a variable parameter, task_id , from the tasks.html page
(which we will create next). This variable is equal to the unique task_id field in the
database. A query is then performed and the appropriate action takes place. In this
case, an action means either marking a task as complete or deleting a task. Notice how
we have to convert the task_id variable to a string, since we are using concatenation
to combine the SQL query to the task_id , which is an integer.

"""