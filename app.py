# app.py # Main Flask application and API endpoints

from flask import Flask, request, jsonify
from flask_cors import CORS
from validator import validate_request_payload, validate_code
from runner import execute_code

app = Flask(__name__)

# Configure CORS to allow requests from any origin (for Render free tier)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute():
    """
    API endpoint to receive and execute Python code.
    Expects a JSON payload with 'code' and 'data' keys.
    """
    payload = request.get_json()
    payload_errors = validate_request_payload(payload)
    if payload_errors:
        return jsonify({'status': 'error', 'message': '. '.join(payload_errors)}), 400

    code_to_run = payload['code']
    sheet_data = payload['data']

    code_validation_errors = validate_code(code_to_run)
    if code_validation_errors:
        error_message = "Security validation failed: " + '. '.join(code_validation_errors)
        return jsonify({'status': 'error', 'message': error_message}), 400

    result = execute_code(code_to_run, sheet_data)

    if result['status'] == 'success':
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@app.route('/')
def health_check():
    return "Python Code Execution Backend is running.", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

