import requests

class TestInput:
    def test_headers(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        print(response.headers)
        header = dict(response.headers)
        secret_header_value = header["x-secret-homework-header"]
        print(f"Headers value = {secret_header_value}")

        assert secret_header_value == "Some secret value", f"Value 'x-secret-homework-header' not equal {secret_header_value}"

