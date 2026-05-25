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
        self.flood_count = 0  # Đếm số lần truyền LSA trong mạng

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

    def remove_link(self, source_id: str, dest_id: str):
        """Mô phỏng sự cố đứt cáp (Link Failure - Giai đoạn 4.6)."""
        # Xóa khỏi danh sách links
        self.links = [link for link in self.links if not (link.source_id == source_id and link.dest_id == dest_id)]
        
        # Xóa khỏi đồ thị kề
        if source_id in self.adjacency_graph and dest_id in self.adjacency_graph[source_id]:
            del self.adjacency_graph[source_id][dest_id]
            
        # Báo cho Router nguồn gỡ interface và tự động flood LSA mới thông báo đứt cáp
        if source_id in self.routers:
            new_lsa = self.routers[source_id].remove_interface(dest_id)
            if new_lsa:
                self.flood_lsa(source_id, new_lsa)
        print(f"[Topology] LINK FAILURE: Đã ngắt kết nối {source_id} -> {dest_id}")

    def update_link_cost(self, source_id: str, dest_id: str, new_bandwidth: float):
        """Mô phỏng sự kiện thay đổi băng thông (Cost Change - Giai đoạn 4.6)."""
        for link in self.links:
            if link.source_id == source_id and link.dest_id == dest_id:
                link.update_bandwidth(new_bandwidth)
                self.adjacency_graph[source_id][dest_id] = link.cost
                # Báo cho Router nguồn sinh LSA mới cập nhật cost
                if source_id in self.routers:
                    new_lsa = self.routers[source_id].generate_lsa()
                    self.flood_lsa(source_id, new_lsa)
                break
    
    def remove_router(self, router_id: str):
        """Mô phỏng sự cố hỏng hóc hoặc rút bớt thiết bị Router (Giai đoạn 2.3)."""
        if router_id in self.routers:
            # 1. Tìm các router láng giềng đang kết nối trực tiếp tới router này
            affected_neighbors = self.get_neighbor_list(router_id)
            
            # 2. Xóa router khỏi danh sách quản lý
            del self.routers[router_id]
            if router_id in self.adjacency_graph:
                del self.adjacency_graph[router_id]
                
            # 3. Xóa các đường link liên quan trong danh sách tổng
            self.links = [link for link in self.links if link.source_id != router_id and link.dest_id != router_id]
            
            # 4. Cập nhật đồ thị kề của các láng giềng và yêu cầu họ flood LSA mới
            for neighbor in affected_neighbors:
                if neighbor in self.adjacency_graph and router_id in self.adjacency_graph[neighbor]:
                    del self.adjacency_graph[neighbor][router_id]
                    # Báo láng giềng gỡ interface và phát tán thông tin mạng thay đổi
                    if neighbor in self.routers:
                        new_lsa = self.routers[neighbor].remove_interface(router_id)
                        self.flood_lsa(neighbor, new_lsa)
                        
            print(f"[Topology] ROUTER FAILURE: Router {router_id} đã dừng hoạt động và bị xóa khỏi mạng.")
            self.broadcast_event(f"Router {router_id} DOWN")

    def broadcast_event(self, event: str):
        """Ghi nhận sự kiện hệ thống vào hàng đợi Event Queue (Giai đoạn 2.3)."""
        self.event_queue.append(event)
        print(f"[Event Queue] Ghi nhận sự kiện: {event}")

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
                # Ghi nhận 1 lần LSA được truyền qua link này
                self.flood_count += 1

                # Gửi LSA cho láng giềng
                is_new = self.routers[neighbor_id].receive_lsa(lsa)
                
                # NẾU Láng giềng thấy đây là LSA mới, nó sẽ tự động flood tiếp cho các node khác
                if is_new:
                    print(f"  -> [Mạng] {neighbor_id} flood tiếp LSA của {lsa.adv_router}")
                    self.flood_lsa(neighbor_id, lsa)
    
    def __repr__(self):
        return f"Topology(Routers: {len(self.routers)}, Links: {len(self.links)})"
