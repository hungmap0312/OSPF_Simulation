import sys
import os
import time
import random
import psutil
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router
from models.link import Link
from models.topology import Topology
from algorithms.dijkstra import calculate_spf
from utils.config import Config

def block_print():
    """Tắt in log ra màn hình để terminal không bị nhiễu khi chạy benchmark."""
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    """Bật lại in log."""
    sys.stdout = sys.__stdout__

def generate_benchmark_topo(num_routers):
    """Tạo ngẫu nhiên một mạng OSPF siêu lớn để stress-test."""
    topo = Topology() 
    routers = [f"R{i}" for i in range(1, num_routers + 1)]
    
    for r in routers:
        topo.add_router(Router(r))

    # Đảm bảo mạng liên thông bằng cách tạo một đường vòng (Ring)
    for i in range(num_routers - 1):
        bw = random.choice([10.0, 50.0, 100.0, 1000.0])
        topo.add_link(Link(routers[i], routers[i+1], bw))
        topo.add_link(Link(routers[i+1], routers[i], bw))

    # Bổ sung thêm các liên kết ngẫu nhiên để tăng độ phức tạp của mạng
    num_extra_links = num_routers * 2
    for _ in range(num_extra_links):
        u, v = random.sample(routers, 2)
        bw = random.choice([10.0, 50.0, 100.0, 1000.0])
        topo.add_link(Link(u, v, bw))
        topo.add_link(Link(v, u, bw))

    return topo

def run_benchmark():
    # Lấy danh sách các kích thước mạng từ Config để chạy benchmark
    sizes = Config.BENCHMARK_ROUTER_SIZES
    spf_times = []
    ram_usages = []

    print("=== BẮT ĐẦU CHẠY BENCHMARK ĐÁNH GIÁ HIỆU NĂNG (GIAI ĐOẠN 7) ===")
    print(f"{'Quy mô Router':<15} | {'Số lượng Cáp':<15} | {'Thời gian SPF (ms)':<20} | {'RAM Tiêu thụ (MB)':<15}")
    print("-" * 75)

    process = psutil.Process(os.getpid())

    for size in sizes:
        block_print()
        # 1. Sinh mạng ngẫu nhiên
        topo = generate_benchmark_topo(size)
        
        # 2. Lấy chỉ số RAM ban đầu
        ram_before = process.memory_info().rss / (1024 * 1024)

        # 3. Đo lường tốc độ tính toán (Mô phỏng cả mạng bị đứt cáp và tất cả Router phải đồng loạt chạy lại Dijkstra)
        start_time = time.perf_counter()
        
        for r_id in topo.routers:
            calculate_spf(topo.adjacency_graph, r_id)
            
        end_time = time.perf_counter()

        # 4. Lấy chỉ số RAM sau khi xử lý để tính toán Overhead
        ram_after = process.memory_info().rss / (1024 * 1024)
        ram_used = max(0.01, ram_after - ram_before) # Ước lượng RAM tăng thêm

        total_spf_time_ms = (end_time - start_time) * 1000
        enable_print()
        
        # Lưu trữ dữ liệu để vẽ biểu đồ
        spf_times.append(total_spf_time_ms)
        ram_usages.append(ram_used)

        print(f"{size:<15} | {len(topo.links):<15} | {total_spf_time_ms:<20.4f} | {ram_used:<15.4f}")

    # --- XUẤT BIỂU ĐỒ BÁO CÁO (SCALABILITY CHART) ---
    print("\nĐang tổng hợp dữ liệu và vẽ biểu đồ báo cáo...")
    plt.figure(figsize=(12, 5))
    
    # Biểu đồ 1: Thời gian hội tụ theo quy mô
    plt.subplot(1, 2, 1)
    plt.plot(sizes, spf_times, marker='o', color='blue', linewidth=2)
    plt.title('Khả năng mở rộng: Thời gian tính toán SPF')
    plt.xlabel('Số lượng Router')
    plt.ylabel('Thời gian xử lý (ms)')
    plt.grid(True, linestyle='--', alpha=0.7)

    # Biểu đồ 2: Chi phí bộ nhớ theo quy mô
    plt.subplot(1, 2, 2)
    plt.plot(sizes, ram_usages, marker='s', color='red', linewidth=2)
    plt.title('Chi phí bộ nhớ (RAM Overhead)')
    plt.xlabel('Số lượng Router')
    plt.ylabel('RAM tiêu thụ (MB)')
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    # Lưu biểu đồ vào thư mục logs
    plt.savefig('logs/benchmark_scalability.png', dpi=300)
    print("✅ Đã lưu biểu đồ thành công tại: logs/benchmark_scalability.png")
    
    # Hiển thị biểu đồ lên màn hình
    plt.show()

if __name__ == '__main__':
    run_benchmark()
