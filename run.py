from api.main.home import app
from api.config import Configurations
import sys

sys.dont_write_bytecode = True

app.config['SECRET_KEY'] == "ThisIsMySecretKey"

if __name__ == '__main__':
    config = Configurations()
    config.create_tables
    app.run(debug=True, port=8080)
