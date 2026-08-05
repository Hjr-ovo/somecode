"""
包裹管理类 - 实现校园快递驿站的包裹管理核心逻辑
"""
import os
from typing import Optional, List
from package import Package, PackageStatus


class ParcelManager:
    """校园快递驿站包裹管理类"""

    def __init__(self, file_path: str = "packages.txt"):
        self.packages: List[Package] = []   # 使用列表存储所有包裹（顺序表）
        self.file_path = file_path          # 数据文件路径
        self._load_from_file()               # 启动时加载数据

    def _generate_pickup_code(self) -> str:
        """生成取件码（从 A001 开始递增）"""
        max_num = 0
        for pkg in self.packages:
            code = pkg.pickup_code
            if len(code) >= 4 and code[0] == 'A' and code[1:].isdigit():
                num = int(code[1:])
                if num > max_num:
                    max_num = num
        max_num += 1
        return f"A{max_num:03d}"

    # ----- 包裹入库 -----
    def add_package(self, recipient_username: str = "") -> None:
        """录入新包裹"""
        print("\n===== 包裹入库 =====")
        tracking_number = input("请输入包裹单号: ").strip()
        recipient_name = input("请输入收件人姓名: ").strip()
        courier_type = input("请输入快递类型(如:顺丰/中通/圆通/韵达等): ").strip()

        if not tracking_number or not recipient_name or not courier_type:
            print("❌ 所有字段不能为空，入库失败！")
            return

        pickup_code = self._generate_pickup_code()
        pkg = Package(
            tracking_number=tracking_number,
            recipient_name=recipient_name,
            pickup_code=pickup_code,
            courier_type=courier_type,
            recipient_username=recipient_username,
        )
        self.packages.append(pkg)

        print(f"\n✅ 包裹入库成功！")
        print(f"👉 取件码为: {pickup_code}，请告知收件人。")
        pkg.display()
        self._save_to_file()

    # ----- 包裹入库（带详细参数，供管理员菜单调用）-----
    def add_package_with_details(self, tracking_number: str, recipient_name: str,
                                   courier_type: str, recipient_username: str = "") -> None:
        """管理员直接传入参数的入库方法"""
        if not tracking_number or not recipient_name or not courier_type:
            print("❌ 所有字段不能为空，入库失败！")
            return

        pickup_code = self._generate_pickup_code()
        pkg = Package(
            tracking_number=tracking_number,
            recipient_name=recipient_name,
            pickup_code=pickup_code,
            courier_type=courier_type,
            recipient_username=recipient_username,
        )
        self.packages.append(pkg)

        print(f"\n✅ 包裹入库成功！")
        print(f"👉 取件码为: {pickup_code}，请告知收件人。")
        if recipient_username:
            print(f"📌 已关联取件人: {recipient_username}")
        pkg.display()
        self._save_to_file()

    # ----- 批量入库 -----
    def batch_add_packages(self, recipient_name: str, recipient_username: str,
                            packages: list) -> list:
        """批量添加包裹，返回生成的取件码列表"""
        results = []
        for item in packages:
            tracking_number = item.get("tracking_number", "").strip()
            courier_type = item.get("courier_type", "").strip()
            if not tracking_number or not courier_type:
                continue

            pickup_code = self._generate_pickup_code()
            pkg = Package(
                tracking_number=tracking_number,
                recipient_name=recipient_name,
                pickup_code=pickup_code,
                courier_type=courier_type,
                recipient_username=recipient_username,
            )
            self.packages.append(pkg)
            results.append({
                "tracking_number": tracking_number,
                "pickup_code": pickup_code,
                "courier_type": courier_type
            })

        if results:
            self._save_to_file()
        return results

    # ----- 取件查询 -----
    def claim_by_pickup_code(self, pickup_code: str) -> bool:
        """按取件码查找并标记已取件"""
        pkg = self._find_by_pickup_code(pickup_code)
        if pkg is None:
            return False

        if pkg.status == PackageStatus.CLAIMED:
            print("⚠️ 该包裹已被取走！")
            return False

        pkg.status = PackageStatus.CLAIMED
        print("\n✅ 取件成功！以下是包裹信息:")
        pkg.display()
        self._save_to_file()
        return True

    # ----- 删除超时未取包裹 -----
    def delete_overdue_packages(self, days: int = 3) -> int:
        """删除超时未取的包裹"""
        count = 0
        remaining = []
        for pkg in self.packages:
            if pkg.is_overdue(days):
                print(f"删除超时包裹: {pkg.tracking_number} "
                      f"({pkg.recipient_name}, "
                      f"入库时间: {pkg.storage_time.strftime('%Y-%m-%d %H:%M:%S')})")
                count += 1
            else:
                remaining.append(pkg)

        self.packages = remaining

        if count > 0:
            print(f"\n✅ 已删除 {count} 个超时未取包裹。")
            self._save_to_file()
        else:
            print("📭 没有超时未取的包裹。")
        return count

    # ----- 修改包裹状态 -----
    def modify_package_status(self, tracking_number: str) -> bool:
        """按单号修改包裹状态为已取件"""
        pkg = self._find_by_tracking_number(tracking_number)
        if pkg is None:
            return False

        if pkg.status == PackageStatus.CLAIMED:
            print("⚠️ 该包裹已经是已取件状态。")
            return False

        pkg.status = PackageStatus.CLAIMED
        print("\n✅ 包裹状态已更新为已取件！")
        pkg.display()
        self._save_to_file()
        return True

    # ----- 删除指定包裹 -----
    def delete_package(self, tracking_number: str) -> bool:
        """按单号删除指定包裹"""
        for i, pkg in enumerate(self.packages):
            if pkg.tracking_number == tracking_number:
                print("删除包裹:")
                pkg.display()
                self.packages.pop(i)
                print("\n✅ 包裹已删除。")
                self._save_to_file()
                return True
        return False

    # ----- 查找功能 -----
    def _find_by_pickup_code(self, pickup_code: str) -> Optional[Package]:
        """按取件码查找包裹（线性查找）"""
        for pkg in self.packages:
            if pkg.pickup_code == pickup_code:
                return pkg
        return None

    def _find_by_tracking_number(self, tracking_number: str) -> Optional[Package]:
        """按单号查找包裹"""
        for pkg in self.packages:
            if pkg.tracking_number == tracking_number:
                return pkg
        return None

    def find_and_display_by_pickup_code(self) -> None:
        """按取件码查找并显示包裹信息（不修改状态）"""
        code = input("请输入取件码: ").strip()
        pkg = self._find_by_pickup_code(code)
        if pkg:
            pkg.display()
        else:
            print("❌ 未找到该取件码对应的包裹。")

    # ----- 显示所有包裹 -----
    def display_all_packages(self) -> None:
        """显示所有包裹信息"""
        if not self.packages:
            print("📭 当前没有包裹记录。")
            return

        print(f"\n========== 所有包裹列表 ==========")
        print(f"共 {len(self.packages)} 个包裹\n")
        for i, pkg in enumerate(self.packages, 1):
            print(f"【包裹 {i}】")
            pkg.display()

    # ----- 取件人：查看自己的包裹 -----
    def display_my_packages(self, username: str) -> None:
        """显示当前取件人关联的所有包裹"""
        my_pkgs = [pkg for pkg in self.packages if pkg.recipient_username == username]

        if not my_pkgs:
            print(f"📭 您目前没有关联的包裹。")
            return

        print(f"\n========== 我的包裹 ==========")
        print(f"共 {len(my_pkgs)} 个包裹\n")
        for i, pkg in enumerate(my_pkgs, 1):
            print(f"【包裹 {i}】")
            pkg.display()

    # ----- 取件人：领取自己的包裹 -----
    def claim_my_package(self, username: str, pickup_code: str) -> bool:
        """取件人按取件码领取自己的包裹"""
        pkg = self._find_by_pickup_code(pickup_code)
        if pkg is None:
            return False

        # 检查是否是自己的包裹
        if pkg.recipient_username and pkg.recipient_username != username:
            print("⚠️ 该取件码不属于您，无法领取。")
            return False

        if pkg.status == PackageStatus.CLAIMED:
            print("⚠️ 该包裹已被取走！")
            return False

        pkg.status = PackageStatus.CLAIMED
        print("\n✅ 取件成功！以下是您的包裹信息:")
        pkg.display()
        self._save_to_file()
        return True

    # ----- 统计功能 -----
    def count_by_courier_type(self) -> None:
        """统计各快递公司的包裹数量"""
        courier_count = {}
        for pkg in self.packages:
            courier_count[pkg.courier_type] = courier_count.get(pkg.courier_type, 0) + 1

        print("\n===== 各快递公司包裹数量统计 =====")
        if not courier_count:
            print("暂无包裹数据。")
            return

        total = 0
        for courier, count in courier_count.items():
            print(f"  {courier} : {count} 个")
            total += count
        print(f"  ---------------------")
        print(f"  总计: {total} 个")

    def count_by_status(self) -> None:
        """统计已取/未取包裹数量"""
        claimed = sum(1 for pkg in self.packages if pkg.status == PackageStatus.CLAIMED)
        unclaimed = sum(1 for pkg in self.packages if pkg.status == PackageStatus.UNCLAIMED)

        print("\n===== 包裹取件状态统计 =====")
        print(f"  已取件: {claimed} 个")
        print(f"  未取件: {unclaimed} 个")
        print(f"  总计:   {claimed + unclaimed} 个")

    # ----- 文件持久化 -----
    def _save_to_file(self) -> None:
        """保存包裹数据到文件"""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                for pkg in self.packages:
                    f.write(pkg.to_file_string() + "\n")
        except IOError as e:
            print(f"❌ 无法保存数据到文件 {self.file_path}：{e}")

    def _load_from_file(self) -> None:
        """从文件加载包裹数据"""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.packages.clear()
                for line in f:
                    line = line.strip()
                    if line:
                        pkg = Package.from_file_string(line)
                        if pkg.tracking_number:  # 有效包裹
                            self.packages.append(pkg)
            print(f"📂 已从 {self.file_path} 加载 {len(self.packages)} 个包裹记录。")
        except IOError:
            pass