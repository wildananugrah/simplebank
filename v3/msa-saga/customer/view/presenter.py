from flask import jsonify
from datetime import datetime

def detail(data, start, status_code):
    
    data = {
        'timestamp' : str(datetime.now() - start),
        'data' : data,
        'status_code': status_code
    }

    return jsonify(data), status_code