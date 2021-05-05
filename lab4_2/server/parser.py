import json
from handlers import name_handler, list_handler, active_handler, inactive_handler, pm_handler, create_handler

def parse_command(msg):
    handlers = {
        "name": name_handler,
        "list": list_handler,
        "active": active_handler,
        "inactive": inactive_handler,
        "pm": pm_handler,
        "create": create_handler,
    }

    msg_object = json.loads(str(msg, encoding='utf-8'))
    return handlers[msg_object['comando']], msg_object['params'] 

