"""
校园快递驿站包裹管理系统 - 主程序入口
支持库存管理员和取件人两种角色登录
"""
import sys
import io

# 强制 UTF-8 输出，避免 Windows 控制台 GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from manager import ParcelManager
from auth import AuthManager, UserRole


def admin_menu(manager: ParcelManager):
    """库存管理员菜单"""
    while True:
        print("\n========================================")
        print("  库存管理员 - 包裹管理")
        print("========================================")
        print("  1. 包裹入库")
        print("  2. 取件查询（按取件码取件）")
        print("  3. 显示所有包裹")
        print("  4. 删除超时未取包裹")
        print("  5. 修改包裹状态")
        print("  6. 删除指定包裹")
        print("  7. 按快递公司统计")
        print("  8. 按取件状态统计")
        print("  0. 退出登录")
        print("========================================")

        choice = input("请选择操作: ").strip()

        if choice == "1":
            # 包裹入库（管理员可设置关联取件人用户名）
            print("\n===== 包裹入库 =====")
            tracking_number = input("请输入包裹单号: ").strip()
            recipient_name = input("请输入收件人姓名: ").strip()
            courier_type = input("请输入快递类型(如:顺丰/中通/圆通/韵达等): ").strip()
            recipient_user = input("请输入关联取件人用户名(可选，直接回车跳过): ").strip()

            if not tracking_number or not recipient_name or not courier_type:
                print("❌ 包裹单号、收件人姓名、快递类型不能为空，入库失败！")
            else:
                manager.add_package_with_details(tracking_number, recipient_name,
                                                  courier_type, recipient_user)

        elif choice == "2":
            print("\n===== 取件查询 =====")
            pickup_code = input("请输入取件码: ").strip()
            if not manager.claim_by_pickup_code(pickup_code):
                print("❌ 未找到该取件码对应的包裹，请检查输入。")

        elif choice == "3":
            manager.display_all_packages()

        elif choice == "4":
            print("\n===== 删除超时未取包裹 =====")
            days_input = input("请输入超时天数(默认3天): ").strip()
            try:
                days = int(days_input) if days_input else 3
                if days <= 0:
                    days = 3
            except ValueError:
                days = 3
            manager.delete_overdue_packages(days)

        elif choice == "5":
            print("\n===== 修改包裹状态 =====")
            tracking_num = input("请输入要标记为已取件的包裹单号: ").strip()
            if not manager.modify_package_status(tracking_num):
                print("❌ 未找到该单号对应的包裹，或已是已取件状态。")

        elif choice == "6":
            print("\n===== 删除指定包裹 =====")
            tracking_num = input("请输入要删除的包裹单号: ").strip()
            if not manager.delete_package(tracking_num):
                print("❌ 未找到该单号对应的包裹。")

        elif choice == "7":
            manager.count_by_courier_type()

        elif choice == "8":
            manager.count_by_status()

        elif choice == "0":
            print("已退出管理员登录。")
            break

        else:
            print("❌ 无效选项，请输入 0-8 之间的数字。")

        input("\n按回车键继续...")


def recipient_menu(manager: ParcelManager, username: str):
    """取件人菜单"""
    while True:
        print("\n========================================")
        print("  取件人 - 我的包裹")
        print("========================================")
        print("  1. 查看我的包裹")
        print("  2. 领取包裹（按取件码）")
        print("  0. 退出登录")
        print("========================================")

        choice = input("请选择操作: ").strip()

        if choice == "1":
            manager.display_my_packages(username)

        elif choice == "2":
            print("\n===== 领取包裹 =====")
            pickup_code = input("请输入取件码: ").strip()
            if not manager.claim_my_package(username, pickup_code):
                print("❌ 未找到该取件码对应的包裹，或该包裹不属于您。")

        elif choice == "0":
            print("已退出取件人登录。")
            break

        else:
            print("❌ 无效选项，请输入 0-2 之间的数字。")

        input("\n按回车键继续...")


def login_screen(auth: AuthManager, manager: ParcelManager):
    """登录界面"""
    while True:
        print("\n========================================")
        print("     校园快递驿站包裹管理系统")
        print("========================================")
        print("  1. 库存管理员登录")
        print("  2. 取件人登录")
        print("  3. 注册取件人账户")
        print("  0. 退出系统")
        print("========================================")

        choice = input("请选择: ").strip()

        if choice == "1":
            # 管理员登录
            print("\n===== 库存管理员登录 =====")
            username = input("用户名: ").strip()
            password = input("密码: ").strip()
            user = auth.login(username, password)

            if user and user.role == UserRole.ADMIN:
                print(f"\n✅ 欢迎，{user.display_name}！")
                admin_menu(manager)
            else:
                print("❌ 用户名或密码错误，或无管理员权限。")
                input("\n按回车键继续...")

        elif choice == "2":
            # 取件人登录
            print("\n===== 取件人登录 =====")
            username = input("用户名: ").strip()
            password = input("密码: ").strip()
            user = auth.login(username, password)

            if user and user.role == UserRole.RECIPIENT:
                print(f"\n✅ 欢迎，{user.display_name}！")
                recipient_menu(manager, username)
            else:
                print("❌ 用户名或密码错误。")
                input("\n按回车键继续...")

        elif choice == "3":
            # 注册取件人
            print("\n===== 注册取件人账户 =====")
            username = input("请输入用户名: ").strip()
            password = input("请输入密码: ").strip()
            display_name = input("请输入显示名称(可选，直接回车使用用户名): ").strip()

            if auth.register_recipient(username, password, display_name):
                print("✅ 注册成功！请使用该账户登录。")
            else:
                print("❌ 注册失败。用户名可能已存在或输入不合法。")
            input("\n按回车键继续...")

        elif choice == "0":
            print("\n感谢使用校园快递驿站包裹管理系统！再见！")
            break

        else:
            print("❌ 无效选项，请输入 0-3 之间的数字。")
            input("\n按回车键继续...")


def main():
    """主函数"""
    manager = ParcelManager("packages.txt")
    auth = AuthManager("users.txt")
    login_screen(auth, manager)


if __name__ == "__main__":
    main()