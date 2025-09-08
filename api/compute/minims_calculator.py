'''
A simple calculator that returns words from minims.
'''
import itertools

NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
USE_MEMO = True

def decompile_string(string):
    '''Decompiles the string into the minims calculator format.'''
    separated_list = []
    current_process = ''
    for char in string:
        if current_process == '':
            current_process = char
        elif char in ['|']:
            if '|' in current_process:
                current_process += char
            else:
                separated_list.append(current_process)
                current_process = char
        elif char in NUMBERS:
            if current_process[0] in NUMBERS:
                current_process += char
            else:
                separated_list.append(current_process)
                current_process = char
        elif ('|' in current_process) or (current_process[0] in NUMBERS):
            separated_list.append(current_process)
            current_process = char
        else:
            current_process += char
    if current_process != '':
        separated_list.append(current_process)
    decompiled_list = []
    for substring in separated_list:
        if '|' in substring:
            decompiled_list.append(len(substring))
        elif substring[0] in NUMBERS:
            decompiled_list.append(int(substring))
        else:
            decompiled_list.append(substring)
    return merge_adjacent_ints(decompiled_list)

def merge_adjacent_ints(decompiled_list):
    '''Merges adjacent integers in the decompiled list.'''
    out_list = []
    i = 0
    is_int = False
    running_total = 0
    while i < len(decompiled_list):
        if isinstance(decompiled_list[i], int):
            if is_int:
                running_total += decompiled_list[i]
                i += 1
            else:
                is_int = True
                running_total = decompiled_list[i]
                i += 1
        elif is_int:
            out_list.append(running_total)
            is_int = False
            running_total = 0
            out_list.append(decompiled_list[i])
            i += 1
        else:
            out_list.append(decompiled_list[i])
            i += 1
    if running_total:
        out_list.append(running_total)
    return out_list

def reconstruct_minims(decompiled_list, use_memo = USE_MEMO):
    '''Reconstructs possible words from the decompiled list.'''
    if not isinstance(decompiled_list, list):
        # Add in throwing errors
        return ''
    if not decompiled_list:
        return ''
    possible_words = []
    memo = {}
    for component in decompiled_list:
        if isinstance(component, int):
            if use_memo:
                calc = memo_minim_calculate(component, memo)
                memo = calc["memo"]
                possible_words.append(calc["out"])
            else:
                possible_words.append(recursive_minim_calculate(component))
        elif isinstance(component, str):
            possible_words.append([component])
        else:
            # throw some kind of error
            continue
    return [''.join(word) for word in itertools.product(*possible_words)]

def recursive_minim_calculate(n):
    '''Returns all possible strings made up of n minims.'''
    '''Can be optimised way more with memoization'''
    if not n:
        return ['']
    elif n == 1:
        return ['I']
    elif n == 2:
        return ['II', 'U', 'V', 'N']
    else:
        out_list = ['I' + word for word in recursive_minim_calculate(n - 1)]
        list_minus_two = recursive_minim_calculate(n - 2)
        for letter in ['U', 'V', 'N']:
            out_list += [letter + word for word in list_minus_two]
        list_minus_three = recursive_minim_calculate(n - 3)
        for letter in ['M']:
            out_list += [letter + word for word in list_minus_three]
    return out_list

def memo_minim_calculate(n, memo):
    '''Returns all possible strings made up of n minims using memoization.'''
    if n in memo:
        return {"memo": memo, "out": memo[n]}
    if not n:
        memo[0] = ['']
        return {"memo": memo, "out": ['']}
    elif n == 1:
        memo[1] = ['I']
        return {"memo": memo, "out": ['I']}
    elif n == 2:
        memo[2] = ['II', 'U', 'V', 'N']
        return {"memo": memo, "out": ['II', 'U', 'V', 'N']}
    else:
        # n - 1 should do it, but lets be safe
        for k in range(3):
            if n - 1 - k not in memo:
                new_memo = memo_minim_calculate(n - 1 - k, memo)["memo"]
                for key in new_memo:
                    memo[key] = new_memo[key]
        out_list = ['I' + word for word in memo[n-1]]
        for letter in ['U', 'V', 'N']:
            out_list += [letter + word for word in memo[n-2]]
        for letter in ['M']:
            out_list += [letter + word for word in memo[n-3]]
        memo[n] = out_list
    return {"memo": memo, "out": out_list}

def compute_minims(string):
    '''Main function to compute minims from a string.'''
    decompiled = decompile_string(string)
    words = reconstruct_minims(decompiled, USE_MEMO)
    return words

if __name__ == '__main__':
    in_string = input('Enter a minim string: ')
    decompiled = decompile_string(in_string)
    words = reconstruct_minims(decompiled)
    print(f'Possible words: {words}')
