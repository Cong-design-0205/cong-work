import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# =========================
# 分析逻辑
# =========================
def basic_analysis(df):
    # ====== 请确认与你的 CSV 列名一致 ======
    COL_START = "start_date"
    COL_END = "end_date"
    # ========================================

    # 日期转换
    df[COL_START] = pd.to_datetime(df[COL_START], errors="coerce")
    df[COL_END] = pd.to_datetime(df[COL_END], errors="coerce")

    # 是否离职
    df["is_left"] = df[COL_END].notna()

    # =========================
    # 基本人数 & 离职率
    # =========================
    total = len(df)
    left = df["is_left"].sum()
    turnover_rate = left / total if total > 0 else 0

    # =========================
    # 仅统计【已离职】员工的在职期间
    # =========================
    left_df = df[df["is_left"]].copy()

    if len(left_df) > 0:
        left_df["work_days"] = (left_df[COL_END] - left_df[COL_START]).dt.days
        avg_work_days = left_df["work_days"].mean()
        avg_work_years = avg_work_days / 365
    else:
        avg_work_days = 0
        avg_work_years = 0

    # =========================
    # 文本输出
    # =========================
    text = []
    text.append("【总体情况】")
    text.append(f"员工总数：{total}")
    text.append(f"已离职人数：{left}")
    text.append(f"离职率：{turnover_rate:.2%}")
    text.append("")
    text.append("【已离职员工在职期间】")
    text.append(f"平均在职期间：{avg_work_days:.1f} 天")
    text.append(f"约合：{avg_work_years:.2f} 年")

    return "\n".join(text)


# =========================
# CSV 读取 + 分析
# =========================
def analyze_csv():
    file_path = filedialog.askopenfilename(
        title="选择员工CSV文件",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    try:
        df = pd.read_csv(file_path)
        result = basic_analysis(df)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("错误", f"分析失败：\n{e}")


# =========================
# GUI
# =========================
root = tk.Tk()
root.title("员工离职率分析工具（个人版）")
root.geometry("520x360")

btn = tk.Button(
    root,
    text="选择 CSV 并分析",
    command=analyze_csv,
    height=2
)
btn.pack(pady=15)

result_text = tk.Text(root, width=60, height=15)
result_text.pack(padx=10, pady=10)

root.mainloop()


