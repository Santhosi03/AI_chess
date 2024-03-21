import random
from gym_chess import ChessEnvV2

env = ChessEnvV2() # or ChessEnvV2

# current state
state = env.state

# select a move and convert it into an action
moves = env.get_possible_moves(state=state, player="WHITE", attack=False)

#nodes of game tree
#one more variable should be added,minimax value and minimax path
class state_D():

    def __init__(self, state,is_max):
        self.is_over=check_gameover_S(state)
        self.state = state
        self.children = []
        self.minimax= None
        self.is_max= is_max

    def add_children(self, children):
        self.children= children


#fuction call to check if game is over
#should be changed
def check_gameover_S(state):
    n = len(state)
    #ROW CHECK
    ret1, ret2 = row_check_S(state)
    if ret1==n:
        return 1
    if ret2==n:
        return -1
    #Column Check
    ret1, ret2 = column_check_S(state)
    if ret1==n:
        return 1
    if ret2==n:
        return -1
    #Diagonal Check
    ret1, ret2 = diagonal_check_S(state)
    if ret1==n:
        return 1
    if ret2==n:
        return -1
    return 0

#symbols should be changed
#Instead of manually calculating moves, gen_moves should be called.Player=WHITE/BLACK can be called
#moves = env.get_possible_moves(state=state, player="WHITE", attack=False)
#instead of min and max, black and white should be given
#max=p1=WHITE,min=p2=BLACK   
#s_map[state]=node, in TTT state was a 2d array, so we had tuple and store it.Now state is just a dictionary, we can directly map it     
def next_states_S(pres_state, is_max):
    next_states=[]
    n=len(pres_state)
    symbol=empty_symbol
    if is_max:
        symbol=p1
    else:
        symbol=p2
    children_player = not is_max
    for i in range(n):
        for j in range(n):
            if pres_state[i][j]==empty_symbol:
                pres_state[i][j]=symbol
                # print(pres_state)
                dup = copy.deepcopy(pres_state)
                dup_tup = tuple_it_D(dup)
                if dup_tup in s_map:
                    global counte
                    counte+=1
                    # print(1)
                    next_states.append(s_map[dup_tup])
                else:
                    child=  state_D(dup, children_player)
                    s_map[dup_tup] = child
                    next_states.append(child)
                # print(" after: ", pres_state)
                pres_state[i][j]=empty_symbol
    return next_states


#dont think any changes need to be made
def build_tree_D(root,depth):
    n = len(root.state)
    q = [root]
    cur_depth = 0
    keep_going = True
    is_max = root.is_max
    while(cur_depth < depth and keep_going):
        size=len(q)
        # print("Size of queue: ", size,"    Is p1:", is_max,"    Current Depth: ",  cur_depth)
        keep_going = False
        for i in range(size):
            node=q[0]
            q.pop(0)
            # print("start " , node.state)
            if node.is_over==0:
                keep_going = True
                children = next_states_S(node.state, is_max)
                node.add_children(children)
                for child in children:
                    # print(child.state, child.is_max)
                    q.append(child)
        cur_depth+=1
        is_max = not is_max
    return root


#should set the minimax values and return the minimax paths
#instead of static_eval_fn , reward should be used
#instead of is_over, minimax value should be used
def K_depth_S(root,depth,k):
    if len(root.children)==0: 
        # root.minimax = root.is_over ##We have changed the meaning of minimax, now it represents the path
        # print(root.state, root.is_over)
        # if(root.is_over==-1):
        #     print(root.is_over)
        return root
    if depth==k:
        max1, max2 = static_eval_fn_D(root.state)
        root.is_over = eval_D(root.is_max,max1,max2,len(root.state))
        return root
    mini=root.children[0]
    maxi=root.children[0]
    for child in root.children:
        v = K_depth_S(child,depth+1, k)
        # print(type(v))
        if(mini.is_over > v.is_over):
            mini = v
        if(maxi.is_over < v.is_over):
            maxi = v
    if root.is_max:
        root.minimax=maxi
        root.is_over = maxi.is_over
        # print(root.state, root.minimax, p1)
        return root
    root.minimax=mini
    root.is_over = mini.is_over
    # print(root.state, root.minimax, p2)
    return root

def tuple_it_D(state):
    return tuple(map(tuple, state))

def get_random_move_D(state):
    moves = env.get_possible_moves(state=state)
    move = random.choice(moves)


#instead of x,y , move should be passed
def make_node(x,y,pres_node):
    pres_state = pres_node.state
    dup = copy.deepcopy(pres_state)
    symbol = empty_symbol
    if pres_node.is_max:
        symbol = p1
    else:
        symbol = p2
    dup[x][y] = symbol
    dup_tup = tuple_it_D(dup)
    if dup_tup in s_map:
        global counte
        counte+=1
    else:
        child=  state_D(dup, not pres_node.is_max)
        s_map[dup_tup] = child
    return s_map[dup_tup]