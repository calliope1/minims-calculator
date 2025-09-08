"""
A simple calculator that returns words from minims.
"""
import itertools
import json
import os

NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
USE_MEMO = True

def decompile_string(string: str) -> list[str | int]:
    """Decompiles the string into the minims calculator format.

    Parameters
    ----------
    string : str
        Minim string to be computed.

    Returns
    -------
    list[str | int]
        Processed list of strings and integers.
    """

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

def merge_adjacent_ints(decompiled_list : list) -> list:
    """Merges adjacent integers in the decompiled list.

    For example, ['a', 3, 4, ['b', 'c']] -> ['a', 7, ['b', 'c']].
    
    Parameters
    ----------
    decompiled_list : list

    Returns
    -------
    list[int | str]
    """

    if not isinstance(decompiled_list, list):
        # TODO: Throw an error
        return []
    out_list = []
    i = 0
    is_int = False
    running_total = 0
    while i < len(decompiled_list):
        if isinstance(decompiled_list[i], int):
            if is_int:
                running_total += decompiled_list[i]
            else:
                is_int = True
                running_total = decompiled_list[i]
        elif is_int:
            out_list.append(running_total)
            is_int = False
            running_total = 0
            out_list.append(decompiled_list[i])
        else:
            out_list.append(decompiled_list[i])
        i += 1
    if running_total:
        out_list.append(running_total)
    return out_list

def reconstruct_minims(decompiled_list : list[int | str], use_memo : bool = USE_MEMO) -> list[str]:
    """Reconstructs possible words from the decompiled list.

    Currently if there are non-int, non-str elements of decompiled_list then these are ignored.

    Parameters
    ----------
    decompiled_list : list[str | int]
        List specifying the minims and known letters of the word.
    use_memo : bool
        Specifies if we use the memoized algorithm.

    Returns
    -------
    list[str]
        All possible words.
    """

    if not isinstance(decompiled_list, list):
        # TODO: Throw an error
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
            # TODO: Throw error
            continue
    return [''.join(word) for word in itertools.product(*possible_words)]

def file_reconstruct_minims(decompiled_list : list[int | str], path : str, max_n : int) -> list[str]:
    """Reconstructs possible words from the decompiled list, saving some memory to file.

    Currently if there are non-int, non-str elements of decompiled_list then these are ignored.

    Parameters
    ----------
    decompiled_list : list[str | int]
        List specifying the minims and known letters of the word.
    path : str
        Path to files to save
    max_n : int
        Maximum n to be saved

    Returns
    -------
    list[str]
        All possible words.
    """

    if not isinstance(decompiled_list, list):
        # TODO: Throw an error
        return ''
    if not decompiled_list:
        return ''
    possible_words = []
    memo = {}
    for component in decompiled_list:
        if isinstance(component, int):
            possible_words.append(file_minims_calculate(component, path, max_n))
        elif isinstance(component, str):
            possible_words.append([component])
        else:
            # TODO: Throw error
            continue
    return [''.join(word) for word in itertools.product(*possible_words)]


def recursive_minim_calculate(n : int) -> list[str]:
    """Returns all possible strings made up of n minims without memoization."""
    
    if not n:
        return ['']
    elif n == 1:
        return ['I']
    elif n == 2:
        return ['II', 'U', 'V', 'N']

    out_list = ['I' + word for word in recursive_minim_calculate(n - 1)]
    
    list_minus_two = recursive_minim_calculate(n - 2)
    for letter in ['U', 'V', 'N']:
        out_list += [letter + word for word in list_minus_two]
    
    out_list += ['M' + word for word in recursive_minim_calculate(n - 3)]
    
    return out_list

def memo_minim_calculate(n : int, memo : dict[int, list[str]]):
    """Returns all possible strings made up of n minims using memoization.
    
    Parameters
    ----------
    n : int
        Number of minims.
    memo : dict[int, list[str]]
        Prior calculations.
        You MUST have that memo[n] is all possible strings made up of n minims, otherwise the result may be incorrect.

    Returns
    -------
    {"memo": memo, "out": out_list}
        memo : dict[int, list[str]
            All calculations in input memo plus any new calculations.
        out_list : list[str]
            All strings made up of n minims.
    """
    
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
    # Just n - 1 would be sufficient, but lets be safe
    for k in range(3):
        if n - 1 - k not in memo:
            new_memo = memo_minim_calculate(n - 1 - k, memo)["memo"]
            for key in new_memo:
                memo[key] = new_memo[key]
    out_list = ['I' + word for word in memo[n-1]]
    for letter in ['U', 'V', 'N']:
        out_list += [letter + word for word in memo[n-2]]
    out_list += ['M' + word for word in memo[n-3]]
    memo[n] = out_list
    return {"memo": memo, "out": out_list}

def file_minims_calculate(n : int, path : str, max_n : int) -> list[str]:
    """Returns all strings made of n minims, looking at files in path.

    If path/minims-<n>.json exists then this reads that file and parses it as a list of strings.
    Returns that list if successful.
    If path/minims-<n>.json is does not exist or is malformed it computes all strings of n minims manually,
    using other files in path.

    If path/minims-<n>.json is malformed then it will be overwritten.

    Parameters
    ----------
    n : int
        Number of minims.
    path : str
        Path to the JSON files.
    max_n : int
        Largest n that this function will allow to save to file.

    Returns
    -------
    list[str]
        All strings made up of n minims.
    """

    if not isinstance(n, int):
        # TODO: Throw error
        print(f"Expected int for 'n' variable ({n}).")
        return []

    file_path = f"{path}//minims-{str(n)}.json"
    out_list = []
    # Check if path/minims-<n>.json exists
    if os.path.exists(file_path):
        manual_required = False
        # Read the file to see if it is well-formed
        with open(file_path, 'r') as f:
            data = json.load(f)

        for item in data:
            if not isinstance(item, str):
                manual_required = True
                break
            out_list.append(item)
        if not manual_required:
            return out_list
    if n == 0:
        out_list = ['']
    elif n == 1:
        out_list = ['I']
    elif n == 2:
        out_list = ['II', 'N', 'U', 'V']
    else:
        out_list = ['I' + word for word in file_minims_calculate(n - 1, path, max_n)]
        for letter in ['U', 'V', 'N']:
            out_list += [letter + word for word in file_minims_calculate(n - 2, path, max_n)]
        out_list += ['M' + word for word in file_minims_calculate(n - 3, path, max_n)]
    if n <= max_n:
        with open(file_path, 'w') as f:
            json.dump(out_list, f, indent = 2)
    return out_list

def compute_minims(string : str) -> list[str]:
    """Compute all possible words from the minims string.
    
    Parameters
    ----------
    string : str
        Minim string to be computed

    Returns
    -------
    list[str]
        All strings that produce the input minim string
    """
    
    decompiled = decompile_string(string)
    words = reconstruct_minims(decompiled, USE_MEMO)
    return words

def file_compute_minims(expression : str, path : str, max_n : int):
    """Compute all possible words from the minims string.

    Saves computed minim combinations up to at most n.
    
    Parameters
    ----------
    string : str
        Minim string to be computed
    path : str
        Path to JSON data files being saved
    max_n : int
        Maximum n for which minims-n.json will be saved

    Returns
    -------
    list[str]
        All strings that produce the input minim string
    """

    if max_n > 10:
        print(f"max_n is set to {max_n}, are you sure you want to continue? This may take a lot of space.")
        verify = "invalid_string"
        while verify.lower() not in ["yes", "y", "no", "n", ""]:
            verify = input("Response [Y]es/[N]o (default: No): ")
            if verify.lower() in ["", "no", "n"]:
                print("Ending computation, returning empty list.")
                return []
        print("Continuing calculation")
        
    
    decompiled = decompile_string(expression)
    words = file_reconstruct_minims(decompiled, path, max_n)
    return words

if __name__ == '__main__':
    expression = str(input('Enter a minim string: '))
    words = file_compute_minims(expression, '..//data', 20)
    print(f'First 10,000 words: {words[:min(10000, len(words))]}')
    print(f'There were {len(words)} many')