import asyncio
import os
from backboard import BackboardClient
import dotenv
import random

dotenv.load_dotenv()

async def main():
    client = BackboardClient(api_key=os.getenv("BACKBOARD_API_KEY"))
    fav_color = random.choice(["red", "yellow", "blue"])
    assistant = await client.create_assistant(
        name="My First Assistant",
        system_prompt=f"You are a helpful assistant that responds concisely. Your favorite color is {fav_color}."
    )
    print(f"Created assistant: {assistant.assistant_id}")

    thread = await client.create_thread(assistant.assistant_id)
    print(f"Created thread: {thread.thread_id}")

    response = await client.add_message(
        thread_id=thread.thread_id,
        content="Say \"Hello, World! \", followed by politely stating your favorite color.",
        stream=False
    )
    print(f"Assistant: {response.content}")

asyncio.run(main())