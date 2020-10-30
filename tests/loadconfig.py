from toml import loads

from typehint.datatype import Dataclass
from typehint.typehintaux import Aux, Box

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
    application: Aux(ApplicationConfig)
    database: Aux(DatabaseConfig)
    cache: Aux(CacheConfig)


config = Config(**data)
print(config.cache, type(config.application), ApplicationConfig)
