from setup import app
from controllers.matches_controller import matches_blueprint
from controllers.general_controller import general_blueprint

app.register_blueprint(matches_blueprint, url_prefix="/matches")
app.register_blueprint(general_blueprint)

if __name__ == '__main__':
    app.run(debug=False)
