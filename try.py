import subprocess as sb
import os




def UkDecode(text):
	text = text.decode("cp866")
	for i in range(len(text) - 1):
		if text[i] == "?":
			text = text[:i] + "і" + text[i+1:]
	return text


out = sb.check_output("dir", shell=True)

print(UkDecode(out))



# for i in out:
# 	if i == "?":
# 		i = "і"
# print(out)

# os.system("dir")