import os

from api.server_api import app

if __name__ == '__main__':
    app.run(debug=bool(os.getenv("DEBUG_MODE", default=False)))
