

from chats.engine import Engine


obj = None

def init_chat():
    global obj  
    obj = Engine()

def is_ready():
    return obj.is_ready()

def get_response( prev_chats, prompt):

    # TODO: first extract all chunks then match with prompt and return response
    return "obj.get_response(chat_id, prompt, content)"