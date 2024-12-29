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
        }
        #editor {
            width: 60%;
            margin-right: 20px;
        }
        textarea { 
            width: 100%; 
            height: 300px; 
            font-family: monospace; 
        }
        pre { 
            background: #f4f4f4; 
            padding: 10px; 
            border: 1px solid #ddd; 
            overflow: auto;
            height: 300px;
        }
        #output-container {
            width: 40%;
        }
    </style>
</head>
<body>
    <div id="editor">
        <h1>Python Web Interpreter</h1>
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
