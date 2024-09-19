from pyscript import document, window
from pyodide.ffi import create_proxy, to_js
import asyncio
from js import eval, File, Uint8Array

import pickle
import base64
import html
import builtins
import io
import pickle
import os

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *

from dataclasses import dataclass
from functools import partial
from collections import defaultdict


def set_loading_status(status: str):
    document.getElementById("loading-status").innerHTML = status


set_loading_status("Initializing web app...")

socket = eval("io()")


unsafe_builtins = {
    "__loader__",
    "__spec__",
    "__build_class__",
    "__import__",
    "eval",
    "exec",
    "format",
    "getattr",
    "globals",
    "hasattr",
    "input",
    "iter",
    "aiter",
    "locals",
    "next",
    "anext",
    "print",
    "open",
    "setattr",
    "sorted",
    "vars",
    "memoryview",
    "bytearray",
    "classmethod",
    "property",
    "staticmethod",
    "super",
    "type",
}


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe classes from builtins.
        if module == "builtins" and name not in unsafe_builtins:
            return getattr(builtins, name)

        if module == "__main__" and name == "Message":
            return Message

        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" % (module, name))


def restricted_loads(s):
    return RestrictedUnpickler(io.BytesIO(s)).load()


def clear_chat():
    document.getElementById("message-container").innerHTML = ""
    document.getElementById("message-recipient").innerHTML = ""


def load_chat(username):
    clear_chat()
    document.getElementById("message-recipient").innerHTML = username


def open_chat_button_click(event):
    event.preventDefault()
    new_user = document.getElementById("new-chat-username").value
    document.getElementById("new-chat-username").value = ""
    load_chat(new_user)


document.getElementById("open-chat").addEventListener(
    "click", create_proxy(open_chat_button_click)
)

os.makedirs("profiles", exist_ok=True)

def profile_picture_click(event):
    event.preventDefault()
    document.getElementById("file-input").click()


document.getElementById("profile-picture").addEventListener(
    "click", create_proxy(profile_picture_click)
)


async def upload_profile_picture(event):
    file_list = event.target.files
    file = file_list.item(0)
    file_name = file.name
    buffer = bytearray(Uint8Array.new(await file.arrayBuffer()))

    if len(buffer) > 500_000:
        window.alert("File too large")
        return

    buffer = base64.b64encode(buffer).decode()
    socket.emit(
        "upload_profile_picture", to_js({"filename": file_name, "buffer": buffer})
    )


document.getElementById("file-input").addEventListener(
    "change", create_proxy(upload_profile_picture)
)


profile_update_queues = defaultdict(list)


def get_cache_blob(filename):
    cache_path = os.path.join("profiles", filename)
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            file_data = f.read()
            image_file = File.new([Uint8Array.new(file_data)], filename)
            return window.URL.createObjectURL(image_file)
    return None


def display_own_profile_picture():
    filename = document.getElementById("profile-picture").dataset.profileKey
    cache_path = os.path.join("profiles", filename)
    blob = get_cache_blob(filename)
    if blob:
        document.getElementById("profile-picture").src = blob
    else:
        socket.emit("request_profile_picture", to_js({"filename": filename}))


def request_profile_picture_handler(data):
    if data.status == "success":
        filename = data.filename
        file_data = base64.b64decode(data.buffer)
        cache_path = os.path.join("profiles", filename)
               
        with open(cache_path, "wb") as f:
            f.write(file_data)

        assert get_cache_blob(filename) is not None, "Failed to cache profile picture"
        blob = get_cache_blob(filename)
        owner = filename.split("_")[0]
        if owner == document.getElementById("username").innerHTML:
            display_own_profile_picture()
        else:
            # check callback queue for any objects that need to be updated
            if owner in profile_update_queues:
                while profile_update_queues[owner]:
                    profile_update_queues[owner].pop()(blob)
                del profile_update_queues[owner]

            # update the current chat if the profile picture is for the current chat
            if owner == document.getElementById("message-recipient").innerHTML:
                document.getElementById("recipient-profile-picture").src = blob

            # update the sidebar if the profile picture is for a user in the sidebar
            panel = document.getElementById(f"panel-{owner}-container")
            if panel:
                panel.children[0].children[0].src = blob
    else:
        print("Failed to request profile picture")


socket.on("request_profile_picture", create_proxy(request_profile_picture_handler))


def update_profile_picture_handler(data):
    if data.status == "success":
        document.getElementById("profile-picture").dataset.profileKey = data.filename
        display_own_profile_picture()

    else:
        window.alert("Failed to upload profile picture")


socket.on("upload_profile_picture", create_proxy(update_profile_picture_handler))


@dataclass
class Message:
    content: str
    sender: str
    recipient: str
    profile_picture: str = "default.jpg"


def send_message_button_click(event):
    event.preventDefault()
    if (
        not document.getElementById("message-recipient").innerHTML
        or not document.getElementById("username").innerHTML
        or not document.getElementById("message-content").value
    ):
        return

    content = document.getElementById("message-content").value
    sender = document.getElementById("username").innerHTML
    recipient = document.getElementById("message-recipient").innerHTML
    profile_picture = document.getElementById("profile-picture").dataset.profileKey

    message = Message(content, sender, recipient, profile_picture)
    message_data = base64.b64encode(pickle.dumps(message)).decode()
    socket.emit("send_message", to_js({"recipient": recipient, "data": message_data}))
    display_new_message(message, sent_myself=True)
    document.getElementById("message-content").value = ""


document.getElementById("submit").addEventListener(
    "click", create_proxy(send_message_button_click)
)

from pyscript.web import dom
from pyscript.web.elements import Element, div, span, img, a


def auto_loading_image(message):
    blob = get_cache_blob(message.profile_picture)
    if blob:
        profile_img = img(classes=["aspect-square", "h-full", "w-full"], src=blob)
    else:
        profile_img = img(
            classes=["aspect-square", "h-full", "w-full"], src="/static/default.jpg"
        )

        def _update(profile, blob):
            profile.src = blob

        profile_update_queues[message.sender].append(partial(_update, profile_img))
        socket.emit(
            "request_profile_picture", to_js({"filename": message.profile_picture})
        )

    return profile_img


def update_sidebar_last_message(message: Message, sent_myself=False):
    if sent_myself:
        username = html.escape(message.recipient)
    else:
        username = html.escape(message.sender)
    content = html.escape(message.content)

    sidebar_container = document.getElementById(f"panel-{username}-container")
    if sidebar_container:
        if not sent_myself:
            # only update the profile picture if the message send by other
            sidebar_container.children[0].innerHTML = ""
            span_el = span(dom_element=sidebar_container.children[0])
            span_el.append(auto_loading_image(message))

        sidebar_container.children[1].children[0].innerHTML = username
        sidebar_container.children[1].children[1].innerHTML = content
    else:
        if sent_myself:
            profile_img = img(
                classes=["aspect-square", "h-full", "w-full"], src="/static/default.jpg"
            )
        else:
            profile_img = auto_loading_image(message)

        sidebar_element = a(
            span(
                profile_img,
                classes=[
                    "relative",
                    "flex",
                    "shrink-0",
                    "overflow-hidden",
                    "rounded-full",
                    "h-10",
                    "w-10",
                ],
            ),
            div(
                div(username, classes=["font-medium", "panel-username"]),
                div(
                    content,
                    classes=[
                        "text-sm",
                        "text-muted-foreground",
                        "text-muted",
                        "panel-content",
                        "truncate",
                    ],
                ),
                classes=["flex-1"],
                id=f"panel-{username}",
            ),
            href="#",
            classes=[
                "flex",
                "items-center",
                "gap-3",
                "rounded-md",
                "bg-muted",
                "p-2",
                "transition-colors",
                "hover:bg-muted-foreground",
                "bg-card-foreground",
                "hover:bg-muted",
            ],
            id=f"panel-{username}-container",
        )
        active_messages_container = dom["#active-messages"][0]
        active_messages_container.append(sidebar_element)

        def chat_clicked(sender, event):
            event.preventDefault()
            load_chat(sender)

        document.getElementById(f"panel-{username}-container").addEventListener(
            "click", create_proxy(partial(chat_clicked, username))
        )


def display_new_message(message: Message, sent_myself=False):
    message.content = html.escape(message.content)
    message.sender = html.escape(message.sender)

    if (
        sent_myself
        or message.sender == document.getElementById("message-recipient").innerHTML
    ):
        if sent_myself:
            message_div = div(
                div(
                    div("You", classes=["font-medium"]),
                    div(
                        message.content,
                        classes=[
                            "max-w-72",
                            "break-words",
                        ],
                    ),
                    classes=[
                        "grid",
                        "gap-1",
                        "rounded-lg",
                        "bg-primary",
                        "p-3",
                        "text-primary-foreground",
                    ],
                ),
                span(
                    auto_loading_image(message),
                    classes=[
                        "relative",
                        "flex",
                        "shrink-0",
                        "overflow-hidden",
                        "rounded-full",
                        "h-10",
                        "w-10",
                    ],
                ),
                classes=["flex", "items-start", "gap-4", "justify-end"],
            )
        else:
            message_div = div(
                span(
                    auto_loading_image(message),
                    classes=[
                        "relative",
                        "flex",
                        "shrink-0",
                        "overflow-hidden",
                        "rounded-full",
                        "h-10",
                        "w-10",
                    ],
                ),
                div(
                    div(message.sender, classes=["font-medium"]),
                    div(
                        message.content,
                        classes=[
                            "max-w-72",
                            "break-words",
                        ],
                    ),
                    classes=[
                        "grid",
                        "gap-1",
                        "rounded-lg",
                        "bg-muted",
                        "p-3",
                        "bg-card-foreground",
                        "text-card-foreground",
                    ],
                ),
                classes=["flex", "items-start", "gap-4"],
            )
        message_container = dom["#message-container"][0]
        message_container.append(message_div)
        eval("document.getElementById('message-container').scrollIntoView(false)")

    update_sidebar_last_message(message, sent_myself)


def load_message(data) -> Message | None:
    try:
        message: Message = restricted_loads(data)
    except Exception as e:
        message = None

    return message


def recieve_message_handler(data):
    try:
        message_data = base64.b64decode(data.data)
        message = load_message(message_data)
        if message:
            display_new_message(message)
    except Exception as e:
        pass


socket.on("recieve_message", create_proxy(recieve_message_handler))


def login(username, password):
    socket.emit("login", to_js({"username": username, "password": password}))


def login_handler(data):
    if data.status == "success":
        username_div = div(
            data.username,
            classes=[
                "font-medium",
            ],
            id="username",
        )      

        logged_in_div = div(
            "Logged in",
            classes=[
                "text-sm",
                "text-muted-foreground",
                "text-muted"
            ],
        )
        profile_container = dom["#profile-container"][0]
        profile_container.append(username_div)
        profile_container.append(logged_in_div)
        
        load_chat(data.username)
        return
    window.alert("Failed to login")


socket.on("login", create_proxy(login_handler))


def register():
    socket.emit("register", to_js({}))


def register_handler(data):
    if data.status == "success":
        if data.username and data.password:
            login(data.username, data.password)
            page_ready()
            return
    window.alert("Failed to register")


socket.on("register", create_proxy(register_handler))

set_loading_status("Registering account...")
register()


def page_ready():
    set_loading_status("Ready!")
    document.getElementById("loadingModal").classList.add("hidden")
