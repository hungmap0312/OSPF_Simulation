import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link
from models.topology import Topology

def main():
    print("=== NGHIỆM THU GIAI ĐOẠN 2: ROUTING TABLE INTERFACE & ROUTER FAILURE ===")
    topo = Topology()
    
    r1, r2, r3 = Router("R1"), Router("R2"), Router("R3")
    topo.add_router(r1); topo.add_router(r2); topo.add_router(r3)
    
    # Thiết lập đường truyền: R1-R2 (Cáp nhanh), R1-R3-R2 (Cáp chậm)
    topo.add_link(Link("R1", "R2", 100.0)); topo.add_link(Link("R2", "R1", 100.0))
    topo.add_link(Link("R1", "R3", 50.0));  topo.add_link(Link("R3", "R1", 50.0))
    topo.add_link(Link("R3", "R2", 50.0));  topo.add_link(Link("R2", "R3", 50.0))
    
    print("\n--- 1. ĐỒNG BỘ MẠNG BAN ĐẦU ---")
    topo.flood_lsa("R1", r1.generate_lsa())
    topo.flood_lsa("R2", r2.generate_lsa())
    topo.flood_lsa("R3", r3.generate_lsa())
    
    print("\n--- 2. BẢNG ĐỊNH TUYẾN CỦA R1 (ĐÃ BỔ SUNG INTERFACE) ---")
    # Kiểm tra xem cấu trúc "via [Next_Hop] on [Interface]" đã xuất hiện chưa
    r1.routing_table.display()
    
    print("\n--- 3. MÔ PHỎNG SỰ CỐ ROUTER FAILURE ---")
    # Mô phỏng R2 bị sập nguồn/rút khỏi mạng hoàn toàn
    topo.remove_router("R2")
    
    print("\n--- 4. BẢNG ĐỊNH TUYẾN CỦA R1 SAU KHI R2 SẬP ---")
    r1.routing_table.display()

if __name__ == "__main__":
    main()