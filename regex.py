import re

"""
keywords = re.finditer(r"\b(break|case|catch|const|const_cast|continue|default|delete|do|dynamic_cast|else|explicit|export|extern|for|friend|goto|if|inline|mutable|namespace|new|operator|private|protected|public|register|reinterpret_cast|return|sizeof|static|static_cast|switch|this|throw|try|typeid|typename|using|virtual|volatile|while)\b", line)
datatypes = re.finditer(r"\b(asm|auto|bool|char|double|enum|float|int|long|class|short|signed|struct|template|typedef|union|unsigned|void|wchar_t)\b", line)
thisptr = re.finditer(r"\b(this)\b", line)
brackets = re.finditer(r"[\w]+(?=\()", line) # TODO: fix up brackets & whitespace
quotes = re.finditer(r"(\"[^\"]+\"|'[^']+')", line)
sComments = re.finditer(r"\/\/[^\n\r]+", line)
mComments = re.finditer(r"\/\*[^]+\*\/", line)
"""

preproc = re.compile(r"^#\S+\b")
keyword = re.compile(r"\b(break|case|catch|const|const_cast|continue|default|delete|do|dynamic_cast|else|explicit|export|extern|for|friend|goto|if|inline|mutable|namespace|new|operator|private|protected|public|register|reinterpret_cast|return|sizeof|static|static_cast|switch|this|throw|try|typeid|typename|using|virtual|volatile|while)\b")
datatype = re.compile(r"\b(asm|auto|bool|char|double|enum|float|int|long|class|short|signed|struct|template|typedef|union|unsigned|void|wchar_t)\b")
numeral = re.compile(r"\b(true|false|\d+)\b")
literal = re.compile(r"(<|\"|\').+(>|\"|\')")
comment = re.compile(r"//.*$")               # nvm about /* */ right now

ex = [(preproc, 5), (keyword, 5), (datatype, 1), (numeral, 2), (literal, 3), (comment, 4)]

line = input()
result = [0] * len(line)
for expr, clr in ex:
	for match in expr.finditer(line):
		for i in range(match.span()[0], match.span()[1]):
			result[i] = clr

print(result)
