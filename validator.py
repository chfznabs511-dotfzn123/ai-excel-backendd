# validator.py # For validating user inputs or code

import ast

# A list of modules/functions that are not allowed to be imported or used.
# This is a critical security measure to create a sandboxed environment.
FORBIDDEN_BUILTINS = [
    'open',
    'eval',
    'exec',
    '__import__',
    'globals',
    'locals',
    'getattr',
    'setattr',
    'delattr'
]

FORBIDDEN_IMPORTS = [
    'os',
    'sys',
    'subprocess',
    'shutil',
    'socket',
    'urllib',
    'ftplib',
    'telnetlib'
]

class CodeValidator(ast.NodeVisitor):
    """
    AST visitor to check for forbidden nodes in the Python code.
    Using an Abstract Syntax Tree (AST) is much more secure than simple string checking.
    """
    def __init__(self):
        self.errors = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in FORBIDDEN_IMPORTS:
                self.errors.append(f"Forbidden module import: '{alias.name}' is not allowed.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in FORBIDDEN_IMPORTS:
            self.errors.append(f"Forbidden module import: '{node.module}' is not allowed.")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_BUILTINS:
            self.errors.append(f"Forbidden function call: '{node.func.id}()' is not allowed.")
        self.generic_visit(node)

def validate_code(code_string: str) -> list[str]:
    """
    Validates a string of Python code against security rules.

    Args:
        code_string: The Python code to validate.

    Returns:
        A list of error messages. An empty list means the code is valid.
    """
    try:
        tree = ast.parse(code_string)
        validator = CodeValidator()
        validator.visit(tree)
        return validator.errors
    except SyntaxError as e:
        return [f"Syntax Error: {e.msg} on line {e.lineno}"]
    except Exception as e:
        return [f"An unexpected validation error occurred: {str(e)}"]

def validate_request_payload(payload: dict) -> list[str]:
    """
    Validates the incoming JSON payload from the frontend.
    
    Args:
        payload: The request JSON data.

    Returns:
        A list of error messages. An empty list means the payload is valid.
    """
    errors = []
    if not isinstance(payload, dict):
        return ["Invalid request format: payload must be a JSON object."]
        
    if 'code' not in payload or not isinstance(payload['code'], str):
        errors.append("Missing or invalid 'code' field in request. It must be a string.")

    if 'data' not in payload or not isinstance(payload['data'], dict):
        errors.append("Missing or invalid 'data' field in request. It must be a dictionary of sheets.")

    return errors
