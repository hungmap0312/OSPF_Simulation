import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link
from models.topology import Topology
from models.lsa import LSA  # <-- Bổ sung import class LSA

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

    # ---------------------------------------------------------
    # PHẦN CODE MỚI THÊM CHO BƯỚC 4: TEST LSA VÀ LSDB
    # ---------------------------------------------------------
    print("\n=== 4. Kiểm thử LSA và LSDB cho Router 1.1.1.1 ===")
    
    # R1 nhìn vào đồ thị kề ở trên, thấy mình chỉ kết nối với R2 (Cost=1)
    # R1 sinh ra bản tin LSA version 1 để thông báo điều này cho mạng
    lsa_v1 = LSA(adv_router="1.1.1.1", seq_num=1, link_info={"2.2.2.2": 1})
    
    print("[Mô phỏng] R1 tự lưu LSA bản 1 vào LSDB của mình...")
    r1.lsdb.update_lsa(lsa_v1)
    
    print("[Mô phỏng] Mạng chập chờn, R1 cập nhật LSA bản 2 với cost tăng lên 50")
    lsa_v2 = LSA(adv_router="1.1.1.1", seq_num=2, link_info={"2.2.2.2": 50})
    r1.lsdb.update_lsa(lsa_v2)
    
    print("[Mô phỏng] R1 nhận lại LSA bản 1 từ router khác (Bản cũ -> Bỏ qua)")
    r1.lsdb.update_lsa(lsa_v1) 
    
    print("\n=== 5. Trạng thái cơ sở dữ liệu cuối cùng của R1 ===")
    r1.lsdb.display()
    r1.routing_table.display()

if __name__ == "__main__":
    main()
