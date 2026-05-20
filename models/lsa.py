from typing import Dict

class LSA:
    def __init__(self, adv_router: str, seq_num: int, link_info: Dict[str, int]):
        self.lsa_id = adv_router      # Trong thiết kế single-area, LSA ID có thể lấy luôn Router ID
        self.adv_router = adv_router  # Router sinh ra LSA này
        self.seq_num = seq_num        # Số thứ tự để kiểm tra bản tin mới/cũ
        self.age = 0                  # Thời gian sống của LSA
        self.link_info = link_info    # Thông tin đường truyền: {neighbor_id: cost}

    def __repr__(self):
        return f"LSA(AdvRouter: {self.adv_router}, Seq: {self.seq_num}, Links: {self.link_info})"
