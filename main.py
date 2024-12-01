import os

from flask import Flask

from assistant import create_app

app = Flask(__name__, instance_relative_config=True)

if __name__ == "__main__":
    create_app(app)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))