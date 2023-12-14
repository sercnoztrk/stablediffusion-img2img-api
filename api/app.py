from flask import Flask
from flask import request, send_file
from werkzeug.utils import secure_filename
import os
from request_id import RequestId

app = Flask(__name__)
RequestId(app)

def modify_path():
    import sys
    sd_path = os.path.join(os.path.abspath("./"), "sd")
    banner_path = os.path.join(os.path.abspath("./"), "banner")
    sys.path.append(sd_path)
    sys.path.append(banner_path)

def allowed_file(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and extension == 'png'

def check_file(request, prop):
    if prop not in request.files:
        print('\nNo file part on request')
        return False
    file = request.files[prop]
    if file:
        if not (file.filename and file.filename.strip()):
            print('\nNo selected file')
            return False
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
#           file.save(os.path.join('', filename))
            return True
        else:
            print('\nFile type not allowed')
            return False
    else:
        print("\nInput image missing!")
        return False

def check_hex(request):
    if 'Renk' not in request.form:
        print("\nHex code parameter missing")
        return False
    hex = request.form['Renk'].strip()
    return hex[0] == '#' and len(hex) == 7

def convert_hex_to_names(hex_input):
    from scipy.spatial import KDTree
    from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(hex_to_rgb(hex_input))
    return names[index]

def run_sd(request):
    import pipeline
    id = request.environ.get('REQUEST_ID', '')
    path = os.path.join(os.path.dirname(__file__), "output", id + ".png")
    renk = convert_hex_to_names(request.form['Renk'])
    prompt = request.form['Prompt'] + ", ((use color " + renk + "))"
    images = pipeline.run(request.files['Image'], prompt)
    images[0].save(path)
    del pipeline
    del images
    return path

def run_template_create(request):       # (41,88,63)
        import template
        id = request.environ.get('REQUEST_ID', '')
        path = os.path.join(os.path.dirname(__file__), "output", id + ".png")
        banner = template.create(request.files['Image'], request.files['Logo'], request.form['Renk'], request.form['Punchline'], request.form['Button'])
        banner.save(path)
        return path

modify_path()

@app.route("/api/generate-sd-image", methods=['GET', 'POST'])
def generate_sd_image():
    if request.method == 'POST':
        if not check_file(request, 'Image'):
            return "Invalid input file or file is missing!"
        if not check_hex(request):
            return "Invalid HEX!"
        if 'Renk' not in request.form:
            return "'Renk' input is missing"
        file_path = run_sd(request)
        return send_file(file_path, mimetype="image/png")
    else:
        return "GET Request"
    
@app.route("/api/create-banner", methods=['GET', 'POST'])
def create_banner():
    if request.method == 'POST':
        if not (check_file(request, 'Image') and check_file(request, 'Logo')):
            return 'Invalid input file or file is missing!'
        if not check_hex(request):
            return 'Invalid HEX!'
        file_path = run_template_create(request)
        return send_file(file_path, mimetype="image/png")
    else:
        return "GET Request"