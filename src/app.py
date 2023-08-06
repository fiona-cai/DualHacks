from setup import app, socket_app
from controllers.matches_controller import matches_blueprint
from controllers.general_controller import general_blueprint
from networking import Sever
import time

app.register_blueprint(matches_blueprint, url_prefix="/matches")
app.register_blueprint(general_blueprint)

server = Sever("192.168.0.16", 5000, app, socket_app)

if __name__ == '__main__':
    server.run_server()
    while True:
        time.sleep(1000)
