import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link
from models.topology import Topology

def main():
    print("=== MÔ PHỎNG OSPF LSA FLOODING ===")
    topo = Topology()
    
    # 1. Tạo 3 Router: R1 nối R2, R2 nối R3 (R1 và R3 không nối trực tiếp)
    r1, r2, r3 = Router("R1"), Router("R2"), Router("R3")
    topo.add_router(r1); topo.add_router(r2); topo.add_router(r3)
    
    topo.add_link(Link("R1", "R2", 100.0)); topo.add_link(Link("R2", "R1", 100.0))
    topo.add_link(Link("R2", "R3", 50.0));  topo.add_link(Link("R3", "R2", 50.0))
    
    print("\n--- BƯỚC 1: R1 SINH LSA VÀ FLOOD VÀO MẠNG ---")
    # R1 tự tạo bản tin LSA của mình (mang thông tin nối với R2)
    lsa_r1 = r1.generate_lsa()
    print(f"R1 phát: {lsa_r1}")
    
    # R1 bắt đầu flood qua Topology
    topo.flood_lsa(source_router_id="R1", lsa=lsa_r1)
    
    print("\n--- BƯỚC 2: KIỂM TRA LSDB CỦA R3 ---")
    # Dù R1 và R3 không nối trực tiếp, R3 vẫn phải có LSA của R1 nhờ R2 flood hộ
    r3.lsdb.display()

if __name__ == "__main__":
    main()