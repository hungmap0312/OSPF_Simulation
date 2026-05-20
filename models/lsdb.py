from typing import Dict
from models.lsa import LSA

class LSDB:
    def __init__(self):
        # Lưu trữ LSA mới nhất của từng Router: {adv_router_id: LSA}
        self.lsas: Dict[str, LSA] = {}

    def update_lsa(self, lsa: LSA) -> bool:
        """
        Nhận LSA và cập nhật LSDB.
        Trả về True nếu là LSA mới và đã cập nhật, False nếu là LSA cũ hoặc trùng.
        """
        # Nếu chưa có thông tin về Router này trong LSDB -> Thêm mới
        if lsa.adv_router not in self.lsas:
            self.lsas[lsa.adv_router] = lsa
            return True
        
        # Nếu đã có, kiểm tra Sequence Number xem LSA nhận được có mới hơn không
        current_lsa = self.lsas[lsa.adv_router]
        if lsa.seq_num > current_lsa.seq_num:
            self.lsas[lsa.adv_router] = lsa
            return True
            
        return False # LSA cũ hoặc bằng sequence hiện tại, bỏ qua (Duplicate)

    def display(self):
        print("--- Link-State Database (LSDB) ---")
        for adv_router, lsa in self.lsas.items():
            print(f"  + {lsa}")

    def __repr__(self):
        return f"LSDB(Size: {len(self.lsas)} LSA(s))"
