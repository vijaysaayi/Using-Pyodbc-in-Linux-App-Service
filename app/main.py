import json , os , jwt , requests
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from flask import Flask, render_template, request, session , flash, redirect, url_for , jsonify

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/headers')
def print_headers():
    return "Max Content Length : " + str(request.max_content_length ) +"<br> <br>" + " Headers : <br> "+ str(request.headers) 

def decode_jwt(app_id,access_token):
    token_header = jwt.get_unverified_header(access_token)

    res = requests.get('https://login.microsoftonline.com/common/.well-known/openid-configuration')
    jwk_uri = res.json()['jwks_uri']
    res = requests.get(jwk_uri)
    jwk_keys = res.json()
    x5c = None
    # Iterate JWK keys and extract matching x5c chain
    for key in jwk_keys['keys']:
        if key['kid'] == token_header['kid']:
            x5c = key['x5c']


    cert = ''.join([
        '-----BEGIN CERTIFICATE-----\n',
        x5c[0],
        '\n-----END CERTIFICATE-----\n',
    ])
    public_key =  load_pem_x509_certificate(cert.encode(), default_backend()).public_key()
    decoded_token =""
    try:
        decoded_token = jwt.decode(
            access_token,
            public_key,
            algorithms='RS256',
            audience=app_id,
        )

    except Exception:
        decoded_token ="Invalid Token"
    
    finally:
        return decoded_token

@app.route('/',methods=["GET","POST"])
def index():
    if(os.environ['WEBSITE_AUTH_ENABLED'] == "False"):
        return render_template("noAuth.html")
    else:
        objects = {
            "has_exception" : False,
            "user_info" : {},
            "app_info" : {},
            "token_info" : {}
        }

        try:
            # session info
            s = requests.session()
            
            objects["token_info"]["ID Token"]      = request.headers.get('X-MS-TOKEN-AAD-ID-TOKEN', "NULL")
            objects["token_info"]["Access Token"]  = request.headers.get('X-MS-TOKEN-AAD-ACCESS-TOKEN', "NULL")
            objects["token_info"]["Refresh Token"] = request.headers.get('X-MS-TOKEN-AAD-REFRESH-TOKEN', "NULL")
            objects["token_info"]["Expires on"]    = request.headers.get('X-MS-TOKEN-AAD-EXPIRES-ON', "NULL")
            
            objects["token_info"]["Decoded Token"] = decode_jwt(os.environ['WEBSITE_AUTH_CLIENT_ID'],objects["token_info"]['ID Token']) 

            objects["app_info"]["name"]            = os.environ['WEBSITE_SITE_NAME'] or "NULL"
            objects["app_info"]["cookies"]         = request.cookies

            objects["user_info"]["X-MS-CLIENT-PRINCIPAL-NAME"] = request.headers.get('X-MS-CLIENT-PRINCIPAL-NAME', None)
            objects["user_info"]["X-MS-CLIENT-PRINCIPAL-ID"]   = request.headers.get('X-MS-CLIENT-PRINCIPAL-ID', None) 
            objects["user_info"]["X-MS-CLIENT-DISPLAY-NAME"]   = request.headers.get('X-MS-CLIENT-DISPLAY-NAME', None) 

            if request.method == "POST":
                res = s.get("https://"+os.environ['WEBSITE_SITE_NAME']+'.azurewebsites.net/.auth/refresh',timeout=5,cookies=request.cookies,headers=request.headers)
                objects["app_info"]["Status Code"] = res.status_code
        
        except Exception as e:
            objects.has_exception = True
            objects["app_info"]["Exception"] = e 
        
        finally:
            return render_template("TokenDetails.html", objects=objects)
            
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
