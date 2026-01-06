import pandas as pd

# 1. Đọc file dữ liệu (Có thể dùng file gốc hoặc file đã clean bước trước đều được)
input_file = 'QueryResults.csv' # Hoặc 'Cleaned_Data_2025.csv'
try:
    df = pd.read_csv(input_file)
    print(f"Tổng số dòng ban đầu: {len(df)}")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file dữ liệu đầu vào.")
    exit()

# Chuyển về chữ thường để xử lý
df['TargetTag'] = df['TargetTag'].str.lower()

# 2. Định nghĩa TỪ ĐIỂN CHUYÊN NGÀNH (Whitelist)
# Chỉ những tag chứa từ khóa trong này mới được giữ lại.
keywords_map = {
    # --- Nhóm 1: Data Science & AI ---
    'Data Science & AI': [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit', 'sklearn', 
        'tensorflow', 'keras', 'pytorch', 'torch', 'dataframe', 'plot', 
        'jupyter', 'conda', 'opencv', 'cv2', 'ocr', 'huggingface', 
        'nlp', 'llm', 'chatgpt', 'openai', 'deep-learning', 'neural'
    ],
    
    # --- Nhóm 2: Web Frontend ---
    'Web Frontend': [
        'react', 'angular', 'vue', 'svelte', 'jquery', 'ajax', 'dom', 
        'css', 'html', 'bootstrap', 'tailwind', 'sass', 'less', 'canvas', 
        'webpack', 'vite', 'next.js', 'nuxt', 'three.js', 'typescript' 
        # (typescript thường là FE, dù có thể làm BE)
    ],
    
    # --- Nhóm 3: Web Backend ---
    'Web Backend': [
        'django', 'flask', 'fastapi', 'spring', 'hibernate', 'jakarta',
        'asp.net', 'entity-framework', 'laravel', 'symfony', 'php', 
        'node.js', 'express', 'nestjs', 'backend', 'rest-api', 'graphql',
        'jwt', 'oauth', 'auth', 'session', 'cookie', 'tomcat', 'jetty'
    ],
    
    # --- Nhóm 4: Mobile App ---
    'Mobile App': [
        'android', 'ios', 'swift', 'kotlin', 'flutter', 'dart', 
        'react-native', 'xcode', 'gradle', 'cocoapods', 'mobile', 
        'uikit', 'swiftui', 'jetpack-compose', 'activity', 'fragment'
    ],
    
    # --- Nhóm 5: Game Development ---
    'Game Development': [
        'unity', 'unreal', 'godot', 'pygame', 'libgdx', 'cocos', 
        'sprite', 'mesh', 'shader', 'opengl', 'directx', 'vulkan', 
        'physics', 'collision', 'rendering', 'animation'
    ],
    
    # --- Nhóm 6: Database (Cơ sở dữ liệu) ---
    'Database': [
        'sql', 'mysql', 'postgresql', 'postgres', 'sqlite', 'mongodb', 
        'redis', 'oracle', 'mariadb', 'cassandra', 'dynamodb', 'firebase',
        'sqlalchemy', 'pymongo', 'db', 'query', 'stored-procedure'
    ],
    
    # --- Nhóm 7: DevOps & Cloud ---
    'DevOps & Cloud': [
        'docker', 'kubernetes', 'k8s', 'aws', 'amazon', 'azure', 'gcp', 
        'google-cloud', 'jenkins', 'gitlab-ci', 'terraform', 'ansible',
        'nginx', 'apache', 'serverless', 'lambda', 'ec2', 's3'
    ]
}

# 3. Hàm gán nhãn logic
def get_label(tag):
    tag = str(tag)
    # Xử lý ưu tiên đặc biệt
    if 'react-native' in tag: return 'Mobile App'
    if 'react' in tag: return 'Web Frontend'
    if 'node' in tag: return 'Web Backend'
    
    # Duyệt qua từ điển
    for label, keywords in keywords_map.items():
        for key in keywords:
            # Nếu từ khóa nằm trong tên tag (ví dụ 'spring' nằm trong 'spring-boot')
            if key in tag:
                return label
    return None # Trả về None nếu không thuộc nhóm nào

# 4. Áp dụng gán nhãn
print("Đang xử lý gán nhãn...")
df['ChuyenNganh'] = df['TargetTag'].apply(get_label)

# 5. LỌC BỎ (Drop) những dòng không gán được nhãn (Giá trị là None/NaN)
df_final = df.dropna(subset=['ChuyenNganh'])

# 6. Thống kê và Xuất file
print("-" * 30)
print("KẾT QUẢ SAU KHI LỌC:")
print(f"Số dòng còn lại: {len(df_final)} (Đã loại bỏ {len(df) - len(df_final)} dòng tạp)")
print("\nPhân bố dữ liệu theo chuyên ngành:")
print(df_final.groupby(['LanguageTag', 'ChuyenNganh']).size().unstack(fill_value=0))

# Lưu file cuối cùng
output_file = 'Final_Dataset_Labeled.csv'
df_final.to_csv(output_file, index=False)
print(f"\nĐã lưu file sạch và có nhãn tại: {output_file}")