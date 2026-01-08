import re

# --- Constants / Keyword Lists ---

MOBILE_KEYWORDS = [
    "ios",
    "android",
    "mobile",
    "flutter",
    "react native",
    "kotlin",
    "swift",
]

AI_DATA_SCIENCE_KEYWORDS = [
    "data scientist",
    "machine learning",
    " ai ",
    "artificial intelligence",
    "nlp",
    "computer vision",
    "llm",
    "deep learning",
    "data sci",
]

DATA_ENGINEER_KEYWORDS = [
    "data engineer",
    "etl",
    "big data",
    "hadoop",
    "spark",
    "data eng",
]

DATA_ANALYST_KEYWORDS = [
    "data analyst",
    "business intelligence",
    " bi ",
    "visualization",
    "data analy",
    "operation analyst",
]

QA_TESTER_KEYWORDS = [
    "tester",
    "qa",
    "qc",
    "quality assurance",
    "kiểm thử",
    "automation test",
]

DEVOPS_CLOUD_KEYWORDS = [
    "devops",
    "sre",
    "cloud",
    "aws",
    "azure",
    "gcp",
    "kubernetes",
    "docker",
    "system engineer",
]

BUSINESS_ANALYST_KEYWORDS = [
    "business analyst",
    " ba ",
    "product owner",
    "product manager",
]

GAME_KEYWORDS = ["game", "unity", "unreal", "cocos"]

EMBEDDED_IOT_KEYWORDS = [
    "embedded",
    "iot",
    "firmware",
    "nhúng",
    "plc",
    "scada",
    "vi mạch",
]

SYSADMIN_NETWORK_SECURITY_KEYWORDS = [
    "system admin",
    "network",
    "mạng",
    "security",
    "bảo mật",
    "helpdesk",
    "support",
    "it support",
    "phần cứng",
    "cyber",
    "hỗ trợ",
    "technician",
    "kỹ thuật viên",
    "triển khai",
]

MANAGEMENT_KEYWORDS = [
    "tech lead",
    "technical lead",
    "cto",
    "chief technology",
    "trưởng phòng",
    "manager",
    "quản lý",
    "director",
    "team lead",
    "head of",
]

BRIDGE_SE_KEYWORDS = [
    "brse",
    "bridge",
    "kỹ sư cầu nối",
]

FULLSTACK_KEYWORDS = ["fullstack", "full stack"]

FRONTEND_KEYWORDS = [
    "frontend",
    "front-end",
    "front end",
    "react",
    "vue",
    "angular",
    "js",
    "javascript",
    "html",
    "css",
    "web",
]

BACKEND_KEYWORDS = [
    "backend",
    "back-end",
    "back end",
    "java",
    "node",
    "python",
    "php",
    ".net",
    "c#",
    "golang",
    "ruby",
    "laravel",
    "spring",
]

# --- Keyword Dictionaries (Moved from etl_linkedin_script.py) ---
PROGRAMMING_LANGUAGES_MAP = {
    "Python": ["python"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "TypeScript": ["typescript", "ts"],
    "Java": ["java"],
    "C#": ["c#", "csharp", ".net core"],
    "C++": ["c++", "cpp"],
    "C": ["c"],
    "Go": ["go", "golang"],
    "Rust": ["rust"],
    "PHP": ["php"],
    "Ruby": ["ruby"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin"],
    "Scala": ["scala"],
    "R": ["r"],
    "Dart": ["dart"],
    "Lua": ["lua"],
    "Perl": ["perl"],
    "Shell": ["shell", "bash", "zsh", "sh"],
    "SQL": ["sql", "mysql", "postgresql", "pl/sql"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "sass", "less", "tailwind"],
    "Assembly": ["assembly", "asm"],
    "MATLAB": ["matlab"],
    "VBA": ["vba"],
    "Objective-C": ["objective-c", "obj-c"],
    "PowerShell": ["powershell"],
}


TECHNOLOGIES_MAP = {
    "React": ["react", "reactjs", "react.js"],
    "Angular": ["angular", "angularjs"],
    "Vue.js": ["vue", "vuejs", "vue.js"],
    "Next.js": ["next.js", "nextjs"],
    "Nuxt.js": ["nuxt", "nuxt.js", "nuxtjs"],
    "Node.js": ["node.js", "nodejs"],
    "Express": ["express", "expressjs"],
    "NestJS": ["nest.js", "nestjs"],
    "Spring": ["spring", "spring boot", "springboot"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Laravel": ["laravel"],
    "Symfony": ["symfony"],
    "CodeIgniter": ["codeigniter"],
    ".NET": [".net", "asp.net", "entity framework", "linq"],
    "Hibernate": ["hibernate"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services", "ec2", "lambda", "s3"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Keras": ["keras"],
    "OpenCV": ["opencv"],
    "Spark": ["spark", "pyspark"],
    "Hadoop": ["hadoop"],
    "Kafka": ["kafka"],
    "RabbitMQ": ["rabbitmq"],
    "Redis": ["redis"],
    "MongoDB": ["mongodb", "mongo"],
    "PostgreSQL": ["postgresql", "postgres", "pgsql"],
    "MySQL": ["mysql"],
    "Oracle": ["oracle", "plsql"],
    "SQL Server": ["sql server", "mssql", "t-sql"],
    "SQLite": ["sqlite"],
    "Elasticsearch": ["elasticsearch", "elk", "kibana"],
    "Git": ["git", "github", "gitlab"],
    "Jenkins": ["jenkins"],
    "GitLab CI": ["gitlab ci", "gitlab-ci"],
    "GitHub Actions": ["github actions"],
    "CircleCI": ["circleci"],
    "Travis CI": ["travis", "travis ci"],
    "Terraform": ["terraform"],
    "Ansible": ["ansible"],
    "Puppet": ["puppet"],
    "Chef": ["chef"],
    "GraphQL": ["graphql"],
    "REST API": ["rest api", "restful", "rest"],
    "gRPC": ["grpc"],
    "WebSocket": ["websocket", "websockets"],
    "Flutter": ["flutter"],
    "React Native": ["react native"],
    "Ionic": ["ionic"],
    "Xamarin": ["xamarin"],
    "Linux": ["linux", "ubuntu", "centos", "redhat", "debian"],
    "Unix": ["unix"],
    "Windows Server": ["windows server"],
    "Nginx": ["nginx"],
    "Apache": ["apache", "httpd"],
}


# --- Helper to convert MAP to RegEx dict for backward compatibility ---
def _map_to_regex(keyword_map):
    regex_dict = {}
    for key, variations in keyword_map.items():
        # Escape special chars and join with OR (|)
        # Add word boundaries (\b) to avoid partial matches like 'script' matching 'javascript'
        pattern = r"\b(" + "|".join([re.escape(v) for v in variations]) + r")\b"
        regex_dict[key] = pattern
    return regex_dict


LANGUAGES = _map_to_regex(PROGRAMMING_LANGUAGES_MAP)
TECHNOLOGIES = _map_to_regex(TECHNOLOGIES_MAP)

# Noise Map for specific legacy subfields or industries
NOISE_MAP = {
    "Thương mại điện tử": "E-commerce/Retail Tech",
    "Tài chính": "Fintech/Banking",
    "Ngân hàng": "Fintech/Banking",
    "Sản xuất": "Manufacturing Tech",
    "Y tế / Dược phẩm": "HealthTech",
    "Bán lẻ - Hàng tiêu dùng - FMCG": "E-commerce/Retail Tech",
    "Giáo dục / Đào tạo": "EdTech / Training",
    "Viễn thông": "Telecom",
    "Nghỉ thứ 7": "Software Engineer (General)",
    "Tiếng Anh Giao tiếp cơ bản": "Software Engineer (General)",
    "Technical Leader": "Management / Lead",
    "IT Project Manager": "Management / Lead",
    "Kỹ sư lập trình PLC/SCADA": "Embedded/IoT Engineer",
    "Shipper (Nhân viên giao hàng)": "Non-IT / Other",
    "Kế toán": "Non-IT / Other",
    "Bán hàng tại cửa hàng/showroom": "Non-IT / Other",
    "Marketing / Quảng cáo": "Digital Marketing / SEO",
    "Digital Marketing": "Digital Marketing / SEO",
    "Chứng khoán": "Fintech/Banking",
    "Bảo hiểm": "Fintech/Banking",
    "Bất động sản": "PropTech",
    "Năng lượng / Môi trường": "Energy/Environment Tech",
    "Du lịch": "TravelTech",
    "Hành chính / Văn phòng": "Non-IT / Other",
}


def get_normalized_subfield(job_title, current_subfield=None):
    """
    Normalizes job subfield based on Job Title and optional current Subfield.
    """
    title = str(job_title).lower() if job_title else ""
    subfield = str(current_subfield) if current_subfield else ""

    # Step 1: Clean prefix
    if subfield.startswith("Chuyên môn "):
        subfield = subfield.replace("Chuyên môn ", "")
    if subfield.startswith("Vị trí "):
        subfield = subfield.replace("Vị trí ", "")

    # Step 1.5: Pre-processing for common ambiguities
    title_lower = title.lower()

    # Ambiguity 1: "Fresher" often needs title context
    if "fresher" in title_lower or "intern" in title_lower or "thực tập" in title_lower:
        # Don't return "Fresher" as subfield, keep digging for tech keywords
        # But if we fail to find anything else, we might want to tag as "Junior/Entry Level" later
        # For now, let it fall through to keyword matching
        pass

    # Step 2: Priority Matching

    # Mobile
    if subfield in ["iOS Developer", "Mobile_App", "Android Developer"] or any(
        k in title_lower for k in MOBILE_KEYWORDS
    ):
        return "Mobile Developer"

    # AI / Data Science
    if subfield in [
        "AI_Data_Science",
        "Data Scientist",
        "ML Engineer",
        "Computer Vision",
        "NLP",
    ] or any(k in title_lower for k in AI_DATA_SCIENCE_KEYWORDS):
        return "AI/Data Science"

    # Data Engineer
    if subfield in ["Data Engineer", "Big Data"] or any(
        k in title_lower for k in DATA_ENGINEER_KEYWORDS
    ):
        return "Data Engineer"

    # Data Analyst
    if subfield in ["Data Analyst", "Phân tích dữ liệu"] or any(
        k in title_lower for k in DATA_ANALYST_KEYWORDS
    ):
        return "Data Analyst"

    # QA / Tester
    if subfield in [
        "QA Engineer",
        "Software Tester (Automation & Manual)",
        "Manual Tester",
        "Automation Tester",
        "Game Tester",
    ] or any(k in title_lower for k in QA_TESTER_KEYWORDS):
        return "QA/QC Engineer"

    # DevOps / Cloud
    if subfield in [
        "DevOps_Cloud",
        "DevOps Engineer",
        "Cloud Engineer",
        "Điện toán đám mây (Cloud)",
    ] or any(k in title_lower for k in DEVOPS_CLOUD_KEYWORDS):
        return "DevOps/Cloud Engineer"

    # Business Analyst
    if subfield in [
        "Business Analyst (Phân tích nghiệp vụ)",
        "Product Owner/Product Manager",
    ] or any(k in title_lower for k in BUSINESS_ANALYST_KEYWORDS):
        return "Business Analyst"

    # Game
    if subfield in ["Game", "Game Developer"] or any(
        k in title_lower for k in GAME_KEYWORDS
    ):
        return "Game Developer"

    # Embedded / IoT
    if subfield in [
        "Embedded_IoT",
        "Embedded Engineer/Lập trình nhúng",
        "Kỹ sư IoT (IoT Engineer)",
        "Cơ khí / Tự động hóa",
    ] or any(k in title_lower for k in EMBEDDED_IOT_KEYWORDS):
        return "Embedded/IoT Engineer"

    # SysAdmin / Network / Security
    if subfield in [
        "System Administrator",
        "Network Engineer",
        "An ninh mạng",
        "IT Helpdesk/IT support",
        "IT - Phần cứng và máy tính",
        "Chuyên viên IT Security",
    ] or any(k in title_lower for k in SYSADMIN_NETWORK_SECURITY_KEYWORDS):
        return "SysAdmin/Network/Security"

    # Web Development (Fullstack, Frontend, Backend)
    is_generic = subfield in [
        "IT - Phần mềm",
        "Web_Development",
        "General IT",
        "Software Engineer",
        "Chuyên môn Công nghệ thông tin khác",
        "Other",
        "Khác",
    ]
    is_specific_web = subfield in [
        "Backend Developer",
        "Frontend Developer",
        "Fullstack Developer",
    ]

    # Force check title if subfield is generic OR if we are in a web category (to refine it)
    if is_generic or is_specific_web or not current_subfield:
        if any(k in title_lower for k in FULLSTACK_KEYWORDS):
            return "Fullstack Developer"
        if any(k in title_lower for k in FRONTEND_KEYWORDS):
            return "Frontend Developer"
        if any(k in title_lower for k in BACKEND_KEYWORDS):
            return "Backend Developer"

        # New: Catch specific languages that imply backend if not specified
        if any(
            k in title_lower
            for k in [
                ".net",
                "java",
                "php",
                "golang",
                "python",
                "ruby",
                "node",
                "c#",
                "c++",
            ]
        ):
            return "Backend Developer"

        if is_specific_web:
            return subfield

    if subfield in ["IT - Phần mềm", "General IT", "Software Engineer"] or (
        not current_subfield and not is_specific_web
    ):
        return "Software Engineer (General)"

    # Noise Map
    if subfield in NOISE_MAP:
        return NOISE_MAP[subfield]

    # Additional Noise Cleaning (Years of Experience, Salary, etc.)
    # Catch strings like "3 năm kinh nghiệm", "Trên 2 năm", "Up to 2000$", "Thỏa thuận"
    subfield_lower = subfield.lower()

    # Check for experience keywords
    experience_keywords = ["năm", "year", "kinh nghiệm", "experience", "exp"]
    if any(k in subfield_lower for k in experience_keywords) and (
        any(char.isdigit() for char in subfield) or "level" not in subfield_lower
    ):
        return "Other"  # Or "General IT" if preferred, but usually exp isn't a subfield

    # Check for salary keywords
    salary_keywords = [
        "$",
        "usd",
        "vnd",
        "lương",
        "salary",
        "triệu",
        "thỏa thuận",
        "negotiable",
    ]
    if any(k in subfield_lower for k in salary_keywords):
        return "Other"

    # Check for generic noise often found in TopCV tags
    generic_noise = ["tất cả", "all", "khác", "other"]
    if subfield_lower in generic_noise:
        return "Other"

    # Sales / Consultant
    if any(k in subfield for k in ["Sales", "Consultant", "Kinh doanh", "Tư vấn"]):
        return "IT Sales / Consultant"

    # --- New Matches for Logic Gap ---

    # Management
    if any(k in title_lower for k in MANAGEMENT_KEYWORDS):
        return "Management / Lead"

    # Solutions Architect
    if "solutions architect" in title_lower or "solution architect" in title_lower:
        return "Solutions Architect"

    # Bridge SE (Improved)
    if any(k in title_lower for k in ["brse", "bridge", "cầu nối"]):
        return "Bridge SE"

    # Business Analyst (Catching Vietnamese variations better)
    if any(
        k in title_lower
        for k in ["phân tích nghiệp vụ", "business analyst", " ba ", "ba/"]
    ):
        return "Business Analyst"

    # IT Support / Admin (Generic IT staff)
    if any(
        k in title_lower
        for k in [
            "nhân viên it",
            "chuyên viên it",
            "it admin",
            "it support",
            "helpdesk",
            "kỹ thuật viên",
        ]
    ):
        return "SysAdmin/Network/Security"

    # Default return existing subfield if valid, or Other
    return subfield if subfield else "Other"
