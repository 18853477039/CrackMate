import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import zipfile
import threading
import time

# 创建主窗口
window = tk.Tk()
window.title("密码破解程序")
window.geometry("400x300")

# 全局变量
cracking = False  # 破解进行状态
start_time = None  # 破解开始时间


# 选择文件并显示文件路径
def select_file():
    file_path = filedialog.askopenfilename()
    file_label.config(text="文件路径: " + file_path)


# 暴力破解文件密码
def crack_password():
    global cracking, start_time
    if cracking:
        return
    zip_file = file_label.cget("text").split(": ")[1]
    cracking = True
    start_time = time.time()
    progress_bar.start(10)  # 启动进度条
    result_label.config(text="正在破解...")
    crack_button.config(state=tk.DISABLED)  # 禁用开始破解按钮
    cancel_button.config(state=tk.NORMAL)  # 启用取消按钮
    threading.Thread(target=crack_zip, args=(zip_file,)).start()  # 在后台线程中执行破解操作


# 在后台线程中进行密码破解
def crack_zip(zip_file):
    global cracking, start_time
    with zipfile.ZipFile(zip_file) as zf:
        for password in generate_passwords():
            if not cracking:
                break
            try:
                zf.extractall(pwd=bytes(password, 'utf-8'))
                cracking = False
                progress_bar.stop()  # 停止进度条
                result_label.config(text="密码破解成功: " + password)
                break
            except:
                continue
        if cracking:
            progress_bar.stop()  # 停止进度条
            result_label.config(text="密码破解失败。")
        crack_button.config(state=tk.NORMAL)  # 启用开始破解按钮
        cancel_button.config(state=tk.DISABLED)  # 禁用取消按钮


# 取消破解
def cancel_crack():
    global cracking
    cracking = False
    crack_button.config(state=tk.NORMAL)  # 启用开始破解按钮
    cancel_button.config(state=tk.DISABLED)  # 禁用取消按钮
    update_ui_cancelled()


# 更新界面状态（破解取消）
def update_ui_cancelled():
    progress_bar.stop()  # 停止进度条
    result_label.config(text="密码破解取消")


# 生成所有可能的四位数字密码
def generate_passwords():
    passwords = []
    for i in range(10000):
        password = str(i).zfill(4)  # 将数字转换为四位数密码
        passwords.append(password)
    return passwords


# 更新计时器
def update_timer():
    if start_time is not None and cracking:
        elapsed_time = int(time.time() - start_time)
        timer_label.config(text="已用时间: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    window.after(1000, update_timer)


# 创建选择文件按钮
file_button = tk.Button(window, text="选择文件", command=select_file)
file_button.pack(pady=20)

# 显示文件路径
file_label = tk.Label(window, text="文件路径: ")
file_label.pack()

# 创建破解按钮
crack_button = tk.Button(window, text="开始破解", command=crack_password)
crack_button.pack(pady=10)

# 创建取消按钮
cancel_button = tk.Button(window, text="取消", command=cancel_crack, state=tk.DISABLED)
cancel_button.pack(pady=10)

# 创建进度条
progress_bar = ttk.Progressbar(window, mode='indeterminate')
progress_bar.pack(pady=10)

# 显示破解结果
result_label = tk.Label(window, text="")
result_label.pack()

# 显示计时器
timer_label = tk.Label(window, text="已用时间: 00:00:00")
timer_label.pack()

# 更新计时器
update_timer()

# 运行主循环
window.mainloop()
