from setup import app, socket_app, server
from controllers.matches_controller import matches_blueprint
from controllers.general_controller import general_blueprint
import time

app.register_blueprint(matches_blueprint, url_prefix="/matches")
app.register_blueprint(general_blueprint)

if __name__ == '__main__':
    app.debug = True
    server.run_server()
