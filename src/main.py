import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.topology import Topology
from simulation.simulator import Simulator
from utils.logger import system_log
from visualization.visualizer import OSPFVisualizer
from utils.network_generator import create_10_node_network
from simulation.chaos_monkey import ChaosMonkey

def main():
    system_log.info("Khởi động Giai đoạn 6: Mạng 10 Router & Chaos Monkey")
    
    # 1. Khởi tạo Simulator và Topology
    sim = Simulator()
    topo = Topology(simulator=sim)
    
    # 2. Sinh mạng 10 Router
    pos, original_links = create_10_node_network(topo)
    
    # 3. Khởi tạo Kẻ phá hoại (Chưa hoạt động cho đến khi bấm nút)
    monkey = ChaosMonkey(topo, sim, original_links)

    # 4. Lên lịch khởi động mạng (Đồng loạt rải LSA ban đầu)
    system_log.info("Đang nạp các sự kiện khởi động...")
    for r_id in topo.routers:
        sim.schedule(0.0, f"STARTUP_{r_id}", topo.flood_lsa, 
                     source_router_id=r_id, lsa=topo.routers[r_id].generate_lsa())
    
    # 5. Kích hoạt Giao diện Người dùng
    viz = OSPFVisualizer(topology=topo, simulator=sim, pos=pos, chaos_monkey=monkey)
    viz.start()

if __name__ == "__main__":
    main()
