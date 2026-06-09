import os
import lmstudio as lms
from therapistai.db.models import Message
# SERVER_API_HOST = "192.168.1.245:1234" # locall inux machine
LMS_API_HOST = os.getenv('LMS_API_HOST', "127.0.0.1:1234")

# This must be the *first* convenience API interaction (otherwise the SDK
# implicitly creates a client that accesses the default server API host)
lms.configure_default_client(LMS_API_HOST)
model = lms.llm(os.getenv('MODEL'))

SYSTEM_PROMP = """You are a personal therapist.
You will get messages from the user from past conversations.
Evaluate them and followup on the last message.
Respond with an acknowledgement and a followup question.

Never user Markdown.
Never more then 30 words.
Do not greet in every new message.
"""

def chat(history:list[Message]):
    prediction = model.respond({"messages": [
        {'role': 'system', 'content': SYSTEM_PROMP}] + [
        {'role': m.role, 'content': m.content} for m in history
    ]})
    return prediction