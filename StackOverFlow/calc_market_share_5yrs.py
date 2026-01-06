import pandas as pd
import os

# 1. Cấu hình
input_file = 'Master_Data_5_Years.csv'
output_file = 'Market_Share_5_Years_Calculated.csv'

# 2. Đọc dữ liệu
try:
    df = pd.read_csv(input_file)
    print(f"Đã nạp dữ liệu 5 năm. Tổng số dòng: {len(df)}")
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file {input_file}")
    exit()

# 3. Xử lý tính toán
print("Đang tính toán thị phần...")

# Bước 3.1: Gom nhóm để tính Tổng số lượng câu hỏi của Ngôn ngữ trong từng Ngành theo từng Năm
# (Ví dụ: Năm 2020, Ngành Data Science, Python có 1200 câu)
df_grouped = df.groupby(['Year', 'ChuyenNganh', 'LanguageTag'])['Quantity'].sum().reset_index()

# Bước 3.2: Tính Tổng số lượng của CẢ CHUYÊN NGÀNH trong năm đó
# (Ví dụ: Năm 2020, Ngành Data Science có tổng cộng 2000 câu từ tất cả ngôn ngữ)
domain_totals = df_grouped.groupby(['Year', 'ChuyenNganh'])['Quantity'].sum().reset_index()
domain_totals = domain_totals.rename(columns={'Quantity': 'Total_Domain_Quantity'})

# Bước 3.3: Kết hợp (Merge) hai bảng lại
df_merged = pd.merge(df_grouped, domain_totals, on=['Year', 'ChuyenNganh'])

# Bước 3.4: Tính phần trăm (Market Share)
df_merged['MarketShare_Percent'] = (df_merged['Quantity'] / df_merged['Total_Domain_Quantity']) * 100
df_merged['MarketShare_Percent'] = df_merged['MarketShare_Percent'].round(2) # Làm tròn 2 số thập phân

# 4. Sắp xếp và Làm đẹp dữ liệu
# Sắp xếp theo: Năm (tăng dần) -> Chuyên ngành -> Phần trăm (giảm dần)
df_final = df_merged.sort_values(by=['Year', 'ChuyenNganh', 'MarketShare_Percent'], ascending=[True, True, False])

# Chọn các cột cần thiết để xuất file
output_cols = ['Year', 'ChuyenNganh', 'LanguageTag', 'Quantity', 'Total_Domain_Quantity', 'MarketShare_Percent']
df_final = df_final[output_cols]

# 5. Xuất file CSV
df_final.to_csv(output_file, index=False)

print("-" * 30)
print(f"HOÀN TẤT! Đã xuất file số liệu chi tiết: {output_file}")
print("Ví dụ 5 dòng đầu tiên:")
print(df_final.head().to_string(index=False))