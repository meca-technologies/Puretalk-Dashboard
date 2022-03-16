from app import app, logger
import config

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=config.debug)