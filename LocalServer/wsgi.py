from app import app
from lsDatabase import *

if __name__ == "__main__":
    createDB()
    app.run()
