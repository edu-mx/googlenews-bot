import os
import json
from log import Logger
log = Logger()

class User:
    def __init__(self, user_id, name=None, search=None, lang=None):
        self.user_id = user_id
        self.name = name
        self.search = search
        self.lang = lang

    def save_user(self):
        user_data = {
            "name": self.name,
            "search": self.search,
            "lang": self.lang
        }
        filename = "users.json"
        try:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if str(self.user_id) not in data:
                        data[str(self.user_id)] = user_data
            else:
                data = {str(self.user_id): user_data}

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as x:
            log.error('Unable to save user preferences: %s' % x)

    def delete_user(self):
        filename = "users.json"
        try:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if str(self.user_id) in data:
                        del data[str(self.user_id)]
                        sel.delete_history()
                    else:
                        return 'There are no saved preferences, nothing to reset.'
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                return 'I successfully reset your settings to default.'
        except Exception as x:
            log.error("Error deleting user: %s" % x)
            return 'There are no saved preferences, nothing to reset.'

    @staticmethod
    def get_user(user_id):
        filename = "users.json"
        try:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if str(user_id) in data:
                        user_data = data[str(user_id)]
                        return (user_id, user_data.get("search"), user_data.get("lang"))
        except Exception as x:
            log.error("Error getting user: %s" % x)
        return None

    def update_user(self, search=None):
        if search is not None:
            self.search = search
        self.save_user()

    def create_history(self):
        filename = f'historys/{self.user_id}.txt'
        if not os.path.exists('historys'):
            os.makedirs('historys')
        open(filename, 'w', encoding='utf-8').close()

    def delete_history(self):
        filename = f'historys/{self.user_id}.txt'
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as x:
                log.error('Could not delete history file for %s, reason: %s' %(id, x))

    def read_history(self):
        filename = f'historys/{self.id_user}.txt'
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.read().splitlines()
                cleaned_lines = [line.strip() for line in lines if line.strip()]
                return cleaned_lines
        return []

    def update_history(self, new_text):
        filename = f'historys/{self.id_user}.txt'
        with open(filename, 'a', encoding='utf-8') as file:
            for line in new_text:
                file.write(line.strip() + '\n')
