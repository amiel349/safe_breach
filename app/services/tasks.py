import socket
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

import requests
from flask import Flask
import requests
from app.db.db_interface import IDatabase
from app.services.server_manager import ServerManager
from app.services.task_interface import ITask
from logger import logger

SERVER_MANAGER = ServerManager()


class DNSQueryTask(ITask):
    def __init__(self, domain: str):
        self.domain = domain

    def execute(self):
        try:

            logger.info(f"Executing DNSQueryTask for domain: {self.domain}")
            return socket.gethostbyname(self.domain)
        except Exception as e:
            logger.error(f"DNSQueryTask failed for domain {self.domain}: {e}")
            raise RuntimeError(f"Failed to resolve domain {self.domain}: {e}")


class HTTPGetTask(ITask):
    def __init__(self, domain: str, port: int, uri: str):
        self.url = f"http://{domain}:{port}{uri}"

    def execute(self):
        try:
            logger.info(f"Executing HTTPGetTask for URL: {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"HTTPGetTask failed for URL {self.url}: {e}")
            raise RuntimeError(f"Failed to perform HTTP GET: {e}")


class StartHTTPServerTask(ITask):
    def __init__(self, port: int, uri: str, data_to_return: str):
        self.port= port
        self.uri = uri
        self.data_to_return = data_to_return

    def execute(self):
        server_uuid = SERVER_MANAGER.start_server(self.port, self.uri, self.data_to_return)
        return {
            "status": "success",
            "uuid": server_uuid,
            "message": f"Server started on port {self.port} with path {self.uri}"
        }


class StopHTTPServerTask(ITask):
    def __init__(self, uuid: str):
        self.server_uuid = uuid

    def execute(self):
        try:
            visitors = SERVER_MANAGER.stop_server(self.server_uuid)
            return {
                "status": "success",
                "uuid": self.server_uuid,
                "visitors": visitors,
                "message": f"Server {self.server_uuid} stopped"
            }
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e)
            }
