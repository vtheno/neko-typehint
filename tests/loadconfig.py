from toml import loads

from typehint.datatype import Dataclass
from typehint.tools import Box, Data

# import orjson

with open("config.toml", "r") as f:
    data = loads(f.read())

print(data)


class ApplicationConfig(Dataclass):
    host: Box(str)
    port: Box(int)
    workers: Box(int)
    backlog: Box(int)


class DatabaseConfig(Dataclass):
    dbname: Box(str)
    user: Box(str)
    password: Box(str)
    host: Box(str)
    port: Box(int)
    min_size: Box(int)
    max_size: Box(int)
    timeout: Box(int)


class CacheConfig(Dataclass):
    host: Box(str)
    port: Box(int)
    min_size: Box(int)


class Config(Dataclass):
    application: Data(ApplicationConfig)
    database: Data(DatabaseConfig)
    cache: Data(CacheConfig)


config = Config(**data)
print(config.cache, type(config.application), ApplicationConfig)
