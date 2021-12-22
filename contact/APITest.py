import json
import unittest
import random
import names
from copy import deepcopy

from contact.views import app

app.testing = True


class TestApi(unittest.TestCase):

    def setUp(self) -> None:
        with open('contact/phonenumbers.json') as json_file:
            self.users = json.load(json_file)

    def tearDown(self) -> None:
        with open('contact/phonenumbers.json', 'w') as json_file:
            json.dump(self.users, json_file, indent=2)

    def test_get_contacts(self):
        with app.test_client() as client:
            result = json.loads(client.get('/contacts').data.decode("utf-8"))
            self.assertEqual(result, self.users)

    def test_delete_contact(self):
        with app.test_client() as client:
            result = json.loads(client.delete('/delete/ArshiaSaeedi').data.decode("utf-8"))
            updated_contact = deepcopy(self.users)
            if "ArshiaSaeedi" in updated_contact:
                updated_contact.pop("ArshiaSaeedi")
            self.assertEqual(result, updated_contact)

    def test_add_contact(self):
        with app.test_client() as client:
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            full_name = first_name + last_name
            city = first_name[:2] + last_name[-2:]
            postal_code = str(random.randint(1000000000, 9999999999))
            phone_numbers = {str(random.randint(10000000000, 99999999999)): random.choice(['phone', 'home']) for _ in
                             range(random.randint(0, 5))}
            result = json.loads(
                client.post('/add', data=json.dumps({full_name: {"first_name": first_name, "last_name": last_name,
                                                                 "city": city, "postal_code": postal_code,
                                                                 "numbers": phone_numbers}})).data.decode("utf-8"))
            updated_contact = deepcopy(self.users)
            updated_contact.update({full_name: {"first_name": first_name, "last_name": last_name,
                                                "city": city, "postal_code": postal_code,
                                                "numbers": phone_numbers}})
            self.assertEqual(result, updated_contact)

    def test_update_contact_delete_number(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            delete_number = "09032507456"
            result = json.loads(client.put('/update', data=json.dumps(
                {"full_name": full_name, "changes": {delete_number: ("delete",)}})).data.decode("utf-8"))
            updated_contact = deepcopy(self.users)
            updated_contact["MahdiMoridi"]["numbers"].pop("09032507456")
            self.assertEqual(result, updated_contact)

    def test_update_contact_edit_number_type(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            update_number = "02188223344"
            result = json.loads(client.put('/update', data=json.dumps(
                {"full_name": full_name, "changes": {update_number: ("edit", "home")}})).data.decode("utf-8"))
            updated_contact = deepcopy(self.users)
            updated_contact["MahdiMoridi"]["numbers"]["02188223344"] = "home"
            self.assertEqual(result, updated_contact)

    def test_update_contact_edit_number_exist(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            update_number = "02188223355"
            result = json.loads(client.put('/update', data=json.dumps(
                {"full_name": full_name, "changes": {"02188223344": ("edit", update_number)}})).data.decode("utf-8"))
            updated_contact = deepcopy(self.users)
            updated_contact["MahdiMoridi"]["numbers"][update_number] = updated_contact["MahdiMoridi"]["numbers"][
                "02188223344"]
            updated_contact["MahdiMoridi"]["numbers"].pop("02188223344")
            self.assertEqual(result, updated_contact)

    def test_update_contact_edit_number_not_exist(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            update_number = "09101002420"
            result = json.loads(client.put('/update', data=json.dumps(
                {"full_name": full_name, "changes": {"09101002400": ("edit", update_number)}})).data.decode("utf-8"))
            updated_contact = deepcopy(self.users)
            self.assertTrue("09101002400" not in updated_contact["MahdiMoridi"]["numbers"])
            self.assertEqual(result, updated_contact)

    def test_update_contact_add_number(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            result = json.loads(client.put('/update', data=json.dumps(
                {"full_name": full_name, "changes": {"09101009999": ("add", "phone")}})).data.decode("utf-8"))
            updated_contact = deepcopy(self.users)
            updated_contact["MahdiMoridi"]["numbers"].update({"09101009999": "phone"})
            self.assertEqual(result, updated_contact)
