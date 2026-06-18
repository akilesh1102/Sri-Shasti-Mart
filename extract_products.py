import re

with open("index.html", "r") as f:
    content = f.read()

titles = re.findall(r'<h3 class="product-title">(.*?)</h3>', content)
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")
