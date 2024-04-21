import asyncio
import websockets

# Set to store connected clients
clients = set()

async def handle_client(websocket, path):
    # Add client to the set of connected clients
    clients.add(websocket)
    print(f"New client connected: {websocket}")

    try:
        async for message in websocket:
            if message == 's':
                print("Starting Face 1 for client...")
                await broadcast(message, exclude_client=websocket)
            elif message == 'r':
                print("Starting Face 2 for client...")
                await broadcast(message, exclude_client=websocket)
            else:
                await broadcast(message, exclude_client=websocket)
    except websockets.exceptions.ConnectionClosedOK:
        # Handle client disconnection
        print("Client disconnected")
    finally:
        # Remove client from the set upon disconnection
        clients.remove(websocket)
        print(f"Client disconnected: {websocket}")

async def broadcast(message, exclude_client=None):
    # Iterate over all connected clients and send the message
    if clients:
        tasks = []
        for client in clients:
            if client != exclude_client:
                tasks.append(client.send(message))
        await asyncio.gather(*tasks)

# Start WebSocket server
start_server = websockets.serve(handle_client, "0.0.0.0", 8665) # Replace 0.0.0.0 with your desired IP address

# Run the server until it is stopped
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
