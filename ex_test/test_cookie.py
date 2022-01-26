import requests

class TestInput:
    def test_short_input(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.post(url)
        cookie_value = response.cookies.get('HomeWork')
        print(dict(response.cookies))
        print(cookie_value)

        assert 'hw_value' == cookie_value, "Wrong, Invalid cookie value received "
