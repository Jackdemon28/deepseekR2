import os
import time
import platform
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import subprocess
import sys
import winreg  # Windows注册表操作

# ======================== 免责声明弹窗 ========================
def show_disclaimer():
    root = tk.Tk()
    root.title("免责声明")
    root.geometry("600x400")
    
    disclaimer_text = """
    ⚠️ 警告：这是一个模拟的假病毒程序，仅用于娱乐或教育目的！

    功能说明：
    - 模拟病毒扫描（无害）
    - 弹窗互动（需输入密码关闭）
    - 60秒倒计时（可取消）

    ❗ 注意：
    1. 此程序不会真正破坏你的电脑。
    2. 仅供测试/玩笑使用，请勿用于恶意目的。
    3. 运行前请保存所有工作（以防意外重启）。

    点击【我同意】继续，点击【拒绝】退出。
    """
    
    label = tk.Label(root, text=disclaimer_text, justify="left", padx=20, pady=20)
    label.pack()
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    def on_agree():
        root.destroy()
        fake_virus()  # 用户同意后运行假病毒
    
    def on_disagree():
        root.destroy()
        sys.exit(0)  # 用户拒绝则退出
    
    tk.Button(button_frame, text="我同意", command=on_agree, bg="green", fg="white", width=10).pack(side="left", padx=20)
    tk.Button(button_frame, text="拒绝", command=on_disagree, bg="red", fg="white", width=10).pack(side="right", padx=20)
    
    root.mainloop()

# ======================== 假病毒主逻辑 ========================
def countdown(seconds):
    for i in range(seconds, 0, -1):
        time.sleep(1)
        print(f"\r系统将在 {i} 秒后重启！", end="", flush=True)
    
    # 真正重启（Windows: shutdown /r | macOS: osascript）
    if platform.system() == "Windows":
        os.system("shutdown /r /t 0")
    else:
        subprocess.run(["osascript", "-e", 'tell app "System Events" to restart'])

def fake_virus():
    is_windows = platform.system() == "Windows"
    
    # 1. 模拟病毒扫描（假的）
    print("=== 模拟病毒扫描（无害玩笑） ===")
    print("警告：输入错误会触发重启！\n")
    time.sleep(2)
    
    # 2. 假感染文件计数
    for i in range(1, 100):
        time.sleep(0.05)
        print(f"\r感染文件 ({i * 100}/9999) [{'■' * (i % 20)}]", end="", flush=True)
    
    # 3. 弹窗“说666”
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("警告", "你的电脑已被假病毒感染！")
    
    # 4. 输入验证
    user_input = simpledialog.askstring("Link:box.chatoyant.top/box/card", "输入卡密关闭病毒:", parent=root)
    
    if user_input == "666":
        print("\n你赢了！假病毒已关闭。")
        return
    else:
        print("\n输入错误！电脑将在60秒后重启！")
        
        # 启动倒计时线程
        countdown_thread = threading.Thread(target=countdown, args=(3,))
        countdown_thread.start()
        
        # 显示重启警告
        messagebox.showwarning(
            "最后警告", 
            "电脑将在3秒后重启！\n\n" 
            "Restarting your computer..."
        )

# ======================== 开机自启动 ========================
def add_to_startup():
    script_path = os.path.abspath(__file__)
    
    if platform.system() == "Windows":
        # Windows: 写入注册表
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "FakeVirus", 0, winreg.REG_SZ, f'python "{script_path}"')
            winreg.CloseKey(key)
            print("✅ 已添加到 Windows 开机启动！")
        except Exception as e:
            print(f"❌ 添加失败: {e}")
    else:
        # macOS: 写入 LaunchAgent
        plist_path = os.path.expanduser("~/Library/LaunchAgents/fake.virus.plist")
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>fake.virus</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
        try:
            os.makedirs(os.path.dirname(plist_path), exist_ok=True)
            with open(plist_path, "w") as f:
                f.write(plist_content)
            os.system(f"launchctl load {plist_path}")
            print("✅ 已添加到 macOS 开机启动！")
        except Exception as e:
            print(f"❌ 添加失败: {e}")

# ======================== 主程序入口 ========================
if __name__ == "__main__":
    if "--setup" in sys.argv:
        add_to_startup()  # 设置开机自启动
    else:
        show_disclaimer()  # 先显示免责声明