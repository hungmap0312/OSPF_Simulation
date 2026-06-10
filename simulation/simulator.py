import heapq
from simulation.event import Event
from utils.logger import system_log
from utils.config import Config

class Simulator:
    def __init__(self):
        self.event_queue = []   # Hàng đợi sự kiện (Priority Queue)
        self.current_time = 0.0 # Thời gian mô phỏng hiện tại (ms)
        self.is_running = False

    def schedule(self, delay: float, event_type: str, handler_func, **kwargs):
        """Lên lịch cho một sự kiện trong tương lai (Delayed propagation)."""
        trigger_time = self.current_time + delay
        event = Event(trigger_time, event_type, handler_func, **kwargs)
        heapq.heappush(self.event_queue, event)
        return event

    def step(self):
        """Thực thi sự kiện tiếp theo (Step-by-step execution)."""
        if not self.event_queue:
            return False

        # Lấy sự kiện xảy ra sớm nhất ra khỏi hàng đợi
        event = heapq.heappop(self.event_queue)
        
        # Cập nhật đồng hồ hệ thống tiến tới mốc thời gian của sự kiện
        self.current_time = event.timestamp
        
        # Thực thi hàm xử lý sự kiện
        event.handler_func(**event.kwargs)
        return True

    def run(self, max_time: float = Config.SIMULATOR_MAX_TIME):
        """Chạy mô phỏng cho đến khi hết sự kiện hoặc đạt giới hạn thời gian."""
        self.is_running = True
        system_log.info(f"=== BẮT ĐẦU MÔ PHỎNG TỪ {self.current_time}ms ===")
        
        while self.event_queue and self.is_running and self.current_time <= max_time:
            self.step()
            
        system_log.info(f"=== KẾT THÚC MÔ PHỎNG TẠI {self.current_time:.3f}ms ===")

    def stop(self):
        """Dừng mô phỏng khẩn cấp."""
        self.is_running = False

    def reset(self):
        """Khởi tạo lại trạng thái."""
        self.event_queue.clear()
        self.current_time = 0.0
        self.is_running = False
