

def readAndSplitNextLine(fstream, separator=','):
    line = fstream.readline()
    return line.split(separator)

def pushDataToBuffer(buffer, data):
    buffer[data[-2]] = (float)(data[-1])

def printBuffer(buffer, data):
    best = sorted(buffer.items(), key=lambda kv: kv[1])[-1][0]
    line = ""
    for i in data[:-2]:
        line+=(i+',')
    with open('test.csv', 'a+') as f:
        f.write(line+best+"\n")


with open('nn_deck_6_round_2000.csv', 'r') as f:
    out = []
    lines = f.readlines()
    data = []
    for line in lines:
        row = line.split(',')
        data.append(row)

    mainRow = data[0]
    bestScore = float(mainRow[-1])
    bestMove = mainRow[-2]
    for row in data[1:]:
        if row[0] == mainRow[0]:
            if bestScore <= float(row[-1]):
                bestScore = float(row[-1])
                bestMove = row[-2]
        else:
            # with open('processed_deck_6_round_2000.csv', 'a+') as outfile:
            #     line = ""
            #     for i in mainRow[:-2]:
            #         line+= (i+',')
            #     outfile.write(line+bestMove+'\n')
            line = ""
            for i in mainRow[:-2]:
                line+= (i+',')
            out.append(line + bestMove + '\n')

            mainRow = row
            bestScore = float(mainRow[-1])
            bestMove = mainRow[-2]

    line = ""
    for i in mainRow[:-2]:
        line += (i + ',')
    out.append(line + bestMove + '\n')

    with open('processed_deck_6_round_2000.csv', 'a+') as outfile:
        # line = ""
        # for i in mainRow[:-2]:
        #     line += (i + ',')
        # outfile.write(line + bestMove + '\n')
        outfile.writelines(out)

