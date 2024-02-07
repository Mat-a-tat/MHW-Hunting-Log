import unittest
from project import monster_cleaner, weapon_cleaner, region_cleaner

class TestProjectFunctions(unittest.TestCase):
    def test_normal_monster(self):
        result = monster_cleaner('anjanath')
        self.assertEqual(result, "Anjanath")
    def test_normal_region(self):
        result = region_cleaner('tundra')
        self.assertEqual(result, "Hoarfrost Reach")
    def test_normal_weapon(self):
        result = weapon_cleaner('hbg')
        self.assertEqual(result, "Heavy Bowgun")
    def test_abnormal_monster(self):
        result = monster_cleaner('pickle')
        self.assertEqual(result, "Savage Deviljho")
    def test_abnormal_region(self):
        result = region_cleaner('r o t t e d')
        self.assertEqual(result, "Rotten Vale")
    def test_abnormal_weapon(self):
        result = weapon_cleaner('bOw')
        self.assertEqual(result, "Bow")
if __name__ == '__main__':
    unittest.main()
