from functools import wraps
import jwt
import logging

logger = logging.getLogger(__name__)


def allow_cors(fn):
    @wraps(fn)
    def f(request):
        if request.method == 'OPTIONS':
            # Allows GET requests from any origin with the Content-Type
            # header and caches preflight response for an 3600s
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }

            return ('', 204, headers)
        else:
            headers = {
                'Access-Control-Allow-Origin': '*'
            }
            try:
                res = fn(request)
                if isinstance(res, tuple):
                    assert len(res) in [2, 3], "tuple response should have two or 3 elements."
                    if isinstance(res[-1], dict):
                        res[-1].update(headers)
                        return res
                    else:
                        return res + (headers,)
                else:
                    return res, headers
            except Exception:
                logging.exception("Internal error.")
                return ("Internal error", 500, headers)

    return f


from jwt import PyJWKClient

url = "https://www.googleapis.com/oauth2/v3/certs"
jwks_client = PyJWKClient(url)


def auth(allowed_users):

    def decorated(fn):
        @wraps(fn)
        def f(request):

            try:
                token = request.args["token"]
            except KeyError:
                return ("Not authenticated", 401)

            signing_key = jwks_client.get_signing_key_from_jwt(token)
            user = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                options={
                    "verify_aud": False,
                    "verify_exp": False
                }
            )
            if user["email"] in allowed_users:
                return fn(request)
            else:
                return ("Forbidden", 403)
        return f
    return decorated

