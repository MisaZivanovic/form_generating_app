from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import logging

app = Flask(__name__)

# Configuration for Flask-Mail using Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_gmail_username'
app.config['MAIL_PASSWORD'] = 'gmail_app_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/data', methods=['POST'])
def api_data():
    if request.is_json:
        data = request.get_json()
        logging.debug(f'Received data: {data}')

        # Construct the email body dynamically
        email_body = "\n".join([f"{key.capitalize()}: {value}" for key, value in data.items()])

        # Send email
        try:
            msg = Message(
                subject="New Form Submission",
                sender=app.config['MAIL_USERNAME'],
                recipients=['recipient_email_address'],  # Replace with recipient email
                body=email_body
            )
            mail.send(msg)
            logging.debug('Email sent successfully')
            return jsonify({"message": "Data received and email sent"}), 200
        except Exception as e:
            logging.error(f'Failed to send email: {e}')
            return jsonify({"message": f"Failed to send email: {str(e)}"}), 500
    else:
        logging.error('Request is not JSON')
        return jsonify({"message": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(port=5001, debug=True)
