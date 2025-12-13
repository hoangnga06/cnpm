import json
import os
# ===========================
# DỮ LIỆU HỆ THỐNG
# ===========================
DATA_FILE = "users.json"
users = []
# Mỗi user:
# {
#   "email": ...,
#   "name": ...,
#   "phone": ...,
#   "password": ...,
#   "role": "admin" / "warehouse" / "sales",
#   "locked": False,
#   "login_fail": 0
# }

session = {"logged_in": False, "email": None, "role": None}


# ===========================
# HÀM HỖ TRỢ
# ===========================
def is_valid_email(email):
    return "@" in email and "." in email


def find_user_by_email(email):
    for u in users:
        if u["email"] == email:
            return u
    return None
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10 and phone.startswith("0")
def load_users():
    global users
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    else:
        users = []
def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# ===========================
# 1) ĐĂNG KÝ TÀI KHOẢN
# ===========================
def register_user():
    print("\n=== ĐĂNG KÝ TÀI KHOẢN ===")

    email = input("Email: ").strip()
    name = input("Họ tên: ").strip()
    phone = input("SĐT: ").strip()
    password = input("Mật khẩu: ").strip()
    confirm_password = input("Nhập lại mật khẩu: ").strip()

    # Kiểm tra nhập đủ
    if not email or not name or not phone or not password or not confirm_password:
        print("❌ Lỗi: Phải nhập đầy đủ thông tin.")
        return

    # Kiểm tra email hợp lệ
    if not is_valid_email(email):
        print("❌ Lỗi: Email không hợp lệ.")
        return

    # Kiểm tra SĐT hợp lệ
    if not is_valid_phone(phone):
        print("❌ Lỗi: SĐT không hợp lệ (10 số, bắt đầu bằng 0).")
        return

    # Kiểm tra email tồn tại
    if find_user_by_email(email):
        print("❌ Lỗi: Email đã tồn tại.")
        return

    # Kiểm tra mật khẩu
    if len(password) < 6:
        print("❌ Lỗi: Mật khẩu phải tối thiểu 6 ký tự.")
        return

    # Kiểm tra mật khẩu nhập lại
    if password != confirm_password:
        print("❌ Lỗi: Mật khẩu nhập lại không khớp.")
        return

    new_user = {
        "email": email,
        "name": name,
        "phone": phone,
        "password": password,
        "role": "sales",   # mặc định
        "locked": False,
        "login_fail": 0
    }

    users.append(new_user)
    save_users()
    print("✔ Đăng ký thành công. Bạn có thể đăng nhập ngay.")

# ===========================
# 2) ĐĂNG NHẬP HỆ THỐNG
# ===========================
def login_user():
    print("\n=== ĐĂNG NHẬP ===")

    email = input("Email: ").strip()
    password = input("Mật khẩu: ").strip()

    if not email or not password:
        print("❌ Phải nhập đầy đủ Email và Mật khẩu.")
        return

    user = find_user_by_email(email)

    if not user:
        print("❌ Email không tồn tại.")
        return

    if user["locked"]:
        print("❌ Tài khoản đã bị khóa do đăng nhập sai nhiều lần.")
        return

    if user["password"] == password:
        session["logged_in"] = True
        session["email"] = email
        session["role"] = user["role"]
        user["login_fail"] = 0

        print("✔ Đăng nhập thành công.")
        print(f"➡ Quyền: {user['role']}")
        return
    else:
        user["login_fail"] += 1
        print("❌ Sai mật khẩu.")

        if user["login_fail"] >= 3:
            user["locked"] = True
            save_users()
            print("⚠ Tài khoản đã bị khóa sau 3 lần sai.")



# ===========================
# 3) ĐĂNG XUẤT
# ===========================
def logout_user():
    if not session["logged_in"]:
        print("❌ Bạn chưa đăng nhập.")
        return

    print("\nBạn có muốn đăng xuất không?")
    print("1. Đồng ý")
    print("2. Hủy")

    choice = input("Chọn: ")

    if choice == "1":
        session["logged_in"] = False
        session["email"] = None
        session["role"] = None
        print("✔ Đã đăng xuất. Không thể truy cập trang bảo mật.")
    else:
        print("↩ Hủy đăng xuất.")


# ===========================
# 4) ĐỔI MẬT KHẨU
# ===========================
def change_password():
    if not session["logged_in"]:
        print("❌ Phải đăng nhập trước.")
        return

    user = find_user_by_email(session["email"])

    old_pass = input("Mật khẩu hiện tại: ")
    new_pass = input("Mật khẩu mới: ")
    confirm = input("Xác nhận mật khẩu mới: ")

    if user["password"] != old_pass:
        print("❌ Mật khẩu hiện tại không đúng.")
        return

    if new_pass != confirm:
        print("❌ Mật khẩu xác nhận không khớp.")
        return

    if len(new_pass) < 6:
        print("❌ Mật khẩu mới phải tối thiểu 6 ký tự.")
        return

    user["password"] = new_pass
    save_users()
    print("✔ Đổi mật khẩu thành công.")



# ===========================
# 5) GÁN QUYỀN NGƯỜI DÙNG (ADMIN)
# ===========================
def manage_roles():
    if not session["logged_in"] or session["role"] != "admin":
        print("❌ Chỉ Admin mới được gán quyền.")
        return

    print("\n--- DANH SÁCH NGƯỜI DÙNG ---")
    for u in users:
        print(f"{u['email']} | {u['name']} | Quyền: {u['role']}")

    email = input("\nEmail cần gán quyền: ").strip()
    role = input("Quyền mới (admin / warehouse / sales): ").strip()

    if role not in ["admin", "warehouse", "sales"]:
        print("❌ Quyền không hợp lệ.")
        return

    user = find_user_by_email(email)
    if not user:
        print("❌ Người dùng không tồn tại.")
        return

    user["role"] = role
    save_users()
    print("✔ Gán quyền thành công.")


# ===========================
# MENU CHÍNH
# ===========================
def main():
    while True:
        print("\n=== HỆ THỐNG QUẢN LÝ NGƯỜI DÙNG ===")
        print("1. Đăng ký")
        print("2. Đăng nhập")
        print("3. Đăng xuất")
        print("4. Đổi mật khẩu")
        print("5. Gán quyền (Admin)")
        print("6. Thoát")

        choice = input("Chọn: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            logout_user()
        elif choice == "4":
            change_password()
        elif choice == "5":
            manage_roles()
        elif choice == "6":
            print("Kết thúc chuong trinh.")
            break
        else:
            print("❌ Lựa chọn không hop le.")


if __name__ == "__main__":
    load_users()
    main()

