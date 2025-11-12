# app.py # Main Flask application and API endpoints

from flask import Flask, request, jsonify
from flask_cors import CORS
from validator import validate_request_payload, validate_code
from runner import execute_code

app = Flask(__name__)

# Configure CORS to allow requests from your frontend's domain.
# In a production environment, you would restrict this to your specific frontend URL.
# For development and Render's free tier, '*' is often acceptable.
CORS(app)

@app.route('/execute', methods=['POST'])
def execute():
    """
    API endpoint to receive and execute Python code.
    Expects a JSON payload with 'code' and 'data' keys.
    """
    # 1. Get and validate the request payload
    payload = request.get_json()
    payload_errors = validate_request_payload(payload)
    if payload_errors:
        return jsonify({'status': 'error', 'message': '. '.join(payload_errors)}), 400

    code_to_run = payload['code']
    sheet_data = payload['data']

    # 2. Validate the Python code for security
    code_validation_errors = validate_code(code_to_run)
    if code_validation_errors:
        error_message = "Security validation failed: " + '. '.join(code_validation_errors)
        return jsonify({'status': 'error', 'message': error_message}), 400

    # 3. If validation passes, execute the code
    result = execute_code(code_to_run, sheet_data)

    # 4. Return the result
    if result['status'] == 'success':
        return jsonify(result), 200
    else:
        # An execution error occurred in the runner
        return jsonify(result), 500

@app.route('/')
def health_check():
    """
    A simple health check endpoint to confirm the server is running.
    """
    return "Python Code Execution Backend is running.", 200

if __name__ == '__main__':
    # This block is for local development only.
    # Gunicorn will be used to run the app in production on Render.
    app.run(debug=True, port=5001)
