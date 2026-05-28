from typing import Dict, List
from models.link import Link
from models.lsdb import LSDB
from models.routing_table import RoutingTable
from models.packet import HelloPacket
from models.lsa import LSA
from algorithms.dijkstra import calculate_spf, get_path
from utils.logger import router_log, lsa_log, spf_log

class Router:
    def __init__(self, router_id: str):
        self.router_id = router_id
        self.state = "ACTIVE"
        self.neighbors: Dict[str, str] = {}  
        self.interfaces: List[Link] = []     
        self.lsdb = LSDB()
        self.routing_table = RoutingTable()
        self.lsa_seq_num = 0  
        self.spf_tree = {}    
        self.spf_runs = 0     

    def add_interface(self, link: Link):
        self.interfaces.append(link)
        router_log.debug(f"[{self.router_id}] Added interface to {link.dest_id} with cost {link.cost}")

    def remove_interface(self, dest_id: str):
        self.interfaces = [link for link in self.interfaces if link.dest_id != dest_id]
        if dest_id in self.neighbors:
            del self.neighbors[dest_id]
        router_log.warning(f"[{self.router_id}] Đã gỡ bỏ interface tới {dest_id}. Đang sinh LSA mới...")
        return self.generate_lsa()

    def build_graph_from_lsdb(self) -> Dict[str, Dict[str, int]]:
        graph = {}
        for adv_router, lsa in self.lsdb.lsas.items():
            graph[adv_router] = lsa.link_info
        if self.router_id not in graph:
            graph[self.router_id] = {}
        for lsa in self.lsdb.lsas.values():
            for neighbor in lsa.link_info.keys():
                if neighbor not in graph:
                    graph[neighbor] = {}
        return graph

    def generate_hello(self) -> HelloPacket:
        return HelloPacket(sender_id=self.router_id, known_neighbors=list(self.neighbors.keys()))

    def receive_hello(self, packet: HelloPacket):
        sender = packet.sender_id
        if sender not in self.neighbors:
            self.neighbors[sender] = "INIT"
            router_log.info(f"[{self.router_id}] Đã nhận HELLO từ {sender} -> Trạng thái: INIT")
        if self.router_id in packet.known_neighbors:
            if self.neighbors[sender] != "FULL":
                self.neighbors[sender] = "FULL"
                router_log.info(f"[{self.router_id}] Thấy ID của mình trong HELLO của {sender} -> Trạng thái: FULL")

    def generate_lsa(self):
        self.lsa_seq_num += 1
        link_info = {link.dest_id: link.cost for link in self.interfaces}
        lsa = LSA(adv_router=self.router_id, seq_num=self.lsa_seq_num, link_info=link_info)
        self.lsdb.update_lsa(lsa)
        # Tự động chạy lại thuật toán cho chính mình khi Topology cục bộ thay đổi
        spf_log.info(f"[{self.router_id}] Tự kích hoạt SPF Recalculation do cáp thay đổi...")
        local_graph = self.build_graph_from_lsdb()
        self.generate_routing_table(local_graph)
        return lsa

    def receive_lsa(self, lsa) -> bool:
        is_new = self.lsdb.update_lsa(lsa)
        if is_new:
            lsa_log.info(f"[{self.router_id}] Cập nhật LSDB: Nhận LSA mới từ {lsa.adv_router} (Seq: {lsa.seq_num})")
            spf_log.info(f"[{self.router_id}] Kích hoạt SPF Recalculation...")
            local_graph = self.build_graph_from_lsdb()
            self.generate_routing_table(local_graph)
        return is_new
    
    def add_neighbor(self, neighbor_id: str):
        self.neighbors[neighbor_id] = "INIT"
        router_log.info(f"[{self.router_id}] Discovered neighbor: {neighbor_id}")

    def __repr__(self):
        return f"Router({self.router_id})"

    def generate_routing_table(self, graph: Dict[str, Dict[str, int]]):
        self.spf_runs += 1    
        distances, previous_nodes = calculate_spf(graph, self.router_id)
        self.spf_tree = previous_nodes 
        self.routing_table.entries.clear() 

        for dest_id, total_cost in distances.items():
            if dest_id == self.router_id or total_cost == float('inf'):
                continue
            path = get_path(previous_nodes, self.router_id, dest_id)
            if not path:
                continue
            next_hop = path[1] if len(path) > 1 else dest_id
            out_interface = f"eth-{next_hop}"
            self.routing_table.add_route(dest_id, next_hop, total_cost, path, out_interface)
            
        spf_log.info(f"[{self.router_id}] Cập nhật xong Bảng định tuyến!")
