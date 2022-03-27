import subprocess as sb
import os



out = sb.check_output("dir", shell=True).decode("cp866")

print(out)
# for i in out:
# 	if i == "?":
# 		i = "і"
# print(out)

# os.system("dir")