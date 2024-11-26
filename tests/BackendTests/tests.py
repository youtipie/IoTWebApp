import unittest

from backend.app import create_test_app
from backend.config import Config


class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = create_test_app(Config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.login_data = {
            "email": "test_user@gmail.com",
            "password": "verySecured8CharPass"
        }
        self.register_data = self.login_data.copy()
        self.register_data["username"] = "test_user"
    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()

    def get_access_headers(self):
        return {
            "Authorization": 'Bearer ' + self.header_tokens['access_token']
        }
    @staticmethod
    def gen_access_headers(tokens):
        return {
            "Authorization": 'Bearer ' + tokens['access_token']
        }
    def get_refresh_header(self):
        return {
            "Authorization": 'Bearer ' + self.header_tokens['refresh_token']
        }
    def login_and_assert(self, client, login_data):
        login_response = client.post('/auth/login', json=login_data)
        self.assertEqual(login_response.status_code, 200)
        self.header_tokens = login_response.json
    def refresh_and_assert(self, client):
        refresh_response = client.post('/auth/refresh', headers=self.get_refresh_header())
        self.assertEqual(refresh_response.status_code, 200)
        self.header_tokens['access_token'] = refresh_response.json['access_token']
    def register_and_assert(self, client, register_data):
        register_response = client.post('/auth/register', json=register_data)
        self.assertEqual(register_response.status_code, 201)
    def profile_get_assert(self, client, register_data):
        me_response = client.get('/me', headers=self.get_access_headers())
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.json['email'], register_data['email'])
        self.assertEqual(me_response.json['username'], register_data['username'])
    def profile_delete_assert(self, client):
        delete_response = client.delete('/me', headers=self.get_access_headers())
        self.assertEqual(delete_response.status_code, 200)
    def init_new_user(self, client):
        self.register_and_assert(client, self.register_data)
        self.login_and_assert(client, self.login_data)
    def delete_user(self, client):
        self.profile_delete_assert(client)
    def network_assert_amount(self, client, amount):
        get_response = client.get('/networks', headers=self.get_access_headers())
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(get_response.json), amount)
    def network_assert_default(self, client):
        get_response = client.get('/networks', headers=self.get_access_headers())
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json[0]['name'], "Default network")
    def network_add_assert(self, client, name):
        post_response = client.post('/networks', headers=self.get_access_headers(),
            json={'name': name}
        )
        self.assertEqual(post_response.status_code, 201)
    def network_add_multiple(self, client, names):
        for name in names:
            self.network_add_assert(client, name)
    def delete_network(self, client, network_id):
        delete_response = client.delete(f'/networks/{network_id}', headers=self.get_access_headers())
        self.assertEqual(delete_response.status_code, 200)
    def fail_to_delete_network(self, client, network_id):
        delete_response = client.delete(f'/networks/{network_id}', headers=self.get_access_headers())
        self.assertNotEqual(delete_response.status_code, 200)
    def get_networks_ids(self, client):
        get_response = client.get('/networks', headers=self.get_access_headers())
        self.assertEqual(get_response.status_code, 200)
        ids = []
        for i in range(len(get_response.json)):
            element = get_response.json[i]
            ids.append(element['id'])
        return ids
    def network_delete_multiple(self, client, ids):
        for _id in ids:
            self.delete_network(client, _id)
    def rename_network(self, client, network_id, new_name):
        rename_response = client.put(f'/networks/{network_id}', headers=self.get_access_headers(),
        json={
            'name': new_name
        })
        self.assertEqual(rename_response.status_code, 200)
        self.assertEqual(rename_response.json['name'], new_name)

    def fail_rename_network(self, client, network_id, new_name):
        rename_response = client.put(f'/networks/{network_id}', headers=self.get_access_headers(),
        json={
            'name': new_name
        })
        self.assertNotEqual(rename_response.status_code, 200)
    def add_device_to_network(self, client, network_id, device_data):
        post_response = client.post(f'/networks/{network_id}/devices', headers=self.get_access_headers(),
                    json=device_data)
        self.assertEqual(post_response.status_code, 200)
        for key, value in device_data.items():
            self.assertEqual(post_response.json[key], value)
    def add_devices_to_network(self, client, network_id, devices_data):
        for device_data in devices_data:
            self.add_device_to_network(client, network_id, device_data)
    def delete_device(self, client, network_id, device_id):
        delete_response = client.delete(f'/networks/{network_id}/devices/{device_id}', headers=self.get_access_headers())
        self.assertEqual(delete_response.status_code, 200)
    def delete_devices(self, client, network_id, devices_ids):
        for device_id in devices_ids:
            self.delete_device(client, network_id, device_id)
    def get_devices(self, client, network_id):
        get_response = client.get(f'/networks/{network_id}/devices', headers=self.get_access_headers())
        self.assertEqual(get_response.status_code, 200)
        return get_response.json

    def create_test_user(self, client, user_data):
        self.register_and_assert(client, user_data)
        login_response = client.post('/auth/login', json=user_data)
        self.assertEqual(login_response.status_code, 200)
        return login_response.json
    def create_test_users(self, client, users_data):
        tokens = []
        for user_data in users_data:
            tokens.append(self.create_test_user(client, user_data))
        return tokens
    def quit_from_network(self, client, access_tokens, network_id):
        post_response = client.post(f'/networks/{network_id}/quit', headers=self.gen_access_headers(access_tokens))
        self.assertEqual(post_response.status_code, 200)
    def get_users_in_network(self, client, network_id):
        get_response = client.get(f'/networks/{network_id}/users', headers=self.get_access_headers())
        self.assertEqual(get_response.status_code, 200)
        return get_response.json
    def get_users_in_network_assert_amount(self, client, network_id, amount_expected):
        amount_got = len(self.get_users_in_network(client, network_id))
        self.assertEqual(amount_expected, amount_got)
    def add_user_to_network(self, client, network_id, user_data):
        post_response = client.post(f'/networks/{network_id}/users', headers=self.get_access_headers(), json=user_data)
        self.assertEqual(post_response.status_code, 200)
    def add_users_to_network(self, client, network_id, users_data):
        for user_data in users_data:
            self.add_user_to_network(client, network_id, user_data)
    def login_and_leave_network(self, client, user_data, network_id):
        post_response = client.post('/auth/login', json=user_data)
        self.assertEqual(post_response.status_code, 200)
        tokens = post_response.json
        self.quit_from_network(client, tokens, network_id)
    def many_login_and_leave_network(self, client, users_data, network_id):
        for user_data in users_data:
            self.login_and_leave_network(client, user_data, network_id)

    def delete_user_from_network(self, client, network_id, user_id):
        delete_response = client.delete(f'/networks/{network_id}/users/{user_id}', headers=self.get_access_headers())
        self.assertEqual(delete_response.status_code, 200)
    def delete_users_from_network(self, client, network_id, users_id):
        for user_id in users_id:
            self.delete_user_from_network(client, network_id, user_id)
    def change_user_rights_in_network(self, client, network_id, user_id, new_rights):
        put_response = client.put(f'/networks/{network_id}/users/{user_id}', headers=self.get_access_headers(), json={
            'rights': new_rights
        })
        self.assertEqual(put_response.status_code, 200)
    def fail_to_change_user_rights_in_network(self, client, network_id, user_id, new_rights):
        put_response = client.put(f'/networks/{network_id}/users/{user_id}', headers=self.get_access_headers(), json={
            'rights': new_rights
        })
        self.assertNotEqual(put_response.status_code, 200)
    def test_full_auth_and_profile(self):
        with self.app.test_client() as client:
            self.register_and_assert(client, self.register_data)
            self.login_and_assert(client, self.login_data)
            self.refresh_and_assert(client)
            self.profile_get_assert(client, self.register_data)
            self.profile_delete_assert(client)
    def test_refresh(self):
        with self.app.test_client() as client:
            self.init_new_user(client)
            self.refresh_and_assert(client)
            self.delete_user(client)
    def test_profile(self):
        with self.app.test_client() as client:
            self.init_new_user(client)
            self.profile_get_assert(client, self.register_data)
            self.delete_user(client)
    def test_default_network(self):
        with self.app.test_client() as client:
            self.init_new_user(client)
            self.network_assert_default(client)
            self.network_assert_amount(client, 1)
            self.delete_user(client)
    def test_add_network(self):
        with self.app.test_client() as client:
            self.init_new_user(client)
            self.network_assert_default(client)
            self.network_assert_amount(client, 1)
            self.network_add_assert(client, 'my_new1')
            self.network_add_assert(client, 'my_new2')
            self.network_assert_amount(client, 3)
            self.network_add_assert(client, 'my_new3')
            self.network_assert_amount(client, 4)
            self.delete_user(client)
    def test_delete_network(self):
        with self.app.test_client() as client:
            self.init_new_user(client)
            self.network_assert_default(client)
            self.network_assert_amount(client, 1)
            self.network_add_multiple(client, ['1', '2', '3', '4', '5', '6', '7', '8'])
            self.network_assert_amount(client, 9)
            ids = self.get_networks_ids(client)
            self.network_delete_multiple(client, ids)
            self.network_assert_amount(client, 0)
            self.delete_user(client)
    def test_rename_network(self):
        with self.app.test_client() as client:
            self.init_new_user(client)
            self.network_assert_default(client)
            self.network_add_multiple(client, ['1', '2'])
            ids = self.get_networks_ids(client)
            self.rename_network(client, ids[0], 'cool name')
            self.rename_network(client, ids[1], 'not cool name')
            self.fail_rename_network(client, 16592894, 'random')
            self.delete_user(client)
    def test_devices_actions(self):
        with self.app.test_client() as client:
            self.init_new_user(client)
            ids = self.get_networks_ids(client)
            devices_data = [
                {
                    "ip": "127.0.0.1",
                    "name": "Device1",
                    "port": 1234
                },
                {
                    "ip": "127.0.0.2",
                    "name": "Device2",
                    "port": 1534
                },
                {
                    "ip": "127.0.0.3",
                    "name": "Device3",
                    "port": 4321
                }
            ]
            self.add_devices_to_network(client, ids[0], devices_data)
            devices_received = self.get_devices(client, ids[0])
            self.assertEqual(len(devices_data), len(devices_received))
            devices_ids = []
            for device in devices_received:
                devices_ids.append(device['id'])
            self.delete_devices(client, ids[0], devices_ids)
    def test_user_managing(self):
        with self.app.test_client() as client:
            self.init_new_user(client)
            default_email = 'test_test_test@gmain.com'
            default_name = 'test_test_test'
            password = '1234567890Ww'
            users_data = []
            users_add_to_network_data = []
            for i in range(10):
                users_data.append({
                    'email': default_email + str(i),
                    'password': password,
                    'username': default_name + str(i),
                })
                users_add_to_network_data.append({
                    'email': users_data[i]['email'],
                    'rights': 'w',
                })
            self.create_test_users(client, users_data)
            network_id = self.get_networks_ids(client)[0]
            self.add_users_to_network(client, network_id, users_add_to_network_data)
            self.get_users_in_network_assert_amount(client, network_id, 11)
            users = self.get_users_in_network(client, network_id)

            self.many_login_and_leave_network(client, users_data[:2], network_id)
            user_ids = []
            for user in users:
                user_ids.append(user['id'])
            self.delete_users_from_network(client, network_id, user_ids[3:5])
            self.change_user_rights_in_network(client, network_id, user_ids[6], 'r')
            self.fail_to_change_user_rights_in_network(client, network_id, user_ids[7], 'a')
            self.change_user_rights_in_network(client, network_id, user_ids[8], 'w')

if __name__ == "__main__":
    unittest.main()
