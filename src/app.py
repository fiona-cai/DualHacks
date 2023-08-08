from setup import app, socket_app, server
from controllers.matches_controller import matches_blueprint
from controllers.general_controller import general_blueprint
import controllers.game_socket_controller

app.register_blueprint(matches_blueprint, url_prefix="/matches")
app.register_blueprint(general_blueprint)

if __name__ == '__main__':
    server.run_server()
