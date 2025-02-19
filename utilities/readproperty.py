import os
from configparser import ConfigParser
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
config_file_path = os.path.join(parent_dir, 'config', 'config.ini')
config = ConfigParser()
config.read(config_file_path)


if not config.sections():
    raise FileNotFoundError(f"Config file not found or sections are missing: {config_file_path}")

class ReadConfig:
    @staticmethod
    def url():
        try:
            url = config.get('basic info', 'url')
            return url
        except Exception as e:
            raise Exception(f"Error reading 'url' from config file: {e}")

    @staticmethod
    def browser():
        try:
            browser = config.get('basic info', 'browser')  # Fetch 'browser' from 'basic info'
            return browser
        except Exception as e:
            raise Exception(f"Error reading 'browser' from config file: {e}")
