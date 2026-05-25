from typing import Dict, List
from models.router import Router
from models.link import Link
from utils.logger import system_log, error_log, lsa_log

class Topology:
    def __init__(self, simulator=None):
        self.routers: Dict[str, Router] = {} 
        self.links: List[Link] = []          
        self.adjacency_graph: Dict[str, Dict[str, int]] = {} 
        self.simulator = simulator  # Kết nối với bộ lõi mô phỏng sự kiện
        self.flood_count = 0  

    def add_router(self, router: Router):
        self.routers[router.router_id] = router
        self.adjacency_graph[router.router_id] = {}
        system_log.info(f"Added Router: {router.router_id}")

    def add_link(self, link: Link):
        self.links.append(link)
        self.adjacency_graph[link.source_id][link.dest_id] = link.cost
        if link.source_id in self.routers:
            self.routers[link.source_id].add_interface(link)
            self.routers[link.source_id].add_neighbor(link.dest_id)
        system_log.info(f"Added Link: {link.source_id} -> {link.dest_id} (Cost: {link.cost})")

    def remove_link(self, source_id: str, dest_id: str):
        self.links = [link for link in self.links if not (link.source_id == source_id and link.dest_id == dest_id)]
        if source_id in self.adjacency_graph and dest_id in self.adjacency_graph[source_id]:
            del self.adjacency_graph[source_id][dest_id]
        if source_id in self.routers:
            new_lsa = self.routers[source_id].remove_interface(dest_id)
            if new_lsa:
                self.flood_lsa(source_id, new_lsa)
        error_log.warning(f"LINK FAILURE: Đã ngắt kết nối {source_id} -> {dest_id}")

    def update_link_cost(self, source_id: str, dest_id: str, new_bandwidth: float):
        for link in self.links:
            if link.source_id == source_id and link.dest_id == dest_id:
                link.update_bandwidth(new_bandwidth)
                self.adjacency_graph[source_id][dest_id] = link.cost
                if source_id in self.routers:
                    new_lsa = self.routers[source_id].generate_lsa()
                    self.flood_lsa(source_id, new_lsa)
                break
    
    def remove_router(self, router_id: str):
        if router_id in self.routers:
            affected_neighbors = self.get_neighbor_list(router_id)
            del self.routers[router_id]
            if router_id in self.adjacency_graph:
                del self.adjacency_graph[router_id]
            self.links = [link for link in self.links if link.source_id != router_id and link.dest_id != router_id]
            for neighbor in affected_neighbors:
                if neighbor in self.adjacency_graph and router_id in self.adjacency_graph[neighbor]:
                    del self.adjacency_graph[neighbor][router_id]
                    if neighbor in self.routers:
                        new_lsa = self.routers[neighbor].remove_interface(router_id)
                        self.flood_lsa(neighbor, new_lsa)
            error_log.warning(f"ROUTER FAILURE: Router {router_id} đã sập.")
            self.broadcast_event(f"Router {router_id} DOWN")

    def broadcast_event(self, event: str):
        system_log.info(f"Ghi nhận sự kiện: {event}")

    def get_neighbor_list(self, router_id: str) -> List[str]:
        if router_id in self.adjacency_graph:
            return list(self.adjacency_graph[router_id].keys())
        return []

    def _deliver_lsa(self, target_router_id: str, lsa):
        """Hàm xử lý khi gói tin LSA thực sự 'chạm' đến Router đích sau một độ trễ vật lý."""
        if target_router_id in self.routers:
            self.flood_count += 1
            is_new = self.routers[target_router_id].receive_lsa(lsa)
            if is_new:
                lsa_log.info(f"[Mạng] {target_router_id} flood tiếp LSA của {lsa.adv_router}")
                self.flood_lsa(target_router_id, lsa)

    def flood_lsa(self, source_router_id: str, lsa):
        """Lan truyền LSA bằng cách đẩy vào Simulator Queue (mô phỏng delay truyền dẫn)."""
        neighbors = self.get_neighbor_list(source_router_id)
        for neighbor_id in neighbors:
            # Tìm Delay thực tế của đường link (mặc định là 1.0ms)
            delay = 1.0
            for link in self.links:
                if link.source_id == source_router_id and link.dest_id == neighbor_id:
                    delay = link.delay
                    break
            
            # Gắn sự kiện vào dòng thời gian của Simulator
            if self.simulator:
                self.simulator.schedule(delay, "LSA_ARRIVAL", self._deliver_lsa, target_router_id=neighbor_id, lsa=lsa)
            else:
                self._deliver_lsa(neighbor_id, lsa) # Fallback nếu chạy không có simulator
