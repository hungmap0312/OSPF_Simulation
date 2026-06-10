from typing import List, Dict

class RouteEntry:
    def __init__(self, destination: str, next_hop: str, total_cost: int, path: List[str], interface: str = ""):
        self.destination = destination      # Đích đến (Destination)
        self.next_hop = next_hop            # ID của Router tiếp theo trên đường đi đến đích
        self.total_cost = total_cost        # Tổng cost từ Source đến Destination qua Next Hop
        self.path = path                    # Full path từ Source đến Destination (dùng để hiển thị)
        self.interface = interface          # Lưu cổng đầu ra vật lý

    def __repr__(self):
        return f"[{self.destination}] via {self.next_hop} on {self.interface} | Cost: {self.total_cost} | Path: {' -> '.join(self.path)}"

class RoutingTable:
    def __init__(self):
        # Lưu các route: {destination_id: RouteEntry}
        self.entries: Dict[str, RouteEntry] = {}

    def add_route(self, destination: str, next_hop: str, total_cost: int, path: List[str], interface: str = ""):
        """Thêm hoặc cập nhật một tuyến đường vào bảng."""
        self.entries[destination] = RouteEntry(destination, next_hop, total_cost, path, interface)

    def display(self):
        """In bảng định tuyến ra màn hình."""
        print("--- Routing Table ---")
        if not self.entries:
            print("  (Empty)")
        for dest, entry in self.entries.items():
            print(f"  {entry}")
