# helper functions for file operations
import os

mime_types = {
    'csv': 'text/csv',
    'json': 'application/json',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'mp3': 'audio/mpeg',
    }

def get_mime_type(file_path):
    ext = file_path.split('.')[-1]
    return mime_types.get(ext, 'application/octet-stream')

def is_file_exists(file_path):
    allowed_extensions = list(mime_types.keys())
    ext = file_path.split('.')[-1]
    return os.path.exists(file_path)

def upload_file(file, file_path):
    upload_path = os.path.join('static', 'uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    file_path = os.path.join(upload_path, file.filename)
    
