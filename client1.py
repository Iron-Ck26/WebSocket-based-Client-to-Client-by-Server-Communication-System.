import asyncio
import websockets

async def client1():
    uri = "ws://0.0.0.0:8665"
    async with websockets.connect(uri) as websocket:
        while True:
            action = input("Press 's' to send a message from client 1: ")
            if action == 's':
                user_input = input("Enter message for client 2: ")
                await websocket.send(user_input)
            else:
                print("Exiting...")
                break

            # Wait to receive a response from client 2
            response = await websocket.recv()
            print("Received message from client 2:", response)

asyncio.run(client1())
