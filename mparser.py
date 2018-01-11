from io import StringIO

f = open("./bit.txt",'r+')

def rt(x) :
    if x == 0 :
        return "□"
    elif x == 1:
        return "■"
    else:
        return "★"
def write_map(mapp) :
    line = ""
    for i in mapp :
        line = "".join( rt(x) for x in i )
        line += "\n"
        f.write(str(line))

def read_map_from_file(mapp,x,y,f) :
    idx = 0
    lineMap = f.read()
    for yy in range(y-1,-1,-1) :
        for xx in range(0,x + 1) :
            if lineMap[idx] == "\n" :
                idx += 1
                continue
            mapp[xx][yy] = int(lineMap[idx])
            idx += 1

def read_map_from_list(mapp,x,y) :
    line_block = ""
    for k in range(y-1 , -1, -1) :
        for i in range(0 , x) :
            line_block += rt(mapp[i][k])
        line_block += '\n'
    print(line_block)
