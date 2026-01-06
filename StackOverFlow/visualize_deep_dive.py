import pandas as pd
import plotly.express as px
import os

# 1. Cấu hình
input_file = 'Master_Data_5_Years.csv'
output_folder = 'BaoCao_ChiTiet_NgonNgu'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

try:
    df = pd.read_csv(input_file)
    print(f"Đã nạp {len(df)} dòng dữ liệu.")
except FileNotFoundError:
    print("Thiếu file Master_Data_5_Years.csv")
    exit()

# ==============================================================================
# BIỂU ĐỒ 1: SỰ TIẾN HÓA CỦA TỪNG NGÔN NGỮ (Normalized Area Chart)
# ==============================================================================
# Mục đích: Xem "Cơ cấu" thay đổi thế nào (Bất chấp việc tổng số lượng giảm)
# Trả lời: "Python năm 2020 làm Web bao nhiêu %, năm 2025 làm AI bao nhiêu %?"
print("1. Đang vẽ biểu đồ cơ cấu (Area Chart)...")

# Gom nhóm dữ liệu
df_area = df.groupby(['Year', 'LanguageTag', 'ChuyenNganh'])['Quantity'].sum().reset_index()

fig1 = px.area(df_area, 
              x="Year", 
              y="Quantity", 
              color="ChuyenNganh", 
              facet_col="LanguageTag", # Tách mỗi ngôn ngữ thành 1 biểu đồ con
              facet_col_wrap=3,        # Mỗi hàng 3 biểu đồ
              groupnorm='percent',     # QUAN TRỌNG: Chuyển đổi sang % (Full 100%)
              title="Sự chuyển dịch cơ cấu chuyên ngành trong từng Ngôn ngữ (2020-2025)",
              labels={'Quantity': 'Tỷ lệ phần trăm (%)', 'Year': 'Năm'})

# Tùy chỉnh trục X để chỉ hiện số năm nguyên
fig1.update_xaxes(dtick=1) 
fig1.write_html(os.path.join(output_folder, '1_Evolution_Per_Language.html'))


# ==============================================================================
# BIỂU ĐỒ 2: TOP 3 CÔNG NGHỆ "CON CƯNG" CỦA TỪNG NGÔN NGỮ (Line Chart)
# ==============================================================================
# Mục đích: Xem cụ thể Framework nào đang "gánh team" cho ngôn ngữ đó.
# Ví dụ: Với JS, xem cuộc đua giữa React, Vue và Angular.
print("2. Đang vẽ biểu đồ Top Tech (Line Chart)...")

# Logic: Tìm Top 3 tag phổ biến nhất của TỪNG ngôn ngữ (tính tổng 5 năm)
top_tags_per_lang = []
for lang in df['LanguageTag'].unique():
    # Lấy data của ngôn ngữ đó
    lang_df = df[df['LanguageTag'] == lang]
    # Tính tổng quantity từng tag
    top_3 = lang_df.groupby('TargetTag')['Quantity'].sum().nlargest(3).index.tolist()
    # Chỉ giữ lại dòng data thuộc top 3 này
    filtered = lang_df[lang_df['TargetTag'].isin(top_3)]
    top_tags_per_lang.append(filtered)

# Gộp lại thành 1 bảng data mới
df_top_tech = pd.concat(top_tags_per_lang)

fig2 = px.line(df_top_tech, 
               x="Year", 
               y="Quantity", 
               color="TargetTag", 
               facet_col="LanguageTag", 
               facet_col_wrap=3,
               markers=True,
               title="Top 3 Công nghệ phổ biến nhất của từng Ngôn ngữ (2020-2025)",
               height=1000) # Tăng chiều cao vì biểu đồ này dài

fig2.update_yaxes(matches=None) # Cho phép trục Y mỗi biểu đồ tự do (vì Python to gấp 10 lần Rust)
fig2.write_html(os.path.join(output_folder, '2_Top_Tech_Trends.html'))


# ==============================================================================
# BIỂU ĐỒ 3: BIỂU ĐỒ XẾP HẠNG (BUMP CHART)
# ==============================================================================
# Mục đích: Xem thứ hạng các ngôn ngữ thay đổi ra sao qua 5 năm.
# Ai leo hạng? Ai tụt hạng?
print("3. Đang vẽ biểu đồ xếp hạng (Bump Chart)...")

# Tính tổng Quantity của mỗi ngôn ngữ theo từng năm
lang_rank = df.groupby(['Year', 'LanguageTag'])['Quantity'].sum().reset_index()
# Tạo cột Rank (Hạng 1, 2, 3...)
lang_rank['Rank'] = lang_rank.groupby('Year')['Quantity'].rank(ascending=False)

fig3 = px.line(lang_rank, 
               x="Year", 
               y="Rank", 
               color="LanguageTag", 
               markers=True,
               title="Bảng Xếp Hạng Độ Phổ Biến Các Ngôn Ngữ (2020-2025)",
               labels={'Rank': 'Thứ hạng (Càng nhỏ càng cao)'})

# Đảo ngược trục Y (vì Hạng 1 phải nằm trên cao nhất)
fig3.update_yaxes(autorange="reversed") 
fig3.update_xaxes(dtick=1)
fig3.write_html(os.path.join(output_folder, '3_Language_Ranking.html'))

print("-" * 30)
print(f"XONG! Hãy vào thư mục '{output_folder}' để xem 3 file HTML.")