from flask import Flask, send_from_directory, request, jsonify
from download import download_blueprint
from KRAFT.main import craft_blueprint
from form_generator_facade import FormGenerator
from flask_cors import CORS
import json

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)

app.register_blueprint(download_blueprint)
app.register_blueprint(craft_blueprint)

# how could I turn /makeintcopies and /makedivcopies into one function that fills a variable with the passed string of the form type?
# lets use a dictionary to map the string to the form type
# then we can use the form type to load the necessary files and call the necessary functions
form_type_map = {
    'INT': 'int1099',
    'DIV' : 'div1099',
    'SA': 'sa1099',
    'Q': 'q1099',
    'NEC': 'nec1099',
    'K1065K1': '1065k1',
    '1120SK1': '1120sk1',
    'MIS': 'misc1099',
    'MISC': 'misc1099',
    'CON1099': 'con1099',
    'CONV2': 'con1099v2',
}

@app.route('/makecopies', methods=['POST'])
def make_copies():
    form_type_string = request.json['form_type']
    print(f"form_type_string: {form_type_string}")
    form_type = form_type_map[form_type_string]
    form_generator = FormGenerator(form_type)
    print(f"form_generator: {form_generator}")
    result = form_generator.generate_forms()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5174)
    
    # push for public
