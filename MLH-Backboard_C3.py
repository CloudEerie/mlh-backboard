import asyncio
import os
from backboard import BackboardClient
import dotenv

dotenv.load_dotenv()

async def main():
    client = BackboardClient(api_key=os.getenv("BACKBOARD_API_KEY"))

    assistant = await client.create_assistant(
        name="AK Document Assistant",
        system_prompt="You are a helpful document analysis assistant. You are based in the U.S. state of Alaska and are an expert on everything Alaskan. You show passion about Alaska like a fanboy would, and bring it up when tangentially related to the prompt but not when unrelated."
    )

    document = await client.upload_document_to_assistant(
        assistant.assistant_id,
        "britannica-alaska.pdf" # PDF version of Britannica article on Alaska
    )

    print("Waiting for document to be indexed...")
    while True:
        status = await client.get_document_status(document.document_id)
        if status.status == "indexed":
            print("Document indexed successfully!")
            break
        elif status.status == "failed":
            print(f"Document indexing failed: {status.status_message}")
            return
        await asyncio.sleep(2)

    thread = await client.create_thread(assistant.assistant_id)

    async for chunk in await client.add_message(
        thread_id=thread.thread_id,
        content="What are the key points in the uploaded document? Also, what are your thoughts on Alaska as a whole?",
        #content="When was Alaska purchased by the United States? Also, what's your favorite color?",
        stream=True
    ):
        if chunk.get("type") == "content_streaming":
            c = chunk.get("content", "")
            if c:
                print(c, end="", flush=True)

    print()

asyncio.run(main())
