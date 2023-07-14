from flask import Flask
from app_container.controllers.data_source import data_source_controller
from app_container.controllers.query import query_controller
import os

os.environ['PATH'] = 'C://Python310/python'
os.environ['PATH'] = 'C://Python310/Scripts/pip'


app = Flask(__name__)


app.register_blueprint(data_source_controller, url_prefix='/data-source')
app.register_blueprint(query_controller, url_prefix='/query')


if __name__ == '__main__':
    app.run()
