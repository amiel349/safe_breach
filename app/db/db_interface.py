from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IDatabase(ABC):
    @abstractmethod
    def add_server(self, server_uuid: str, port: int, page_path: str, return_data: str):
        pass

    @abstractmethod
    def add_visitor(self, server_uuid: str, ip_address: str):
        pass

    @abstractmethod
    def get_server_details(self, server_uuid: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_server_visitors(self, server_uuid: str) -> List[str]:
        pass

    @abstractmethod
    def remove_server(self, server_uuid: str):
        pass
