import json
from handlers import name_handler, list_handler

def parse_command(msg):
    handlers = {
        "name": name_handler,
        "list": list_handler,
    }

    msg_object = json.loads(str(msg, encoding='utf-8'))
    return handlers[msg_object['comando']], msg_object['params'] 
