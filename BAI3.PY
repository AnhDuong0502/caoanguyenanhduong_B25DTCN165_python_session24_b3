class MemberCard:
    point_value_vnd = 1000

    def __init__(self, card_id, name):
        self.card_id = card_id
        self.name = name.title()
        self.__points = 0
        self.__tier = "Standard"

    @property
    def points(self):
        return self.__points

    @property
    def tier(self):
        return self.__tier

    def earn_points(self, bill_amount):
        earned = bill_amount // 10000
        self.__points += earned

        upgraded = False

        if self.__points >= 100 and self.__tier != "VIP":
            self.__tier = "VIP"
            upgraded = True

        return earned, upgraded

    def redeem_points(self, points_to_use):
        if points_to_use <= 0:
            return False, 0

        if points_to_use > self.__points:
            return False, 0

        self.__points -= points_to_use

        discount = points_to_use * MemberCard.point_value_vnd

        return True, discount

    @classmethod
    def update_point_value(cls, new_value):
        cls.point_value_vnd = new_value

    @staticmethod
    def is_valid_card_id(card_id):
        if len(card_id) != 4:
            return False

        if not card_id.startswith("RC"):
            return False

        if not card_id[2:].isdigit():
            return False

        return True


cards_database = [
    MemberCard("RC01", "Nguyen Van A"),
    MemberCard("RC02", "Tran Thi B")
]

cards_database[0].earn_points(1500000)
cards_database[1].earn_points(200000)


def find_card(card_id):
    for card in cards_database:
        if card.card_id == card_id:
            return card
    return None


while True:
    choice = input("""
===== HỆ THỐNG THẺ THÀNH VIÊN RIKKEI COFFEE =====
1. Xem danh sách thẻ thành viên
2. Đăng ký thẻ mới
3. Khách mua hàng (Tích điểm)
4. Khách dùng điểm (Đổi ưu đãi)
5. Cập nhật tỷ giá quy đổi điểm (Hệ thống)
6. Thoát chương trình
======================================================
Chọn chức năng (1-6):
""")

    match choice:
        case "1":
            if not cards_database:
                print("Chưa có thẻ thành viên nào.")
            else:
                for index, card in enumerate(cards_database, start=1):
                    print(
                        f"{index}. Mã: {card.card_id} | "
                        f"Tên: {card.name} | "
                        f"Điểm: {card.points} | "
                        f"Hạng: {card.tier}"
                    )

        case "2":
            print("\n--- ĐĂNG KÝ THẺ THÀNH VIÊN MỚI ---")

            card_id = input("Nhập mã thẻ: ").strip()

            if not MemberCard.is_valid_card_id(card_id):
                print("Mã thẻ không hợp lệ!")
                continue

            if find_card(card_id):
                print("\nMã thẻ đã tồn tại trong hệ thống!")
                print("Vui lòng kiểm tra lại.")
                continue

            name = input("Nhập tên khách hàng: ").strip()

            new_card = MemberCard(card_id, name)
            cards_database.append(new_card)

            print("\nĐăng ký thẻ thành viên thành công!")
            print(f"Mã thẻ: {new_card.card_id}")
            print(f"Tên khách hàng: {new_card.name}")
            print(f"Điểm ban đầu: {new_card.points}")
            print(f"Hạng thẻ: {new_card.tier}")

        case "3":
            print("\n--- KHÁCH MUA HÀNG - TÍCH ĐIỂM ---")

            card_id = input("Nhập mã thẻ: ").strip()

            card = find_card(card_id)

            if not card:
                print("Không tìm thấy thẻ!")
                continue

            try:
                bill_amount = int(
                    input("Nhập tổng tiền hóa đơn: ")
                )

                if bill_amount <= 0:
                    print("Hóa đơn không hợp lệ!")
                    continue

            except ValueError:
                print("Hóa đơn không hợp lệ!")
                continue

            earned, upgraded = card.earn_points(
                bill_amount
            )

            print(f"\nKhách hàng: {card.name}")
            print(f"Hóa đơn: {bill_amount:,} VNĐ")
            print(f"Số điểm được tích: {earned}")
            print(f"Tổng điểm hiện tại: {card.points}")

            if upgraded:
                print(
                    "\nChúc mừng! Khách hàng đã được nâng hạng lên VIP."
                )

            print(f"Hạng thẻ hiện tại: {card.tier}")

        case "4":
            print(
                "\n--- KHÁCH DÙNG ĐIỂM - ĐỔI ƯU ĐÃI ---"
            )

            print(
                f"Tỷ giá hiện tại: 1 điểm = {MemberCard.point_value_vnd:,} VNĐ"
            )

            card_id = input("Nhập mã thẻ: ").strip()

            card = find_card(card_id)

            if not card:
                print("Không tìm thấy thẻ!")
                continue

            try:
                points_to_use = int(
                    input("Nhập số điểm muốn sử dụng: ")
                )
            except ValueError:
                print("Điểm sử dụng không hợp lệ!")
                continue

            success, discount = card.redeem_points(
                points_to_use
            )

            if success:
                print(f"\nĐã trừ {points_to_use} điểm.")
                print(
                    f"Khách hàng được giảm giá {discount:,} VNĐ vào hóa đơn!"
                )
                print(
                    f"Số điểm còn lại: {card.points}"
                )
                print(
                    f"Hạng thẻ hiện tại: {card.tier}"
                )
            else:
                print("\nKhông thể đổi điểm!")
                print(
                    "Số điểm muốn sử dụng vượt quá số điểm hiện có."
                )
                print(
                    f"Điểm hiện tại của khách: {card.points}"
                )
                print("Điểm cũ được giữ nguyên:")
                print(
                    f"Số điểm sau giao dịch: {card.points}"
                )

        case "5":
            print(
                "\n--- CẬP NHẬT TỶ GIÁ QUY ĐỔI ĐIỂM ---"
            )

            print(
                f"Tỷ giá hiện tại: 1 điểm = {MemberCard.point_value_vnd:,} VNĐ"
            )

            try:
                new_value = int(
                    input(
                        "Nhập tỷ giá mới cho 1 điểm: "
                    )
                )

                if new_value <= 0:
                    print("Tỷ giá không hợp lệ!")
                    continue

            except ValueError:
                print("Tỷ giá không hợp lệ!")
                continue

            MemberCard.update_point_value(
                new_value
            )

            print("\nCập nhật tỷ giá thành công!")
            print(
                f"Tỷ giá mới: 1 điểm = {MemberCard.point_value_vnd:,} VNĐ"
            )

        case "6":
            print(
                "Cảm ơn bạn đã sử dụng hệ thống thẻ thành viên Rikkei Coffee!"
            )
            break

        case _:
            print("Lựa chọn không hợp lệ!")