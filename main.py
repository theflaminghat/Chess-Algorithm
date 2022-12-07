board = ["XXXXXXXXXXXX","XXXXXXXXXXXX",
"XXRNBQKBNRXX",
"XXPPPPPPPPXX",
"XXOOOOOOOOXX",
"XXOOOOOOOOXX",
"XXOOOOOOOOXX",
"XXOOOOOOOOXX",
"XXppppppppXX",
"XXrnbqkbnrXX","XXXXXXXXXXXX","XXXXXXXXXXXX","K1Q1","k1q1","en0O","tw"]

wait = 50000
movelist = []
setboardmovelist=[]
maxheight = 5

class move:
    def __init__(self,move,children,parent,height,eval,valboard):
        self.parent = parent
        self.children=children
        self.height = height
        self.eval = eval
        self.move = move
        self.valboard = valboard
    def givechildren(self,children):
        self.children = children
    def subtractHeight(self,height):
        self.height -=1
    def getMove(self):
        return self.move
    def getHeight(self):
        return self.height
    def getvalboard(self):
        return self.valboard
    def geteval(self):
        return self.eval
    def getparent(self):
        return self.parent
    def setvalboard(self,a):
        self.valboard = a
    def seteval(self,a):
        self.eval = a


def interpret(a):
    index = ['a','b','c','d','e','f','g','h']
    ret = (str(index[int(a[1])-2])+str((int(a[0])-1))+str(index[int(a[3])-2])+str(int(a[2])-1))
    if len(a) > 4:
        ret += a[4]
    return ret


def uninterpret(a):
    list = ['a','b','c','d','e','f','g','h']
    ret=  str(int(a[1])+1) + str(int(list.index(a[0]))+2) + str(int(a[3])+1) + str(int(list.index(a[2]))+2)
    if len(a) > 4:
        ret += a[4]
    return ret

def setBoard(a,b):
    returnBoard = []
    returnBoard += b
    returnBoard[int(a[2])] = (returnBoard[int(a[2])][:int(a[3])])+returnBoard[int(a[0])][int(a[1])] + (returnBoard[int(a[2])][int(a[3])+1:])
    
    returnBoard[int(a[0])] = (returnBoard[int(a[0])][:int(a[1])])+'O' + (returnBoard[int(a[0])][int(a[1])+1:]) 
    if len(a)>4:
        returnBoard[int(a[0])] = (returnBoard[int(a[2])][:int(a[3])])+ a[4] + (returnBoard[int(a[2])][int(a[3])+1:])
    return returnBoard

def evaluate(b):
    sum = 0

    pieces = ['p','b','n','r','q','k','P','B','N','R','Q','K']
    value = [-10,-30,-30,-50,-90,-1000,10,30,30,50,90,1000]
    evalplaces = [[
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,-5,-5,-5,-5,-5,-5,-5,-5,0,0],
    [0,0,-1,-1,-2,-3,-3,-2,-1,-1,0,0],
    [0,0,-0.5,-0.5,-1,-2.5,-2.5,-1,-0.5,-0.5,0,0],
    [0,0,0,0,0,-2,-2,0,0,0,0,0],
    [0,0,-0.5,0.5,1,0,0,1,0.5,-0.5,0,0],
    [0,0,-0.5,-1,-1,2,2,-1,-1,-.5,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],],

    [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]],

    [[0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,5,4,3,3,3,3,4,5,0,0],
    [0,0,4,2,0,0,0,0,2,4,0,0],
    [0,0,3,0,-1,-1.5,-1.5,-1,0,3,0,0],
    [0,0,3,-0.5,-1.5,-2,-2,-1.5,-0.5,3,0,0],
    [0,0,3,0,-1.5,-2,-2,-1.5,0,3,0,0],
    [0,0,3,-0.5,-1,-1.5,-1.5,-1,-0.5,3,0,0],
    [0,0,4,2,0,-0.5,-0.5,0,2,4,0,0],
    [0,0,5,4,3,3,3,3,4,5,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]],

    [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]],

    [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]],

    [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]],
    [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0.5,1,1,-2,-2,1,1,0.5,0,0],
    [0,0,0.5,-0.5,-1,0,0,-1,-0.5,0.5,0,0],
    [0,0,0,0,0,2,2,0,0,0,0,0],
    [0,0,0.5,1,1,2.5,2.5,1,1,0.5,0,0],
    [0,0,1,1,2,3,3,2,1,1,0,0],
    [0,0,5,5,5,5,5,5,5,5,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]],
    
    [[0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,-5,-4,-3,-3,-3,-3,-4,-5,0,0],
    [0,0,-4,-2,0,0.5,0.5,0,-2,-4,0,0],
    [0,0,-3,0.5,1,1.5,1.5,1,0.5,-3,0,0],
    [0,0,-3,0,1.5,2,2,1.5,0,-3,0,0],
    [0,0,-3,0.5,1.5,2,2,1.5,0.5,-3,0,0],
    [0,0,-3,0,1,1.5,1.5,1,0,-3,0,0],
    [0,0,-4,-2,0,0,0,0,-2,-4,0,0],
    [0,0,-5,-4,-3,-3,-3,-3,-4,-5,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]],

    [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]]
    ]
    for i in range(2,10):
        for j in range(2,10):
            if b[j][i] in pieces:
                sum += value[pieces.index(b[j][i])]
                sum += evalplaces[pieces.index(b[j][i])][j][i]

    
    return sum



def whitePromotion(a):
    return [a+'B',a+'N',a+'R',a+'Q']

def blackPromotion(a):
    return [a+'b',a+'n',a+'r',a+'q']


    

def possibleWhitePawn(a):
    takeAble = ["p","r","b","q","n","k"]
    possiblemoves = []
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'P':
                if a[j+1][i]=='O':
                    if j==3 and a[j+2][i]=='O':
                        possiblemoves.append(str(j)+str(i)+str(j+2)+str(i))
                    if j == 8:
                        possiblemoves+=whitePromotion(str(j)+str(i)+str(j+1)+str(i))
                    if j != 8:
                        possiblemoves.append(str(j)+str(i)+str(j+1)+str(i))
                if a[j+1][i+1] in takeAble:
                    if j == 8:
                        possiblemoves+=whitePromotion(str(j)+str(i)+str(j+1)+str(i+1))
                    else:
                        possiblemoves.append(str(j)+str(i)+str(j+1)+str(i+1))
                if a[j+1][i-1] in takeAble:
                    if j == 8:
                        possiblemoves+=whitePromotion(str(j)+str(i)+str(j+1)+str(i-1))
                    else:
                        possiblemoves.append(str(j)+str(i)+str(j+1)+str(i-1))
    return possiblemoves
def possibleBlackPawn(a):
    takeAble = ["P","R","B","Q","N","K"]
    possiblemoves = []
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'p':
                if a[j-1][i]=='O':
                    if j==8 and a[j-2][i]=='O':
                        possiblemoves.append(str(j)+str(i)+str(j-2)+str(i))
                    if j == 3:
                        possiblemoves+=blackPromotion(str(j)+str(i)+str(j-1)+str(i))
                    if j != 3:
                        possiblemoves.append(str(j)+str(i)+str(j-1)+str(i))
                if a[j-1][i-1] in takeAble:
                    if j == 3:
                        possiblemoves+=blackPromotion(str(j)+str(i)+str(j-1)+str(i-1))
                    else:
                        possiblemoves.append(str(j)+str(i)+str(j-1)+str(i-1))
                if a[j-1][i+1] in takeAble:
                    if j == 3:
                        possiblemoves+=blackPromotion(str(j)+str(i)+str(j-1)+str(i+1))
                    else:
                        possiblemoves.append(str(j)+str(i)+str(j-1)+str(i+1))
    return possiblemoves
def possibleBlackRook(a):
    possiblemoves = []
    takeAble = ["P","R","B","Q","N","K"]
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'r':
                #up
                for index in range(1,8):
                    if a[j+index][i] == 'O':
                        possiblemoves.append(str(j)+str(i)+str(j+index)+str(i))
                #up
                    elif a[j+index][i] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j+index)+str(i))
                        break
                    else:
                        break
                #down
                for index in range(1,8):
                    if a[j-index][i] == 'O':
                        possiblemoves.append(str(j)+str(i)+str(j-index)+str(i))
                    elif a[j-index][i] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j-index)+str(i))
                        break
                    else:
                        break
                for index in range(1,8):
                    if a[j][i+index] == 'O':
                        possiblemoves.append(str(j)+str(i)+str(j)+str(i+index))
                    elif a[j][i+index] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j)+str(i+index))
                        break
                  #up
                    else:
                        break
                #down
                for index in range(1,8):
                    if a[j][i-index] == 'O':
                        possiblemoves.append(str(j)+str(i)+str(j)+str(i-index))
                    elif a[j][i-index] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j)+str(i-index))
                        break
                    else:
                        break
    return possiblemoves
def possibleWhiteRook(a):
    possiblemoves = []
    takeAble = ["p","r","b","q","n","k"]
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'R':
                #up
                for index in range(1,8):
                    if a[j+index][i] == 'O':
                        possiblemoves.append(str(j)+str(i)+str(j+index)+str(i))
                #up
                    elif a[j+index][i] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j+index)+str(i))
                        break
                    else:
                        break
                #down
                for index in range(1,8):
                    if a[j-index][i] == 'O':
                        possiblemoves.append(str(j)+str(i)+str(j-index)+str(i))
                    elif a[j-index][i] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j-index)+str(i))
                        break
                    else:
                        break
                for index in range(1,8):
                    if a[j][i+index] == 'O':
                        possiblemoves.append(str(j)+str(i)+str(j)+str(i+index))
                    elif a[j][i+index] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j)+str(i+index))
                        break
                  #up
                    else:
                        break
                #down
                for index in range(1,8):
                    if a[j][i-index] == 'O':
                        possiblemoves.append(str(j)+str(i)+str(j)+str(i-index))
                    elif a[j][i-index] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j)+str(i-index))
                        break
                    else:
                        break
    return possiblemoves
def possibleWhiteKnight(a):
    possiblemoves = []
    coords = [[1,2],[2,1],[2,-1],[1,-2],[-1,-2],[-2,-1],[-2,1],[-1,2]]
    takeAble = ["p","r","b","q","n","k","O"]
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'N':
                for index in range(8):
                    if a[j+coords[index][0]][i+coords[index][1]] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j+coords[index][0])+str(i+coords[index][1]))
    return possiblemoves
def possibleBlackKnight(a):
    possiblemoves = []
    coords = [[1,2],[2,1],[2,-1],[1,-2],[-1,-2],[-2,-1],[-2,1],[-1,2]]
    takeAble = ["P","R","B","Q","N","K",'O']
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'n':
                for index in range(8):
                    if a[j+coords[index][0]][i+coords[index][1]] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j+coords[index][0])+str(i+coords[index][1]))
    return possiblemoves
def possibleWhiteBishop(a):
    possiblemoves = []
    takeAble = ["p","r","b","q","n","k"]
    coords = [[1,1],[1,-1],[-1,1],[-1,-1]]
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'B':
                for coord in range(4):
                    for index in range(1,8):
                        if a[j+coords[coord][0]*index][i+coords[coord][1]*index] == 'O':
                            possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0]*index)+str(i+coords[coord][1]*index))
                        elif a[j+coords[coord][0]*index][i+coords[coord][1]*index] in takeAble:
                            possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0]*index)+str(i+coords[coord][1]*index))
                            break
                        else:
                            break
    return possiblemoves
def possibleBlackBishop(a):
    possiblemoves = []
    takeAble = ["P","R","B","Q","N","K"]
    coords = [[1,1],[1,-1],[-1,1],[-1,-1]]
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'b':
                for coord in range(4):
                    for index in range(1,8):
                        if a[j+coords[coord][0]*index][i+coords[coord][1]*index] == 'O':
                            possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0]*index)+str(i+coords[coord][1]*index))
                        elif a[j+coords[coord][0]*index][i+coords[coord][1]*index] in takeAble:
                            possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0]*index)+str(i+coords[coord][1]*index))
                            break
                        else:
                            break
    return possiblemoves
def possibleBlackQueen(a):
    possiblemoves = []
    takeAble = ["P","R","B","Q","N","K"]
    coords = [[1,1],[1,-1],[-1,1],[-1,-1],[0,1],[1,0],[0,-1],[-1,0]]
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'q':
                for coord in range(8):
                    for index in range(1,8):
                        if a[j+coords[coord][0]*index][i+coords[coord][1]*index] == 'O':
                            possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0]*index)+str(i+coords[coord][1]*index))
                        elif a[j+coords[coord][0]*index][i+coords[coord][1]*index] in takeAble:
                            possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0]*index)+str(i+coords[coord][1]*index))
                            break
                        else:
                            break
    return possiblemoves
def possibleWhiteQueen(a):
    possiblemoves = []
    takeAble = ["p","r","b","q","n","k"]
    coords = [[1,1],[1,-1],[-1,1],[-1,-1],[0,1],[1,0],[0,-1],[-1,0]]
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'Q':
                for coord in range(8):
                    for index in range(1,8):
                        if a[j+coords[coord][0]*index][i+coords[coord][1]*index] == 'O':
                            possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0]*index)+str(i+coords[coord][1]*index))
                        elif a[j+coords[coord][0]*index][i+coords[coord][1]*index] in takeAble:
                            possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0]*index)+str(i+coords[coord][1]*index))
                            break
                        else:
                            break
    return possiblemoves
def possibleWhiteKing(a):
    possiblemoves = []
    takeAble = ["p","r","b","q","n",'k','O']
    coords = [[1,1],[1,-1],[-1,1],[-1,-1],[0,1],[1,0],[0,-1],[-1,0]]
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'K':
                for coord in range(8):
                        if a[j+coords[coord][0]][i+coords[coord][1]] in takeAble:
                            possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0])+str(i+coords[coord][1]))
    return possiblemoves
def possibleBlackKing(a):
    possiblemoves = []
    takeAble = ["P","R","B","Q","N","K","O"]
    coords = [[1,1],[1,-1],[-1,1],[-1,-1],[0,1],[1,0],[0,-1],[-1,0]]
    for i in range(2,10):
        for j in range(2,10):
            if a[j][i] == 'k':
                for coord in range(8):
                    if a[j+coords[coord][0]][i+coords[coord][1]] in takeAble:
                        possiblemoves.append(str(j)+str(i)+str(j+coords[coord][0])+str(i+coords[coord][1]))
    return possiblemoves

def whitePossible(a):
    possiblemoves = []
    possiblemoves+=(possibleWhitePawn(a))
    possiblemoves+=(possibleWhiteRook(a))
    possiblemoves+=(possibleWhiteKnight(a))
    possiblemoves+=(possibleWhiteBishop(a))
    possiblemoves+=(possibleWhiteQueen(a))
    possiblemoves+=(possibleWhiteKing(a))
    return possiblemoves
def BlackPossible(a):
    possiblemoves = []
    possiblemoves+=(possibleBlackPawn(a))
    possiblemoves+=(possibleBlackRook(a))
    possiblemoves+=(possibleBlackKnight(a))
    possiblemoves+=(possibleBlackBishop(a))
    possiblemoves+=(possibleBlackQueen(a))
    possiblemoves+=(possibleBlackKing(a))
    return possiblemoves

def possibleMoves(a,value):
    possiblemoves = []
    if value > 0:
        possiblemoves+=(possibleWhitePawn(a))
        possiblemoves+=(possibleWhiteRook(a))
        possiblemoves+=(possibleWhiteKnight(a))
        possiblemoves+=(possibleWhiteBishop(a))
        possiblemoves+=(possibleWhiteQueen(a))
        possiblemoves+=(possibleWhiteKing(a))
    else:
        possiblemoves+=(possibleBlackPawn(a))
        possiblemoves+=(possibleBlackRook(a))
        possiblemoves+=(possibleBlackKnight(a))
        possiblemoves+=(possibleBlackBishop(a))
        possiblemoves+=(possibleBlackQueen(a))
        possiblemoves+=(possibleBlackKing(a))
    return possiblemoves

def createmoves(board,value):
    king = ['0','K','k']
    moves = possibleMoves(board,value)
    removelist = []
    for i in moves:
        black = possibleMoves(setBoard(i,board),value*-1)
        for j in black:
            if setBoard(i,board)[int(j[2])][int(j[3])] == king[value]:
                removelist.append(i)
    for i in removelist:
        if i in moves:
            moves.remove(i)
    return moves
        
def eventhandler(height,value):
    temp = []
    for i in movelist:
        if i.getHeight() == height-1:
            temp.append(i)
    for i in temp:
        tempmoves = (createmoves(i.getvalboard(),value))
        for j in tempmoves:
            movelist.append(move(j,None,i,height,None,setBoard(j,i.getvalboard())))
            if len(movelist)% wait == 0:
                print(len(movelist))


def minimax():
    templist = []
    for i in movelist:
        if i.getHeight() == 3:
            templist.append(i)
    for i in templist:
        i.seteval(evaluate(i.getvalboard()))
        parent = i.getparent()
        if parent.geteval() == None:
            parent.seteval(i.geteval())
        elif parent.geteval() > i.geteval():
            parent.seteval(i.geteval())
    templist = []
    for i in movelist:
        if i.getHeight() == 2:
            templist.append(i)
    for i in templist:
        i.seteval(evaluate(i.getvalboard()))
        parent = i.getparent()
        if parent.geteval() == None:
            parent.seteval(i.geteval())
        elif parent.geteval() < i.geteval():
            parent.seteval(i.geteval())
    templist = []
    for i in movelist:
        if i.getHeight() == 1:
            templist.append(i)
    for i in templist:
        i.seteval(evaluate(i.getvalboard()))
        parent = i.getparent()
        if parent.geteval() == None:
            parent.seteval(i.geteval())
        elif parent.geteval() > i.geteval():
            parent.seteval(i.geteval())
    templist = []
    for i in movelist:
        if i.getHeight() == 0:
            templist.append(i)
        max = templist[0]
        for i in templist:
            if i.geteval() > max.geteval():
                max = i
    return interpret(max.getMove()),max.geteval()



for i in setboardmovelist:
    board = setBoard(uninterpret(i),board)

a = createmoves(board,1)
for i in a:
    movelist.append(move(i,None,i,0,None,setBoard(i,board)))

print (len(movelist))
eventhandler(1,-1)
print (len(movelist))
eventhandler(2,1)
print (len(movelist))
eventhandler(3,-1)
print (len(movelist))

print(minimax())
