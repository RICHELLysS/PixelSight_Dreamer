content = "GEMINI_API_KEY=AIzaSyBrFnoggFqv9Wi3geyqbr3eTi1ul44J9Xg"

try:
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(content)
    print("成功！.env 文件已重建为标准的 UTF-8 格式。")
except Exception as e:
    print(f"失败：{e}")