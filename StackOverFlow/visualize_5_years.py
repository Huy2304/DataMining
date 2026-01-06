import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 1. Cấu hình
input_file = 'Master_Data_5_Years.csv'
output_folder = 'BaoCao_5Nam'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

try:
    df = pd.read_csv(input_file)
    print(f"Đã nạp dữ liệu 5 năm. Tổng số dòng: {len(df)}")
except FileNotFoundError:
    print("Thiếu file Master_Data_5_Years.csv")
    exit()

# ==========================================================
# BIỂU ĐỒ 1: KIỂM TRA ĐỘ CÂN BẰNG (HEATMAP DATA COVERAGE)
# ==========================================================
# Mục tiêu: Chứng minh rằng mọi ngôn ngữ đều có dữ liệu đầy đủ qua các năm
print("1. Vẽ Heatmap kiểm tra độ phủ dữ liệu...")

# Đếm số lượng targetTag thu thập được cho mỗi cặp (Năm, Ngôn ngữ)
coverage_data = df.pivot_table(index='LanguageTag', columns='Year', values='TargetTag', aggfunc='count', fill_value=0)

plt.figure(figsize=(10, 6))
sns.heatmap(coverage_data, annot=True, fmt='d', cmap='Greens', linewidths=.5)
plt.title('Độ Cân Bằng Dữ Liệu: Số lượng thẻ thu thập được (Mục tiêu: ~100)', fontsize=14)
plt.ylabel('Ngôn ngữ')
plt.xlabel('Năm')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, '1_Check_Balance_Heatmap.png'), dpi=300)
plt.close()

# ==========================================================
# BIỂU ĐỒ 2: KIỂM TRA PHÂN PHỐI & ĐỘ TIN CẬY (BOX PLOT)
# ==========================================================
# Mục tiêu: Xem phân phối điểm số (Quantity) có ổn định qua các năm không?
# Nếu một năm có cái hộp quá thấp hoặc quá cao bất thường -> Dữ liệu năm đó bị nhiễu.
print("2. Vẽ Box Plot kiểm tra phân phối...")

plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Year', y='Quantity', showfliers=False) # showfliers=False để ẩn bớt các điểm ngoại lai quá xa
plt.title('Phân phối số lượng câu hỏi qua 5 năm (Kiểm tra độ ổn định)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig(os.path.join(output_folder, '2_Check_Reliability_BoxPlot.png'), dpi=300)
plt.close()

# ==========================================================
# BIỂU ĐỒ 3: XU HƯỚNG CHUYÊN NGÀNH (LINE CHART - INTERACTIVE)
# ==========================================================
# Mục tiêu: Chứng minh dữ liệu "Make Sense" (Hợp lý).
# Ví dụ: Data Science phải tăng, Web Backend có thể đi ngang.
print("3. Vẽ biểu đồ xu hướng chuyên ngành...")

# Tính tổng lượng câu hỏi cho từng chuyên ngành theo từng năm
trend_data = df.groupby(['Year', 'ChuyenNganh'])['Quantity'].sum().reset_index()

fig = px.line(trend_data, 
              x="Year", 
              y="Quantity", 
              color="ChuyenNganh", 
              markers=True,
              title="Xu hướng phát triển các chuyên ngành CNTT (2020 - 2025)",
              labels={'Quantity': 'Tổng mức độ quan tâm (Quantity)', 'Year': 'Năm'})

fig.update_xaxes(dtick=1) # Hiển thị đủ các năm 2020, 21, 22...
fig.write_html(os.path.join(output_folder, '3_Trend_Line_Chart.html'))

# ==========================================================
# BIỂU ĐỒ 4: CUỘC ĐUA CÔNG NGHỆ (RACING BAR - STATIC VIEW)
# ==========================================================
# Mục tiêu: So sánh sự thay đổi của các "Ông lớn" cụ thể (React vs Pandas vs Spring)
print("4. Vẽ biểu đồ so sánh công nghệ cụ thể...")

# Lọc ra 3 đại diện tiêu biểu: React (Web), Pandas (Data), Unity (Game)
top_techs = ['reactjs', 'pandas', 'unity', 'flutter', 'spring'] 
# Lưu ý: Cần đảm bảo tên tag trong list khớp với dữ liệu (thường là chữ thường)
# Trong bước trước ta đã clean tag thành chữ thường chưa? Nếu chưa thì cẩn thận.
# Ở code gộp trước, ta dùng `get_label` có .lower(), nhưng cột TargetTag gốc có thể chưa.
# Tốt nhất ta chuẩn hóa lại ở đây cho chắc:
df['TargetTag'] = df['TargetTag'].str.lower()

tech_trend = df[df['TargetTag'].isin(top_techs)].groupby(['Year', 'TargetTag'])['Quantity'].sum().reset_index()

fig2 = px.line(tech_trend, x="Year", y="Quantity", color="TargetTag", markers=True,
               title="Cuộc đua của các Framework hàng đầu (2020-2025)")
fig2.write_html(os.path.join(output_folder, '4_Tech_Race_Chart.html'))

print("-" * 30)
print(f"XONG! Đã tạo 4 biểu đồ trong thư mục '{output_folder}'")