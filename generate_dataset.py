import csv

data = []

# SQL Injection examples
for i in range(300):
    code = f"query = 'SELECT * FROM users WHERE id=' + user_input_{i}"
    data.append([code, "sql_injection"])

# XSS examples
for i in range(300):
    code = f"<script>alert('XSS{i}')</script>"
    data.append([code, "xss"])

# Hardcoded secrets
for i in range(300):
    code = f"password = 'admin{i}'"
    data.append([code, "hardcoded_secret"])

# Safe code
for i in range(300):
    code = f"cursor.execute('SELECT * FROM users WHERE id=%s', (id_{i},))"
    data.append([code, "safe"])

# Save dataset
with open("dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["code", "label"])
    writer.writerows(data)

print("✅ Dataset created with", len(data), "samples")