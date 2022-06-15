





text = "Text messaging, or texting, is the act of composing and sending electronic messages, typically consisting of alphabetic and numeric characters, between two or more users of mobile devices, desktops/laptops, or another type of compatible computer. Text messages may be sent over a cellular network, or may also be sent via an Internet connection."

c = 0
for s in range(len(text)):
	c += 1
	if c == 20:
		while text[s] != " ":
			s -= 1
		text = list(text)
		text[s] = "\n"
		text = "".join(text)
		c = 0

print(text)