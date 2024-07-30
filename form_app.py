from flask import Flask, request, render_template, redirect, url_for, session
import requests
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def configure_form():
    return render_template('configure_form.html')

@app.route('/generate_form', methods=['POST'])
def generate_form():
    field_names = request.form.getlist('field_names')
    session['field_names'] = field_names
    return redirect(url_for('index'))

@app.route('/form')
def index():
    field_names = session.get('field_names', [])
    return render_template('form.html', field_names=field_names)

@app.route('/submit', methods=['POST'])
def submit():
    field_names = session.get('field_names', [])
    data = {field: request.form[field] for field in field_names}
    try:
        response = requests.post('http://localhost:5001/api/data', json=data)
        response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
        logging.debug('Data successfully sent to API')
        return redirect(url_for('index', success=True))
    except requests.exceptions.HTTPError as err:
        logging.error(f'HTTP error occurred: {err}')
        return render_template('form.html', error=f'HTTP error occurred: {err}', field_names=field_names)
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
        return render_template('form.html', error=f'An error occurred: {err}', field_names=field_names)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
