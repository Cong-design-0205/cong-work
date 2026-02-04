import pandas as pd

# ========= 1. 文件路径 =========
input_file = r"C:\python_work\kintoneアプリデータ整理（20260203）.xlsx"
output_file = r"C:\python_work\app_summary1.xlsx"

# ========= 2. 读取 Excel =========
df = pd.read_excel(input_file)

# ========= 3. 时间列转换 =========
df["作成日時"] = pd.to_datetime(df["作成日時"])
df["設定の最終更新日時"] = pd.to_datetime(df["設定の最終更新日時"])

# ========= 4. 计算开发期间（天） =========
df["開発期間（日）"] = (
    df["設定の最終更新日時"] - df["作成日時"]
).dt.days

# ========= 5. 作成者別集計 =========
creator_summary = (
    df
    .groupby("作成者")
    .agg(
        部署名=("部署名", "first"),
        アプリ数=("アプリ名", "count"),
        累計開発日数=("開発期間（日）", "sum")
    )
    .reset_index()
)

# ========= 6. 部署別集計 =========
dept_summary = (
    df
    .groupby("部署名")
    .agg(
        アプリ数=("アプリ名", "count"),
        累計開発日数=("開発期間（日）", "sum")
    )
    .reset_index()
)

# ========= 7. 输出到一个 Excel（两个 Sheet） =========
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    creator_summary.to_excel(writer, sheet_name="作成者別集計", index=False)
    dept_summary.to_excel(writer, sheet_name="部署別集計", index=False)

print("集計完了：", output_file)

