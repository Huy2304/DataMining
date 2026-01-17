import gradio as gr
from transformers import pipeline
import re

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_tech_terms(text, labels):
    """Extract and classify tech-related terms from text"""
    labels_list = [label.strip() for label in labels.split(",") if label.strip()]

    if not text.strip():
        return "Vui lòng nhập văn bản!", {}

    if len(labels_list) < 2:
        return "Vui lòng nhập ít nhất 2 nhãn!", {}

    # Tách văn bản thành các từ/cụm từ tiềm năng
    words = re.findall(r'\b[\w\-\.]+\b', text)  # Lấy các từ
    phrases = re.findall(r'\b[\w\s\-\.]{3,20}\b', text)  # Lấy cụm từ 3-20 ký tự

    # Kết hợp cả từ đơn và cụm từ
    candidates = list(set(words + phrases))
    # candidates = [c for c in candidates if len(c) > 2]  # Loại bỏ từ quá ngắn

    # Phân loại từng candidate
    classified_results = {}

    for label in labels_list:
        classified_results[label] = []

    for candidate in candidates[:20]:  # Giới hạn số lượng để tránh quá tải
        try:
            result = classifier(candidate, candidate_labels=labels_list)
            top_label = result["labels"][0]
            top_score = result["scores"][0]

            if top_score > 0.4:  # Ngưỡng tin cậy
                classified_results[top_label].append((candidate, top_score))
        except:
            continue

    # Tạo output
    output_text = f"**📝 Văn bản gốc:**\n\"{text}\"\n\n"
    output_text += f"**🏷️ Nhãn đã nhập:** {', '.join(labels_list)}\n\n"
    output_text += "**📊 Kết quả phân loại từ/cụm từ:**\n\n"

    for label in labels_list:
        if classified_results[label]:
            output_text += f"### 🔵 {label.upper()}:\n"
            # Sắp xếp theo độ tin cậy giảm dần
            sorted_items = sorted(classified_results[label], key=lambda x: x[1], reverse=True)
            for word, score in sorted_items:
                output_text += f"- `{word}` ({score:.1%})\n"
            output_text += "\n"

    # Đếm tổng số từ được phân loại
    total_classified = sum(len(items) for items in classified_results.values())
    output_text += f"\n**📈 Tổng kết:** Phân loại được {total_classified} từ/cụm từ từ văn bản."

    return output_text, classified_results

# Create the Gradio interface
with gr.Blocks(title="Tech Term Classifier", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔬 Phân loại Thuật ngữ Công nghệ")
    gr.Markdown("Phân loại các từ/cụm từ trong văn bản theo nhãn công nghệ")

    with gr.Row():
        with gr.Column(scale=1):
            text_input = gr.Textbox(
                label="📄 Văn bản công nghệ",
                placeholder="Ví dụ: Python, machine learning, deep neural networks, AI algorithms...",
                lines=5
            )

            labels_input = gr.Textbox(
                label="🏷️ Nhãn công nghệ",
                placeholder="programming, ai, data_science, web_dev, cloud, database",
                value="technology, programming, artificial_intelligence, data_science, web_development, cloud_computing, database, other"
            )

            submit_btn = gr.Button("🔍 Phân loại Thuật ngữ", variant="primary")
            clear_btn = gr.Button("🔄 Xóa")

        with gr.Column(scale=2):
            output_text = gr.Markdown(label="📊 Kết quả phân loại")

            with gr.Accordion("📋 Xem dữ liệu thô", open=False):
                json_output = gr.JSON(label="Dữ liệu phân loại")

    # Ví dụ mẫu cho công nghệ
    gr.Examples(
        examples=[
            [
                "Python is great for machine learning and data science. TensorFlow and PyTorch are popular deep learning frameworks. Django is used for web development.",
                "programming, machine_learning, web_framework, deep_learning, data_analysis"
            ],
            [
                "AWS provides cloud computing services like EC2 and S3. MongoDB is a NoSQL database. React and Vue are frontend JavaScript frameworks.",
                "cloud, database, frontend, backend, infrastructure"
            ],
            [
                "Trí tuệ nhân tạo và học máy đang phát triển mạnh. Python được dùng trong khoa học dữ liệu. TensorFlow hỗ trợ deep learning.",
                "ai, machine_learning, programming, data_science, research"
            ],
            [
                "Java Spring for backend, React for frontend, Docker for containerization, Kubernetes for orchestration, PostgreSQL for database.",
                "backend, frontend, devops, container, database"
            ]
        ],
        inputs=[text_input, labels_input],
        label="💻 Ví dụ công nghệ"
    )

    # Xử lý sự kiện
    def process_and_format(text, labels):
        output, json_data = extract_tech_terms(text, labels)
        return output, json_data

    submit_btn.click(
        fn=process_and_format,
        inputs=[text_input, labels_input],
        outputs=[output_text, json_output]
    )

    def clear_all():
        return "", "programming, artificial_intelligence, data_science, web_development, cloud_computing, database, deep_learning", "", {}

    clear_btn.click(fn=clear_all, outputs=[text_input, labels_input, output_text, json_output])

    gr.Markdown("""
    ## 📖 Hướng dẫn:
    1. Nhập văn bản công nghệ vào ô đầu tiên
    2. Nhập các nhãn công nghệ phân cách bằng dấu phẩy
    3. Nhấn "Phân loại Thuật ngữ" để xem các từ được phân loại theo nhãn

    ## 🎯 Đầu ra:
    - Mỗi từ/cụm từ trong văn bản sẽ được phân loại vào nhãn phù hợp nhất
    - Chỉ hiển thị các từ có độ tin cậy > 40%
    - Từ được đóng khung `` để dễ nhận diện
    """)

# Launch the interface
if __name__ == "__main__":
    demo.launch()
