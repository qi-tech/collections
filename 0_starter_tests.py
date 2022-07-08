from typing import Optional
from requests import post, get
import json


from utils.crypto import qi_sign_message, qi_translate_message

CONTENT_TYPE = "application/json"

class StartTest:
    def __init__(
        self, base_url: Optional[str] = None, pix_transfer_key: Optional[str] = None
    ):
        self.pix_transfer_key = pix_transfer_key
        self.base_url = (
            base_url if base_url is not None else "https://api-auth.sandbox.qitech.app"
        )
        
    def test_get(self):
        print("First Test - GET")
        
        # Request parameters
        endpoint = f'{"/test/ping"}'
        url = f"{self.base_url}{endpoint}"
        body = {}
        method = "GET"
        # Signed request
        header, body = qi_sign_message(
            endpoint=endpoint,
            method=method,
            body=body,
            content_type=CONTENT_TYPE,
        )
        # Request execution
        resp = get(url=url, headers=header)
        try:
            resp.raise_for_status()
            # Response translated
            response_body = json.loads(resp.text)
            print(response_body)
            response_header = resp.headers
            response = qi_translate_message(
                endpoint=endpoint,
                method=method,
                response_body=response_body,
                response_header=response_header,
            )
            print(response)
        except Exception as e:
            print(e)
            print(resp.text)

    def test_post(self):
        print("Second Test - POST")
        endpoint = "/test"
        url = f"{self.base_url}{endpoint}"
        body = {"document_number": "31559929804"}

        method = "POST"
        content_type = "application/json"
        # Signed request
        header, body = qi_sign_message(
            endpoint=endpoint,
            method=method,
            body=body,
            content_type=content_type,
        )
        # Request execution
        resp = post(url=url, headers=header, json=body)
        try:
            resp.raise_for_status()
            # Response translated
            response_body = json.loads(resp.text)
            print(response_body)
            response_header = resp.headers
            response = qi_translate_message(
                endpoint=endpoint,
                method=method,
                response_body=response_body,
                response_header=response_header,
            )
            print(response)
        except Exception as e:
            print(e)
            print(resp.text)
         

if __name__ == "__main__":
    request_client = StartTest(base_url="https://api-auth.qitech.app")
    request_client.test_get()
    request_client.test_post()