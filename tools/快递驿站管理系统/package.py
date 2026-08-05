"""
包裹类 - 定义包裹数据结构和相关操作
"""
import datetime
from enum import Enum
from typing import Optional


class PackageStatus(Enum):
    """包裹状态枚举"""
    UNCLAIMED = 0  # 未取件
    CLAIMED = 1    # 已取件

    def __str__(self) -> str:
        return "已取件" if self == PackageStatus.CLAIMED else "未取件"


class Package:
    """包裹类"""

    def __init__(
        self,
        tracking_number: str = "",
        recipient_name: str = "",
        pickup_code: str = "",
        courier_type: str = "",
        storage_time: Optional[datetime.datetime] = None,
        status: PackageStatus = PackageStatus.UNCLAIMED,
        recipient_username: str = "",  # 关联的取件人用户名
    ):
        self.tracking_number = tracking_number          # 包裹单号
        self.recipient_name = recipient_name            # 收件人姓名
        self.pickup_code = pickup_code                  # 取件码
        self.courier_type = courier_type                 # 快递类型
        self.storage_time = storage_time or datetime.datetime.now()  # 入库时间
        self.status = status                             # 取件状态
        self.recipient_username = recipient_username     # 关联取件人用户名

    def is_overdue(self, days: int = 3) -> bool:
        """判断是否超时（已取件的包裹不算超时）"""
        if self.status == PackageStatus.CLAIMED:
            return False
        delta = datetime.datetime.now() - self.storage_time
        return delta.days >= days

    def to_file_string(self) -> str:
        """将包裹信息格式化为一行文本（用于文件存储）"""
        return (
            f"{self.tracking_number},{self.recipient_name},"
            f"{self.pickup_code},{self.courier_type},"
            f"{self.storage_time.isoformat()},{self.status.value},"
            f"{self.recipient_username}"
        )

    @staticmethod
    def from_file_string(line: str) -> "Package":
        """从文本行解析包裹信息"""
        parts = line.strip().split(",")
        if len(parts) < 6:
            return Package()

        tracking_number = parts[0]
        recipient_name = parts[1]
        pickup_code = parts[2]
        courier_type = parts[3]
        storage_time = datetime.datetime.fromisoformat(parts[4])
        status = PackageStatus(int(parts[5]))
        recipient_username = parts[6] if len(parts) >= 7 else ""

        return Package(
            tracking_number=tracking_number,
            recipient_name=recipient_name,
            pickup_code=pickup_code,
            courier_type=courier_type,
            storage_time=storage_time,
            status=status,
            recipient_username=recipient_username,
        )

    def display(self) -> None:
        """显示包裹信息"""
        print("┌─────────────────────────────────────────────┐")
        print(f"│ 包裹单号: {self.tracking_number:<26}│")
        print(f"│ 收件人:   {self.recipient_name:<26}│")
        print(f"│ 取件码:   {self.pickup_code:<26}│")
        print(f"│ 快递类型: {self.courier_type:<26}│")
        print(f"│ 入库时间: {self.storage_time.strftime('%Y-%m-%d %H:%M:%S'):<26}│")
        print(f"│ 状态:     {str(self.status):<26}│")
        print("└─────────────────────────────────────────────┘")