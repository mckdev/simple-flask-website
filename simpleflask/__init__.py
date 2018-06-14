import os

from flask import Flask, render_template

def create_app(test_config=None):
    # Create and configure the app.
    app = Flask(__name__, instance_relative_config=True)

    # Set default app config.
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    # Override default config with values from file or passed test config.
    if test_config is None:
        # Load config file, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import views
    app.register_blueprint(views.bp)
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/add', endpoint='add')
    app.add_url_rule('/<int:id>/edit', endpoint='edit')
    app.add_url_rule('/<int:id>/delete', endpoint='delete')

    from . import db
    db.init_app(app)

    return app
