from app import google_login


def after_init(app):
    @app.context_processor
    def inject_auth_url():
        return dict(authorization_url=google_login.authorization_url())
