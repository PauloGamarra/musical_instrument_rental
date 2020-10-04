import os

class Config:
    def __init__(self):
        self._config = {}

    def load(self):
        self._load_env()

        return self

    def _load_env(self):
        self._config["RENTAL_DATABASE_HOST"] = os.getenv("RENTAL_DATABASE_HOST")
        self._config["RENTAL_DATABASE_USER"] = os.getenv("RENTAL_DATABASE_USER")
        self._config["RENTAL_DATABASE_PASSWORD"] = os.getenv("RENTAL_DATABASE_PASSWORD")
        self._config["RENTAL_DATABASE_DATABASE"] = os.getenv("RENTAL_DATABASE_DATABASE")
        self._config["RENTAL_DATABASE_PORT"] = os.getenv("RENTAL_DATABASE_PORT") or "5432"

    def __getitem__(self, key):
        """Make accessing configurations easier."""
        try:
            value = self._config[key]
        except KeyError as e:
            value = None
            print("Invalid key: {}".format(key))  
        finally:
            return value