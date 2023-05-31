# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar


# 建立表情包存放目錄，若已存在則跳過
if not os.path.exists("emojis"):
    os.mkdir("emojis")

# 定義函式：新增表情包
def add_emoji():
    # 開啟檔案選擇器
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        # 取得檔案名稱
        file_name = os.path.basename(file_path)
        # 開啟對話框讓使用者輸入檔案命名
        new_file_name = filedialog.asksaveasfilename(initialdir="emojis", initialfile=file_name, defaultextension=".png")
        # 若使用者有輸入檔案命名，則複製檔案到表情包目錄下
        if new_file_name:
            print(new_file_name)
            os.system(("copy "+file_path+" "+new_file_name).replace("/", "\\"))
            messagebox.showinfo("新增表情包", "表情包新增成功！")

# 定義函式：搜尋表情包
def search_emoji():
    # 取得搜尋關鍵字
    keyword = keyword_entry.get()
    # 搜尋表情包目錄下的所有檔案
    result = []
    for file_name in os.listdir("emojis"):
        # 若檔案名稱中包含關鍵字，則加入搜尋結果
        if keyword.lower() in file_name.lower():
            result.append(file_name)
    # 顯示搜尋結果
    if result:
        result_label.config(text="\n".join(result))
    else:
        result_label.config(text="查無結果！")

# 建立主視窗
window = tk.Tk()
window.title("表情包管理軟體")

# 建立元件：新增表情包按鈕
add_button = tk.Button(window, text="新增表情包", command=add_emoji)
add_button.pack(padx=20, pady=10)

# 建立元件：搜尋表情包標籤
search_label = tk.Label(window, text="搜尋表情包", font=("Arial", 16))
search_label.pack(padx=20, pady=10)

# 建立元件：搜尋表情包輸入框

sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: on_keyword_changed(sv))

keyword_entry = tk.Entry(window, font=("Arial", 14), textvariable=sv)
keyword_entry.pack(padx=20, pady=5)

# 建立元件：搜尋表情包按鈕
search_button = tk.Button(window, text="搜尋", font=("Arial", 14), command=search_emoji)
search_button.pack(padx=20, pady=5)

# 建立元件：搜尋結果標籤
result_label = tk.Label(window, text="", font=("Arial", 12), wraplength=600)
result_label.pack(padx=20, pady=5)
#建立元件：滾動條
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#建立元件：搜尋結果列表
result_listbox = tk.Listbox(window, yscrollcommand=scrollbar.set, font=("Arial", 12), width=50, height=10)
result_listbox.pack(padx=20, pady=10)

#設定滾動條與列表的連動
scrollbar.config(command=result_listbox.yview)

#定義函式：更新搜尋結果列表
def update_result_list():
    # 取得搜尋關鍵字
    keyword = sv.get()
    # 清空搜尋結果列表
    result_listbox.delete(0, tk.END)
    # 搜尋表情包目錄下的所有檔案
    for file_name in os.listdir("emojis"):
        # 若檔案名稱中包含關鍵字，則加入搜尋結果列表
        if keyword.lower() in file_name.lower():
            result_listbox.insert(tk.END, file_name)

#設定搜尋關鍵字輸入框的事件處理函式
def on_keyword_changed(*args):
    # 更新搜尋結果列表
    update_result_list()

    sv.trace_add("write", on_keyword_changed)

#設定搜尋結果列表的雙擊事件處理函式
def on_result_listbox_double_click(event):
    # 取得所選擇的檔案名稱
    selected_file_name = result_listbox.get(result_listbox.curselection())
    # 開啟該檔案
    os.system("")

    result_listbox.bind("<Double-Button-1>", on_result_listbox_double_click)

#啟動主視窗
window.mainloop()