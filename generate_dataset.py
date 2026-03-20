import csv
import random

safe_code = [
    "print('Hello World')",
    "SELECT * FROM users WHERE id=1",
    "if(x > 5){ return x; }",
    "def add(a,b): return a+b",
    "console.log('safe code')",
    "for i in range(10): print(i)",
    "let x = 10;",
    "user = input('Enter name')",
    "SELECT name FROM products",
]

vulnerable_code = [
    "SELECT * FROM users WHERE id=1 OR 1=1",
    "SELECT * FROM users WHERE username='' OR '1'='1'",
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "eval(input())",
    "exec(user_input)",
    "password = '123456'",
    "os.system(user_input)",
    "SELECT * FROM users WHERE name = '" + "' + user_input + '",
]

data = []

# generate samples
for _ in range(500):
    data.append([random.choice(safe_code), 0])
    data.append([random.choice(vulnerable_code), 1])

# shuffle
random.shuffle(data)

# save
with open("dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["code", "label"])
    writer.writerows(data)

print("✅ Dataset created with", len(data), "samples")