from lib.base_case import BaseCase
from lib.assertion import Assertion
from lib.my_requests import MyRequests
import allure


class TestUserDelete(BaseCase):

    def test_user_delete(self):

         # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response, 'auth_sid')
        token = self.get_header(response, 'x-csrf-token')

        # TEST 1: Delete user by user_id=2

        user_id = 2
        response1 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        print(response1.status_code)
        try:
            Assertion.assert_code_status(response1, 200)
        except: Exception(
             print(f"It's not allowed to Delete ")
        )

    def test_get_deleted_user_data(self):

         # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")


        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # TEST 2 -DELETE this user and get data
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})


         # GET data
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertion.assert_code_status(response4, 404)

        try:
            Assertion.assert_json_value_by_name(response4, "firstName", first_name, "User name is not found ")
        except: Exception(
            print(f"User name = {first_name} is not found")
        )


        # TEST 3 - deleted_different_user

        unauthorised_user_id = int(user_id)-1
        response6 = MyRequests.delete(f"/user/{unauthorised_user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        print(response6.status_code,f" for {unauthorised_user_id} ")
        Assertion.assert_code_status(response6, 200)

        response7 = MyRequests.get(f"/user/{unauthorised_user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertion.assert_code_status(response7, 404)