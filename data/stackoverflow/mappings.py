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
    "objective-c",
    "xamarin",
    "ionic",
    "maui",
    "mobile app",
    " lập trình di động",
    "app developer",
]

AI_DATA_SCIENCE_KEYWORDS = [
    "data scientist",
    "machine learning",
    " ai ", # Spaced to avoid partial matches
    "artificial intelligence",
    "trí tuệ nhân tạo",
    "nlp",
    "natural language processing",
    "computer vision",
    "thị giác máy tính",
    "llm",
    "large language model",
    "generative ai",
    "genai",
    "deep learning",
    "data sci",
    "mlops",
    "ml engineer",
    "gpt",
]

DATA_ENGINEER_KEYWORDS = [
    "data engineer",
    "kỹ sư dữ liệu",
    "etl",
    "elt",
    "big data",
    "hadoop",
    "spark",
    "data eng",
    "data warehouse",
    "kho dữ liệu",
    "data pipeline",
    "airflow",
    "databricks",
    "snowflake",
]

DATA_ANALYST_KEYWORDS = [
    "data analyst",
    "chuyên viên phân tích dữ liệu",
    "business intelligence",
    " bi ",
    "visualization",
    "data analy",
    "operation analyst",
    "tableau",
    "power bi",
    "looker",
    "analyst",
    "phân tích số liệu",
]

QA_TESTER_KEYWORDS = [
    "tester",
    "qa",
    "qc",
    "quality assurance",
    "quality control",
    "kiểm thử",
    "test engineer",
    "automation test",
    "manual test",
    "selenium",
    "cypress",
    "kỹ sư kiểm định",
]

DEVOPS_CLOUD_KEYWORDS = [
    "devops",
    "sre",
    "site reliability engineering",
    "cloud",
    "điện toán đám mây",
    "aws",
    "azure",
    "gcp",
    "kubernetes",
    "k8s",
    "docker",
    "system engineer",
    "kỹ sư hệ thống",
    "ci/cd",
    "infrastructure",
    "hạ tầng",
    "terraform",
    "ansible",
]

BUSINESS_ANALYST_KEYWORDS = [
    "business analyst",
    "chuyên viên phân tích nghiệp vụ",
    " ba ",
    "product owner",
    "product manager",
    "quản lý sản phẩm",
    "nghiệp vụ",
    "requirements",
    "quy trình",
    "scrum master",
    "agile",
]

GAME_KEYWORDS = [
    "game",
    "unity",
    "unreal",
    "cocos",
    "godot",
    "lập trình game",
    "gameplay",
    "shader",
    "directx",
    "opengl",
]

EMBEDDED_IOT_KEYWORDS = [
    "embedded",
    "iot",
    "internet of things",
    "firmware",
    "nhúng",
    "lập trình nhúng",
    "plc",
    "scada",
    "vi mạch",
    "microcontroller",
    "vi điều khiển",
    "rtos",
    "stm32",
    "arduino",
    "driver development",
]

SYSADMIN_NETWORK_SECURITY_KEYWORDS = [
    "system admin",
    "sysadmin",
    "quản trị hệ thống",
    "network",
    "mạng",
    "kỹ sư mạng",
    "security",
    "bảo mật",
    "an ninh mạng",
    "helpdesk",
    "support",
    "it support",
    "phần cứng",
    "cyber",
    "soc",
    "pentest",
    "hỗ trợ",
    "technician",
    "kỹ thuật viên",
    "triển khai",
    "lắp đặt",
    "vận hành",
    "it operations",
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
    "trưởng nhóm",
    "head of",
    "leader",
    "giám đốc",
    "vp of engineering",
]

BRIDGE_SE_KEYWORDS = [
    "brse",
    "bridge",
    "kỹ sư cầu nối",
    "comtor",
    "phiên dịch",
    "translator",
]

FULLSTACK_KEYWORDS = [
    "fullstack",
    "full stack",
    "full-stack",
    "lập trình viên toàn năng",
]

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
    "giao diện",
    "ui/ux",
    "figma", 
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
    "server",
    "hệ thống",
    "api",
    "microservices",
    "database",
]

BLOCKCHAIN_KEYWORDS = [
    "blockchain",
    "smart contract",
    "solidity",
    "web3",
    "crypto",
    "defi",
    "nft",
    "ethereum",
]

ERP_CRM_KEYWORDS = [
    "erp",
    "crm",
    "salesforce",
    "sap",
    "odoo",
    "magento",
    "sharepoint",
    "dynamics 365",
    "abap",
]

# --- Keyword Dictionaries (Moved from etl_linkedin_script.py) ---
PROGRAMMING_LANGUAGES_MAP = {
    "Python": ["python", "py"],
    "JavaScript": ["javascript", "js", "ecmascript", "es6", "es5"],
    "TypeScript": ["typescript", "ts"],
    "Java": ["java", "jdk", "jre"],
    "C#": ["c#", "csharp", ".net core", "dotnet"],
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
    "Shell": ["shell", "bash", "zsh", "sh", "linux shell"],
    "SQL": ["sql", "mysql", "postgresql", "pl/sql", "t-sql"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "sass", "less", "tailwind", "scss"],
    "Assembly": ["assembly", "asm"],
    "MATLAB": ["matlab"],
    "VBA": ["vba", "visual basic"],
    "Objective-C": ["objective-c", "obj-c"],
    "PowerShell": ["powershell"],
    "Groovy": ["groovy"],
    "Elixir": ["elixir"],
    "Haskell": ["haskell"],
    "Solidity": ["solidity"],
}


TECHNOLOGIES_MAP = {
    # --- Frontend ---
    "React": ["react", "reactjs", "react.js", "react js"],
    "Angular": ["angular", "angularjs", "ng"],
    "Vue.js": ["vue", "vuejs", "vue.js", "vue 2", "vue 3"],
    "Next.js": ["next.js", "nextjs", "next js"],
    "Nuxt.js": ["nuxt", "nuxt.js", "nuxtjs"],
    "Svelte": ["svelte", "sveltekit"],
    "jQuery": ["jquery"],
    "Tailwind CSS": ["tailwind", "tailwindcss"],
    "Bootstrap": ["bootstrap"],
    "Material UI": ["material ui", "mui"],
    "Redux": ["redux", "redux-saga", "rtk"],
    "Webpack": ["webpack"],
    "Vite": ["vite"],

    # --- Backend & Frameworks ---
    "Node.js": ["node.js", "nodejs", "node"],
    "Express": ["express", "expressjs"],
    "NestJS": ["nest.js", "nestjs"],
    "Spring": ["spring", "spring boot", "springboot", "spring mvc"],
    "Django": ["django", "django rest framework", "drf"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Laravel": ["laravel"],
    "Symfony": ["symfony"],
    "CodeIgniter": ["codeigniter"],
    ".NET": [".net", "asp.net", "entity framework", "linq", "asp.net core", "blazor"],
    "Hibernate": ["hibernate"],
    "Gin": ["gin", "gin-gonic"],
    "Ruby on Rails": ["ruby on rails", "rails"],
    "GraphQL": ["graphql", "apollo"],
    "REST API": ["rest api", "restful", "rest"],
    "gRPC": ["grpc"],
    "WebSocket": ["websocket", "websockets", "socket.io"],

    # --- Mobile ---
    "Flutter": ["flutter"],
    "React Native": ["react native", "rn"],
    "Ionic": ["ionic"],
    "Xamarin": ["xamarin", "maui"],
    "SwiftUI": ["swiftui"],
    "Jetpack Compose": ["jetpack compose"],
    "UIKit": ["uikit"],

    # --- Infrastructure & DevOps ---
    "Docker": ["docker", "docker-compose"],
    "Kubernetes": ["kubernetes", "k8s", "helm"],
    "AWS": ["aws", "amazon web services", "ec2", "lambda", "s3", "dynamodb", "rds"],
    "Azure": ["azure", "azure devops"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Terraform": ["terraform"],
    "Ansible": ["ansible"],
    "Jenkins": ["jenkins"],
    "GitLab CI": ["gitlab ci", "gitlab-ci"],
    "GitHub Actions": ["github actions"],
    "CircleCI": ["circleci"],
    "Travis CI": ["travis", "travis ci"],
    "Puppet": ["puppet"],
    "Chef": ["chef"],
    "Nginx": ["nginx"],
    "Apache": ["apache", "httpd"],
    "Linux": ["linux", "ubuntu", "centos", "redhat", "debian", "alpine"],
    "Prometheus": ["prometheus"],
    "Grafana": ["grafana"],

    # --- AI / Data Science ---
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Keras": ["keras"],
    "OpenCV": ["opencv", "cv2"],
    "Hugging Face": ["hugging face", "transformers"],
    "LLM": ["llm", "openai", "gpt", "langchain", "llama"],
    "Jupyter": ["jupyter", "notebooks"],

    # --- Big Data / Data Engineering ---
    "Spark": ["spark", "pyspark"],
    "Hadoop": ["hadoop", "hdfs"],
    "Kafka": ["kafka"],
    "RabbitMQ": ["rabbitmq"],
    "Airflow": ["airflow"],
    "Databricks": ["databricks"],
    "Snowflake": ["snowflake"],
    "BigQuery": ["bigquery"],
    "Redshift": ["redshift"],
    "dbt": ["dbt"],
    "Tableau": ["tableau"],
    "Power BI": ["power bi", "powerbi"],

    # --- Database & Storage ---
    "Redis": ["redis"],
    "MongoDB": ["mongodb", "mongo", "mongoose"],
    "PostgreSQL": ["postgresql", "postgres", "pgsql"],
    "MySQL": ["mysql", "mariadb"],
    "Oracle": ["oracle", "plsql"],
    "SQL Server": ["sql server", "mssql", "t-sql"],
    "SQLite": ["sqlite"],
    "Elasticsearch": ["elasticsearch", "elk", "kibana", "logstash"],
    "Cassandra": ["cassandra"],
    "DynamoDB": ["dynamodb"],
    "Firestore": ["firestore", "firebase"],

    # --- Tools & Testing ---
    "Git": ["git", "github", "gitlab", "bitbucket"],
    "Selenium": ["selenium", "webdriver"],
    "Cypress": ["cypress"],
    "Postman": ["postman"],
    "Jira": ["jira", "confluence"],
    "Figma": ["figma"],
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

    if any(k in title_lower for k in FULLSTACK_KEYWORDS):
        return "Fullstack Developer"
    if any(k in title_lower for k in FRONTEND_KEYWORDS):
        return "Frontend Developer"
    if any(k in title_lower for k in BACKEND_KEYWORDS):
        return "Backend Developer"

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

    # ERP / SAP
    if any(
        k in title_lower
        for k in ["erp", "sap", "odoo", "salesforce", "crm", "oracle ebs"]
    ):
        return "ERP/CRM Engineer"

    # Default return existing subfield if valid, or Other
    return (
        subfield if subfield and subfield != "Other" else "Software Engineer (General)"
    )
