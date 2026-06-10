import logging
import os
from utils.config import Config

# Đảm bảo thư mục logs tồn tại
if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logger(name, log_file, level=None):
    """Hàm khởi tạo các bộ logger chuyên biệt (Router, LSA, SPF, v.v.)"""
    #  Nếu không truyền level, sử dụng cấu hình mặc định từ Config
    if level is None:
        level = Config.LOG_LEVEL

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | [%(name)s] %(message)s', datefmt='%H:%M:%S')

    handler = logging.FileHandler(f'logs/{log_file}')        
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Tránh việc thêm nhiều handler nếu logger đã tồn tại (đặc biệt khi chạy nhiều lần trong cùng một phiên)
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)

    return logger

# Khởi tạo các logger chuyên biệt cho từng loại thông tin
system_log = setup_logger('SYSTEM', 'system.log')
router_log = setup_logger('ROUTER', 'router.log')
lsa_log = setup_logger('LSA', 'lsa.log')
spf_log = setup_logger('SPF', 'spf.log')
error_log = setup_logger('ERROR', 'error.log', level=logging.ERROR)
