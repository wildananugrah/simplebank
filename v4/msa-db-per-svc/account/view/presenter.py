from flask import jsonify
from datetime import datetime

def view_detail(data, start, status_code = 200):
    
    data = {
        'timestamp' : str(datetime.now() - start),
        'data' : data,
        'status_code': status_code
    }

    return jsonify(data), status_code