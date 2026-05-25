import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link
from models.topology import Topology
from simulation.simulator import Simulator
from utils.logger import system_log

def main():
    system_log.info("Khởi động Hệ thống Mô phỏng Sự kiện Rời rạc (Discrete Event Simulator)")
    
    # 1. Khởi tạo Simulator
    sim = Simulator()
    
    # 2. Khởi tạo Topology và gắn Simulator vào
    topo = Topology(simulator=sim)
    
    # Setup mạng
    r1, r2, r3 = Router("R1"), Router("R2"), Router("R3")
    topo.add_router(r1); topo.add_router(r2); topo.add_router(r3)
    
    topo.add_link(Link("R1", "R2", 100.0, delay=2.0)) # Cáp tới R2 trễ 2ms
    topo.add_link(Link("R2", "R1", 100.0, delay=2.0))
    topo.add_link(Link("R1", "R3", 50.0, delay=5.0))  # Cáp tới R3 chậm hơn, trễ 5ms
    topo.add_link(Link("R3", "R1", 50.0, delay=5.0))
    topo.add_link(Link("R3", "R2", 50.0, delay=3.0))
    topo.add_link(Link("R2", "R3", 50.0, delay=3.0))

    # 3. Lên lịch các sự kiện theo Dòng thời gian (Timeline)
    system_log.info("Đang lên lịch các sự kiện vào Event Queue...")
    
    # Sự kiện 1: Các router khởi động và gửi LSA tại ms thứ 0.0
    sim.schedule(0.0, "STARTUP_R1", topo.flood_lsa, source_router_id="R1", lsa=r1.generate_lsa())
    sim.schedule(0.0, "STARTUP_R2", topo.flood_lsa, source_router_id="R2", lsa=r2.generate_lsa())
    sim.schedule(0.0, "STARTUP_R3", topo.flood_lsa, source_router_id="R3", lsa=r3.generate_lsa())
    
    # Sự kiện 2: Máy xúc đào đứt cáp R1-R2 tại ms thứ 20.0
    sim.schedule(20.0, "EXCAVATOR_INCIDENT", topo.remove_link, source_id="R1", dest_id="R2")
    sim.schedule(20.0, "EXCAVATOR_INCIDENT", topo.remove_link, source_id="R2", dest_id="R1")

    # Sự kiện 3: In bảng định tuyến của R1 tại ms thứ 35.0 (sau khi mạng đã chữa lành)
    sim.schedule(35.0, "PRINT_ROUTING", r1.routing_table.display)

    # 4. Giao quyền điều khiển cho Simulator!
    sim.run(max_time=100.0)

if __name__ == "__main__":
    main()