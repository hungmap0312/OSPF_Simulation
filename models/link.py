from utils.config import Config

class Link:
    def __init__(self, source_id: str, dest_id: str, bandwidth_mbps: float, delay: float = Config.DEFAULT_LINK_DELAY):
        self.source_id = source_id       # ID của Router nguồn
        self.dest_id = dest_id           # ID của Router đích
        self.bandwidth = bandwidth_mbps  # Đơn vị: Mbps
        self.delay = delay               # Đơn vị: ms (mặc định 1ms)
        self.state = "UP"                # Trạng thái của liên kết: "UP" (hoạt động) hoặc "DOWN" (đứt)
        
        self.reference_bandwidth = Config.REFERENCE_BANDWIDTH
        self.cost = self._calculate_cost()

    def _calculate_cost(self) -> int:
        """Tính toán metric cost dựa trên bandwidth."""
        if self.bandwidth <= 0:
            return float('inf')
        
        # OSPF Cost = Reference Bandwidth / Interface Bandwidth
        cost = int(self.reference_bandwidth / self.bandwidth)
        return cost if cost > 0 else 1  # Cost tối thiểu là 1

    def update_bandwidth(self, new_bandwidth: float):
        """Cập nhật bandwidth và tính toán lại cost"""
        self.bandwidth = new_bandwidth
        self.cost = self._calculate_cost()
        print(f"[Link] Cập nhật bandwidth {self.source_id}->{self.dest_id}: Cost mới = {self.cost}")

    def __repr__(self):
        return f"Link({self.source_id} -> {self.dest_id}, Cost: {self.cost})"
