from flask import Flask, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__, template_folder=os.getcwd()+'/templates/')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index_chat.html')

@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    socketio.emit('message', data)

if __name__ == '__main__':
    socketio.run(app, host='192.168.0.80', port=9050, debug=True)
    # socketio.run(app, host='192.168.0.78', port=4000, debug=True)