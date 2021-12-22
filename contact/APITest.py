import json
import unittest
import random
import names
from contact.index import app

app.testing = True


class TestApi(unittest.TestCase):

    def test_get_contacts(self):
        with app.test_client() as client:
            result = client.get('/contacts')
            print(result.data)

    def test_delete_contact(self):
        with app.test_client() as client:
            result = client.delete('/delete/ArshiaSaeedi')
            print(result.data)

    def test_add_contact(self):
        with app.test_client() as client:
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            full_name = first_name + last_name
            city = first_name[:2] + last_name[-2:]
            postal_code = str(random.randint(1000000000, 9999999999))
            phone_numbers = {str(random.randint(10000000000, 99999999999)): random.choice(['phone', 'home']) for _ in
                             range(random.randint(0, 5))}
            result = client.post('/add', data=json.dumps({full_name: {"first_name": first_name,
                                                                     "last_name": last_name,
                                                                     "city": city,
                                                                     "postal_code": postal_code,
                                                                     "numbers": phone_numbers}}))
            print(result.data)

    def test_update_contact_delete_number(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            delete_number = "09032507456"
            result = client.put('/update',
                                data=json.dumps({"full_name": full_name, "changes": {delete_number: ("delete",)}}))
            print(result.data)

    def test_update_contact_edit_number_type(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            update_number = "02188223344"
            result = client.put('/update',
                                data=json.dumps({"full_name": full_name, "changes": {update_number: ("edit", "home")}}))
            print(result.data)

    def test_update_contact_edit_number_exist(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            update_number = "02188223355"
            result = client.put('/update', data=json.dumps(
                {"full_name": full_name, "changes": {"02188223344": ("edit", update_number)}}))
            print(result.data)

    def test_update_contact_edit_number_not_exist(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            update_number = "09101002420"
            result = client.put('/update', data=json.dumps(
                {"full_name": full_name, "changes": {"09101002400": ("edit", update_number)}}))
            print(result.data)

    def test_update_contact_add_number(self):
        with app.test_client() as client:
            full_name = "MahdiMoridi"
            result = client.put('/update', data=json.dumps(
                {"full_name": full_name, "changes": {"09101009999": ("add", "phone")}}))
            print(result.data)
