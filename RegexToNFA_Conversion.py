# Converts input Regular Expression into an e-NFA, then into NFA to test membership of input string.
# Created By: Nick Flouty & Joey Robinson.
import re
import string

state = 0
nfa_stack = []
epsilon_matrix = []
d = {}
Q = 0
postfix = []
temp = []
operator = -10
operand = -20
leftparentheses = -30
rightparentheses = -40
empty = -50

# Deletes the first state that has an output to the passed state.
def remove_state(k1, k1_state):
    size = len(k1)
    i = 0
    while i < size:
        if (k1[i][2] == k1_state):
            del k1[i]
            size -= 1
            break
        i += 1

# Removes states that have an outgoing epsilon edge to a dead state (state with no outgoing edges).
def remove_deadStates(k1):
    size = len(k1)
    i = 0
    while i < size:
        match = 0
        times = 0
        for j in range(len(k1)):
            if(k1[i][2] == k1[j][0]):   #finds a match
                match = 1
                break
        if (match == 0 and k1[i][1] == 'e'):    #did not find a match which means its useless
            remove_state(k1, k1[i][2])
            size -= 1
        i += 1

# Returns True if state is a useless state.
def useless_state(k1, state):
    size = len(k1)
    i = 0
    while i < size:
        match = 0
        times = 0
        for j in range(len(k1)):
            if(k1[i][2] == k1[j][0]):   #finds a match
                match = 1
                break
        if (match == 0 and k1[i][1] == 'e'):    #did not find a match which means its useless
            return(True)
        i+=1

# build_delta recursive helper function.
def build_delta_Recursive_helper(k1, i, accepting):
    e=0
    if(useless_state(k1, k1[i][2]) and (k1[i][2] in accepting)):
        return(i)
    poss_edges = possible_edges(k1, i)
    for w in range(len(poss_edges)):
        e = poss_edges[w]
        if(k1[e][1] == 'e'):
            e = build_delta_Recursive_helper(k1, e, accepting)
            if (Is_Accepting(accepting, k1[e][2])):
                return(e)
    return(e)

# Changes all epsilon moves to a non-epsilon edge.              
def build_delta(k1, accepting):
    delta = []
    for i in range(len(k1)):  
        e = i
        if(k1[i][1] == 'e'):
            e = build_delta_Recursive_helper(k1, i, accepting)
        delta.append([k1[i][0], k1[e][1], k1[e][2]])
    return(delta)

# Recursive helper function for build_accepting()
def build_accepting_Recursive_helper(k1, i, biggest, accepting, j):
    e = 0
    if (useless_state(k1, k1[i][2]) and int(k1[i][2]) == biggest):
        accepting.append(k1[j][0])
        return()
    while(k1[e][0] != k1[i][2]):
        e += 1
    if(int(k1[i][0]) == biggest):
        accepting.append(k1[j][0])
    if(k1[e][1] == 'e'):
        build_accepting_Recursive_helper(k1, e, biggest, accepting, j)

# Builds an array of accepting states.              
def build_accepting(k1, biggest):
    accepting = [str(biggest)]
    for i in range(len(k1)):  
        if(k1[i][1] == 'e'):
           build_accepting_Recursive_helper(k1, i, biggest, accepting, i)
    return(accepting)

# Removes duplicate states.
def remove_duplicates(delta):
    for i in range(len(delta)):
        j = i+1
        while j < len(delta):
            if(delta[i] == delta[j]):
                del delta[j]
                break
            j += 1

# Checks if state is an accepting state.
def Is_Accepting(accepting, state):
    if state in accepting:
        return True
    return False

# Walks through NFA with passed input, and returns the state on after input is read.
def walk_through_nfa(current_state, test_string, nfa, state_changes, i, accepting):
    while i < len(test_string):
            for j in range(len(nfa)):
                if int(nfa[j][0]) == current_state and nfa[j][1] == test_string[i]:
                        poss_moves = possible_moves(nfa, j)
                        for w in range(len(poss_moves)):
                            state_changes[0] += 1
                            current_state = walk_through_nfa(int(nfa[poss_moves[w]][2]), test_string, nfa, state_changes, i+1, accepting)
                            if(Is_Accepting(accepting, current_state)):
                                return(current_state)
            i += 1
    return(current_state)

# Returns the possible moves on an input.
def possible_moves(delta, state):
    poss_moves = []
    for i in range(len(delta)):
        if(delta[state][0] == delta[i][0] and delta[state][1] == delta[i][1]):
            poss_moves.append(i)
    return(poss_moves) 

# Returns the possible connectioned states an epsilong edge can lead to.
def possible_edges(k1, state):
    poss_moves = []
    for i in range(len(k1)):
        if(k1[state][2] == k1[i][0]):
            poss_moves.append(i)
    return(poss_moves) 

# Returns the precedence of each operator.
def precedence(s):
    if s is '(':
        return 0
    elif s is '+':
        return 1
    elif s is '*' or '.':
        return 2
    else:
        return 99

# Returns name of char.
def typeof(s):
    if s is '(':
        return leftparentheses
    elif s is ')':
        return rightparentheses
    elif s is '+' or s is '.' or s is '*':
        return operator
    elif s is ' ':
        return empty   
    else :
        return operand

# Asks user for input RE
def inputExpression():
    infix = input("Enter the infix notation of the Regular Expression : ")
    for i in infix:
        type = typeof(i)
        if type is leftparentheses :
            temp.append(i)
        elif type is rightparentheses :
            next = temp.pop()
            while next is not '(':
                postfix.append(next)
                next = temp.pop()
        elif type is operand:
            postfix.append(i)
        elif type is operator:
            p = precedence(i)
            while len(temp) is not 0 and p <= precedence(temp[-1]) :
                postfix.append(temp.pop())
            temp.append(i)
        elif type is empty:
            continue
                     
    while len(temp) > 0 :
        postfix.append(temp.pop())
   
def or_(v1,v2):
    
    global state
    s = state
    e = s+1
    state = e+1
    
    if isinstance(v1, list)==True and isinstance(v2, list) == True:
        max1_= 0
        min1_= 0
        t1 = []
        t2 = []
        r1 = []
        r = ""

        a = lstOfStrngToLstOfChars(v2)
        b = lstOfStrngToLstOfChars(v1)
        
        t1 = extractIntegersIntoALst(a)
        t2 = extractIntegersIntoALst(b)
        
        start1 = t1[0]
        end1 = t1[len(t1)-1]
        start2 = t2[0]
        end2 = t2[len(t2)-1]

        r = (str)(s) + 'e' + (str)(start1)
        r1.append(r)
        r1.extend(v2)
        t = (str)(end1) + 'e' + (str)(e)
        r1.append(t)
        u = (str)(s) + 'e' + (str)(start2)
        r1.append(u)
        r1.extend(v1)
        v = (str)(end2) + 'e' + (str)(e)
        r1.append(v)
        
        nfa_stack.append(r1)
    elif isinstance(v1, str) == True and isinstance(v2, str) == True:
        max1_= 0
        min1_= 0
        t1 = []
        t2 = []
        r1 = []
        r = ""
        
        a = convertString2List(v2)
        b = convertString2List(v1)
        
        t1 = extractIntegersIntoALst(a)
        t2 = extractIntegersIntoALst(b)
  
        start1 = t1[0]
        end1 = t1[len(t1)-1]
        start2 = t2[0]
        end2 = t2[len(t2)-1]

        r = (str)(s) + 'e' + (str)(start1)
        r1.append(r)
        r1.append(v2)
        t = (str)(end1) + 'e' + (str)(e)
        r1.append(t)
        u = (str)(s) + 'e' + (str)(start2)
        r1.append(u)
        r1.append(v1)
        v = (str)(end2) + 'e' + (str)(e)
        r1.append(v)
        
        nfa_stack.append(r1)
    elif isinstance(v1, str) == True and isinstance(v2, list) == True:
        max1_= 0
        min1_= 0
        t1 = []
        t2 = []
        r1 = []
        r = ""
        
        a = convertString2List(v1)
        b = lstOfStrngToLstOfChars(v2)
        
        t1 = extractIntegersIntoALst(a)
        t2 = extractIntegersIntoALst(b)
        
        start1 = t1[0]
        end1 = t1[len(t1)-1]
        start2 = t2[0]
        end2 = t2[len(t2)-1]
      
        r = (str)(s) + 'e' + (str)(start1)
        r1.append(r)
        
        r1.extend(v2)
        
        t = (str)(end1) + 'e' + (str)(e)
        r1.append(t)
        
        u = (str)(s) + 'e' + (str)(start2)
        r1.append(u)
       
        r1.append(v1)
        
        v = (str)(end2) + 'e' + (str)(e)
        r1.append(v)
      
        nfa_stack.append(r1)
    elif isinstance(v1, list) == True and isinstance(v2, str) == True:
        max1_= 0
        min1_= 0
        t1 = []
        t2 = []
        r1 = []
        r = ""
        
        a = convertString2List(v2)
        b = lstOfStrngToLstOfChars(v1)
        
        t1 = extractIntegersIntoALst(a)
        t2 = extractIntegersIntoALst(b)
        
        start1 = t1[0]
        end1 = t1[len(t1)-1]
        start2 = t2[0]
        end2 = t2[len(t2)-1]
        
        r = (str)(s) + 'e' + (str)(start1)
        r1.append(r)
        r1.append(v2)
        t = (str)(end1) + 'e' + (str)(e)
        r1.append(t)
        u = (str)(s) + 'e' + (str)(start2)
        r1.append(u)
        r1.extend(v1)
        v = (str)(end2) + 'e' + (str)(e)
        r1.append(v)
                          
        nfa_stack.append(r1)
    return

def star_(v1):
    
    global state
    s = state
    e = s+1
    state = e+1
    if(isinstance(v1, str) == True):
        r = ""
        r1 = []
              
        r = (str)(s) + 'e' + (str)(s-2)
        r1.append(r)   
        r1.append(v1)
        u = (str)(e-2) + 'e' + (str)(e)
        r1.append(u)
        s1 = (str)(e) + 'e' + (str)(s-2)
        r1.append(s1)
        t = (str)(s) + 'e' + (str)(e)
        r1.append(t)
        
        nfa_stack.append(r1)
    elif(isinstance(v1, list) == True):
        a = lstOfStrngToLstOfChars(v1)
        t1 = extractIntegersIntoALst(a)
        end = t1[len(t1)-1]
        start = t1[0]
        r = ""
        r1 = []
              
        r = (str)(s) + 'e' + (str)(start)
        r1.append(r)
        r1.extend(v1)
        u = (str)(end) + 'e' + (str)(e)
        r1.append(u)
        t = (str)(e) + 'e' + (str)(start)
        r1.append(t)
        w = (str)(s) + 'e' + (str)(e)
        r1.append(w)

        nfa_stack.append(r1)
    return
    
def concat_(v1, v2):
    
    if isinstance(v1, str) == True and isinstance(v2, str) == True:
        max1_= 0
        min1_= 0
        t1 = []
        t2 = []
        r1 = []
        r = ""
        
        a = convertString2List(v2)
        b = convertString2List(v1)
        
        t1 = extractIntegersIntoALst(a)
        t2 = extractIntegersIntoALst(b)

  
        max1_ = max(t1)
        min1_ = min(t2)
        
        r += (str)(max1_) + 'e' + (str)(min1_)
        r1.append(v2)
        r1.append(r)
        r1.append(v1)
        
        nfa_stack.append(r1)
    elif isinstance(v1, list) == True and isinstance(v2, list) == True:
        max1_= 0
        min1_= 0
        t1 = []
        t2 = []
        r1 = []
        r = ""

        a = lstOfStrngToLstOfChars(v2)
        b = lstOfStrngToLstOfChars(v1)
        
        t1 = extractIntegersIntoALst(a)
        t2 = extractIntegersIntoALst(b)
        
        end = t1[len(t1)-1]
        start = t2[0]
        
        r += (str)(end) + 'e' + (str)(start)
        
        r1.extend(v2)
        r1.append(r)
        r1.extend(v1)
    
        nfa_stack.append(r1)
    elif isinstance(v1, str)==True and isinstance(v2, list)==True:
        max1_= 0
        min1_= 0
        t1 = []
        t2 = []
        r1 = []
        r = ""
        
        a = convertString2List(v1)
        b = lstOfStrngToLstOfChars(v2)
        
        t1 = extractIntegersIntoALst(a)
        t2 = extractIntegersIntoALst(b)
        
        end = t2[len(t2)-1]
        start = t1[0]
        
        r += (str)(end) + 'e' + (str)(start)
        
        v2.append(r)
        v2.append(v1)
                
        nfa_stack.append(v2)
    elif isinstance(v1, list) == True and isinstance(v2, str) == True:
        max1_= 0
        min1_= 0
        t1 = []
        t2 = []
        r1 = []
        r = ""
        
        a = convertString2List(v2)
        b = lstOfStrngToLstOfChars(v1)
        
        t1 = extractIntegersIntoALst(a)
        t2 = extractIntegersIntoALst(b)
        
        end = t1[len(t2)-1]
        start = t2[0]
        
        r += (str)(end) + 'e' + (str)(start)
        
        v1.append(r)
        v1.append(v2)
                
        nfa_stack.append(v1)
        
    return

def extractIntegersIntoALst(v):
    t1 = []
    
    for a1l in v:
            try:
                if(int)(a1l) >= 0 and (int)(a1l) <= 1000:
                    t1.append((int)(a1l))
            except:
                pass
    return t1

def lstOfStrngToLstOfChars(a):
    t = []
    for b in a:
        t.extend(re.split("([^0-9])", b))
    return t

def convertString2List(v):
    a = []
    a.extend(re.split("([^0-9])", v))
    return a    

def main():
    global nfa_stack
    global epsilon_matrix
    global state
    global d, Q
    
    t = []
    k = 0

    inputExpression()
    test_string = input("Enter a test string for the Regular Expression: ")
    
    for i in postfix:
        if (i != '+' and i != '.' and i != '*'):
            t.append(i)
            k += 1
    t = list(set(t))
    t.append('e')


    for i in t:
        d[i] = []

    r = ""
    for i in postfix:

        if i != '+' and i != '.' and i != '*':

            s = state
            e = state+1
                 
            r = (str)(s)+i+str(e)
            state = state+2
            nfa_stack.append(r)            

        elif i == '+':
            if(nfa_stack != []):
                a = nfa_stack.pop()
            else:
                print ("Stack Underflow")
                break
            if(nfa_stack!=[]):
                b = nfa_stack.pop()
            else:
                print ("Stack Underflow")
                break
            or_(a, b)

        elif(i == '.'):
            if(nfa_stack != []):
                a = nfa_stack.pop()
            else:
                print ("Stack Underflow")
                break
            if(nfa_stack != []):
                b = nfa_stack.pop()
            else:
                print ("Stack Underflow")
                break
            concat_(a, b)
        elif(i == '*'):
            if(nfa_stack != []):
                a = nfa_stack.pop()
            else:
                print ("Stack Underflow")
                break
            star_(a)
        else:
            print ("Wrong Input")  

    k1 = []
    for i in nfa_stack:
        for j in i:
            k = j
            k1.append(convertString2List(k))

    for i in nfa_stack:
        a = lstOfStrngToLstOfChars(i)
    b = extractIntegersIntoALst(a)

    filler = []
    biggest = 0 # biggest is the accepting state.
    for i in range(len(k1)):
        if (int(k1[i][2]) > biggest):
            biggest = int(k1[i][2])

    accepting = build_accepting(k1, biggest)
    new_delta = build_delta(k1, accepting)
    remove_duplicates(new_delta)

    accepting = extractIntegersIntoALst(accepting)
    current_state = b[0]
    state_changes = [0]
    if (len(test_string) == 0):
        if(Is_Accepting(accepting, current_state)):
            print('This String is Accepted')
    else:
        current_state = walk_through_nfa(current_state, test_string, new_delta, state_changes, 0, accepting)

    if state_changes[0] > 0:
        if (Is_Accepting(accepting, current_state)):
            print('This string is Accepted')
        else:
            print('This string is Not Accepted')


    
if __name__ == "__main__":
    main()