import re

f = open("AT678/AT678.cpp")
line = f.read()

keywords = re.finditer(r"\b(break|case|catch|const|const_cast|continue|default|delete|do|dynamic_cast|else|explicit|export|extern|for|friend|goto|if|inline|mutable|namespace|new|operator|private|protected|public|register|reinterpret_cast|return|sizeof|static|static_cast|switch|this|throw|try|typeid|typename|using|virtual|volatile|while)\b", line)
datatypes = re.finditer(r"\b(asm|auto|bool|char|double|enum|float|int|long|class|short|signed|struct|template|typedef|union|unsigned|void|wchar_t)\b", line)
numerals = re.finditer(r"\b(true|false)\b", line)
thisptr = re.finditer(r"\b(this)\b", line)
quotes = re.finditer(r"(\"[^\"]+\"|'[^']+')", line)

for i in quotes:
	temp = i.span()
	print(temp, end=' ')
	for i in range(temp[0], temp[1]):
		print(line[i], end='')
	print()