from flask import Flask, request, jsonify
import mammoth
import PyPDF2
import io

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract_text():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    filename = file.filename.lower()
    content = ""

    if filename.endswith(".docx"):
        result = mammoth.extract_raw_text(file)
        content = result.value
    elif filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        content = "\n".join([page.extract_text() or "" for page in reader.pages])
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    return jsonify({"text": content.strip()})
