from flask import render_template, request, redirect, url_for, flash, jsonify, Blueprint

main_bp = Blueprint('main_bp', __name__, template_folder='../templates/Main_Page')

@main_bp.route("/")
def index():
    return render_template('index.html')
