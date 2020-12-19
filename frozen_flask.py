from flask_frozen import Freezer
from hackermd.src import app

freezer = Freezer(app.app)

if __name__ == '__main__':
    freezer.freeze()