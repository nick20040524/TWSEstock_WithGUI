# gui_main.py（最終更新版，若代碼不存在會語音播報）
import os
import warnings
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import threading
from gtts import gTTS
import speech_recognition as sr
from stock import workflow
from stock.setup_chinese_font import setup_chinese_font
import matplotlib.pyplot as plt
import urllib3

warnings.filterwarnings("ignore", category=UserWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

prop = setup_chinese_font()
plt.rcParams['font.sans-serif'] = [prop.get_name()]

from stock.update_module import get_target_codes
stock_codes = get_target_codes()

root = tk.Tk()
root.title("台股收盤價預測系統")
root.geometry("1000x800")

marquee_job = None
marquee_counter = 0

top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X, pady=5)

tk.Label(top_frame, text="選擇股票代碼：").pack(side=tk.LEFT, padx=5)
stock_code_var = tk.StringVar(value=stock_codes[0])
stock_code_menu = ttk.Combobox(top_frame, textvariable=stock_code_var, values=stock_codes, state="readonly", width=10)
stock_code_menu.pack(side=tk.LEFT, padx=5)

tk.Label(top_frame, text="選擇預測區間：").pack(side=tk.LEFT, padx=5)
predict_period_var = tk.StringVar(value="10天")
predict_period_menu = ttk.Combobox(top_frame, textvariable=predict_period_var, values=["10天", "全部"], state="readonly", width=10)
predict_period_menu.pack(side=tk.LEFT, padx=5)

tk.Button(top_frame, text="更新資料並預測", command=lambda: threading.Thread(target=threaded_workflow, daemon=True).start(), bg="lightblue").pack(side=tk.LEFT, padx=5)

tk.Button(top_frame, text="[MIC] 語音輸入股票代碼", command=lambda: threading.Thread(target=voice_input, daemon=True).start(), bg="lightgreen").pack(side=tk.LEFT, padx=5)

tk.Button(top_frame, text="結束", command=lambda: close_app(), bg="lightcoral").pack(side=tk.LEFT, padx=5)

status_label = tk.Label(root, text="[READY] 系統就緒", fg="blue", font=("Arial", 12, "bold"))
status_label.pack(pady=5)

info_frame = tk.Frame(root)
info_frame.pack(fill=tk.X, pady=5)
result_text = tk.Text(info_frame, height=7)
result_text.pack(fill=tk.X, padx=10)

paned_window = tk.PanedWindow(root, orient=tk.VERTICAL)
paned_window.pack(fill=tk.BOTH, expand=True)

table_frame = tk.Frame(paned_window)
tk.Label(table_frame, text="[TABLE] 預測統整表格：").pack()
tree_frame = tk.Frame(table_frame)
tree_frame.pack(fill=tk.BOTH, expand=True)
summary_tree = ttk.Treeview(tree_frame, show="headings")
summary_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=summary_tree.yview)
summary_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
paned_window.add(table_frame, stretch="always")

img_frame = tk.Frame(paned_window)
tk.Label(img_frame, text="[CHART] 收盤價趨勢圖：").pack()
img_label = tk.Label(img_frame)
img_label.pack(fill=tk.BOTH, expand=True)
paned_window.add(img_frame, stretch="always")


def speak_chinese(text):
    tts = gTTS(text=text, lang='zh-tw')
    tts.save("tts_output.mp3")
    os.system("mpg321 tts_output.mp3")


def threaded_workflow():
    status_text("[UPDATING] 資料更新中", "orange")
    result_text.delete("1.0", tk.END)
    for col in summary_tree["columns"]:
        summary_tree.heading(col, text="")
    summary_tree.delete(*summary_tree.get_children())
    img_label.config(image="")
    root.update()

    stock_code = stock_code_var.get()
    predict_period = predict_period_var.get()

    try:
        result_df, stock_name, model_r2 = workflow.update_and_predict_workflow(stock_code, verify_ssl=False)

        latest = result_df.sort_values("日期").groupby("股票代號").tail(1).copy()
        latest["預測日期"] = (pd.Timestamp.today() + pd.Timedelta(days=1)).strftime("%Y/%m/%d")
        latest_info = (
            f"股票代號: {stock_code}\n"
            f"股票名稱: {stock_name}\n"
            f"模型 R²: {model_r2*100:.2f}%\n"
            f"預測日期: {latest['預測日期'].values[0]}\n"
            f"實際收盤價: {latest['收盤價'].values[0]:.2f}\n"
            f"預測收盤價: {latest['預測收盤價'].values[0]:.2f}\n"
            f"信心度: {latest['信心度'].values[0]*100:.2f}%\n"
        )
        result_text.insert(tk.END, latest_info)

        speech = (
            f"股票代號 {stock_code}，"
            f"股票名稱 {stock_name}，"
            f"模型信心度 {model_r2*100:.1f}%，"
            f"預測收盤價 {latest['預測收盤價'].values[0]:.2f} 元，"
            f"信心度 {latest['信心度'].values[0]*100:.1f}%。"
        )
        speak_chinese(speech)

        if os.path.exists("prediction_report.xlsx"):
            df_summary = pd.read_excel("prediction_report.xlsx")
            summary_tree["columns"] = list(df_summary.columns)
            for col in df_summary.columns:
                summary_tree.heading(col, text=col)
                summary_tree.column(col, width=100, anchor="center")
            for _, row in df_summary.iterrows():
                summary_tree.insert("", tk.END, values=list(row))

        root.after(0, lambda: show_prediction_image(stock_code, predict_period))
        status_text("[DONE] 更新完成", "green")
    except Exception as e:
        status_text(f"[ERROR] 發生錯誤：{e}", "red")
        messagebox.showerror("錯誤", f"執行時發生錯誤：\n{e}")
        # 🔧 加上語音播報提示
        speak_chinese("找不到股票代碼，請再說一次")


def voice_input():
    recognizer = sr.Recognizer()
    device_index = 7  # 使用 PulseAudio 虛擬裝置
    try:
        with sr.Microphone(device_index=device_index, sample_rate=16000) as source:
            status_text("[MIC] 請說出股票代碼", "blue")
            audio = recognizer.listen(source, timeout=5)
            code_text = recognizer.recognize_google(audio, language="zh-TW")
            code_text = "".join(filter(str.isdigit, code_text))
            if code_text:
                stock_code_var.set(code_text)
                status_text(f"[OK] 偵測到股票代碼：{code_text}，即將開始預測", "green")
                speak_chinese(f"已偵測到股票代碼 {code_text}，即將開始預測")
                threading.Thread(target=threaded_workflow, daemon=True).start()
            else:
                status_text(f"[WARN] 語音無法辨識為數字", "red")
                speak_chinese("無法辨識為數字，請再試一次")
    except sr.UnknownValueError:
        status_text("[WARN] 語音無法辨識，請再說一次", "red")
        speak_chinese("無法辨識，請再說一次")
    except sr.WaitTimeoutError:
        status_text("[WARN] 語音輸入逾時", "red")
        speak_chinese("語音輸入逾時，請再試一次")
    except Exception as e:
        import traceback
        traceback.print_exc()
        status_text(f"[ERROR] 發生錯誤：{e}", "red")
        speak_chinese("發生錯誤")


def show_prediction_image(stock_code, period):
    img_path = f"charts/price_prediction_{stock_code}_{'ten' if period == '10天' else 'all'}.png"
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img = img.resize((600, 400))
        photo = ImageTk.PhotoImage(img)
        img_label.config(image=photo)
        img_label.image = photo
    else:
        img_label.config(text="[ERROR] 找不到圖檔", fg="red")


def status_text(text, color):
    global marquee_job, marquee_counter
    result_text.insert(tk.END, f"\n狀態：{text}\n")
    result_text.tag_configure("status", foreground=color)
    result_text.tag_add("status", "end-2l", "end-1l")
    status_label.config(text=text, fg=color)
    if marquee_job:
        root.after_cancel(marquee_job)
        marquee_job = None
    if "更新中" in text:
        marquee_counter = 0
        animate_marquee(text, color)


def animate_marquee(base_text, color):
    global marquee_job, marquee_counter
    dots = "." * (marquee_counter % 4)
    status_label.config(text=base_text + dots, fg=color)
    marquee_counter += 1
    marquee_job = root.after(500, animate_marquee, base_text, color)


def close_app():
    print("GUI 已關閉，返回 shell！")
    root.destroy()


status_text("[READY] 系統就緒", "blue")
root.mainloop()
