import uuid
import threading
import http.server
import socketserver
from typing import List, Dict, Any, Set
from logger import logger

from app.db.in_memory_db import InMemoryDatabase


class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, server_uuid=None, return_data=None, db=None, **kwargs):
        self.server_uuid = server_uuid
        self.return_data = return_data
        self.db = db
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Log visitor IP
        if self.server_uuid and self.db:
            client_ip = self.client_address[0]
            self.db.add_visitor(self.server_uuid, client_ip)

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(self.return_data.encode())


class ServerManager:
    def __init__(self):
        self.active_servers: Dict[str, Dict[str, Any]] = {}
        self.db = InMemoryDatabase()

    def start_server(self, port, page_path: str, return_data: str) -> str:
        logger.info(f"Start new server: port:'{port}', page_path: '{page_path}', data: {return_data} ")
        # Generate unique UUID for this server
        server_uuid = str(uuid.uuid4())

        # Create custom request handler with specific parameters
        def create_handler(*args, **kwargs):
            return CustomRequestHandler(
                *args,
                server_uuid=server_uuid,
                return_data=return_data,
                db=self.db,
                **kwargs
            )

        # Create and start server
        try:
            handler = socketserver.TCPServer(("", port), create_handler)

            # Run server in a separate thread
            def run_server():
                handler.serve_forever()

            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()

            # Store server information
            self.active_servers[server_uuid] = {
                'handler': handler,
                'port': port,
                'page_path': page_path,
                'thread': server_thread
            }

            # Save server details in database
            self.db.add_server(server_uuid, port, page_path, return_data)

            return server_uuid

        except OSError as e:
            logger.error(f"Could not start server: {e}")
            raise ValueError(f"Could not start server: {e}")

    def stop_server(self, server_uuid: str) -> List[str]:
        logger.info(f"Stop server: uuid: {server_uuid}")
        if server_uuid not in self.active_servers:
            raise ValueError(f"No server found with UUID {server_uuid}")

        # Get visitor IPs before removing the server
        visitors = self.db.get_server_visitors(server_uuid)

        # Stop the server
        server_info = self.active_servers[server_uuid]
        server_info['handler'].shutdown()
        server_info['handler'].server_close()

        # Remove from active servers
        del self.active_servers[server_uuid]

        # Remove from database
        self.db.remove_server(server_uuid)

        return visitors

    def list_active_servers(self) -> List[Dict[str, Any]]:
        return [
            {
                'uuid': uuid,
                'port': info['port'],
                'page_path': info['page_path']
            }
            for uuid, info in self.active_servers.items()
        ]