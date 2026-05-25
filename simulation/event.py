class Event:
    def __init__(self, timestamp: float, event_type: str, handler_func, **kwargs):
        self.timestamp = timestamp
        self.event_type = event_type
        self.handler_func = handler_func  # Hàm sẽ được gọi khi sự kiện xảy ra
        self.kwargs = kwargs              # Tham số truyền vào hàm

    # Định nghĩa toán tử so sánh để ưu tiên sự kiện xảy ra trước trong Priority Queue
    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __repr__(self):
        return f"Event({self.event_type} at {self.timestamp:.3f}ms)"
