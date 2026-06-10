from typing import Dict

class LSA:
    def __init__(self, adv_router: str, seq_num: int, link_info: Dict[str, int]):
        self.lsa_id = adv_router      # ID của LSA, thường là ID của Router sinh ra LSA này
        self.adv_router = adv_router  # ID của Router quảng bá LSA này (LSA Originator)
        self.seq_num = seq_num        # Số thứ tự của LSA, tăng dần mỗi khi LSA được cập nhật
        self.age = 0                  # Tuổi của LSA (Age), tính bằng giây kể từ khi LSA được tạo hoặc cập nhật lần cuối
        self.link_info = link_info    # Thông tin đường truyền: {neighbor_id: cost}
    
    def __repr__(self):
        return f"LSA(AdvRouter: {self.adv_router}, Seq: {self.seq_num}, Links: {self.link_info})"
