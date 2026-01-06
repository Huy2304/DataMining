import pandas as pd

# ---------------------------------------------------------
# PHẦN 1: CẤU HÌNH TỪ ĐIỂN CHUYÊN NGÀNH (Giữ nguyên như cũ)
# ---------------------------------------------------------
keywords_map = {
    'Data Science & AI': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit', 'sklearn', 'tensorflow', 'keras', 'pytorch', 'torch', 'dataframe', 'plot', 'jupyter', 'opencv', 'cv2', 'nlp', 'llm', 'deep-learning', 'neural', 'ai'],
    'Web Frontend': ['react', 'angular', 'vue', 'svelte', 'jquery', 'ajax', 'dom', 'css', 'html', 'bootstrap', 'tailwind', 'typescript', 'webpack', 'vite', 'next.js'],
    'Web Backend': ['django', 'flask', 'fastapi', 'spring', 'hibernate', 'asp.net', 'entity-framework', 'laravel', 'symfony', 'php', 'node', 'express', 'nestjs', 'backend', 'rest-api', 'auth', 'jwt'],
    'Mobile App': ['android', 'ios', 'swift', 'kotlin', 'flutter', 'dart', 'react-native', 'xcode', 'mobile', 'swiftui', 'jetpack'],
    'Game Development': ['unity', 'unreal', 'godot', 'pygame', 'libgdx', 'shader', 'opengl', 'directx', 'physics', 'rendering'],
    'Database': ['sql', 'mysql', 'postgresql', 'postgres', 'sqlite', 'mongodb', 'redis', 'oracle', 'firebase', 'sqlalchemy', 'db', 'query'],
    'DevOps & Cloud': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'terraform', 'nginx', 'serverless']
}

def get_label(tag):
    tag = str(tag).lower()
    if 'react-native' in tag: return 'Mobile App'
    if 'react' in tag: return 'Web Frontend'
    if 'node' in tag: return 'Web Backend'
    for label, keywords in keywords_map.items():
        for key in keywords:
            if key in tag: return label
    return None

# ---------------------------------------------------------
# PHẦN 2: XỬ LÝ FILE 2020-2024
# ---------------------------------------------------------
print("1. Đang xử lý dữ liệu 2020-2024...")
try:
    df_old = pd.read_csv('QueryResults_2020_2024.csv')
    
    # Gán nhãn
    df_old['ChuyenNganh'] = df_old['TargetTag'].apply(get_label)
    
    # Lọc bỏ dòng không có nhãn
    df_old = df_old.dropna(subset=['ChuyenNganh'])
    
    print(f"   - Đã tải {len(df_old)} dòng sạch từ 2020-2024.")
    
except FileNotFoundError:
    print("   LỖI: Thiếu file QueryResults_2020_2024.csv")
    exit()

# ---------------------------------------------------------
# PHẦN 3: XỬ LÝ FILE 2025 (File bạn đã làm sạch trước đó)
# ---------------------------------------------------------
print("2. Đang xử lý dữ liệu 2025...")
try:
    # Đọc file kết quả clean của năm 2025
    df_2025 = pd.read_csv('Final_Dataset_Labeled.csv')
    
    # File 2025 chưa có cột Year, ta phải thêm vào thủ công
    df_2025['Year'] = 2025
    
    # Đảm bảo thứ tự cột giống nhau để gộp không bị lỗi
    # Cấu trúc chuẩn: Year, LanguageTag, TargetTag, Quantity, ChuyenNganh
    df_2025 = df_2025[['Year', 'LanguageTag', 'TargetTag', 'Quantity', 'ChuyenNganh']]
    
    print(f"   - Đã tải {len(df_2025)} dòng sạch từ 2025.")
    
except FileNotFoundError:
    print("   LỖI: Thiếu file Final_Dataset_Labeled.csv. Hãy chạy lại bước trước.")
    exit()

# ---------------------------------------------------------
# PHẦN 4: GỘP VÀ XUẤT FILE MASTER
# ---------------------------------------------------------
print("3. Đang gộp dữ liệu...")

# Gộp 2 DataFrame lại
df_master = pd.concat([df_old, df_2025], ignore_index=True)

# Sắp xếp lại cho đẹp: Theo Năm -> Ngôn ngữ -> Số lượng giảm dần
df_master = df_master.sort_values(by=['Year', 'LanguageTag', 'Quantity'], ascending=[True, True, False])

# Lưu file tổng
output_file = 'Master_Data_5_Years.csv'
df_master.to_csv(output_file, index=False)

print("-" * 30)
print(f"HOÀN TẤT! Tổng số dòng dữ liệu 5 năm: {len(df_master)}")
print(f"File đã lưu tại: {output_file}")
print("Dữ liệu này đã sẵn sàng để vẽ biểu đồ xu hướng (Trend Line).")