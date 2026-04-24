<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
   GỬI TIN NHẮN BROADCAST QUA UDP
</h2>
<div align="center">
    <p align="center">
        <img alt="AIoTLab Logo" width="170" src="https://github.com/user-attachments/assets/711a2cd8-7eb4-4dae-9d90-12c0a0a208a2" />
        <img alt="AIoTLab Logo" width="180" src="https://github.com/user-attachments/assets/dc2ef2b8-9a70-4cfa-9b4b-f6c2f25f1660" />
        <img alt="DaiNam University Logo" width="200" src="https://github.com/user-attachments/assets/77fe0fd1-2e55-4032-be3c-b1a705a1b574" />
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 1. Giới thiệu

Đề tài tập trung xây dựng một ứng dụng chat đơn giản cho phép các máy tính trong cùng mạng LAN **trao đổi thông tin với nhau thông qua giao thức UDP (User Datagram Protocol) và cơ chế broadcast**.
Thay vì gửi tin nhắn trực tiếp tới một máy cụ thể, ứng dụng sẽ **gửi một gói tin broadcast đến tất cả các thiết bị trong mạng**, giúp **tất cả các client đang lắng nghe trên cùng một cổng (port)** đều nhận được cùng một tin nhắn.

Việc sử dụng UDP giúp việc truyền dữ liệu trở nên **nhanh, gọn, không cần thiết lập kết nối (connectionless)** như TCP.  
Tuy không đảm bảo tin nhắn đến đúng thứ tự, nhưng UDP phù hợp cho các ứng dụng cần **gửi thông báo nhanh đến nhiều người cùng lúc** như:  
- Chat nội bộ trong mạng LAN  
- Gửi thông báo hệ thống  
- Tìm kiếm và khám phá thiết bị IoT trong mạng

---

## 2. Công nghệ sử dụng
- **Ngôn ngữ lập trình:** Java (JDK 21)  
- **Giao diện:** Java Swing  
- **Giao thức mạng:** UDP (User Datagram Protocol)  
- **IDE:** Eclipse  
## 3. Hình ảnh các chức năng
<p align="center">
  <img src="images/hinh2.jpg" alt="Ảnh 2" width="700"/>
</p>

<p align = "center">Hình 1: Giao diện server </p>

<p align="center">
  <img src="images/hinh3.jpg" alt="Ảnh 2" width="700"/>
</p>  

<p align = "center">Hình 3: Nhập tên cho client </p>

<p align="center">
  <img src="images/hinh1.jpg" alt="Ảnh 2" width="700"/>
</p>  

<p align = "center">Hình 3: Giao diện client </p>

<p align="center">
  <img src="images/hinh4.jpg" alt="Ảnh 2" width="700"/>
</p> 

<p align = "center">Hình 4: Server nhắn tin cho client </p>


## 4. Các bước cài đặt
### Yêu cầu hệ thống
- JDK 21 hoặc cao hơn
- Eclipse IDE (khuyến nghị bản mới nhất)
- Git đã cài trên máy

Bước 1: Clone project từ GitHub
```bash
git clone https://github.com/sam04cd/LTM-Gui-tin-nhan-Broadcast-qua-UDP.git
```
Bước 2: Import project vào Eclipse

- Mở Eclipse
- Vào File → Import
- Chọn Existing Projects into Workspace
- Chọn thư mục project vừa clone về
- Nhấn Finish

Bước 3: Kiểm tra môi trường

- Đảm bảo project chạy trên JavaSE-21 (hoặc phiên bản JDK bạn đã cài).
- Nếu thiếu thư viện, vào Project → Properties → Java Build Path để thêm JDK phù hợp.

Bước 4: Chạy ứng dụng

- Mở class Server → Run để khởi động server.
- Mở class Client → Run để khởi động client.
- Có thể mở nhiều client cùng lúc để test broadcast.

Bước 5: Gửi và nhận tin nhắn

- Nhập nội dung tin nhắn → nhấn Send.
- Tất cả client khác trong cùng mạng LAN sẽ nhận được tin nhắn broadcast.

## 📬 Thông tin liên hệ
- Họ và tên: Mẫn Bá Sâm
- Lớp: CNTT 16-03
- Email: sam40741@gmail.com

© 2025 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.

---
