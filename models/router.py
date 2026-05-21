from typing import Dict, List
from models.link import Link
from models.lsdb import LSDB
from models.routing_table import RoutingTable
from models.packet import HelloPacket
from models.lsa import LSA
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
        self.lsa_seq_num = 0  # ĐẾM VERSION CỦA LSA
        self.spf_tree = {}    # Lưu trữ cây SPF Tree (Giai đoạn 2.1)
        self.spf_runs = 0     # Đếm số lần chạy thuật toán SPF

    def add_interface(self, link: Link):
        """Thêm một đường truyền (interface) vào router."""
        self.interfaces.append(link)
        print(f"[Router {self.router_id}] Added interface to {link.dest_id} with cost {link.cost}")

    def remove_interface(self, dest_id: str):
        """Gỡ bỏ kết nối khi có sự cố đứt cáp và sinh LSA mới."""
        self.interfaces = [link for link in self.interfaces if link.dest_id != dest_id]
        if dest_id in self.neighbors:
            del self.neighbors[dest_id]
        print(f"[Router {self.router_id}] Đã gỡ bỏ interface tới {dest_id}. Đang sinh LSA mới...")
        return self.generate_lsa()

    def build_graph_from_lsdb(self) -> Dict[str, Dict[str, int]]:
        """Xây dựng lại đồ thị mạng cục bộ từ kho LSDB của chính router này."""
        graph = {}
        
        # 1. Nạp tất cả thông tin đã biết từ LSDB vào đồ thị
        for adv_router, lsa in self.lsdb.lsas.items():
            graph[adv_router] = lsa.link_info
            
        # 2. Đảm bảo bản thân router luôn là 1 đỉnh (node) trong đồ thị (tránh KeyError)
        if self.router_id not in graph:
            graph[self.router_id] = {}
            
        # 3. Đảm bảo mọi neighbor xuất hiện trong các LSA đều có mặt như một đỉnh
        for lsa in self.lsdb.lsas.values():
            for neighbor in lsa.link_info.keys():
                if neighbor not in graph:
                    graph[neighbor] = {}
                    
        return graph

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

    def generate_lsa(self):
        """Tạo bản tin LSA chứa thông tin các đường truyền hiện tại của Router."""
        self.lsa_seq_num += 1
        link_info = {}
        # Đóng gói thông tin các láng giềng trực tiếp và cost tương ứng
        for link in self.interfaces:
            link_info[link.dest_id] = link.cost
        
        lsa = LSA(adv_router=self.router_id, seq_num=self.lsa_seq_num, link_info=link_info)
        # Tự lưu vào LSDB của chính mình trước tiên
        self.lsdb.update_lsa(lsa)
        return lsa

    def receive_lsa(self, lsa) -> bool:
        """Nhận LSA từ mạng. Trả về True nếu đây là LSA mới (để tiếp tục Flooding)."""
        is_new = self.lsdb.update_lsa(lsa)
        if is_new:
            print(f"[Router {self.router_id}] Cập nhật LSDB: Nhận LSA mới từ {lsa.adv_router} (Seq: {lsa.seq_num})")
            
            # --- 4.4. SPF Recalculation: Tự động chạy lại Dijkstra khi có thay đổi Topology ---
            print(f"[Router {self.router_id}] Kích hoạt SPF Recalculation...")
            local_graph = self.build_graph_from_lsdb()
            self.generate_routing_table(local_graph)
            
        return is_new
    
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
        self.spf_runs += 1    # Mỗi lần gọi hàm là tăng bộ đếm lên 1

        # 1. Chạy thuật toán để lấy danh sách cost và node liền trước
        distances, previous_nodes = calculate_spf(graph, self.router_id)
        self.spf_tree = previous_nodes # Lưu trữ SPF Tree

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

