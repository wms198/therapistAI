import lmstudio as lms
from therapistai.db.models import Message
# SERVER_API_HOST = "192.168.1.245:1234" # locall inux machine
SERVER_API_HOST = "127.0.0.1:1234"

# This must be the *first* convenience API interaction (otherwise the SDK
# implicitly creates a client that accesses the default server API host)
lms.configure_default_client(SERVER_API_HOST)
model = lms.llm("lmstudio-community/gemma-3-1B-it-qat-GGUF")

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