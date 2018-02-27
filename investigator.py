import base
import mparser
import copy
import time
map0 = [[ 0 for row in range (14)] for col in range(10)]
wei0 = [[ round(0.1 * row,1) for row in range(14)] for col in range(10)]


f = open("./bit.txt","r")
mparser.read_map_from_file(map0,10,14,f)

def render_case(pmap, plist) :
    print ("size : " , len(plist))
    for li in range(len(plist)) :
        for idx in range(0,4) :
            pmap[plist[li][idx][0]][plist[li][idx][1]] += 2
        time.sleep(0.5)
        mparser.read_map_from_list(pmap,10,14)
        for idxx in range(0, 4) :
            pmap[plist[li][idxx][0]][plist[li][idxx][1]] -= 2

def get_max_score_position(pmap, plist, weight,bias) :
    idx = 0
    sList = []
    print(len(plist))
    for ls in plist :
        summ = 0
        idxx = 0
        for pls in ls :
            summ += weight[pls[0]][pls[1]] + bias[pls[0]][pls[1]]
            idxx += 1
        sList.append(summ)
        print(summ)
    return sList.index(max(sList))

blc = base.block("stick",map0)
aList = base.find_all_possible_pos(blc , map0 , 3)
render_case(map0, aList)
