from datetime import datetime
from typing import List, Dict, Any, Set, Optional
from app.db.db_interface import IDatabase
from logger import logger


class InMemoryDatabase(IDatabase):
    def __init__(self):
        # Dictionary to store server information
        self.servers: Dict[str, Dict[str, Any]] = {}

        # Dictionary to store visitors for each server
        self.visitors: Dict[str, Set[str]] = {}

        # Track used ports
        self.used_ports: Set[int] = set()

    def add_server(self, server_uuid: str, port: int, page_path: str, return_data: str):
        logger.info(f"Add new server: port:'{port}', page_path: '{page_path}', data: {return_data}")
        self.servers[server_uuid] = {
            'uuid': server_uuid,
            'port': port,
            'page_path': page_path,
            'return_data': return_data,
            'created_at': datetime.now()
        }
        # Initialize visitors set for this server
        self.visitors[server_uuid] = set()
        # Mark port as used
        self.used_ports.add(port)

    def add_visitor(self, server_uuid: str, ip_address: str):
        logger.info(f"add new visitor: ip: {ip_address}")
        if server_uuid in self.visitors:
            self.visitors[server_uuid].add(ip_address)

    def get_server_details(self, server_uuid: str) -> Dict[str, Any]:
        return self.servers.get(server_uuid)

    def get_server_visitors(self, server_uuid: str) -> List[str]:
        return list(self.visitors.get(server_uuid, set()))

    def remove_server(self, server_uuid: str):
        logger.info(f"Remove server: {server_uuid}")
        # Remove server and its visitors
        if server_uuid in self.servers:
            # Remove the port from used ports
            self.used_ports.remove(self.servers[server_uuid]['port'])

            self.servers.pop(server_uuid, None)
            self.visitors.pop(server_uuid, None)
