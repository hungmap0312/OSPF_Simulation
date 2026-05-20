import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link
from models.topology import Topology

def main():
    print("=== 1. Khởi tạo Topology OSPF ===")
    topo = Topology()
    
    # Tạo 3 Router
    r1 = Router("1.1.1.1")
    r2 = Router("2.2.2.2")
    r3 = Router("3.3.3.3")
    
    # Nạp Router vào Topology
    topo.add_router(r1)
    topo.add_router(r2)
    topo.add_router(r3)
    
    print("\n=== 2. Kết nối các Router ===")
    # Nối R1 và R2 bằng cáp xịn (FastEthernet - 100 Mbps) -> Cost dự kiến: 1
    topo.add_link(Link(source_id="1.1.1.1", dest_id="2.2.2.2", bandwidth_mbps=100.0))
    topo.add_link(Link(source_id="2.2.2.2", dest_id="1.1.1.1", bandwidth_mbps=100.0))
    
    # Nối R2 và R3 bằng cáp chậm (Ethernet - 10 Mbps) -> Cost dự kiến: 10
    topo.add_link(Link(source_id="2.2.2.2", dest_id="3.3.3.3", bandwidth_mbps=10.0))
    topo.add_link(Link(source_id="3.3.3.3", dest_id="2.2.2.2", bandwidth_mbps=10.0))
    
    print("\n=== 3. Kết quả Đồ thị kề (Adjacency Graph) ===")
    for r_id, neighbors in topo.adjacency_graph.items():
        print(f"Router {r_id} kết nối với: {neighbors}")

if __name__ == "__main__":
    main()
