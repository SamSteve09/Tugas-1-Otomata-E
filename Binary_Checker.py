#q0 = start state, q1 = 0, q2 = 1, q3 = 01, q4 = 010, q5 = 0100, q6 = 01001
#DFA with backtracking
def is_valid(s, current_state):
    states = {'q0': {'0': 'q1', '1': 'q2'},
              'q1': {'0': 'q0', '1': 'q3'},
              'q2': {'0': 'q0'},
              'q3': {'0': 'q4'},
              'q4': {'0': 'q5', '1': 'q2'},
              'q5': {'0': 'q0', '1': 'q6'},
              'q6': {'0': 'q1', '1': 'q2'}}
    accept_states = ['q0','q4','q6']
    checkpoint = []
    i = 0
    # less than 2 because the default is q0, if s is empty, s could be misattributed as valid even though lambda is not included in S
    # minimum correct is 00 (2 char), current state q0 so that it doesn't flag the recursion which starts with q4 as false
    # in the case where there is less than 2 char left (010010) which only have 0 char left but is actually valid (010 + 010)
    if len(s) < 2 and current_state == 'q0':
        return False
    while i < len(s):
        c = s[i]
        # backtracking to oldest checkpoint with q4 if with q6 is not valid (010010 instead of 01001)
        if c not in states[current_state]:
            if checkpoint and (c == '0' or c =='1'):
                current_state = 'q4'
                i = checkpoint.pop(0)+1
                continue  
            else:
                return False
        current_state = states[current_state][c]
        # each time the pattern 010010 is encountered, create a checkpoint at the last 0, continue using q6 (01001) first
        # if using q6 results to failure, will try using 2 q4 (010 + 010) next
        if current_state == 'q6' and (i + 1) < len(s) and s[i + 1] == '0':
            checkpoint.append(i+1)
            #print("checkpoint added at",  i+1)
        i += 1
    if current_state not in accept_states:
        if checkpoint:
            new_start = s[checkpoint.pop(0)+1:]
            return is_valid(new_start, 'q4')
        return False
    
    return current_state in accept_states
def print_status(s):
    print('Bit string:', s)
    if is_valid(s, 'q0'):
        print('Given bit string is valid.')
    else:
        print('Given bit string is invalid.')
# Test cases:
# valid without backtracking
#s = '01001000000010010010010' # True (01001 + 00 + 00 + 00 + 01001 + 00 + 010)
# valid with backtracking
#s = '010010' # True (010 + 010)
s = '0100100000000100100100100' # True (010 + 010 + 00 + 00 + 00 + 010 + 010 + 010100 + 00)
# invalid
#s = '01001000000001001001001100' # False (010 + 010 + 00 + 00 + 00 + 010 + 010 + 010100 + 00)
# obviously invalid (incorrect syntax)
#s = '010010010Z0010010'
# invalid (less than 2 char)
#s = '010010'
print_status(s)

    