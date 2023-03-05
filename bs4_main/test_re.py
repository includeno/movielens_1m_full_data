import re

# 要处理的文本内容
text = "xyzydasd($534,987,076)"

# 匹配括号及括号内的内容
pattern = re.compile(r'\([^)]*\)')

# 替换匹配到的内容为空字符串
text = pattern.sub('', text)

# 输出结果
print(text)
