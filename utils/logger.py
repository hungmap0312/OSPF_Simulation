import logging
import os
from utils.config import Config

# Đảm bảo thư mục logs tồn tại
if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logger(name, log_file, level=None):
    """Hàm khởi tạo các bộ logger chuyên biệt (Router, LSA, SPF, v.v.)"""
    # Lấy mức độ hiển thị log từ file Config nếu không được chỉ định
    if level is None:
        level = Config.LOG_LEVEL

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | [%(name)s] %(message)s', datefmt='%H:%M:%S')

    handler = logging.FileHandler(f'logs/{log_file}')        
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Tránh duplicate log nếu gọi hàm nhiều lần
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)

    return logger

# Khởi tạo các Logger độc lập theo yêu cầu Giai đoạn 5.3
system_log = setup_logger('SYSTEM', 'system.log')
router_log = setup_logger('ROUTER', 'router.log')
lsa_log = setup_logger('LSA', 'lsa.log')
spf_log = setup_logger('SPF', 'spf.log')
error_log = setup_logger('ERROR', 'error.log', level=logging.ERROR)
