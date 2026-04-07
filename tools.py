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


# ==================================================
# TOOL 4: search_by_budget
# ==================================================

@tool
def search_by_budget(origin: str, budget: int) -> str:
    """
    Tìm tất cả điểm đến có thể đi từ một thành phố trong phạm vi ngân sách vé máy bay.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - budget: ngân sách tối đa cho vé máy bay (VNĐ)
    Trả về danh sách điểm đến và chuyến bay rẻ nhất phù hợp ngân sách.
    """
    try:
        matches = []
        for (orig, dest), flights in FLIGHTS_DB.items():
            if orig == origin:
                affordable = [f for f in flights if f["price"] <= budget]
                if affordable:
                    cheapest = min(affordable, key=lambda f: f["price"])
                    matches.append((dest, cheapest))
            elif dest == origin:
                affordable = [f for f in flights if f["price"] <= budget]
                if affordable:
                    cheapest = min(affordable, key=lambda f: f["price"])
                    matches.append((orig, cheapest))

        if not matches:
            budget_str = f"{budget:,}".replace(",", ".")
            return f"Không tìm thấy chuyến bay nào từ {origin} trong tầm {budget_str}đ."

        budget_str = f"{budget:,}".replace(",", ".")
        result = f"Điểm đến từ {origin} trong tầm {budget_str}đ:\n"
        result += "-" * 40 + "\n"
        for dest, f in sorted(matches, key=lambda x: x[1]["price"]):
            price_str = f"{f['price']:,}".replace(",", ".")
            result += (
                f"- {dest}: {f['airline']} {f['departure']}→{f['arrival']} | {price_str}đ ({f['class']})\n"
            )
        return result

    except Exception as e:
        return f"Lỗi khi tìm theo ngân sách: {str(e)}"


# ==================================================
# TOOL 5: compare_options
# ==================================================

@tool
def compare_options(origin: str, destination1: str, destination2: str, budget: int, nights: int) -> str:
    """
    So sánh tổng chi phí (vé rẻ nhất + khách sạn tốt nhất trong tầm tiền) giữa 2 điểm đến.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội')
    - destination1: điểm đến thứ nhất (VD: 'Đà Nẵng')
    - destination2: điểm đến thứ hai (VD: 'Phú Quốc')
    - budget: tổng ngân sách (VNĐ)
    - nights: số đêm ở lại
    Trả về bảng so sánh và gợi ý điểm đến phù hợp hơn.
    """
    def _analyze(dest):
        # Tìm vé rẻ nhất
        flights = FLIGHTS_DB.get((origin, dest)) or FLIGHTS_DB.get((dest, origin)) or []
        if not flights:
            return None, f"Không có chuyến bay từ {origin} đến {dest}."
        cheapest_flight = min(flights, key=lambda f: f["price"])
        flight_cost = cheapest_flight["price"]

        # Tính budget còn lại cho khách sạn mỗi đêm
        hotel_budget_per_night = (budget - flight_cost) // nights if nights > 0 else 0
        hotels = HOTELS_DB.get(dest, [])
        affordable_hotels = [h for h in hotels if h["price_per_night"] <= hotel_budget_per_night]

        if not affordable_hotels:
            best_hotel = min(hotels, key=lambda h: h["price_per_night"]) if hotels else None
        else:
            best_hotel = max(affordable_hotels, key=lambda h: h["rating"])

        hotel_cost = best_hotel["price_per_night"] * nights if best_hotel else 0
        total = flight_cost + hotel_cost
        fits = total <= budget

        return {
            "dest": dest,
            "flight": cheapest_flight,
            "flight_cost": flight_cost,
            "hotel": best_hotel,
            "hotel_cost": hotel_cost,
            "total": total,
            "fits": fits,
        }, None

    try:
        info1, err1 = _analyze(destination1)
        info2, err2 = _analyze(destination2)

        result = f"So sánh: {destination1} vs {destination2} ({nights} đêm, ngân sách {budget:,}đ)\n".replace(",", ".")
        result += "=" * 50 + "\n"

        for info, err, dest in [(info1, err1, destination1), (info2, err2, destination2)]:
            result += f"\n[{dest}]\n"
            if err:
                result += f"  {err}\n"
                continue
            f = info["flight"]
            h = info["hotel"]
            flight_str = f"{info['flight_cost']:,}".replace(",", ".")
            hotel_str = f"{info['hotel_cost']:,}".replace(",", ".")
            total_str = f"{info['total']:,}".replace(",", ".")
            result += f"  Ve may bay: {f['airline']} {f['departure']}→{f['arrival']} | {flight_str}d\n"
            if h:
                result += f"  Khach san:  {h['name']} ({h['stars']} sao, {h['area']}) | {hotel_str}d ({nights} dem)\n"
            result += f"  Tong: {total_str}d | {'Phu hop ngan sach' if info['fits'] else 'VUOT NGAN SACH'}\n"

        # Gợi ý
        result += "\n" + "-" * 50 + "\n"
        if info1 and info2:
            if info1["fits"] and not info2["fits"]:
                result += f"=> Nen chon: {destination1} (vua ngan sach)\n"
            elif info2["fits"] and not info1["fits"]:
                result += f"=> Nen chon: {destination2} (vua ngan sach)\n"
            elif info1["fits"] and info2["fits"]:
                better = destination1 if info1["total"] <= info2["total"] else destination2
                result += f"=> Ca hai deu phu hop. {better} tiet kiem hon.\n"
            else:
                cheaper = destination1 if info1["total"] <= info2["total"] else destination2
                result += f"=> Ca hai deu vuot ngan sach. {cheaper} it vuot hon.\n"

        return result

    except Exception as e:
        return f"Lỗi khi so sánh: {str(e)}"


# ==================================================
# TOOL 6: get_trip_summary
# ==================================================

@tool
def get_trip_summary(origin: str, destination: str, nights: int, budget: int) -> str:
    """
    Tạo gói du lịch trọn gói: tìm vé máy bay + khách sạn phù hợp + tính ngân sách còn lại.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    - nights: số đêm lưu trú
    - budget: tổng ngân sách (VNĐ)
    Trả về kế hoạch hoàn chỉnh gồm vé, khách sạn và tổng chi phí.
    """
    try:
        # --- Chuyến bay ---
        flights = FLIGHTS_DB.get((origin, destination)) or FLIGHTS_DB.get((destination, origin)) or []
        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

        cheapest_flight = min(flights, key=lambda f: f["price"])
        flight_cost = cheapest_flight["price"]

        # --- Khách sạn ---
        remaining_after_flight = budget - flight_cost
        hotel_budget_per_night = remaining_after_flight // nights if nights > 0 else 0
        hotels = HOTELS_DB.get(destination, [])
        affordable = [h for h in hotels if h["price_per_night"] <= hotel_budget_per_night]

        if affordable:
            best_hotel = max(affordable, key=lambda h: h["rating"])
        elif hotels:
            best_hotel = min(hotels, key=lambda h: h["price_per_night"])
        else:
            best_hotel = None

        hotel_cost = best_hotel["price_per_night"] * nights if best_hotel else 0
        total_cost = flight_cost + hotel_cost
        remaining = budget - total_cost

        # --- Format ---
        budget_str = f"{budget:,}".replace(",", ".")
        flight_str = f"{flight_cost:,}".replace(",", ".")
        hotel_str = f"{hotel_cost:,}".replace(",", ".")
        total_str = f"{total_cost:,}".replace(",", ".")
        remaining_str = f"{abs(remaining):,}".replace(",", ".")

        result = f"GOI DU LICH: {origin} → {destination} ({nights} dem)\n"
        result += "=" * 50 + "\n"
        result += f"Ve may bay:\n"
        result += (
            f"  {cheapest_flight['airline']} | "
            f"{cheapest_flight['departure']}→{cheapest_flight['arrival']} | "
            f"{flight_str}d ({cheapest_flight['class']})\n"
        )
        if best_hotel:
            hotel_per_night_str = f"{best_hotel['price_per_night']:,}".replace(",", ".")
            result += f"Khach san ({nights} dem):\n"
            result += (
                f"  {best_hotel['name']} | {best_hotel['stars']} sao | "
                f"{hotel_per_night_str}d/dem | {best_hotel['area']} | Rating {best_hotel['rating']}\n"
                f"  => {hotel_str}d\n"
            )
        result += "-" * 50 + "\n"
        result += f"  Tong chi phi: {total_str}d\n"
        result += f"  Ngan sach:    {budget_str}d\n"
        if remaining >= 0:
            result += f"  Con lai:      {remaining_str}d (co the dung an uong, tham quan)\n"
        else:
            result += f"  Vuot ngan sach: {remaining_str}d — can dieu chinh.\n"

        return result

    except Exception as e:
        return f"Lỗi khi tạo gói du lịch: {str(e)}"