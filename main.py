# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
from PIL import Image, ImageTk

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
            
# 定義函式：選擇顯示
def select(event):
    widget = event.widget
    selection=widget.curselection()
    if widget.curselection():
        picked = widget.get(selection[0])
        image = Image.open("emojis\\"+picked)
        zoomy = int(image.size[1]/(image.size[0]/160))
        image = image.resize((160,zoomy))
        img = ImageTk.PhotoImage(image)
        labelimage.place(x=292, y=220-int(zoomy/2))
        labelimage.configure(image=img)
        labelimage.image = img



# 建立主視窗
window = tk.Tk()
window.title("表情包管理軟體")
window.iconbitmap("ico.ico")
window.resizable(width=False, height=False)
window.minsize(width=480, height=320)
window.configure(bg="#DDDDFF")

labelimage = tk.Label(window,bg="#DDDDFF")
labelimage.place(x=292, y=320)

# 建立元件：新增表情包按鈕
add_button = tk.Button(window, text="新增表情包", command=add_emoji, font=("Arial", 10), width=8, height=4, bg="#D0E0EE")
add_button.place(x=340, y=40)

# 建立元件：搜尋表情包標籤
search_label = tk.Label(window, text="搜尋表情包", font=("Arial", 16),bg="#DDDDFF")
search_label.place(x=90, y=30)

# 建立元件：搜尋表情包輸入框

sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: on_keyword_changed(sv))

keyword_entry = tk.Entry(window, font=("Arial", 14), textvariable=sv)
keyword_entry.place(x=35, y=80)

#建立元件：滾動條
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#建立元件：搜尋結果列表
result_listbox = tk.Listbox(window, yscrollcommand=scrollbar.set, font=("Arial", 12), width=30, height=10)
result_listbox.place(x=10, y=125)
result_listbox.bind("<<ListboxSelect>>",select)

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