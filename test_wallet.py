import unittest
from wallet.models import init_db, make_payment, get_contacts, get_history

class TestWallet(unittest.TestCase):
    def setUp(self):
        self.db = init_db()

    def test_get_contacts_success(self):
        contacts = get_contacts(self.db, "21345")
        self.assertEqual(contacts, {"123": "Luisa", "456": "Andrea"})

    def test_make_payment_success(self):
        result = make_payment(self.db, "21345", "123", 100)
        self.assertIn("success", result)

    def test_make_payment_insufficient_funds(self):
        result = make_payment(self.db, "21345", "123", 300)
        self.assertIn("error", result)

    def test_make_payment_invalid_contact(self):
        result = make_payment(self.db, "21345", "789", 100)
        self.assertIn("error", result)

    def test_get_history(self):
        make_payment(self.db, "21345", "123", 100)
        history = get_history(self.db, "21345")
        self.assertIn("saldo", history)
        self.assertIn("operaciones", history)

if __name__ == '__main__':
    unittest.main()
