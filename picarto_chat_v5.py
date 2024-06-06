import asyncio
import websockets
import json
import time
from datetime import datetime

async def connect_and_communicate():
    uri = "wss://chat.picarto.tv/chat/token="
    

    
    while True:
        # Get the current date in the format YYYY-MM-DD
        current_date = datetime.now().strftime("%Y-%m-%d")
        file_name = f"{current_date}.txt"
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(json.dumps({"type": "welcomeMessage"}))
                await websocket.send(json.dumps({"type": "accessLevelMessage"}))
                await websocket.send(json.dumps({"type": "multistreamMessage"}))
                await websocket.send(json.dumps({"type": "chatNext", "page": 1, "paginated": False}))
                await websocket.send(json.dumps({"type": "settings"}))
                await websocket.send(json.dumps({"type": "topChips"}))

                while True:
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=50)
                        response_json = json.loads(response)
                        if "t" in response_json and response_json["t"] == "c":
                            with open(file_name, "a") as file:
                                file.write(json.dumps(response_json) + '\n')
                            print(response_json)
                    except asyncio.TimeoutError:
                        print("Sending ping message...")
                        await websocket.send(json.dumps({"type": "ping", "message": "__ping__"}))
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed unexpectedly. Reconnecting in 10 seconds...")
            await asyncio.sleep(10)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in 10 seconds...")
            await asyncio.sleep(10)

# Run the WebSocket connection
#asyncio.get_event_loop().run_until_complete(connect_and_communicate())
# Modern approach to run the asyncio event loop
asyncio.run(connect_and_communicate())