# HỆ THỐNG MÔ PHỎNG GIAO THỨC ĐỊNH TUYẾN OSPF HƯỚNG SỰ KIỆN

## MÔ TẢ NGẮN DỰ ÁN
Dự án này cung cấp một môi trường mô phỏng sự kiện rời rạc (Discrete Event Simulation) nhằm đánh giá và trực quan hóa giao thức định tuyến trạng thái liên kết OSPF (Open Shortest Path First). Hệ thống được thiết kế hoàn toàn từ kiến trúc cơ sở bằng ngôn ngữ Python, tích hợp thuật toán tìm đường đi ngắn nhất Dijkstra với độ phức tạp tối ưu, cơ chế đồng bộ cơ sở dữ liệu trạng thái liên kết (LSDB), và mô hình nhiễu loạn mạng ngẫu nhiên (Chaos Monkey). Thông qua dự án này, người sử dụng có thể trực tiếp quan sát quá trình hội tụ của mạng lưới khi xảy ra các sự cố ngắt kết nối vật lý, đồng thời trích xuất các số liệu đánh giá hiệu năng (benchmark) về thời gian tính toán và chi phí bộ nhớ trên các đồ thị mạng quy mô lớn.

## YÊU CẦU HỆ THỐNG
- **Hệ điều hành:** Tương thích đa nền tảng (Windows, macOS, Linux; đặc biệt tương thích tốt với môi trường Ubuntu/Debian).
- **Môi trường thực thi:** Khuyến nghị sử dụng Python phiên bản 3.8 trở lên. Nên triển khai trong môi trường ảo (Virtual Environment) như Conda hoặc venv để đảm bảo tính cô lập của hệ thống.
- **Thư viện phụ thuộc:** Hệ thống yêu cầu các gói thư viện toán học và đồ họa để tính toán cấu trúc liên kết và trực quan hóa dữ liệu. Các chỉ lệnh cài đặt chi tiết như sau:
1. Cập nhật trình quản lý thư viện: 
```
pip install --upgrade pip
```
2. Cài đặt thư viện xử lý đồ thị:
```
pip install networkx
```
3. Cài đặt thư viện đồ họa và trực quan hóa:
```
pip install matplotlib
```
4. Cài đặt thư viện giám sát tài nguyên phần cứng (phục vụ đánh giá hiệu năng):
```
pip install psutil
```

## HƯỚNG DẪN CÀI ĐẶT DỰ ÁN
Để triển khai dự án trên môi trường cục bộ, thực hiện tuần tự các chỉ lệnh quản lý mã nguồn dưới đây thông qua giao diện dòng lệnh (Terminal/Command Prompt):

Bước 1: Sao chép kho lưu trữ mã nguồn từ hệ thống phân phối:
```
git clone https://github.com/hungmap0312/OSPF_Simulation.git
```
Bước 2: Di chuyển không gian làm việc vào thư mục gốc của dự án:
```
cd OSPF_Simulation
```
Bước 3: Khởi tạo và kích hoạt môi trường ảo. Ví dụ đối với hệ thống quản lý Conda:
```
conda create --name ospf_sim python=3.10
conda activate ospf_sim
```

## HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH
Hệ thống cung cấp hai luồng thực thi chính, phục vụ cho các mục đích nghiên cứu và kiểm thử khác nhau. Đảm bảo terminal đang ở thư mục gốc của dự án trước khi thực thi lệnh.

### **Luồng 1: Vận hành chế độ Trực quan hóa và Tương tác (Giao diện người dùng)**
- Chế độ này khởi chạy đồ thị mạng với quy mô được định nghĩa trong tệp cấu hình, kết hợp bộ đếm thời gian thực và mô đun sự cố ngẫu nhiên.
- Lệnh thực thi: 
```
python src/main.py
```
- Mô tả: Sau khi khởi chạy, một cửa sổ đồ họa sẽ xuất hiện. Người dùng có thể tương tác với hệ thống thông qua bảng điều khiển để tạo các sự cố ngắt kết nối mạng lưới và quan sát trực tiếp thuật toán định tuyến lại lưu lượng truyền dẫn.

### **Luồng 2: Vận hành chế độ Đánh giá Hiệu năng (Benchmark)**
- Chế độ này loại bỏ giao diện đồ họa, ép hệ thống tính toán với công suất tối đa trên các quy mô đồ thị mạng lớn (từ hàng chục đến hàng trăm bộ định tuyến) nhằm thu thập số liệu về thời gian xử lý thuật toán và mức độ tiêu thụ bộ nhớ (RAM).
- Lệnh thực thi:
```
python tests/benchmark.py
```
- Mô tả: Kết quả phân tích sẽ được xuất trực tiếp ra màn hình dòng lệnh dưới dạng bảng thống kê. Đồng thời, hệ thống tự động kết xuất các biểu đồ đánh giá khả năng mở rộng (Scalability) dưới dạng tệp ảnh lưu tại thư mục logs.

## NHÓM THỰC HIỆN
Tài liệu và mã nguồn hệ thống được nghiên cứu, thiết kế và phát triển bởi:
- LÊ TUẤN HƯNG