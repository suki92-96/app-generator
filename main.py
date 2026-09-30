import random
import re
import tkinter as tk
from tkinter import filedialog


def process_line(line, remove_index):
    """Xử lý từng dòng: xóa vị trí ký tự chỉ định và tự động thêm số ngẫu nhiên từ 1-2026

    nếu độ dài phần username bằng đúng 4 ký tự.
    """
    if not line:
        return ""

    # Tách phần username và domain (nếu có chứa ký tự @)
    if "@" in line:
        parts = line.split("@", 1)
        user = parts[0]
        domain = "@" + parts[1]
    else:
        user = line
        domain = ""

    # Kiểm tra chỉ số xóa hợp lệ (Chuyển từ vị trí người dùng nhập 1-based sang 0-based index)
    idx = remove_index - 1

    # Nếu chỉ số hợp lệ với độ dài username thì thực hiện xóa ký tự tại vị trí đó
    if 0 <= idx < len(user):
        user = user[:idx] + user[idx + 1 :]

    # Nếu độ dài của phần username sau khi xóa bằng đúng 4 ký tự -> thêm số ngẫu nhiên từ 1 đến 2026
    if len(user) == 4:
        rand_num = random.randint(1, 2026)
        user = f"{user}{rand_num}"

    return user + domain


def main():
    # Ẩn cửa sổ gốc tkinter
    root = tk.Tk()
    root.withdraw()

    print("==================================================")
    print("      CÔNG CỤ XỬ LÝ CHUỖI USER/EMAIL THÔNG MINH    ")
    print("==================================================\n")

    # 1. Chọn file txt đầu vào
    print("-> Đang mở hộp thoại chọn file đầu vào...")
    file_path = filedialog.askopenfilename(
        title="Chọn file txt chứa danh sách",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )

    if not file_path:
        print("x Bạn chưa chọn file. Chương trình kết thúc.")
        input("\nNhấn Enter để thoát...")
        return

    print(f"✓ Đã chọn file: {file_path}\n")

    # 2. Hỏi vị trí ký tự muốn xóa (ví dụ nhập 1 là xóa ký tự đầu tiên)
    try:
        remove_pos = int(
            input("Nhập vị trí ký tự cần xóa (ví dụ: 1 để xóa ký tự thứ 1): ")
            .strip()
        )
        if remove_pos <= 0:
            print("x Vị trí ký tự phải là số nguyên lớn hơn 0!")
            input("\nNhấn Enter để thoát...")
            return
    except ValueError:
        print("x Lỗi: Vui lòng nhập số nguyên hợp lệ!")
        input("\nNhấn Enter để thoát...")
        return

    # 3. Đọc file đầu vào
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"x Lỗi đọc file: {e}")
        input("\nNhấn Enter để thoát...")
        return

    # 4. Xử lý logic dữ liệu
    results = []
    for line in lines:
        processed = process_line(line, remove_pos)
        if processed:
            results.append(processed)

    # 5. Chọn nơi lưu file kết quả
    print("\n-> Đang mở hộp thoại lưu file kết quả...")
    output_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Lưu file kết quả",
    )

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print(f"\n==================================================")
        print(f" Thành công! Đã lưu kết quả tại:\n {output_path}")
        print(f" Tổng số dòng đã xử lý: {len(results)}")
        print(f"==================================================")
    else:
        print("\nKhông chọn nơi lưu file. Kết quả trực tiếp:")
        for r in results:
            print(r)

    input("\nNhấn Enter để kết thúc...")


if __name__ == "__main__":
    main()
