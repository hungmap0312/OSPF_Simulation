from typing import Dict, List
from models.router import Router
from models.link import Link

class Topology:
    def __init__(self):
        # Lưu trữ các Router theo Router ID
        self.routers: Dict[str, Router] = {} 
        # Lưu trữ tất cả các đường truyền trong mạng
        self.links: List[Link] = []          
        # Đồ thị kề phục vụ thuật toán SPF: {router_id: {neighbor_id: cost}}
        self.adjacency_graph: Dict[str, Dict[str, int]] = {} 
        
        # Placeholder cho Event Queue (sẽ dùng ở Giai đoạn 5)
        self.event_queue = [] 

    def add_router(self, router: Router):
        """Thêm một Router vào hệ thống mạng."""
        self.routers[router.router_id] = router
        # Khởi tạo node rỗng trong đồ thị kề
        self.adjacency_graph[router.router_id] = {}
        print(f"[Topology] Added Router: {router.router_id}")

    def add_link(self, link: Link):
        """Thêm một đường truyền và tự động cập nhật kết nối cho Router."""
        self.links.append(link)
        
        # Cập nhật đồ thị kề (Adjacency Graph)
        self.adjacency_graph[link.source_id][link.dest_id] = link.cost
        
        # Gắn link vào interface của Router nguồn và cập nhật láng giềng
        if link.source_id in self.routers:
            self.routers[link.source_id].add_interface(link)
            self.routers[link.source_id].add_neighbor(link.dest_id)
            
        print(f"[Topology] Added Link: {link.source_id} -> {link.dest_id} (Cost: {link.cost})")

    def get_neighbor_list(self, router_id: str) -> List[str]:
        """Lấy danh sách láng giềng của một router từ đồ thị kề."""
        if router_id in self.adjacency_graph:
            return list(self.adjacency_graph[router_id].keys())
        return []

    def flood_lsa(self, source_router_id: str, lsa):
        """Mô phỏng LSA Flooding: Lan truyền LSA tới tất cả láng giềng."""
        neighbors = self.get_neighbor_list(source_router_id)
        for neighbor_id in neighbors:
            if neighbor_id in self.routers:
                # Gửi LSA cho láng giềng
                is_new = self.routers[neighbor_id].receive_lsa(lsa)
                
                # NẾU Láng giềng thấy đây là LSA mới, nó sẽ tự động flood tiếp cho các node khác
                if is_new:
                    print(f"  -> [Mạng] {neighbor_id} flood tiếp LSA của {lsa.adv_router}")
                    self.flood_lsa(neighbor_id, lsa)
    
    def __repr__(self):
        return f"Topology(Routers: {len(self.routers)}, Links: {len(self.links)})"
