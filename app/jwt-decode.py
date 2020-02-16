import jwt
import requests
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

#app_id = '0c3f2778-2595-43dc-babb-5b4df385aedb'
#access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCIsImtpZCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCJ9.eyJhdWQiOiIwYzNmMjc3OC0yNTk1LTQzZGMtYmFiYi01YjRkZjM4NWFlZGIiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9lZjNjZWQ1Zi05MmUxLTRjOTMtODg0OS0xOGIwZmFkOGU2NWMvIiwiaWF0IjoxNTUwMzMwNTA5LCJuYmYiOjE1NTAzMzA1MDksImV4cCI6MTU1MDMzNDQwOSwiYWlvIjoiQVdRQW0vOEtBQUFBQWtsRGhnWUprRzVrMHd2QmxEZ3VYZE9wditsaWtSMjJLTm5SbHdBcHIyOHhVNmhKMGMvN3NtMzhhTTU4R2IvTGtZSk5JOC9lRk9VbDhUUzBtdVB6SktKRzVwNDlrV3RvWjA1KzZSSEs5amRtd1VGSGxOSkF4NUp0VW1IbXJmNW8iLCJhbXIiOlsicnNhIiwid2lhIl0sImVtYWlsIjoidmlzYWF5aXJAbWljcm9zb2Z0LmNvbSIsImZhbWlseV9uYW1lIjoiUiIsImdpdmVuX25hbWUiOiJ2aXNhYXlpckBtaWNyb3NvZnQuY29tIiwiZ3JvdXBzIjpbIjI1NTIxN2ExLTBlYmUtNDllZS1iYThmLWM5ZmM2ZTk5YTQxNSIsIjE5NzEzMDI5LWE2YzYtNDdhNC1hMGE1LTU0OWIxMjRiNTRkOSIsIjYzMjhmMmZiLTcxNDYtNDQyZS04ZmZiLWJmOWJlMjFkNjgxZCIsImMxM2M1OGRkLWI2ZDMtNDI5Ny1iYTg2LWY0MDBlMzY5N2Y2NCIsIjM1YjY2MTYxLTQ0MWUtNDI2ZS1hOWQzLWVhNDlkN2E0OTBlZCIsIjE1NWU5MDJiLTc2YzctNDQ3Mi1iMWRiLWZhNDc1OTM0Mjc0OSIsIjJmM2JhZWMyLThlMDYtNDY0OC04OGVmLWJlMzVlYzg5Y2E2YyIsImZmYTFmMTY0LTczMDgtNDQzNy04YmQzLWJjYmIwZDFlNzdmMiJdLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDcvIiwiaW5fY29ycCI6InRydWUiLCJpcGFkZHIiOiIxMDYuNTEuMjkuMzEiLCJuYW1lIjoidmlzYWF5aXJAbWljcm9zb2Z0LmNvbSBSIiwibm9uY2UiOiIwODg1MDlmMTJlMWI0NzJlOTcxNmRmZDUwOTcwMGU0OF8yMDE5MDIxNjE1MzE0NiIsIm9pZCI6IjEyMDNjMGExLTRlOGUtNDdmNi04MmMyLWMyODdlYjUwMWE4MyIsInN1YiI6IkdWMmlBalNQTEhIYTdKSXNWUXkxWTJFRzVSVUxKRXA3c0g2Z09CblFGWm8iLCJ0aWQiOiJlZjNjZWQ1Zi05MmUxLTRjOTMtODg0OS0xOGIwZmFkOGU2NWMiLCJ1bmlxdWVfbmFtZSI6InZpc2FheWlyQG1pY3Jvc29mdC5jb20iLCJ1dGkiOiJYdHUtMXZkR2VFV1Z6cGdaOExJUkFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyI2MmU5MDM5NC02OWY1LTQyMzctOTE5MC0wMTIxNzcxNDVlMTAiXX0.P9d_D_aJTo_Ja0KzwqMUVfwAwRaRiAwyjUD0A2J3tdIShF3RVuXS8tv8Dlzqt62cNBo6nzTaBvdsSCQd-WGPbUAWb_p6pKm5MjJ2cX0T9E12HqCcXZKwAUAf0Pkn21dZHt7qGSh5Ufv0_MjfFxpRyy-5gdVjyj9ytHIQYL-Z05k337zrf58sZvr7rUZNaulPZhUrFSAwQnJ-ULnW42YFR9O5dY1rUg-rRr6Xxd_iHmf21G8dmkqcf3A5obEja-Ym2VGZdPtVCFsLzHVbGHX47_IP9UjPirrgHnHnshouXwnz60F6II-7YGbYrVhiWvRLpF51_Bw74BjhjlyolPiLLQ'

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
    except Exception as e:
        decoded_token ="Inavlid Token"
    return decoded_token

#print(decode_jwt(app_id,access_token))
