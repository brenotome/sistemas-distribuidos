from dataclasses import dataclass

@dataclass()
class User:
    sock_conn: ...
    active: bool = False
    name: str = ''
    address: str = ''
    channels: dict = {}

@dataclass()
class Channel:
    name: str
    owner: User