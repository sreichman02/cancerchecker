from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from matplotlib import image
from .models import Note
from . import db
import json
from werkzeug.utils import secure_filename
import cv2
from .deeplearn.Network import Network
from PIL import Image

views = Blueprint('views', __name__)
network = Network()


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        f = request.files['image']
        f.save(secure_filename(f.filename))
        if f:
            flash("input recieved", category = 1)
            img = cv2.imread(f.filename, cv2.IMREAD_COLOR)        
            pred_val = network.prediction(img)
            return render_template("return.html", user=current_user, img_val = pred_val)
        else:
            flash("input not recieved", category = 0)   
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})