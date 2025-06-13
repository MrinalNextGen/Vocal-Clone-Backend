from flask import jsonify
from functools import wraps
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def success_response(data=None, message="Success", status_code=200):
    """Create a standardized success response"""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400, errors=None):
    """Create a standardized error response"""
    response = {
        "success": False,
        "message": message
    }
    if errors:
        response["errors"] = errors
    
    return jsonify(response), status_code

def log_request(f):
    """Decorator to log API requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.info(f"API Request: {f.__name__}")
        try:
            result = f(*args, **kwargs)
            logger.info(f"API Response: {f.__name__} - Success")
            return result
        except Exception as e:
            logger.error(f"API Error: {f.__name__} - {str(e)}")
            return error_response(f"Internal server error: {str(e)}", 500)
    return decorated_function

def validate_json(required_fields=None):
    """Decorator to validate JSON request data"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            if not request.is_json:
                return error_response("Request must be JSON", 400)
            
            data = request.get_json()
            if not data:
                return error_response("No JSON data provided", 400)
            
            if required_fields:
                missing_fields = []
                for field in required_fields:
                    if field not in data or not str(data[field]).strip():
                        missing_fields.append(field)
                
                if missing_fields:
                    return error_response(
                        f"Missing required fields: {', '.join(missing_fields)}", 
                        400
                    )
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
