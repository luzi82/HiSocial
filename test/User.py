from admin import reset
from base import Database, Runtime
from base.Runtime import trace
from sqlalchemy.orm.session import sessionmaker
from user import User
import unittest

class TestUser(unittest.TestCase):
    
    def setUp(self):
        reset.reset()
        Runtime.enable_trace = True

    def test_hash(self):
        apple_hash = User._gen_password_hash("apple")
#        trace(apple_hash)
        self.assertEqual(len(apple_hash), User.PASSWORD_HASH_LENGTH)
        self.assertTrue(User._check_password_hash("apple", apple_hash))
        self.assertFalse(User._check_password_hash("orange", apple_hash))
        
    def test_add_user(self):
        Session = sessionmaker(bind=Database.create_sqlalchemy_engine())
        session = Session()
        self.assertFalse(User.check_user_account_exist(session=session, user_id="apple"))
        User.add_user_account(session=session, user_id="apple", password="apple_pass")
        self.assertTrue(User.check_user_account_exist(session=session, user_id="apple"))
        self.assertTrue(User.check_user_account_password(session=session, user_id="apple", password="apple_pass"))
        session.close()
        
    def test_check_user_password(self):
        Session = sessionmaker(bind=Database.create_sqlalchemy_engine())
        session = Session()
        User.add_user_account(session=session, user_id="apple", password="apple_pass")
        self.assertTrue(User.check_user_account_password(session=session, user_id="apple", password="apple_pass"))
        self.assertFalse(User.check_user_account_password(session=session, user_id="apple", password="xxx"))
        self.assertFalse(User.check_user_account_password(session=session, user_id="xxx", password="xxx"))
        session.close()

    def test_check_change_user_password(self):
        Session = sessionmaker(bind=Database.create_sqlalchemy_engine())
        session = Session()
        User.add_user_account(session=session, user_id="apple", password="apple_pass")
        self.assertTrue(User.check_user_account_password(session=session, user_id="apple", password="apple_pass"))
        self.assertFalse(User.check_user_account_password(session=session, user_id="apple", password="apple_passs"))
        self.assertFalse(User.check_user_account_password(session=session, user_id="apple", password="xxx"))
        self.assertFalse(User.check_user_account_password(session=session, user_id="xxx", password="xxx"))
        self.assertTrue(User.change_password(session=session, user_id="apple", password="apple_passs"))
        self.assertTrue(User.check_user_account_password(session=session, user_id="apple", password="apple_passs"))
        self.assertFalse(User.check_user_account_password(session=session, user_id="apple", password="apple_pass"))
        self.assertFalse(User.check_user_account_password(session=session, user_id="apple", password="xxx"))
        self.assertFalse(User.check_user_account_password(session=session, user_id="xxx", password="xxx"))
        session.close()
    
    def test_check_user_id_valid(self):
        self.assertTrue(User.check_user_id_valid("Helloxx"))
        self.assertTrue(User.check_user_id_valid("Hello123"))
        self.assertTrue(User.check_user_id_valid("Hello--3"))
        self.assertTrue(User.check_user_id_valid("Hello__3"))
        self.assertFalse(User.check_user_id_valid(None))
        self.assertFalse(User.check_user_id_valid("123Hello"))
        self.assertFalse(User.check_user_id_valid("Hel lo"))
        self.assertFalse(User.check_user_id_valid("llo"))
        self.assertFalse(User.check_user_id_valid("x"*200))

    def test_check_password_valid(self):
        self.assertTrue(User.check_password_valid("Helloxx"))
        self.assertTrue(User.check_password_valid("Hello123"))
        self.assertTrue(User.check_password_valid("Hello--3"))
        self.assertTrue(User.check_password_valid("Hello__3"))
        self.assertTrue(User.check_password_valid("123Hello"))
        self.assertFalse(User.check_password_valid(None))
        self.assertFalse(User.check_password_valid("Hel lo"))
        self.assertFalse(User.check_password_valid("llo"))
        self.assertFalse(User.check_password_valid("x"*200))

if __name__ == '__main__':
    unittest.main()
