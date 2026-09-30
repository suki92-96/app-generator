import re
import tkinter as tk
from tkinter import filedialog


def process_username(user, formatted_num, separator):
  digits_match = re.search(r"\d+", user)
  if digits_match:
    start_pos, end_pos = digits_match.span()
    if start_pos > 0 and end_pos < len(user):
      return user[:start_pos] + formatted_num + user[end_pos:]
    else:
      if separator:
        clean_user = re.sub(r"\d+", "", user).strip("_-.")
        return f"{clean_user}{separator}{formatted_num}"
      else:
        return user[:start_pos] + formatted_num + user[end_pos:]
  else:
    if separator:
      return f"{user}{separator}{formatted_num}"
    else:
      return f"{user}{formatted_num}"


def main():
  root = tk.Tk()
  root.withdraw()

  print("=== PHẦN MỀM TẠO DANH SÁCH USER/EMAIL THÔNG MINH ===")

  file_path = filedialog.askopenfilename(
      title="Chọn file txt chứa danh sách",
      filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
  )

  if not file_path:
    print("Bạn chưa chọn file. Chương trình kết thúc.")
    return

  try:
    start_num = int(input("Nhập số bắt đầu (ví dụ: 1): ").strip())
    end_num = int(input("Nhập số kết thúc (ví dụ: 11): ").strip())
  except ValueError:
    print("Lỗi: Vui lòng nhập số nguyên hợp lệ!")
    return

  try:
    extra_zeros = int(
        input(
            "Nhập số lượng số 0 ở đầu (ví dụ: 1 thì 1->01, 2 thì 1->001): "
        ).strip()
    )
  except ValueError:
    extra_zeros = 0

  print(
      "\nChọn dấu nối giữa user và số (có thể chọn nhiều, cách nhau bằng dấu"
      " phẩy):"
  )
  print("1. Không có dấu nối")
  print("2. Gạch dưới (_)")
  print("3. Gạch ngang (-)")
  print("4. Dấu chấm (.)")

  sep_input = input("Nhập lựa chọn của bạn (ví dụ: 1, 2, 4): ").strip()
  sep_choices = [s.strip() for s in sep_input.split(",") if s.strip()]

  separator_map = {"1": "", "2": "_", "3": "-", "4": "."}
  selected_separators = []
  for choice in sep_choices:
    if choice in separator_map:
      sep_val = separator_map[choice]
      if sep_val not in selected_separators:
        selected_separators.append(sep_val)

  if not selected_separators:
    selected_separators = [""]

  try:
    with open(file_path, "r", encoding="utf-8") as f:
      lines = [line.strip() for line in f if line.strip()]
  except Exception as e:
    print(f"Lỗi đọc file: {e}")
    return

  results = []
  for line in lines:
    if "@" in line:
      parts = line.split("@", 1)
      user = parts[0]
      domain = "@" + parts[1]
    else:
      user = line
      domain = ""

    for num in range(start_num, end_num + 1):
      num_str = str(num)
      if num < 10 and extra_zeros > 0:
        formatted_num = ("0" * extra_zeros) + num_str
      else:
        formatted_num = num_str

      for separator in selected_separators:
        new_user = process_username(user, formatted_num, separator)
        results.append(new_user + domain)

  output_path = filedialog.asksaveasfilename(
      defaultextension=".txt",
      filetypes=[("Text files", "*.txt")],
      title="Lưu file kết quả",
  )

  if output_path:
    with open(output_path, "w", encoding="utf-8") as f:
      f.write("\n".join(results))
    print(f"\nThành công! Đã lưu kết quả tại: {output_path}")
    print(f"Tổng số dòng được tạo: {len(results)}")
  else:
    print("\nKhông lưu file. Hiển thị kết quả trực tiếp:")
    for r in results:
      print(r)


if __name__ == "__main__":
  main()
