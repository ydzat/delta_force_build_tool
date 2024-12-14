import json

class DataManager:
    def __init__(self, weapons_file, rules_file):
        self.weapons_file = weapons_file
        self.rules_file = rules_file
        self.weapons_data = {}
        self.rules_data = {}

    def load_data(self):
        with open(self.weapons_file, 'r') as f:
            self.weapons_data = json.load(f)

    def load_rules(self):
        with open(self.rules_file, 'r') as f:
            self.rules_data = json.load(f)

    def get_weapon_data(self, weapon_type, weapon_name):
        return self.weapons_data.get(weapon_type, {}).get(weapon_name, {})

    def get_weapon_rules(self, weapon_type, weapon_name):
        return self.rules_data.get(weapon_type, {}).get(weapon_name, {})