from flask_mail import Mail


def mail_config(app):
    """use service such as mailtrap.io to get your own details!

    Note that mailtrap literally traps the mail for testing purposes!
    Don't panic that the email doesn't get the end recipient if using this service.
    The email will arrive in your mailtrap inbox, stating the intended recipient address.

    If you want to use a 'real' account for this, don't choose Gmail as it has
    security features that need to be turned off to allow this functionality.
    """
    app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '9e1b4547782291'
    app.config['MAIL_PASSWORD'] = '2274231c2ae413'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    return Mail(app)
