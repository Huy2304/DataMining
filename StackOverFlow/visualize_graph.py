import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# 1. Cấu hình & Tạo thư mục lưu trữ
# Tạo folder riêng để chứa ảnh, tránh lộn xộn
output_folder = 'BaoCao_HinhAnh'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Đã tạo thư mục '{output_folder}'")

# 2. Đọc dữ liệu
input_file = 'Final_Dataset_Labeled.csv'
try:
    df = pd.read_csv(input_file)
    print(f"Đã đọc {len(df)} dòng dữ liệu.")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file Final_Dataset_Labeled.csv")
    exit()

# Cấu hình font chữ cho đẹp (tùy chọn)
plt.rcParams.update({'font.size': 12})

# ==========================================
# BIỂU ĐỒ 1: HEATMAP (BẢN ĐỒ NHIỆT) - File PNG
# ==========================================
print("Đang vẽ Heatmap...")
plt.figure(figsize=(14, 8))
# Tạo bảng pivot: Hàng=Ngôn ngữ, Cột=Chuyên ngành
pivot_data = df.pivot_table(index='LanguageTag', columns='ChuyenNganh', values='Quantity', aggfunc='sum', fill_value=0)

# Vẽ heatmap
sns.heatmap(pivot_data, annot=True, fmt='d', cmap='YlGnBu', linewidths=.5)
plt.title('Phân bố số lượng câu hỏi giữa Ngôn ngữ và Chuyên ngành (2025)', fontsize=16)
plt.ylabel('Ngôn ngữ Lập trình')
plt.xlabel('Chuyên ngành CNTT')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Lưu file
save_path = os.path.join(output_folder, '1_Heatmap_PhanBo.png')
plt.savefig(save_path, dpi=300) # DPI 300 để in ấn nét căng
plt.close()

# ==========================================
# BIỂU ĐỒ 2: STACKED BAR CHART (CỘT CHỒNG) - File PNG
# ==========================================
print("Đang vẽ Stacked Bar Chart...")
# Chuẩn hóa dữ liệu về phần trăm (%) để dễ so sánh cơ cấu
cross_tab_prop = pd.crosstab(index=df['LanguageTag'], columns=df['ChuyenNganh'], values=df['Quantity'], aggfunc='sum', normalize='index')

# Vẽ biểu đồ
ax = cross_tab_prop.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='tab10')
plt.title('Tỷ lệ % Chuyên ngành trong từng Ngôn ngữ', fontsize=16)
plt.ylabel('Tỷ lệ (0.0 - 1.0)')
plt.xlabel('Ngôn ngữ')
plt.legend(title='Chuyên ngành', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()

# Lưu file
save_path = os.path.join(output_folder, '2_CoCau_ChuyenNganh.png')
plt.savefig(save_path, dpi=300)
plt.close()

# ==========================================
# BIỂU ĐỒ 3: TOP 10 CÔNG NGHỆ HOT NHẤT - File PNG
# ==========================================
print("Đang vẽ Top Technologies Chart...")
# Gom nhóm theo TargetTag (bất kể ngôn ngữ nào)
top_tech = df.groupby('TargetTag')['Quantity'].sum().nlargest(15).sort_values()

plt.figure(figsize=(12, 8))
top_tech.plot(kind='barh', color='#e74c3c')
plt.title('Top 15 Công nghệ/Thư viện được hỏi nhiều nhất 2025', fontsize=16)
plt.xlabel('Tổng số lượng câu hỏi')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()

# Lưu file
save_path = os.path.join(output_folder, '3_Top_CongNghe.png')
plt.savefig(save_path, dpi=300)
plt.close()

# ==========================================
# BIỂU ĐỒ 4: SUNBURST (TƯƠNG TÁC) - File HTML
# ==========================================
print("Đang vẽ Sunburst Interactive Chart...")
fig = px.sunburst(
    df, 
    path=['ChuyenNganh', 'LanguageTag', 'TargetTag'], 
    values='Quantity',
    title='Hệ sinh thái Công nghệ CNTT 2025 (Click để tương tác)',
    color='ChuyenNganh',
    height=800
)
# Lưu file HTML
save_path = os.path.join(output_folder, '4_Interactive_Sunburst.html')
fig.write_html(save_path)

print("-" * 30)
print(f"XONG! Đã lưu tất cả 4 biểu đồ vào thư mục: '{output_folder}'")
print("Bạn có thể mở thư mục này để lấy hình báo cáo.")