import os
from flask import Flask, request, redirect, make_response
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

app = Flask(__name__)

def prepare_flask_request(req):
    url_data = req.url
    return {
        'https': 'on' if req.scheme == 'https' else 'off',
        'http_host': req.host,
        'server_port': req.environ.get('SERVER_PORT'),
        'script_name': req.path,
        'get_data': req.args.copy(),
        'post_data': req.form.copy()
    }

def init_saml_auth(req):
    return OneLogin_Saml2_Auth(
        prepare_flask_request(req),
        custom_base_path=os.path.join(os.path.dirname(__file__), 'saml')
    )

@app.route('/')
def index():
    return '<a href="/login">SSO ile Giriş Yap</a>'

@app.route('/login')
def login():
    auth = init_saml_auth(request)
    return redirect(auth.login())

@app.route('/acs', methods=['POST'])
def acs():
    auth = init_saml_auth(request)
    auth.process_response()
    errors = auth.get_errors()

    if errors:
        return f"Hata: {errors}", 400

    if not auth.is_authenticated():
        return "Kimlik doğrulama başarısız", 401

    user_data = auth.get_attributes()
    return f"Hoş geldin {auth.get_nameid()}<br>Attributes: {user_data}"

@app.route('/metadata')
def metadata():
    auth = init_saml_auth(request)
    settings = auth.get_settings()
    metadata_str = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata_str)
    if len(errors) > 0:
        return f"Hatalar: {errors}", 500
    response = make_response(metadata_str, 200)
    response.headers['Content-Type'] = 'text/xml'
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
