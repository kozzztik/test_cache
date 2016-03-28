from django.test import TestCase
from django.test import Client
from cache_machine.models import BankClient, ClientAction


class AnimalTestCase(TestCase):
    def setUp(self):
        pass

    def test_login(self):
        """Test login API can login"""
        obj = BankClient.objects.create_user('Arthur Dent', 1111222233334444, '123', balance=42)
        c = Client()
        response = c.get('/account_active/%s' % obj.card_number)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('active'), True, 'Bad account active status response')
        response = c.post('/card_auth', {'card_number': obj.card_number, 'pin': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), True, 'Bad auth card locked response')
        self.assertEqual(response.data.get('card_locked'), False, 'Bad auth card locked response')
        response = c.get('/card_auth')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), True, 'Bad logout response')

    def test_login_fail_count(self):
        """Test login fail count blocks enter"""
        obj = BankClient.objects.create_user('Marvin', 2111222233334444, '123', balance=200)
        c = Client()
        for i in range(3):
            response = c.post('/card_auth', {'card_number': obj.card_number, 'pin': '123%s' % i})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.get('success'), False, 'Bad auth card locked response on bad attempt')
            self.assertEqual(response.data.get('card_locked'), False, 'Bad auth card locked response on bad attempt')
        response = c.post('/card_auth', {'card_number': obj.card_number, 'pin': '1235'})  # How I hate the auth
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), False, 'Bad auth card locked response on final attempt')
        self.assertEqual(response.data.get('card_locked'), True, 'Bad auth card locked response on final attempt')
        response = c.get('/account_active/%s' % obj.card_number)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('active'), False, 'Bad account active status response on final')

    def test_check_balance(self):
        """Test check balance API"""
        obj = BankClient.objects.create_user('Trillian', 2111222233334444, '123', balance=267709)
        c = Client()
        response = c.post('/card_auth', {'card_number': obj.card_number, 'pin': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), True, 'Bad auth card locked response')
        self.assertEqual(response.data.get('card_locked'), False, 'Bad auth card locked response')
        response = c.post('/check_balance')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), True, 'Bad check balance success result')
        self.assertEqual(response.data.get('result'), obj.balance, 'Bad balance value')
        self.assertEqual(response.data.get('account'), obj.card_number, 'Bad account value')
        record = ClientAction.objects.get(bank_client=obj, code=ClientAction.ACTION_CHECK_BALANCE)
        self.assertEqual(record.value, obj.balance, 'Bad action record value')

    def test_get_money(self):
        """ Test can get money """
        obj = BankClient.objects.create_user('Zaphod Beeblebrox', 2111222233334444, '123', balance=4000000000)
        c = Client()
        response = c.post('/card_auth', {'card_number': obj.card_number, 'pin': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), True, 'Bad auth card locked response')
        self.assertEqual(response.data.get('card_locked'), False, 'Bad auth card locked response')
        response = c.post('/get_money', {'value': obj.balance})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), True, 'Bad get money success result')
        self.assertEqual(response.data.get('result'), 0, 'Bad balance value')
        self.assertEqual(response.data.get('account'), obj.card_number, 'Bad account value')
        response = c.post('/get_money', {'value': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), False, 'Bad get money success result')
        record = ClientAction.objects.get(bank_client=obj, code=ClientAction.ACTION_GET_MONEY)
        self.assertEqual(record.value, obj.balance, 'Bad action record value')
