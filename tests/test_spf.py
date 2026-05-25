import sys
import os
import time
import random
import networkx as nx

# Khai báo đường dẫn gốc để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link
from models.topology import Topology
from algorithms.dijkstra import calculate_spf, get_path

def block_print():
    """Tạm thời tắt in log ra màn hình để terminal không bị trôi khi tạo mạng lớn."""
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    """Bật lại in log ra màn hình."""
    sys.stdout = sys.__stdout__

def run_networkx_comparison():
    print("--- 1. SO SÁNH ĐỘ CHÍNH XÁC VỚI NETWORKX ---")
    block_print()
    topo = Topology()
    # Tạo 5 router
    for i in range(1, 6):
        topo.add_router(Router(f"R{i}"))
    
    # R1-R2 (Cost 1), R1-R3 (Cost 4), R2-R3 (Cost 2), R3-R4 (Cost 1), R2-R5 (Cost 6), R4-R5 (Cost 2)
    edges = [("R1", "R2", 100.0), ("R1", "R3", 25.0), ("R2", "R3", 50.0), 
             ("R3", "R4", 100.0), ("R2", "R5", 16.6), ("R4", "R5", 50.0)]
    for src, dst, bw in edges:
        topo.add_link(Link(src, dst, bw))
        topo.add_link(Link(dst, src, bw))
    enable_print()

    # 1. Chạy thuật toán tự code
    distances_custom, prev_custom = calculate_spf(topo.adjacency_graph, "R1")
    
    # 2. Xây dựng đồ thị NetworkX và chạy Dijkstra của NetworkX
    G = nx.DiGraph()
    for u, neighbors in topo.adjacency_graph.items():
        for v, cost in neighbors.items():
            G.add_edge(u, v, weight=cost)
            
    distances_nx, paths_nx = nx.single_source_dijkstra(G, "R1", weight='weight')
    
    # 3. So sánh kết quả
    is_match = True
    for target in topo.routers.keys():
        if target == "R1": continue
        
        custom_path = get_path(prev_custom, "R1", target)
        nx_path = paths_nx[target]
        
        if distances_custom[target] != distances_nx[target] or custom_path != nx_path:
            is_match = False
            print(f"❌ Lệch kết quả tại {target}!")
            print(f"   - Custom: Cost={distances_custom[target]}, Path={custom_path}")
            print(f"   - NetowrkX: Cost={distances_nx[target]}, Path={nx_path}")
            
    if is_match:
        print("✅ KẾT QUẢ KHỚP 100% VỚI THƯ VIỆN CHUẨN NETWORKX!")
        for target in distances_nx.keys():
            if target != "R1":
                print(f"   [R1 -> {target}] Cost: {distances_nx[target]} | Path: {' -> '.join(paths_nx[target])}")

def run_benchmark():
    print("\n--- 2. BENCHMARK TỐC ĐỘ THỰC THI (100 ROUTERS, 200 LINKS) ---")
    block_print()
    topo = Topology()
    routers = [f"R{i}" for i in range(100)]
    for r in routers:
        topo.add_router(Router(r))
        
    links_created = 0
    while links_created < 200:
        src, dst = random.sample(routers, 2)
        if dst not in topo.adjacency_graph[src]:
            bw = random.choice([10.0, 50.0, 100.0, 1000.0])
            topo.add_link(Link(src, dst, bw))
            topo.add_link(Link(dst, src, bw))
            links_created += 1
    enable_print()

    print("Đang chạy thuật toán SPF Custom...")
    start_time = time.perf_counter()
    calculate_spf(topo.adjacency_graph, "R0")
    end_time = time.perf_counter()
    
    print("Đang chạy thuật toán NetworkX...")
    nx_G = nx.DiGraph()
    for u, neighbors in topo.adjacency_graph.items():
        for v, cost in neighbors.items():
            nx_G.add_edge(u, v, weight=cost)
            
    start_nx = time.perf_counter()
    nx.single_source_dijkstra(nx_G, "R0", weight='weight')
    end_nx = time.perf_counter()

    custom_ms = (end_time - start_time) * 1000
    nx_ms = (end_nx - start_nx) * 1000
    
    print(f"⏱️ Thời gian chạy Custom SPF : {custom_ms:.4f} ms")
    print(f"⏱️ Thời gian chạy NetworkX  : {nx_ms:.4f} ms")

if __name__ == "__main__":
    print("=== NGHIỆM THU GIAI ĐOẠN 3: KIỂM THỬ VÀ BENCHMARK ===")
    run_networkx_comparison()
    run_benchmark()
