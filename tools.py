from langchain_core.tools import tool

# ==================================================
# MOCK DATA
# ==================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air",      "departure": "08:30", "arrival": "09:50", "price": 890_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "07:30", "arrival": "09:40", "price": 950_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "13:00", "arrival": "14:20", "price": 780_000,   "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "15:00", "arrival": "16:00", "price": 650_000,   "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury",  "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê",    "rating": 4.5},
        {"name": "Sala Danang Beach",   "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê",    "rating": 4.3},
        {"name": "Fivitel Danang",      "stars": 3, "price_per_night": 650_000,   "area": "Sơn Trà",   "rating": 4.1},
        {"name": "Memory Hostel",       "stars": 2, "price_per_night": 250_000,   "area": "Hải Châu",  "rating": 4.6},
        {"name": "Christina's Homestay","stars": 2, "price_per_night": 350_000,   "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort",     "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài",     "rating": 4.4},
        {"name": "Sol by Meliá",        "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường",  "rating": 4.2},
        {"name": "Lahana Resort",       "stars": 3, "price_per_night": 800_000,   "area": "Dương Đông",  "rating": 4.0},
        {"name": "9Station Hostel",     "stars": 2, "price_per_night": 200_000,   "area": "Dương Đông",  "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel",           "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central",     "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel",    "stars": 3, "price_per_night": 550_000,   "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room",     "stars": 2, "price_per_night": 180_000,   "area": "Quận 1", "rating": 4.6},
    ],
}


# ==================================================
# TOOL 1: search_flights
# ==================================================

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    """
    try:
        # Thử tra theo chiều xuôi
        flights = FLIGHTS_DB.get((origin, destination))

        # Nếu không có, thử chiều ngược
        if not flights:
            flights = FLIGHTS_DB.get((destination, origin))

        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

        # Format kết quả
        result = f"✈️ Chuyến bay từ {origin} đến {destination}:\n"
        result += "-" * 40 + "\n"
        for i, f in enumerate(flights, 1):
            price_str = f"{f['price']:,}".replace(",", ".")
            result += (
                f"{i}. {f['airline']} | {f['departure']} → {f['arrival']} | "
                f"{price_str}đ | {f['class']}\n"
            )
        return result

    except Exception as e:
        return f"Lỗi khi tìm chuyến bay: {str(e)}"


# ==================================================
# TOOL 2: search_hotels
# ==================================================

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    try:
        hotels = HOTELS_DB.get(city)

        if not hotels:
            return f"Không tìm thấy dữ liệu khách sạn tại {city}."

        # Lọc theo giá
        filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

        if not filtered:
            budget_str = f"{max_price_per_night:,}".replace(",", ".")
            return (
                f"Không tìm thấy khách sạn tại {city} với giá dưới {budget_str}đ/đêm. "
                f"Hãy thử tăng ngân sách."
            )

        # Sắp xếp theo rating giảm dần
        filtered.sort(key=lambda h: h["rating"], reverse=True)

        # Format kết quả
        result = f"🏨 Khách sạn tại {city} (giá ≤ {max_price_per_night:,}đ/đêm):\n".replace(",", ".")
        result += "-" * 40 + "\n"
        for i, h in enumerate(filtered, 1):
            price_str = f"{h['price_per_night']:,}".replace(",", ".")
            result += (
                f"{i}. {h['name']} | {h['stars']} sao | "
                f"{price_str}d/dem | {h['area']} | Rating: {h['rating']}\n"
            )
        return result

    except Exception as e:
        return f"Lỗi khi tìm khách sạn: {str(e)}"


# ==================================================
# TOOL 3: calculate_budget
# ==================================================

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, định dạng 'tên_khoản:số_tiền'
      cách nhau bởi dấu phẩy. VD: 'vé_máy_bay:890000,khách_sạn:650000'
    Trả về bảng chi tiết và số tiền còn lại.
    """
    try:
        # Parse chuỗi expenses thành dict
        expense_dict = {}
        for item in expenses.split(","):
            item = item.strip()
            if ":" not in item:
                return f"Lỗi định dạng: '{item}' không đúng dạng 'tên:số_tiền'."
            name, amount_str = item.split(":", 1)
            expense_dict[name.strip()] = int(amount_str.strip())

        # Tính tổng chi phí
        total_expense = sum(expense_dict.values())
        remaining = total_budget - total_expense

        # Format bảng chi tiết
        budget_str = f"{total_budget:,}".replace(",", ".")
        result = "💰 Bảng chi phí:\n"
        result += "-" * 40 + "\n"
        for name, amount in expense_dict.items():
            amount_str = f"{amount:,}".replace(",", ".")
            result += f"  - {name.replace('_', ' ').title()}: {amount_str}đ\n"

        total_str = f"{total_expense:,}".replace(",", ".")
        remaining_str = f"{abs(remaining):,}".replace(",", ".")

        result += "-" * 40 + "\n"
        result += f"  Tổng chi: {total_str}đ\n"
        result += f"  Ngân sách: {budget_str}đ\n"

        if remaining >= 0:
            result += f"  ✅ Còn lại: {remaining_str}đ"
        else:
            result += f"  ❌ Vượt ngân sách: {remaining_str}đ! Cần điều chỉnh."

        return result

    except ValueError as e:
        return f"Lỗi: số tiền không hợp lệ — {str(e)}"
    except Exception as e:
        return f"Lỗi khi tính ngân sách: {str(e)}"