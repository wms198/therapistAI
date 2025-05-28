import lmstudio as lms
from db.models import Message
SERVER_API_HOST = "192.168.1.245:1234"

# This must be the *first* convenience API interaction (otherwise the SDK
# implicitly creates a client that accesses the default server API host)
lms.configure_default_client(SERVER_API_HOST)
model = lms.llm("llama-3.2-3b-instruct")

SYSTEM_PROMP = """You are a personal therapist.
You will get messages from the user from past conversations.
Evaluate them and followup on the last message.
"""

def chat(history:list[Message]):
    prediction = model.respond({"messages": [
        {'role': 'system', 'content': SYSTEM_PROMP}] + [
        {'role': m.role, 'content': m.content} for m in history
    ]})
    return prediction