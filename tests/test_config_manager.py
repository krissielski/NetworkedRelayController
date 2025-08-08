
import unittest
from src.config_manager import ConfigManager
import os
import tempfile
import yaml


class ConfigManagerTestCase(unittest.TestCase):
    def test_load_and_validate(self):
        config_data = {
            'api': {'host': '0.0.0.0', 'port': 5000},
            'relays': {'pins': {1: 31, 2: 33, 3: 35, 4: 37}},
            'logging': {'level': 'INFO', 'file': 'test.log'},
            'system': {'version': '1.0.0'}
        }
        path = make_config_file(config_data)
        cfg = ConfigManager(path)
        self.assertEqual(cfg.get('api', 'host'), '0.0.0.0')
        self.assertEqual(cfg.get('relays', 'pins')[1], 31)
        os.remove(path)

    def test_missing_section(self):
        config_data = {'api': {}, 'relays': {'pins': {}}, 'logging': {}, 'system': {}}
        path = make_config_file(config_data)
        cfg = ConfigManager(path)
        self.assertEqual(cfg.get('api'), {})
        os.remove(path)

    def test_invalid_config(self):
        config_data = {'api': {}, 'logging': {}, 'system': {}}
        path = make_config_file(config_data)
        with self.assertRaises(ValueError):
            ConfigManager(path)
        os.remove(path)


def make_config_file(data):
    tmp = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml')
    yaml.dump(data, tmp)
    tmp.close()
    return tmp.name


if __name__ == "__main__":
    unittest.main()

