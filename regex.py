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

call = re.compile(r"\b\S+(?=\()")
preproc = re.compile(r"^#\S+\b")
keyword = re.compile(r"\b(break|case|catch|const|const_cast|continue|default|delete|do|dynamic_cast|else|explicit|export|extern|for|friend|goto|if|inline|mutable|namespace|new|operator|private|protected|public|register|reinterpret_cast|return|sizeof|static|static_cast|switch|this|throw|try|typeid|typename|using|virtual|volatile|while)\b")
datatype = re.compile(r"\b(asm|auto|bool|char|double|enum|float|int|long|class|short|signed|struct|template|typedef|union|unsigned|void|wchar_t)\b")
numeral = re.compile(r"\b(true|false|\d+)\b")
literal = re.compile(r"(\"|\').*(\"|\')")
comment = re.compile(r"//.*$")               # nvm about /* */ right now

f = open("default-skin.gskin")
palette = eval(f.read())
f.close()

ex = [(call, palette["call"]), (preproc, palette["preproc"]), (keyword, palette["keyword"]), (datatype, palette["datatype"]), (numeral, palette["numeral"]), (literal, palette["literal"]), (comment, palette["comment"])]

def parse(self, lineNum=-1):
	if lineNum < 0:
		for i in range(len(self.txtBuffer)):
			parse(self, i)
	line = ''
	for i, pack in enumerate(self.txtBuffer[lineNum]):
		line += pack[0]
		self.txtBuffer[lineNum][i][1] = (255, 255, 255)
	for expr, clr in ex:
		for match in expr.finditer(line):
			for i in range(match.start(), match.end()):
				self.txtBuffer[lineNum][i][1] = clr
