import os
from flask import Flask, request, redirect, make_response, render_template, session
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Rastgele bir key üretir

def prepare_flask_request(req): # Flask isteğini SAML için uygun hale getirir
    url_data = req.url
    return {
        'https': 'on' if req.scheme == 'https' else 'off',
        'http_host': req.host,
        'server_port': req.environ.get('SERVER_PORT'),
        'script_name': req.path,
        'get_data': req.args.copy(),
        'post_data': req.form.copy()
    }

def init_saml_auth(req): # SAML oturumunu başlatır
    return OneLogin_Saml2_Auth(
        prepare_flask_request(req),
        custom_base_path=os.path.join(os.path.dirname(__file__), 'saml')
    )

@app.route('/')
def index():
    return render_template("index.html", logged_in=('samlUserdata' in session))

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

    session['samlUserdata'] = auth.get_attributes()
    session['samlNameId'] = auth.get_nameid()
    session['samlSessionIndex'] = auth.get_session_index()

    return render_template(
        "index.html",
        logged_in=True,
        user_data=session['samlUserdata'],
        auth=session['samlNameId']
    )

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

@app.route('/logout')
def logout():
    auth = init_saml_auth(request)
    name_id = session.get('samlNameId')
    session_index = session.get('samlSessionIndex')
    return redirect(auth.logout(
        name_id=name_id,
        session_index=session_index,
        return_to="http://localhost:5000/"
    ))

@app.route('/sls', methods=['GET', 'POST'])
def sls():
    if 'SAMLRequest' not in request.args and 'SAMLResponse' not in request.args:
        # Direkt girilmiş, SAML isteği yok
        session.clear()
        return redirect('/')
    
    auth = init_saml_auth(request)
    url = auth.process_slo(delete_session_cb=lambda: session.clear())
    errors = auth.get_errors()

    if errors:
        return f"Hata: {errors}", 400

    return redirect(url or '/')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
