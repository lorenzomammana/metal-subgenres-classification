temp = open('temp.csv', "r", encoding="utf-8")
out1 = open('out1.csv', "w+", encoding="utf-8")

print("stage 1")

endstage = False
for line in temp.readlines():

    if line.split(',')[0] == 'AFTERBLOOD':
        endstage = True

    if endstage:
        out1.write(line)
    else:
        lst = list(line)
        for i in range(1, len(lst) - 1):
            if lst[i] == '"':
                if lst[i - 1] == "," or lst[i + 1] == "\n":
                    continue
                else:
                    lst[i] = ""

        out1.write("".join(lst))

out1.close()
temp.close()

print("stage 2")
out1 = open('out1.csv', "r", encoding="utf-8")
out2 = open('out2.csv', "w+", encoding="utf-8")

while True:
    line = out1.readline()

    if not line:
        break

    splitline = line.split(",")

    if len(splitline) == 5 and line[-2] == '"':
        out2.write(line)
        continue

    if len(splitline) > 5:
        i = 0
        while True:
            try:
                int(splitline[i])
                break
            except ValueError:
                i += 1

        album_name = " ".join(splitline[1:i])
        splitline[1] = album_name
        del splitline[2:i]

    lyrics = "" + splitline[-1].replace("\n", "")

    while line[-2] != '"':
        line = out1.readline()
        lyrics += line.replace("\n", "")

    out2.write(",".join(splitline[0:-1]) + "," + lyrics + "\n")

out1.close()
out2.close()

out2 = open('out2.csv', "r", encoding="utf-8")

for line in out2.readlines():
    splitline = line.split(",")

    if len(splitline) == 5 and line[-2] == '"':
        continue

    print(line)

out2.close()
