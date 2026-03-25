from flask import Flask, request, jsonify, render_template
from phishing_detection_tool import analyze_url

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    result = analyze_url(url)
    return jsonify(result)

if __name__ == '__main__':
    # Enable debug mode for development
    app.run(host='0.0.0.0', port=5000, debug=True)
