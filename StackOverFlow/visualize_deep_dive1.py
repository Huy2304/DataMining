import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# 1. Cấu hình
input_file = 'Final_Dataset_Labeled.csv' # Dữ liệu năm 2025
output_folder = 'BaoCao_ThiPhan_2025'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 2. Đọc dữ liệu
try:
    df = pd.read_csv(input_file)
    print(f"Đã nạp dữ liệu. Tổng dòng: {len(df)}")
except FileNotFoundError:
    print("Không tìm thấy file Final_Dataset_Labeled.csv")
    exit()

# 3. Xử lý dữ liệu: Tính tổng và Phần trăm
# Gom nhóm: Chuyên ngành -> Ngôn ngữ -> Tổng Quantity
df_grouped = df.groupby(['ChuyenNganh', 'LanguageTag'])['Quantity'].sum().reset_index()

# Tính tổng Quantity của cả chuyên ngành để chia phần trăm
df_total = df_grouped.groupby('ChuyenNganh')['Quantity'].sum().reset_index()
df_total = df_total.rename(columns={'Quantity': 'TotalQuantity'})

# Merge lại để có cột Total
df_merged = pd.merge(df_grouped, df_total, on='ChuyenNganh')

# Tính %
df_merged['Percentage'] = (df_merged['Quantity'] / df_merged['TotalQuantity']) * 100
df_merged['Percentage'] = df_merged['Percentage'].round(1) # Làm tròn 1 số thập phân

# Sắp xếp để vẽ biểu đồ đẹp hơn (Ngôn ngữ nào chiếm nhiều % nhất nằm dưới cùng)
df_merged = df_merged.sort_values(by=['ChuyenNganh', 'Percentage'], ascending=[True, False])

print("Đã tính toán xong tỷ lệ phần trăm.")

# ==============================================================================
# BIỂU ĐỒ 1: TỔNG QUAN THỊ PHẦN (100% STACKED BAR CHART)
# ==============================================================================
print("1. Đang vẽ biểu đồ cột chồng 100%...")

fig1 = px.bar(df_merged, 
              x="Percentage", 
              y="ChuyenNganh", 
              color="LanguageTag", 
              orientation='h', # Vẽ nằm ngang cho dễ đọc tên ngành
              text="Percentage", # Hiển thị số % lên cột
              title="Thị phần các Ngôn ngữ trong từng Chuyên ngành (Năm 2025)",
              labels={'Percentage': 'Thị phần (%)', 'ChuyenNganh': 'Chuyên ngành'},
              height=600)

fig1.update_traces(texttemplate='%{text}%', textposition='inside')
fig1.update_layout(barmode='stack', xaxis=dict(range=[0, 100])) # Cố định trục X là 100%

fig1.write_html(os.path.join(output_folder, '1_Market_Share_Overview.html'))


# ==============================================================================
# BIỂU ĐỒ 2: CHI TIẾT TỪNG CHUYÊN NGÀNH (DONUT CHARTS)
# ==============================================================================
print("2. Đang vẽ biểu đồ tròn chi tiết cho từng ngành...")

categories = df_merged['ChuyenNganh'].unique()
# Tính số hàng cần thiết cho lưới biểu đồ (Mỗi hàng 3 biểu đồ)
rows = (len(categories) // 3) + (1 if len(categories) % 3 > 0 else 0)

# Tạo khung subplot
fig2 = make_subplots(
    rows=rows, cols=3, 
    subplot_titles=categories,
    specs=[[{'type':'domain'}]*3]*rows # Khai báo kiểu biểu đồ là 'domain' (cho Pie chart)
)

row_idx = 1
col_idx = 1

for cat in categories:
    # Lấy dữ liệu của ngành đó
    data_cat = df_merged[df_merged['ChuyenNganh'] == cat]
    
    fig2.add_trace(
        go.Pie(
            labels=data_cat['LanguageTag'], 
            values=data_cat['Percentage'],
            name=cat,
            hole=.4, # Tạo lỗ ở giữa (Donut chart)
            textinfo='label+percent', # Hiển thị Tên + %
            textposition='inside'
        ),
        row=row_idx, col=col_idx
    )
    
    # Logic chuyển ô
    col_idx += 1
    if col_idx > 3:
        col_idx = 1
        row_idx += 1

fig2.update_layout(
    title_text="Chi tiết tỷ lệ cạnh tranh trong các Chuyên ngành CNTT",
    height=300 * rows, # Chiều cao tự động theo số hàng
    showlegend=True
)

fig2.write_html(os.path.join(output_folder, '2_Detailed_Donut_Charts.html'))

print("-" * 30)
print(f"HOÀN TẤT! Đã lưu 2 biểu đồ vào thư mục '{output_folder}'.")