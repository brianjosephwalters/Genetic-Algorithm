import os

def getComments(lines):
    comments = []
    for line in lines:
        if line.find("Comment:") == 0:
            comments.append(line)
    return comments
    
def getDataCount(lines):
    count = 0;
    for line in line:
        if line.find("TotalProtein:") == 0:
            parts = line.split('=')
            count = int(parts[1])
    return count

def getData(lines):
    strings = []
    values = []
    for line in lines:
        if line.find("Seq") == 0:
            parts = line.split('=')
            strings.append(parts[1].strip())
        if line.find("Fitness") == 0:
            parts = line.split('=')
            values.append(int(parts[1]))
    return (strings, values)

def loadDefaultData():
    f = open("../../data/Input.txt")
    lines = f.readlines()
    f.close()
    return getData(lines)


if __name__ == '__main__':
    print os.getcwd()
    f = open("../../data/Input.txt")
    lines = f.readlines()
    f.close()
    
    strings, values = getData(lines)
    print strings
    print values