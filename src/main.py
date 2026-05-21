import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link
from models.topology import Topology

def main():
    print("=== MÔ PHỎNG HỘI TỤ MẠNG & THỐNG KÊ (PHASE 4.5) ===")
    topo = Topology()
    r1, r2, r3 = Router("R1"), Router("R2"), Router("R3")
    topo.add_router(r1); topo.add_router(r2); topo.add_router(r3)
    
    # Thiết lập đường truyền
    topo.add_link(Link("R1", "R2", 100.0)); topo.add_link(Link("R2", "R1", 100.0))
    topo.add_link(Link("R1", "R3", 50.0));  topo.add_link(Link("R3", "R1", 50.0))
    topo.add_link(Link("R3", "R2", 50.0));  topo.add_link(Link("R2", "R3", 50.0))
    
    print("\n--- ĐỒNG BỘ MẠNG BAN ĐẦU ---")
    topo.flood_lsa("R1", r1.generate_lsa())
    topo.flood_lsa("R2", r2.generate_lsa())
    topo.flood_lsa("R3", r3.generate_lsa())
    
    # Reset biến đếm sau khi đồng bộ khởi tạo để chỉ tính riêng phần hội tụ sự cố
    topo.flood_count = 0
    r1.spf_runs = r2.spf_runs = r3.spf_runs = 0


    print("\n--- BẮT ĐẦU SỰ CỐ ĐỨT CÁP R1 -> R2 ---")
    
    # Bắt đầu bấm giờ
    start_time = time.time()
    
    # Cắt đứt cáp (Hành động này sẽ tự động trigger Flooding và SPF Recalculation)
    topo.remove_link("R1", "R2")
    topo.remove_link("R2", "R1")
    
    # Kết thúc bấm giờ
    end_time = time.time()
    
    # Tính thời gian bằng mili-giây (ms)
    convergence_time_ms = (end_time - start_time) * 1000

    print("\n=== KẾT QUẢ THỐNG KÊ HỘI TỤ (CONVERGENCE METRICS) ===")
    print(f"1. Thời gian hội tụ (Convergence Time): {convergence_time_ms:.4f} ms")
    print(f"2. Số lượng bản tin LSA lan truyền (Flooding Count): {topo.flood_count} gói")
    print(f"3. Số lần chạy lại thuật toán Dijkstra (SPF Runs):")
    print(f"   - Router R1: {r1.spf_runs} lần")
    print(f"   - Router R2: {r2.spf_runs} lần")
    print(f"   - Router R3: {r3.spf_runs} lần")
    
    print("\n[Bảng định tuyến của R1 sau khi hội tụ]")
    r1.routing_table.display()

if __name__ == "__main__":
    main()