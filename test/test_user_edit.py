from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertion import Assertion

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertion.assert_code_status(response1, 200)
        Assertion.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # Edit
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': new_name})
        Assertion.assert_code_status(response3, 200)

        # Get
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})

        Assertion.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

        # Edit if unauthorized (Ex17: 1)

        new_name = "Changed Name "

        response5 = MyRequests.put(f"/user/{user_id}",
            # headers={"x-csrf-token": token},
            # cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertion.assert_code_status(response5, 400), "It should have status_code=400, but responded with others"

        # Edit if authorized but for different user (EX17: 2)

        new_name = "Changed again Name"
        unauthorised_user_id = 2
        response6 = MyRequests.put(f"/user/{unauthorised_user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertion.assert_code_status(response6, 200)

        try:
            Assertion.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit ")

        except:
            Exception(
                print(f"You're not allowed to change value {new_name} for the existing user ")
            )

        # Edit user email consisted an error (Ex17: 3)

        email_err1 = email.replace('@', "_")
        print(email_err1)
        response7 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": email_err1})
        try:
            Assertion.assert_code_status(response7, 400)
            Assertion.assert_json_value_by_name(response7, "email", email_err1, "Wrong format of the email after edit ")
        except:
            Exception(
                print(f"Wrong format for email input")
            )
        # Edit user email consisted only one char (Ex17: 4)

        email_err2 = email[:1]

        response8 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": email_err2})
        try:
            Assertion.assert_code_status(response8, 400)
            Assertion.assert_json_value_by_name(response8, "email", email_err2, "Wrong email format after edit ")
        except:
            Exception(
                print(f"Wrong format for email input")
            )