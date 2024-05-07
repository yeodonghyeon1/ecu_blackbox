from flask import Flask, render_template
from flask_socketio import SocketIO
 
app = Flask(__name__)
socketio = SocketIO(app)
 
@app.route('/')
def index_chat():
    return render_template('index_chat.html')
 
@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    socketio.emit('message', data)
 
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000, debug=True)
