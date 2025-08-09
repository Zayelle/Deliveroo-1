# app/routes/email_routes.py
from flask import Blueprint, request, jsonify
from app.utils.email_utils import send_email

email_bp = Blueprint('email', __name__)

@email_bp.route('/send', methods=['POST'])
def send_email_route():
    data = request.get_json()
    to_email = data.get('to_email')
    subject = data.get('subject')
    content = data.get('content')

    result, status_code = send_email(to_email, subject, content)
    return jsonify(result), status_code
