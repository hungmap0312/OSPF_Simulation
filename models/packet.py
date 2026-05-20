class OSPF_Packet:
    """Class cơ sở cho mọi gói tin OSPF."""
    pass

class HelloPacket(OSPF_Packet):
    def __init__(self, sender_id: str, known_neighbors: list):
        self.type = "HELLO"
        self.sender_id = sender_id
        # Danh sách các router mà sender này đã nhận được Hello
        self.known_neighbors = known_neighbors 

    def __repr__(self):
        return f"HelloPacket(From: {self.sender_id}, Known: {self.known_neighbors})"
