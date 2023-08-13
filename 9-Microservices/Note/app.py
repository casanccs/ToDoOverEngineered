from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@dbNote/main'
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    text = db.Column(db.String(200))

@app.route('/')
def index():
    return 'Hello'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')