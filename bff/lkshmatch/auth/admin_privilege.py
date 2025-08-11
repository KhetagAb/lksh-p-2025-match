from pymongo import MongoClient
client = MongoClient()
db = client['admin_login']
collection = db['tg_login']
# TODO спросить про то что передавать
headers = {'admin_token':'asd'}

class PrivilegeChecker:
    def __init__(self):
        pass


    def auth_admin(self):
        pass