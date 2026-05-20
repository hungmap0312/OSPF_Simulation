from typing import Dict, List
from models.link import Link
from models.lsdb import LSDB
from models.routing_table import RoutingTable
from models.packet import HelloPacket
from algorithms.dijkstra import calculate_spf, get_path

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

    def generate_hello(self) -> HelloPacket:
        """Tạo gói tin Hello mang theo danh sách láng giềng hiện tại."""
        return HelloPacket(sender_id=self.router_id, known_neighbors=list(self.neighbors.keys()))

    def receive_hello(self, packet: HelloPacket):
        """Xử lý khi nhận được gói tin Hello từ một Router khác."""
        sender = packet.sender_id
        
        # 1. Nếu đây là lần đầu nghe thấy láng giềng này -> Chuyển trạng thái INIT
        if sender not in self.neighbors:
            self.neighbors[sender] = "INIT"
            print(f"[Router {self.router_id}] Đã nhận HELLO từ {sender} -> Trạng thái: INIT")
            
        # 2. Nếu thấy ID của mình trong gói Hello của đối phương -> Chuyển trạng thái FULL (2-WAY)
        if self.router_id in packet.known_neighbors:
            if self.neighbors[sender] != "FULL":
                self.neighbors[sender] = "FULL"
                print(f"[Router {self.router_id}] Thấy ID của mình trong HELLO của {sender} -> Trạng thái: FULL")

    def add_neighbor(self, neighbor_id: str):
        """Khởi tạo một neighbor mới với trạng thái ban đầu."""
        self.neighbors[neighbor_id] = "INIT"
        print(f"[Router {self.router_id}] Discovered neighbor: {neighbor_id}")

    def __repr__(self):
        return f"Router(ID: {self.router_id}, Neighbors: {list(self.neighbors.keys())})"

    def generate_routing_table(self, graph: Dict[str, Dict[str, int]]):
        """
        Chạy thuật toán Dijkstra và cập nhật Bảng định tuyến (Routing Table).
        """
        # 1. Chạy thuật toán để lấy danh sách cost và node liền trước
        distances, previous_nodes = calculate_spf(graph, self.router_id)
        
        # Xóa bảng định tuyến cũ để tạo mới
        self.routing_table.entries.clear() 

        # 2. Duyệt qua từng đích đến để xây bảng định tuyến
        for dest_id, total_cost in distances.items():
            # Bỏ qua chính nó hoặc các node không thể tới được (cost = vô cực)
            if dest_id == self.router_id or total_cost == float('inf'):
                continue
                
            # 3. Trích xuất đường đi đầy đủ
            path = get_path(previous_nodes, self.router_id, dest_id)
            if not path:
                continue
                
            # 4. Xác định Next-hop (trạm kế tiếp)
            # Nếu đường đi là [R1, R3, R2], thì next_hop từ R1 là R3 (phần tử index 1)
            next_hop = path[1] if len(path) > 1 else dest_id
            
            # 5. Lưu vào Bảng định tuyến
            self.routing_table.add_route(
                destination=dest_id, 
                next_hop=next_hop, 
                total_cost=total_cost, 
                path=path
            )
        print(f"[Router {self.router_id}] Cập nhật xong Bảng định tuyến!")

