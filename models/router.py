from typing import Dict, List
from models.link import Link
from models.lsdb import LSDB
from models.routing_table import RoutingTable

class Router:
    def __init__(self, router_id: str):
        self.router_id = router_id
        self.state = "ACTIVE"
        
        # Neighbor Table: Lưu trữ trạng thái của các router láng giềng
        self.neighbors: Dict[str, str] = {}  
        
        # Interface List: Danh sách các link kết nối trực tiếp
        self.interfaces: List[Link] = []     
        
        # LSDB và Routing Table sẽ được khởi tạo chi tiết ở các bước sau
        self.lsdb = LSDB()
        self.routing_table = RoutingTable()

    def add_interface(self, link: Link):
        """Thêm một đường truyền (interface) vào router."""
        self.interfaces.append(link)
        print(f"[Router {self.router_id}] Added interface to {link.dest_id} with cost {link.cost}")

    def add_neighbor(self, neighbor_id: str):
        """Khởi tạo một neighbor mới với trạng thái ban đầu."""
        self.neighbors[neighbor_id] = "INIT"
        print(f"[Router {self.router_id}] Discovered neighbor: {neighbor_id}")

    def __repr__(self):
        return f"Router(ID: {self.router_id}, Neighbors: {list(self.neighbors.keys())})"
