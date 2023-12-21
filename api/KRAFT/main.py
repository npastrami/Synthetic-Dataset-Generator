from flask import Flask
from KRAFT.FeedOCR import craft_blueprint

app = Flask(__name__)
app.register_blueprint(craft_blueprint)

if __name__ == '__main__':
    app.run(debug=True)