import requests

class TestInput:
    def test_short_input(self):
        phrase = input("Set a phrase: ")
        length = len(phrase)

        assert length < 15, "Wrong! You entered more than 15 characters "

