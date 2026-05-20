import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.router import Router

def main():
    print("=== MÔ PHỎNG OSPF NEIGHBOR DISCOVERY ===")
    r1 = Router("R1")
    r2 = Router("R2")
    
    print("\n--- BƯỚC 1: R1 gửi Hello đầu tiên ---")
    hello_r1 = r1.generate_hello()
    print(f"R1 phát: {hello_r1}")
    r2.receive_hello(hello_r1)  # R2 nhận
    print(f"Trạng thái láng giềng R2: {r2.neighbors}")
    
    print("\n--- BƯỚC 2: R2 gửi Hello phản hồi ---")
    # Lúc này R2 đã biết R1, nên danh sách known_neighbors của R2 sẽ có 'R1'
    hello_r2 = r2.generate_hello()
    print(f"R2 phát: {hello_r2}")
    r1.receive_hello(hello_r2)  # R1 nhận
    print(f"Trạng thái láng giềng R1: {r1.neighbors}")
    
    print("\n--- BƯỚC 3: R1 gửi Hello xác nhận lại ---")
    hello_r1_v2 = r1.generate_hello()
    print(f"R1 phát: {hello_r1_v2}")
    r2.receive_hello(hello_r1_v2) # R2 nhận
    print(f"Trạng thái láng giềng R2: {r2.neighbors}")

if __name__ == "__main__":
    main()