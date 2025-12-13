import json
import os

BOOK_FILE = "books.json"

def load_books():
    if not os.path.exists(BOOK_FILE):
        return {}
    with open(BOOK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_books():
    with open(BOOK_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

# =============================
# QUẢN LÝ SÁCH - FULL CODE
# =============================

# Database giả lập
books = load_books()

# ============================================
# 1) THÊM SÁCH MỚI — add_new_book()
# ============================================
def add_new_book():
    """
    Chức năng:
    - Thiết kế form nhập thông tin
    - API thêm sách (giả lập)
    - Kiểm tra trùng mã
    - Lưu vào hệ thống
    """
    print("\n=== THÊM SÁCH MỚI ===")
    book_id = input("Nhập mã sách: ")
    if book_id in books:
        print("❌ Mã sách đã tồn tại!")
        return

    name = input("Tên sách: ")
    author = input("Tác giả: ")
    category = input("Thể loại: ")
    try:
        price = float(input("Giá: "))
        qty = int(input("Số lượng: "))
    except:
        print("Giá hoặc số lượng không hợp lệ!")
        return

    if price <= 0 or qty < 0:
        print("Giá phải > 0 và số lượng ≥ 0!")
        return

    # Lưu vào database
    books[book_id] = {
        "name": name,
        "author": author,
        "category": category,
        "price": price,
        "qty": qty
    }
    save_books()
    print("Thêm sách thành công!")

# ============================================
# 2) CHỈNH SỬA TT SÁCH — edit_book()
# ============================================
def edit_book():
    """
    - Hiển thị form với dữ liệu cũ
    - Validate dữ liệu chỉnh sửa
    - API cập nhật (giả lập)
    """
    print("\n=== CHỈNH SỬA THÔNG TIN SÁCH ===")
    book_id = input("Nhập mã sách cần sửa: ")
    if book_id not in books:
        print("❌ Không tìm thấy mã sách!")
        return

    book = books[book_id]
    print("\n--- DỮ LIỆU HIỆN TẠI ---")
    print(book)
    print("\nNhập thông tin mới (Enter để giữ nguyên):")
    
    name = input(f"Tên sách ({book['name']}): ") or book['name']
    author = input(f"Tác giả ({book['author']}): ") or book['author']
    category = input(f"Thể loại ({book['category']}): ") or book['category']

    try:
        price_input = input(f"Giá ({book['price']}): ")
        price = float(price_input) if price_input else book['price']
        qty_input = input(f"Số lượng ({book['qty']}): ")
        qty = int(qty_input) if qty_input else book['qty']
    except:
        print("❌ Dữ liệu chỉnh sửa không hợp lệ!")
        return

    if price <= 0 or qty < 0:
        print("❌ Giá phải > 0 và số lượng ≥ 0!")
        return

    # Cập nhật dữ liệu
    books[book_id] = {
        "name": name,
        "author": author,
        "category": category,
        "price": price,
        "qty": qty
    }
    save_books()
    print("✅ Cập nhật thành công!")

# ============================================
# 3) XÓA SÁCH — delete_book()
# ============================================
def delete_book():
    """
    - Hiển thị danh sách
    - Phân trang đơn giản
    - Xóa theo mã
    - Xử lý lỗi
    """
    print("\n=== XÓA SÁCH ===")
    if len(books) == 0:
        print("❌ Kho sách trống.")
        return view_books(show_pause=False)

    book_id = input("Nhập mã sách muốn xóa: ")
    if book_id not in books:
        print("❌ Không tìm thấy mã sách!")
        return

    confirm = input("Bạn chắc chắn muốn xóa? (y/n): ")
    if confirm.lower() == "y":
        del books[book_id]
        save_books()
        print("✅ Đã xóa sách thành công!")
    else:
        print("❌ Hủy xóa.")

# ============================================
# 4) XEM DANH SÁCH SÁCH — view_books()
# ============================================
def view_books(show_pause=True):
    print("\n=== DANH SÁCH SÁCH ===")

    if len(books) == 0:
        print("❌ Không có dữ liệu.")
        return

    print("{:<10} {:<25} {:<20} {:<15} {:<10} {:<10}".format(
        "Mã", "Tên sách", "Tác giả", "Thể loại", "Giá", "SL"
    ))
    print("-" * 95)

    for book_id, b in books.items():
        print("{:<10} {:<25} {:<20} {:<15} {:<10} {:<10}".format(
            book_id,
            b["name"],
            b["author"],
            b["category"],
            b["price"],
            b["qty"]
        ))

    if show_pause:
        input("\nNhấn Enter để quay lại menu...")


# ============================================
# 5) TÌM KIẾM SÁCH — search_book()
# ============================================
def search_book():
    """
    - Tìm kiếm theo mã / tên / tác giả
    - Hiển thị dạng bảng
    """
    print("\n=== TÌM KIẾM SÁCH ===")
    keyword = input("Nhập từ khóa: ").lower()
    results = {}
    for book_id, b in books.items():
        if (keyword in book_id.lower() or
            keyword in b['name'].lower() or
            keyword in b['author'].lower()):
            results[book_id] = b

    if len(results) == 0:
        print("❌ Ko tìm thấy sách.")
        return

    print("\n--- KẾT QUẢ TÌM KIẾM ---")
    for book_id, b in results.items():
        print(f"{book_id} | {b['name']} | {b['author']} | {b['category']} | "
              f"Giá: {b['price']} | SL: {b['qty']}")
    input("\nNhấn Enter để quay lại menu...")

# ============================================
# MENU CHÍNH — main()
# ============================================
def main(role):
    while True:
        print("\n====== QUẢN LÝ SÁCH ======")
        if role == "admin":
            print("1. Thêm sách mới")
            print("2. Chỉnh sửa thông tin sách")
            print("3. Xóa sách")
            print("4. Xem danh sách sách")
            print("5. Tìm kiếm sách")
            print("6. Thoát")
            choice = input("Chọn: ")
            if choice == "1":
                add_new_book()
            elif choice == "2":
                edit_book()
            elif choice == "3":
                delete_book()
            elif choice == "4":
                view_books()
            elif choice == "5":
                search_book()
            elif choice == "6":
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
        else:  # USER
            print("1. Xem danh sách sách")
            print("2. Tìm kiếm sách")
            print("3. Thoát")
            choice = input("Chọn: ")
            if choice == "1":
                view_books()
            elif choice == "2":
                search_book()
            elif choice == "3":
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
