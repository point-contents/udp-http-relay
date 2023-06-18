import asyncio
import aiohttp
import json
import time

UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 5432
HTTP_URL = "http://localhost:4321/"  # Replace with your actual HTTP endpoint

class UDPServerProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        source_ip = addr[0]
        message = data.decode("utf-8")

        # Create JSON payload
        payload = {
            "source_ip": source_ip,
            "timestamp": time.time(),
            "udp_message": message
        }

        headers = {'Content-Type': 'application/json'}

        # Send POST request to HTTP endpoint
        async def send_post_request():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(HTTP_URL, data=json.dumps(payload), headers=headers) as response:
                        if response.status == 200:
                            print("Message sent successfully via HTTP")
                        else:
                            print(f"Failed to send message via HTTP. Response: {await response.text()}")
            except aiohttp.ClientError as e:
                print(f"Failed to send message via HTTP. Error: {str(e)}")

        asyncio.create_task(send_post_request())

# Create the event loop and run the UDP server
loop = asyncio.get_event_loop()
transport, protocol = loop.run_until_complete(loop.create_datagram_endpoint(
    UDPServerProtocol,
    local_addr=(UDP_IP, UDP_PORT)
))
print(f"UDP server listening on {UDP_IP}:{UDP_PORT}")

# Keep the event loop running
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Server stopped by the user")
finally:
    transport.close()
    loop.close()

