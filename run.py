from api.main.home import app
import sys

sys.dont_write_bytecode = True

if __name__ == '__main__':
    
    app.run(debug=True, port=8080)
