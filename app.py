from flask import Flask, request, jsonify, render_template_string
import sys
import io

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Web Interpreter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            display: flex;
            flex-direction: row;
            background-color: #121212;
            color: #e0e0e0;
        }
        #editor {
            width: 60%;
            margin-right: 20px;
        }
        textarea {
            width: 95%;
            height: 300px;
            font-family: monospace;
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #333;
            padding: 10px;
            border-radius: 5px;
        }
        button {
            background-color: #333;
            color: #e0e0e0;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s, box-shadow 0.3s;
        }
        button:hover {
            background-color: #444;
            box-shadow: 0 0 10px 2px #00ff00;
        }
        pre {
            background: #1e1e1e;
            color: #e0e0e0;
            padding: 10px;
            border: 1px solid #333;
            border-radius: 5px;
            overflow: auto;
            height: 300px;
        }
        #output-container {
            width: 40%;
        }
        h1, h3 {
            color: #e0e0e0;
        }
    </style>
</head>
<body>
    <div id="editor">
        <h3>Python Web Interpreter</h3>
        <form id="codeForm">
            <textarea id="code" placeholder="Write your Python code here..."></textarea><br>
            <button type="submit">Run Code</button>
        </form>
    </div>
    <div id="output-container">
        <h3>Output:</h3>
        <pre id="output"></pre>
    </div>

    <script>
        document.getElementById('codeForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const code = document.getElementById('code').value;

            const response = await fetch('/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });

            const result = await response.json();
            document.getElementById('output').textContent = result.output;
        });
    </script>
</body>
</html>



"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run', methods=['POST'])
def run_code():
    try:
        # Capture code from the request
        code = request.json.get('code', '')

        # Redirect stdout to capture print outputs
        stdout = io.StringIO()
        sys.stdout = stdout

        # Execute the code
        exec(code, {})

        # Get the output
        output = stdout.getvalue()
    except Exception as e:
        output = str(e)
    finally:
        # Reset stdout
        sys.stdout = sys.__stdout__

    return jsonify({ 'output': output })

if __name__ == '__main__':
    app.run(debug=True)
