from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message

@app.route("/post_message",methods=["POST"])
def post_message():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "send_id": request.form['send_id'],
        "receiver_id": request.form['receiver_id'],
        "posts": request.form['posts']
    }
    Message.save(data)
    return redirect('/dashboard')

@app.route("/destroy/message/<int:id>")
def destroy_message(id):
    data = {
        "id": id
    }
    Message.destroy(data)
    return redirect('/dashboard')