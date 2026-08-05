"""
校园快递驿站包裹管理系统 - Web 服务器
Flask 后端，提供 RESTful API 和前端界面
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import datetime
import json
from flask import Flask, render_template, request, jsonify, session
from manager import ParcelManager
from auth import AuthManager, UserRole
from package import Package, PackageStatus

app = Flask(__name__)
app.secret_key = "campus_package_secret_key_2026"

# 全局实例（单例）
manager = ParcelManager("packages.txt")
auth = AuthManager("users.txt")

# 快递公司列表
COURIER_TYPES = ["顺丰", "中通", "圆通", "韵达", "申通", "极兔", "京东", "邮政", "德邦", "其他"]


# ==================== 页面路由 ====================

@app.route("/")
def index():
    """首页"""
    return render_template("index.html")


# ==================== 用户认证 API ====================

@app.route("/api/login", methods=["POST"])
def api_login():
    """用户登录"""
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    user = auth.login(username, password)
    if user is None:
        return jsonify({"success": False, "message": "用户名或密码错误"})

    session["username"] = user.username
    session["role"] = user.role.value
    session["display_name"] = user.display_name

    return jsonify({
        "success": True,
        "message": f"欢迎，{user.display_name}！",
        "user": {
            "username": user.username,
            "role": user.role.value,
            "display_name": user.display_name
        }
    })


@app.route("/api/register", methods=["POST"])
def api_register():
    """注册取件人"""
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    display_name = data.get("display_name", "").strip()

    if auth.register_recipient(username, password, display_name):
        return jsonify({"success": True, "message": "注册成功！请登录。"})
    else:
        return jsonify({"success": False, "message": "注册失败，用户名可能已存在。"})


@app.route("/api/session", methods=["GET"])
def api_session():
    """获取当前会话信息"""
    if "username" not in session:
        return jsonify({"success": False, "logged_in": False})
    return jsonify({
        "success": True,
        "logged_in": True,
        "user": {
            "username": session["username"],
            "role": session["role"],
            "display_name": session["display_name"]
        }
    })


@app.route("/api/logout", methods=["POST"])
def api_logout():
    """登出"""
    session.clear()
    return jsonify({"success": True, "message": "已退出登录"})


# ==================== 用户列表 API ====================

@app.route("/api/recipients", methods=["GET"])
def api_get_recipients():
    """获取所有取件人列表（供入库时选择）"""
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "权限不足"}), 403

    recipients = []
    for user in auth.users:
        if user.role == UserRole.RECIPIENT:
            recipients.append({
                "username": user.username,
                "display_name": user.display_name
            })
    return jsonify({"success": True, "recipients": recipients})


# ==================== 包裹数据 API ====================

def _package_to_dict(pkg: Package) -> dict:
    """将包裹对象转为字典"""
    return {
        "tracking_number": pkg.tracking_number,
        "recipient_name": pkg.recipient_name,
        "pickup_code": pkg.pickup_code,
        "courier_type": pkg.courier_type,
        "storage_time": pkg.storage_time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "已取件" if pkg.status == PackageStatus.CLAIMED else "未取件",
        "is_claimed": pkg.status == PackageStatus.CLAIMED,
        "is_overdue": pkg.is_overdue(3),
        "recipient_username": pkg.recipient_username
    }


@app.route("/api/packages", methods=["GET"])
def api_get_packages():
    """获取包裹列表（管理员看全部，取件人只能看自己的）"""
    if "username" not in session:
        return jsonify({"success": False, "message": "未登录"}), 401

    role = session["role"]
    username = session["username"]

    if role == "admin":
        pkg_list = [_package_to_dict(p) for p in manager.packages]
    else:
        # 取件人只能看到关联到自己账户的包裹
        pkg_list = [
            _package_to_dict(p) for p in manager.packages
            if p.recipient_username == username
        ]

    return jsonify({"success": True, "packages": pkg_list, "total": len(pkg_list)})


@app.route("/api/packages", methods=["POST"])
def api_add_package():
    """添加单个包裹（仅管理员）"""
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "权限不足"}), 403

    data = request.get_json()
    tracking_number = data.get("tracking_number", "").strip()
    recipient_name = data.get("recipient_name", "").strip()
    courier_type = data.get("courier_type", "").strip()
    recipient_username = data.get("recipient_username", "").strip()

    if not tracking_number or not recipient_name or not courier_type:
        return jsonify({"success": False, "message": "请填写必填字段"})

    if not recipient_username:
        return jsonify({"success": False, "message": "请选择收件人，每个包裹必须关联一个取件人账户"})

    manager.add_package_with_details(tracking_number, recipient_name,
                                      courier_type, recipient_username)
    for pkg in manager.packages:
        if pkg.tracking_number == tracking_number:
            return jsonify({
                "success": True,
                "message": f"包裹入库成功！取件码: {pkg.pickup_code}",
                "package": _package_to_dict(pkg)
            })
    return jsonify({"success": True, "message": "入库成功"})


@app.route("/api/packages/batch", methods=["POST"])
def api_batch_add_packages():
    """批量添加包裹（仅管理员）- 分栏式入库"""
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "权限不足"}), 403

    data = request.get_json()
    recipient_username = data.get("recipient_username", "").strip()
    recipient_name = data.get("recipient_name", "").strip()
    packages = data.get("packages", [])

    if not recipient_username or not recipient_name:
        return jsonify({"success": False, "message": "请选择收件人"})

    if not packages or len(packages) == 0:
        return jsonify({"success": False, "message": "请至少添加一个包裹"})

    results = manager.batch_add_packages(recipient_name, recipient_username, packages)

    return jsonify({
        "success": True,
        "message": f"成功入库 {len(results)} 个包裹！",
        "results": results,
        "count": len(results)
    })


@app.route("/api/packages/claim", methods=["PUT"])
def api_claim_package():
    """领取包裹（仅限关联的取件人领取）"""
    if "username" not in session:
        return jsonify({"success": False, "message": "未登录"}), 401

    data = request.get_json()
    pickup_code = data.get("pickup_code", "").strip()
    username = session["username"]

    if session["role"] == "admin":
        # 管理员可以代领，但也需要校验收件人
        success = manager.claim_by_pickup_code(pickup_code)
    else:
        # 取件人只能领自己的（manager.claim_my_package 会校验 recipient_username）
        success = manager.claim_my_package(username, pickup_code)

    if success:
        return jsonify({"success": True, "message": "取件成功！"})
    else:
        return jsonify({"success": False, "message": "取件失败，请检查取件码是否正确。"})


@app.route("/api/packages/query", methods=["GET"])
def api_query_package():
    """按取件码查询包裹信息"""
    if "username" not in session:
        return jsonify({"success": False, "message": "未登录"}), 401

    pickup_code = request.args.get("pickup_code", "").strip()
    if not pickup_code:
        return jsonify({"success": False, "message": "请输入取件码"})

    # 线性查找
    pkg = manager._find_by_pickup_code(pickup_code)
    if pkg is None:
        return jsonify({"success": False, "message": f"未找到取件码为 {pickup_code} 的包裹"})

    # 权限校验：取件人只能查看自己的包裹
    if session["role"] != "admin":
        if pkg.recipient_username and pkg.recipient_username != session["username"]:
            return jsonify({"success": False, "message": "该取件码不属于您"})

    return jsonify({"success": True, "package": _package_to_dict(pkg)})


@app.route("/api/packages/<tracking_number>", methods=["DELETE"])
def api_delete_package(tracking_number):
    """删除指定包裹（仅管理员）"""
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "权限不足"}), 403

    if manager.delete_package(tracking_number):
        return jsonify({"success": True, "message": "包裹已删除"})
    else:
        return jsonify({"success": False, "message": "未找到该包裹"})


@app.route("/api/packages/overdue", methods=["DELETE"])
def api_delete_overdue():
    """删除超时包裹（仅管理员）"""
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "权限不足"}), 403

    days = request.args.get("days", 3, type=int)
    count = manager.delete_overdue_packages(days)
    return jsonify({"success": True, "message": f"已删除 {count} 个超时包裹", "count": count})


@app.route("/api/packages/mark-claimed", methods=["PUT"])
def api_mark_claimed():
    """管理员标记包裹为已取件"""
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "权限不足"}), 403

    data = request.get_json()
    tracking_number = data.get("tracking_number", "").strip()
    if manager.modify_package_status(tracking_number):
        return jsonify({"success": True, "message": "状态已更新"})
    else:
        return jsonify({"success": False, "message": "未找到该包裹或已是已取件状态"})


# ==================== 统计 API ====================

def _get_filtered_packages():
    """根据角色获取该用户能看到的包裹列表"""
    if "username" not in session:
        return manager.packages
    role = session["role"]
    username = session["username"]
    if role == "admin":
        return manager.packages
    else:
        return [p for p in manager.packages if p.recipient_username == username]


@app.route("/api/statistics/courier")
def api_stats_courier():
    """各快递公司统计（仅管理员可见完整数据）"""
    if session.get("role") != "admin":
        return jsonify({"success": True, "data": [], "total": 0})
    from collections import Counter
    courier_count = Counter(p.courier_type for p in manager.packages)
    data = [{"name": k, "count": v} for k, v in courier_count.items()]
    return jsonify({"success": True, "data": data, "total": sum(courier_count.values())})


@app.route("/api/statistics/status")
def api_stats_status():
    """取件状态统计（取件人只看自己的，管理员看全部）"""
    filtered = _get_filtered_packages()
    claimed = sum(1 for p in filtered if p.status == PackageStatus.CLAIMED)
    unclaimed = sum(1 for p in filtered if p.status == PackageStatus.UNCLAIMED)
    return jsonify({
        "success": True,
        "claimed": claimed,
        "unclaimed": unclaimed,
        "total": claimed + unclaimed
    })


# ==================== 启动 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("  校园快递驿站包裹管理系统 - Web 服务")
    print("=" * 50)
    print("  启动地址: http://127.0.0.1:5000")
    print("  管理员账户: admin / admin123")
    print("=" * 50)
    app.run(debug=True, host="127.0.0.1", port=5000)