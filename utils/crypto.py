from datetime import datetime, timedelta
from hashlib import md5
from jose import jwt
from config import CLIENT_PRIVATE_KEY, API_KEY, QI_PUBLIC_KEY



def qi_sign_message(
    endpoint,
    method,
    body=None,
    content_type="",
    additional_headers=None,
):
    md5_body = ""
    request_body = None
    if body:
        encoded_body_token = jwt.encode(
            claims=body, key=CLIENT_PRIVATE_KEY, algorithm="ES512"
        )
        request_body = {"encoded_body": encoded_body_token}
        # Create body hash
        md5_encode = md5()
        md5_encode.update(encoded_body_token.encode())
        md5_body = md5_encode.hexdigest()
    date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    string_to_sign = (
        method + "\n" + md5_body + "\n" + content_type + "\n" + date + "\n" + endpoint
    )
    headers = {"alg": "ES512", "typ": "JWT"}
    claims = {"sub": API_KEY, "signature": string_to_sign}
    encoded_header_token = jwt.encode(
        claims=claims, key=CLIENT_PRIVATE_KEY, algorithm="ES512", headers=headers
    )
    authorization = "QIT" + " " + API_KEY + ":" + encoded_header_token
    request_header = {"AUTHORIZATION": authorization, "API-CLIENT-KEY": API_KEY}
    if additional_headers:
        request_header.update(additional_headers)
    return request_header, request_body


def qi_translate_message(
    endpoint,
    method,
    response_body,
    response_header=None,
):
    qi_public_key = QI_PUBLIC_KEY

    body = jwt.decode(
        response_body.get("encoded_body", None),
        key=qi_public_key,
        algorithms=["ES512"],
    )

    authorization = response_header.get("AUTHORIZATION") # type: ignore
    header_api_key = response_header.get("API-CLIENT-KEY") # type: ignore
    if header_api_key != API_KEY:
        raise Exception(
            "The api_key gathered on message's header does not match the one provided "
            "to the function"
        )
    split_authorization = authorization.split(":")
    if len(split_authorization) != 2:
        raise Exception("Wrong format for the Authorization header")
    authorization_api_key = split_authorization[0].split(" ")[1]
    if authorization_api_key != API_KEY:
        raise Exception(
            "The api_key gathered on message's authorization header does not match the "
            "one provided to the function"
        )
    header_token = split_authorization[1]
    decoded_header_token = jwt.decode(
        token=header_token, key=qi_public_key, algorithms=["ES512"]
    )
    signature = decoded_header_token.get("signature", None)
    split_signature = signature.split("\n")
    signature_method = split_signature[0]
    signature_md5_body = split_signature[1]
    signature_date = split_signature[3]
    signature_endpoint = split_signature[4]
    if signature_endpoint != endpoint:
        raise Exception(
            "The 'endpoint' parameter gathered on message's signature does not match the "
            "one provided to the function"
        )
    if signature_method != method:
        raise Exception(
            "The 'method' parameter gathered on message's signature does not match the "
            "one provided to the function"
        )
    md5_encode = md5()
    md5_encode.update(response_body.get("encoded_body", None).encode())
    md5_body = md5_encode.hexdigest()
    if signature_md5_body != md5_body:
        raise Exception(
            "The 'md5_body' parameter gathered on message's signature does not match "
            "the 'body' provided to the function"
        )
    utc_now = datetime.utcnow()
    time_delta = timedelta(minutes=5)
    utc_signature_date = datetime.strptime(signature_date, "%a, %d %b %Y %H:%M:%S GMT")
    if utc_signature_date > utc_now or utc_signature_date < (utc_now - time_delta):
        raise Exception("Invalid signature timestamp")
    return body
