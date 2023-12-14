import httpx
from enum import Enum


class logLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 9
    CRITICAL = 4


class Client:
    def __init__(self, key: str, ndb: str, kvdb: str, logger: str):
        self.ndb = ndb
        self.key = {"X-DATAKEY": key}
        self.baseURL = "https://api.conserve.cloud/v1/"
        self.ndb = ndb
        self.kv = kvdb
        self.log = logger

    def __str__(self) -> str:
        return f"Client({self.nosql},{self.kv},{self.log})"

    @property
    def logger(self):
        return Logger(self.log, self.key, self.baseURL)

    @property
    def nosql(self):
        return noSQL(self.ndb, self.key, self.baseURL)

    @property
    def keys(self):
        return KVStore(self.kv, self.key, self.baseURL)


class noSQL:
    def __init__(self, db, key, url):
        self.db = db
        self.key = key
        self.baseURL = f"{url}nosql/"

    def put(self, data):
        with httpx.Client() as client:
            r = client.post(
                f"{self.baseURL}{self.db}",
                headers=self.key,
                json={"data": data},
            )
            return r.json()

    def fetch_all(self):
        with httpx.Client() as client:
            r = client.get(f"{self.baseURL}{self.db}", headers=self.key)
            return r.json()

    def fetch(self, query):
        with httpx.Client() as client:
            r = client.request(
                "GET",
                f"{self.baseURL}{self.db}",
                headers=self.key,
                json={"query": query},
            )
            return r.json()

    def update(self, key, updates):
        with httpx.Client as client:
            r = client.put(
                f"{self.baseURL}{self.db}",
                headers=self.key,
                json={"key": key, "updates": updates},
            )
            return r.json()

    def delete(self, key):
        with httpx.Client() as client:
            r = client.request(
                "DELETE",
                f"{self.baseURL}{self.db}",
                headers=self.key,
                data={"key": key},
            )
            return r.json()


class KVStore:
    def __init__(self, db, key, url):
        self.db = db
        self.key = key
        self.baseURL = url

    def set(self, key, value):
        with httpx.Client() as client:
            r = client.post(
                f"{self.baseURL}kv/{self.db}",
                headers=self.key,
                data={"key": key, "value": value},
            )
            return r.json()

    def get(self, key):
        with httpx.Client() as client:
            r = client.request(
                "GET",
                f"{self.baseURL}kv/{self.db}",
                headers=self.key,
                json={"key": key},
            )

            return r.json()

    def delete(self, key):
        with httpx.Client() as client:
            r = client.request(
                "DELETE",
                f"{self.baseURL}kv/{self.db}",
                headers=self.key,
                data={"key": key},
            )
            return r.json()


class Logger:
    def __init__(self, db, key, baseURL):
        self.db = db
        self.key = key
        self.url = baseURL

    def log(self, message: str, loglevel):
        with httpx.Client() as client:
            r = client.post(
                f"{self.url}logger/{self.db}",
                headers=self.key,
                data={"message": message, "level": loglevel.name},
            )
            print(r.json())
