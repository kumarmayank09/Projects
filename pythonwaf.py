from flask import Flask, request, abort

app = Flask(__name__)

# Simple SQL Injection patterns (payloads)
SQLI_PATTERNS = ["'", '"', "--", "/*", "*/", " OR ", " AND "]

# Simple XSS patterns (payloads)
XSS_PATTERNS = ["<script>", "</script>", "javascript:", "<img", "<iframe", "<svg"]

# Function to check for SQL Injection
def is_sql_injection(data):
    for pattern in SQLI_PATTERNS:
        if pattern.lower() in data.lower():
            return True
    return False

# Function to check for XSS
def is_xss_attack(data):
    for pattern in XSS_PATTERNS:
        if pattern.lower() in data.lower():
            return True
    return False

# Middleware to check incoming requests for attacks
@app.before_request
def waf_middleware():
    query_string = request.query_string.decode("utf-8")
    if is_sql_injection(query_string) or is_xss_attack(query_string):
        abort(403)  # Forbidden

    # Check POST data
    if request.method == "POST":
        for key, value in request.form.items():
            if is_sql_injection(value) or is_xss_attack(value):
                abort(403)  # Forbidden

# Basic test route
@app.route('/')
def home():
    return "Welcome to the protected application!"

# Example vulnerable route
@app.route('/search', methods=["GET", "POST"])
def search():
    query = request.args.get("q", "")
    return f"Search results for: {query}"

if __name__ == "__main__":
    app.run(debug=True)
