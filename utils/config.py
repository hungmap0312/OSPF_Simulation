# utils/config.py
import logging

class Config:
    # --- 1. CẤU HÌNH QUY MÔ MẠNG (NETWORK SCALE) ---
    BENCHMARK_ROUTER_SIZES = [5, 20, 50, 100, 200, 500] # Quy mô kiểm thử hiệu năng
    REFERENCE_BANDWIDTH = 100.0  # Mbps (Dùng để tính OSPF Cost)
    DEFAULT_LINK_DELAY = 1.0     # ms (Độ trễ cáp mặc định)
    MAX_OSPF_COST = 20           # Trọng số Cost lớn nhất khi sinh ngẫu nhiên

    # --- 2. BỘ ĐẾM THỜI GIAN CHUẨN OSPF (OSPF TIMERS) ---
    HELLO_INTERVAL = 10.0         # giây (Khoảng thời gian định kỳ gửi gói Hello)
    DEAD_INTERVAL = 40.0          # giây (Thời gian chờ trước khi coi láng giềng đã sập)
    LSA_REFRESH_TIME = 1800.0     # giây (Thời gian định kỳ làm mới LSA toàn mạng)

    # --- 3. MỨC ĐỘ GHI LOG (LOGGING LEVEL) ---
    # Giá trị có thể chọn: logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR
    LOG_LEVEL = logging.INFO

    # --- 4. TÙY CHỈNH GIAO DIỆN (UI THEMING) ---
    COLOR_ROOT_NODE = '#FFD700'   # Màu vàng cho Router gốc (R1)
    COLOR_NORMAL_NODE = '#87CEFA' # Màu xanh da trời cho các Router thành viên
    COLOR_ACTIVE_PATH = 'red'       # Màu đỏ cho tuyến đường ngắn nhất đang chạy dữ liệu
    COLOR_IDLE_PATH = 'gray'        # Màu xám cho các tuyến đường dự phòng
    NODE_SIZE = 1200                # Kích thước vòng tròn Router
    FONT_SIZE = 10                  # Kích thước chữ hiển thị tên Router
    ACTIVE_EDGE_WIDTH = 4.0         # Độ dày nét vẽ cho đường đang active
    IDLE_EDGE_WIDTH = 1.5           # Độ dày nét vẽ cho đường dự phòng

    # --- THÔNG SỐ MÔ PHỎNG & CHAOS MONKEY ---
    SIMULATOR_MAX_TIME = 10000.0 # ms
    CHAOS_MIN_DELAY = 30.0       # ms
    CHAOS_MAX_DELAY = 100.0      # ms
    ANIMATION_INTERVAL = 33      # ms (Tốc độ cập nhật giao diện đồ họa khi chạy mô phỏng)