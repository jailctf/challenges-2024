from flask import Flask, request
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import base64
import imghdr
import os

app = Flask(__name__)

UPLOAD_FOLDER = "images/"
app.config["SECRET_KEY"] = os.urandom(32).hex()
socketio = SocketIO(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
sessions = {}
users = {}
login_details = {}


def set_user_session(username, id):
    sessions[username] = id
    users[id] = username


def remove_user(username):
    try:
        id = sessions[username]
        del sessions[username]
        del users[id]
        return True
    except:
        return False


def remove_session(id):
    try:
        username = users[id]
        del sessions[username]
        del users[id]
        print(f"[+] Removed session for {username}  ")
        return True
    except:
        return False


def verify_login(username, password):
    try:
        return login_details[username] == password
    except:
        return False


@socketio.on("login")
def login(data):
    username = data["username"]
    password = data["password"]

    print(f"[+] Attempting to login with {username} and {password}")
    if verify_login(username, password):
        print(f"[+] Login successful for {username}")
        session = request.sid
        set_user_session(username, session)
        emit("login", {"status": "success", "username": username})
    else:
        print(f"[+] Login failed with credentials {username} and {password}")
        emit("login", {"status": "failure"})


@socketio.on("register")
def register(data):
    from account import generate_username, generate_password

    while True:
        username = generate_username()
        if username not in sessions:
            break

    password = generate_password()
    login_details[username] = password

    set_user_session(username, request.sid)

    emit("register", {"status": "success", "username": username, "password": password})


@socketio.on("disconnect")
def disconnect():
    remove_session(request.sid)


@socketio.on("send_message")
def send_message(data):
    recipient = data["recipient"]
    raw_data = data["data"]

    session = request.sid
    if session in users and recipient in sessions:
        print(f"[+] Sending message from {users[request.sid]} to {recipient}")
        emit("recieve_message", {"data": raw_data}, to=sessions[recipient])
    else:
        emit("recieve_message", {"status": "failure"})


@socketio.on("upload_profile_picture")
def upload_profile_picture(data):
    if request.sid not in users:
        emit("upload_profile_picture", {"status": "failure", "error": "Not logged in"})
        return

    try:
        file_data = data["buffer"]
        filename = data["filename"]

        file_data = base64.b64decode(file_data)
        assert len(file_data) <= 500_000

        filename = f"{users[request.sid]}_{secure_filename(filename)}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb+") as f:
            f.write(file_data)

        print(f"[+] Uploaded profile picture for {users[request.sid]}")

        if imghdr.what(file_path):
            emit("upload_profile_picture", {"status": "success", "filename": filename})
        else:
            os.remove(file_path)
            emit(
                "upload_profile_picture",
                {"status": "failure", "error": "Invalid image file"},
            )
    except Exception as e:
        print(e)
        emit(
            "upload_profile_picture",
            {"status": "failure", "error": f"Failed to upload image ({e})"},
        )


@socketio.on("request_profile_picture")
def request_profile_picture(data):
    if request.sid not in users:
        emit("request_profile_picture", {"status": "failure", "error": "Not logged in"})
        return

    try:
        filename = secure_filename(data["filename"])
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode()
                emit(
                    "request_profile_picture",
                    {"status": "success", "buffer": file_data, "filename": filename},
                )
        else:
            emit(
                "request_profile_picture",
                {"status": "failure", "error": "Profile picture not found"},
            )
    except Exception as e:
        emit(
            "request_profile_picture",
            {"status": "failure", "error": f"Failed to request image ({e})"},
        )


@app.route("/")
def index():
    return open("index.html").read()


@app.route("/view")
def view():
    return open("view.html").read()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
