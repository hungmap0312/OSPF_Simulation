import heapq
from typing import Dict, Tuple
from typing import List

def calculate_spf(graph: Dict[str, Dict[str, int]], source: str) -> Tuple[Dict[str, int], Dict[str, str]]:
    """
    Hàm tính toán đường đi ngắn nhất bằng thuật toán Dijkstra.
    
    Args:
        graph: Đồ thị kề dạng dictionary (vd: {'1.1.1.1': {'2.2.2.2': 1, '3.3.3.3': 10}})
        source: Router ID làm gốc của cây SPF (SPF Tree Root)
        
    Returns:
        distances: Dictionary chứa tổng cost ngắn nhất đến mỗi node.
        previous_nodes: Dictionary chứa node liền trước (predecessor) trên đường đi.
    """
    # Khởi tạo khoảng cách đến tất cả các node là vô cực, trừ node nguồn là 0
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    
    # Lưu lại vết đường đi (predecessor) để sinh bảng định tuyến sau này
    previous_nodes = {node: None for node in graph}
    
    # Hàng đợi ưu tiên (Priority Queue): lưu trữ các tuple (current_cost, current_node)
    pq = [(0, source)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Nếu tìm thấy một đường khác trong hàng đợi dài hơn khoảng cách hiện tại đã biết -> Bỏ qua
        if current_distance > distances[current_node]:
            continue
            
        # Duyệt qua các neighbor của node hiện tại
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # Nếu tìm được đường đi ngắn hơn -> Cập nhật lại
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                
                # Đẩy vào hàng đợi ưu tiên để duyệt tiếp
                heapq.heappush(pq, (distance, neighbor))
                
    return distances, previous_nodes

def get_path(previous_nodes: Dict[str, str], source: str, target: str) -> List[str]:
    """
    Lần ngược previous_nodes để tạo danh sách đường đi từ source đến target.
    """
    path = []
    current_node = target
    
    # Lần ngược từ đích về nguồn
    while current_node is not None:
        path.insert(0, current_node)
        if current_node == source:
            break
        current_node = previous_nodes[current_node]
        
    # Nếu phần tử đầu tiên không phải source, nghĩa là không có đường đi
    if path[0] != source:
        return []
        
    return path
