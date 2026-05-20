import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link
from models.topology import Topology

def main():
    print("=== KHỞI TẠO MẠNG VÀ ĐỒ THỊ ===")
    topo = Topology()
    r1, r2, r3, r4 = Router("R1"), Router("R2"), Router("R3"), Router("R4")
    
    topo.add_router(r1); topo.add_router(r2); topo.add_router(r3); topo.add_router(r4)
    
    # R1 - R2: Cáp chậm (10Mbps -> Cost 10)
    topo.add_link(Link("R1", "R2", 10.0)); topo.add_link(Link("R2", "R1", 10.0))
    # R1 - R3: Cáp vừa (20Mbps -> Cost 5)
    topo.add_link(Link("R1", "R3", 20.0)); topo.add_link(Link("R3", "R1", 20.0))
    # R3 - R2: Cáp nhanh (50Mbps -> Cost 2)
    topo.add_link(Link("R3", "R2", 50.0)); topo.add_link(Link("R2", "R3", 50.0))
    # R2 - R4: Cáp siêu nhanh (100Mbps -> Cost 1)
    topo.add_link(Link("R2", "R4", 100.0)); topo.add_link(Link("R4", "R2", 100.0))

    print("\n=== ĐỒ THỊ KỀ CỦA MẠNG ===")
    for node, neighbors in topo.adjacency_graph.items():
        print(f"{node}: {neighbors}")

    print("\n=== CHẠY THUẬT TOÁN DIJKSTRA CHO R1 ===")
    # Cho R1 chạy Dijkstra dựa trên đồ thị tổng của toàn mạng
    r1.generate_routing_table(topo.adjacency_graph)
    
    # In bảng định tuyến của R1 ra để xem thuật toán có chọn đường đi vòng qua R3 không
    r1.routing_table.display()

if __name__ == "__main__":
    main()