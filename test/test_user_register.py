import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertion import Assertion

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    missed_params = [
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email"),
        ("password")
    ]

    @allure.description("This test successfully register user by prepare data")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertion.assert_code_status(response, 200)
        Assertion.assert_json_has_key(response, "id")

    @allure.description("This test doesn't register user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertion.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.description("This test doesn't register user with email without '@'")
    def test_create_user_with_incorrect_email(self):
        email = 'test-test.ru'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = MyRequests.post("/user/", data=data)
        Assertion.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    @allure.description("This test doesn't register user with missed param")
    @pytest.mark.parametrize('missed_param', missed_params)
    def test_create_user_without_param(self, missed_param):
       data = self.prepare_registration_data()
       data.pop(missed_param)
       data_with_missed_param = data
       response = MyRequests.post("/user/", data=data_with_missed_param)
       Assertion.assert_code_status(response, 400)
       assert response.content.decode("utf-8") == f"The following required params are missed: {missed_param}", \
            f"Unexpected response content {response.content} with missed param: {missed_param}"

    @allure.description("This test doesn't register user with too short name")
    def test_create_user_with_short_name(self):
       data = self.prepare_registration_data()
       data['firstName'] = 't'
       response = MyRequests.post("/user/", data=data)
       Assertion.assert_code_status(response, 400)
       assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", \
           f"Unexpected response content for field 'firstName' when it is too short"

    @allure.description("This test doesn't register user with too long name")
    def test_create_user_with_long_name(self):
       data = self.prepare_registration_data()
       long_name = ""
       while len(long_name) <= 250:
           long_name += "t"
       data['firstName'] = long_name
       response = MyRequests.post("/user/", data=data)
       Assertion.assert_code_status(response, 400)
       assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", \
                f"Unexpected response content for field 'firstName' when it is too long"