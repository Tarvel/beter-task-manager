from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta
from threading import Timer

app = Flask(__name__)
socketio = SocketIO(app)

tasks = [] 


def notify_user(task):
    socketio.emit('notification', {'message': f"Task '{task['title']}' is overdue!"})


def schedule_notification(task):
    time_now = datetime.now()
    delay = (task['deadline'] - time_now).total_seconds()

    if delay > 0:
        Timer(delay, notify_user, args=(task,)).start() #Timer used to count down to when the set deadline takes place then implements the function


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    time_delta = int(request.form['time'])
    deadline = datetime.now() + timedelta(minutes=time_delta)

    task = {'title': title, 'deadline': deadline, 'completed': False}
    tasks.append(task)

    schedule_notification(task)

    return redirect(url_for('index'))


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks[task_id]['completed'] = True
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task from the list."""
    tasks.pop(task_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    socketio.run(app, debug=True)
