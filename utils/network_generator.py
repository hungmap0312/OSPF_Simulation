import random
from models.router import Router
from models.link import Link

def create_10_node_network(topo):
    """Khởi tạo 10 Router với trọng số (Cost) ngẫu nhiên từ 1 đến 20."""
    for i in range(1, 12):
        topo.add_router(Router(f"R{i}"))

    # Chỉ định nghĩa các cặp nối, Cost sẽ được quay ngẫu nhiên
    link_pairs = [
        ("R1", "R2"), ("R2", "R3"), ("R3", "R4"), ("R4", "R5"),
        ("R5", "R6"), ("R6", "R7"), ("R7", "R8"), ("R8", "R1"),
        ("R9", "R2"), ("R9", "R8"), ("R10", "R4"), ("R10", "R6"),
        ("R9", "R10"), ("R11", "R3"), ("R11", "R5")
    ]

    original_links = []
    for src, dst in link_pairs:
        # 1. Quay ngẫu nhiên trọng số từ 1 đến 20
        random_cost = random.randint(1, 20)
        
        # 2. Quy đổi ngược ra Bandwidth để thỏa mãn công thức của class Link
        bw = 100.0 / random_cost
        dly = random.uniform(1.0, 5.0) 
        
        l1, l2 = Link(src, dst, bw, dly), Link(dst, src, bw, dly)
        topo.add_link(l1)
        topo.add_link(l2)
        original_links.extend([l1, l2])

    # Tọa độ cố định
    pos = {
        "R1": (1, 5), "R2": (3, 7), "R3": (5, 8),
        "R4": (7, 6), "R5": (8, 3), "R6": (6, 1),
        "R7": (3, 1), "R8": (1, 3),
        "R9": (3.5, 4.5), "R10": (5.5, 3.5), "R11": (8, 8.5)
    }
    
    return pos, original_links

