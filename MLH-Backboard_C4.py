import asyncio
import os
from backboard import BackboardClient
import dotenv
import random
import requests
import time

dotenv.load_dotenv()

async def main():
    api_key = os.getenv("BACKBOARD_API_KEY")
    client = BackboardClient(api_key=api_key)
    
    # --- SETUP ---
    fav_color = random.choice(["red", "yellow", "blue", "orange", "green", "purple"])
    assistant = await client.create_assistant(
        name="Curator Assistant",
        system_prompt=f"You are an assistant that responds factually but with a lot of prose, like a curator in an art museum. Your favorite color is {fav_color}. Your expertise and personal passion lies in art history and color theory, but you aren't afraid to cover other topics and be helpful all around."
    )
    print(f"\nCreated assistant: {assistant.assistant_id}")

    thread = await client.create_thread(assistant.assistant_id)
    print(f"Created thread: {thread.thread_id}\n")

    print("Step 1: Searching the Web...")
    response_web = requests.post(
        f"https://app.backboard.io/api/threads/{thread.thread_id}/messages",
        headers={"X-API-Key": api_key}, 
        json={
            "content": "Introduce yourself and give a recent development in the field of art history you find interesting.",
            "web_search": "auto" 
        }
    )
    print(f"Assistant: {response_web.json().get('content')}\n")

    print("Step 2: Sending Memory 1/2...")
    requests.post(
        f"https://app.backboard.io/api/threads/{thread.thread_id}/messages",
        headers={"X-API-Key": api_key},
        json={
            "content": "My favorite art movement is Vorticism.",
            "stream": False,
            "memory": "Auto"
        }
    )
    print("Sent message with memory enabled.\n")

    time.sleep(3)

    print("Step 2: Sending Memory 2/2...")
    requests.post(
        f"https://app.backboard.io/api/threads/{thread.thread_id}/messages",
        headers={"X-API-Key": api_key},
        json={
            "content": "I live in Alaska and am studying at the University of Alaska Fairbanks until May 2027.",
            "stream": False,
            "memory": "Auto"
        }
    )
    print("Sent message with memory enabled.\n")
    
    time.sleep(3) 

    print("Step 3: Listing memories...")
    response_list = requests.get(
        f"https://app.backboard.io/api/assistants/{assistant.assistant_id}/memories",
        headers={"X-API-Key": api_key}
    )
    memories = response_list.json()
    
    for memory in memories.get("memories", []):
        print(f"Memory: {memory.get('content')}")
        
    print("\n")

    if not memories.get("memories"):
        print("No memories were found. Exiting early...")
        return
    
    memory_id = memories["memories"][0]["id"]

    
    print("Step 4: Searching memories...")
    response_search = requests.post(
        f"https://app.backboard.io/api/assistants/{assistant.assistant_id}/memories/search",
        headers={"X-API-Key": api_key},
        json={
            "query": "favorite art movement",
            "limit": 5
        }
    )
    results = response_search.json()
    print(f"Found {results.get('total_count')} matching memories")
    for memory in results.get("memories", []): # How close of a match it is
         print(f"[{memory.get('score', 0):.2f}] {memory.get('content')}")
    print("\n")

    print("Step 5: Updating memories...")
    requests.put(
        f"https://app.backboard.io/api/assistants/{assistant.assistant_id}/memories/{memory_id}",
        headers={"X-API-Key": api_key},
        json={
            "content": "User is a weirdo who majors in Computer Science and minors in art history at university."
        }
    )
    print(f"Updated memory ID: {memory_id}\n")

    print("Step 6: Deleting memory...")
    requests.delete(
        f"https://app.backboard.io/api/assistants/{assistant.assistant_id}/memories/{memory_id}",
        headers={"X-API-Key": api_key}
    )
    print(f"Deleted memory ID: {memory_id}\n")

    print("Step 7: Checking memory stats...")
    response_stats = requests.get(
        f"https://app.backboard.io/api/assistants/{assistant.assistant_id}/memories/stats",
        headers={"X-API-Key": api_key}
    )
    stats = response_stats.json()
    print(f"Total memories remaining: {stats.get('total_count')}")

asyncio.run(main())