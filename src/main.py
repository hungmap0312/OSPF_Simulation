import sys
import os

# Thêm thư mục gốc vào sys.path để Python nhận diện được module 'models'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link

def main():
    print("=== Khởi tạo OSPF Simulation ===")
    
    # 1. Tạo 2 Router
    r1 = Router("1.1.1.1")
    r2 = Router("2.2.2.2")
    
    # 2. Tạo đường truyền FastEthernet (100 Mbps) giữa R1 và R2
    link_r1_to_r2 = Link(source_id=r1.router_id, dest_id=r2.router_id, bandwidth_mbps=100.0)
    link_r2_to_r1 = Link(source_id=r2.router_id, dest_id=r1.router_id, bandwidth_mbps=100.0)
    
    # 3. Gắn đường truyền vào Router
    r1.add_interface(link_r1_to_r2)
    r2.add_interface(link_r2_to_r1)
    
    # 4. Mô phỏng quá trình khám phá Neighbor (Neighbor Discovery)
    r1.add_neighbor(r2.router_id)
    r2.add_neighbor(r1.router_id)
    
    print("\n=== Trạng thái hiện tại ===")
    print(r1)
    print(r2)

if __name__ == "__main__":
    main()
