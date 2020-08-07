# from app import app

# # app.run(debug=True)

from app import app
from flask_session.__init__ import Session
sess = Session()


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
    