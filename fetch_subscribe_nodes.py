#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_subscribe_nodes.py
自动获取VPN订阅节点，清理反斜杠和双引号，并保存到文档
"""

import sys
import uuid
import requests

def main():
    # 生成随机UUID（大写格式，与示例一致）
    device_id = str(uuid.uuid4()).upper()
    print(f"生成设备ID: {device_id}")

    # ---------- 第一步：登录获取 auth_data ----------
    login_url = "http://8.217.172.131/api/v1/passport/auth/appLoginWithDeviceId"
    login_headers = {
        "Host": "8.217.172.131",
        "Content-Type": "application/json; charset=utf-8",
        "Connection": "keep-alive",
        "app": "iOS",
        "Accept": "*/*",
        "version": "1.1",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "PeaVPN/8 CFNetwork/1399 Darwin/22.1.0"
    }
    login_payload = {"device_id": device_id}

    try:
        resp = requests.post(login_url, headers=login_headers, json=login_payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 200:
            print(f"登录失败: {data}")
            sys.exit(1)
        auth_data = data["data"]["auth_data"]
        print("登录成功，已获取 auth_data")
    except Exception as e:
        print(f"登录请求异常: {e}")
        sys.exit(1)

    # ---------- 第二步：获取订阅节点 ----------
    subscribe_url = "http://8.217.172.131/api/v1/user/appGetSubscribe"
    subscribe_headers = {
        "Host": "8.217.172.131",
        "Content-Type": "application/json; charset=utf-8",
        "deviceid": device_id,                # 使用相同的设备ID
        "app": "iOS",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "version": "1.1",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Authorization": auth_data,           # 上一步获取的JWT
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "PeaVPN/8 CFNetwork/1399 Darwin/22.1.0"
    }

    try:
        resp = requests.get(subscribe_url, headers=subscribe_headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 200:
            print(f"获取订阅失败: {data}")
            sys.exit(1)

        nodes = data["data"]["nodes"]
        # 删除每个节点字符串中的反斜杠和双引号
        cleaned_nodes = [node.replace("\\", "").replace('"', "") for node in nodes]

        # 写入文档（纯文本，每行一个节点）
        output_file = "subscribe_nodes.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            for node in cleaned_nodes:
                f.write(node + "\n")

        print(f"成功获取 {len(cleaned_nodes)} 个节点，已保存至 {output_file}")
    except Exception as e:
        print(f"订阅请求异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()