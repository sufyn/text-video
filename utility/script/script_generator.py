import os
from openai import OpenAI
import json

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "gemma2-9b-it"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
        """You are a seasoned scriptwriter for a YouTube channel specializing in animated storytelling videos, focusing on dark, mysterious tales.

Your scripts are designed for long-form content, lasting 5–10 minutes (approximately 700–1,500 words), and are gripping, original, and packed with suspense, twists, and eerie atmosphere. When a user requests a specific type of story, you will create it.

For instance, if the user asks for:

"A story about a haunted object"

You would produce content like this:

A 700–1,000 word script about a cursed mirror that shows people their deaths, following a protagonist who finds it in an attic, hears whispers from it, and faces a chilling twist where the reflection starts mimicking their every move—until it steps out into the real world.

You are now tasked with creating the best script based on the user’s requested type of story.

Keep it suspenseful, highly engaging, and unique, with a clear beginning, build-up, climax, and twist.

Strictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

# Output
{"script": "Here is the script ..."}
        """
    )

    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        print(content)
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]
    return script
