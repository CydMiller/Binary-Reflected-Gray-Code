'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Filename: main.py
    Author: Cydney Miller
    Date Created: 11/22/2025
    Date Updated: 11/27/2025
    Purpose: Driver for Binary Reflected Gray Code educational tool. 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import os
import time
import re

# Define global color variables used throughout program
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
ORANGE = "\033[93m"
END = "\033[0m"

def main():
    # Print welcome message and purpose of program
    print("\nWelcome to the Binary Reflected Gray Code Visualizer!")
    print("\nThis program will briefly describe the purpose and applications of Binary")
    print("Relflected Gray Code (BRGC), then provide a demonstration of generating such codes.\n")
    os.system('pause')
    print("---------------------------------------------------------------------------------------------")

    # Print overview
    print_overview()
    os.system('pause')
    print("---------------------------------------------------------------------------------------------")

    # Print applications
    print_applications()
    os.system('pause')
    print("---------------------------------------------------------------------------------------------")

    # Demonstration
    demonstration()
    print("---------------------------------------------------------------------------------------------\n")

def print_overview():
    print("\nBinary Reflected Gray Code (BRGC) is a special sequence of binary numbers")
    print("where each successive number differs from the previous one by exactly one bit.\n")

def print_applications():
    print("\nApplications:")
    print("\n- Rotary and Digital Encoders: ")
    print("\t  Minimizes reading errors by changing only one bit at a time as positions change.")
    print("\n- Analog-to-Digital Conversion (ADC): ")
    print("\t  Reduces glitches when converting continuous signals to digital.")
    print("\n- Finite State Machines (FSMs):")
    print("\t  Lowers switching errors and power use in sequential circuits.")
    print("\n- Error Detection in Communication:")
    print("\t  Makes single-bit errors easier to detect and manage.\n")

def demonstration():
    print_procedure()
    os.system('pause')
    print("---------------------------------------------------------------------------------------------")
    print("\nLet's generate Gray code step-by-step!")
    while True:
        user_input = input("\nEnter the number of bits for Gray code: ")
        try:
            n = int(user_input)
            if n < 0:
                print("\nNumber of bits must be a positive integer.")
            elif n > 5:
                print("\nRecursion tree will be too long, please choose a number below 6.")
            else:
                break
        except ValueError:
            print("\nPlease input an integer.")
    print("\nRecursive call tree and steps:")
    gray_codes = generate_gray_code(n)
    print(f"\nFinal Gray code for {n} bits:")
    print("[" + ", ".join([f"'{code}'" for code in gray_codes]) + "]")
    print()
    os.system('pause')
    print("---------------------------------------------------------------------------------------------")
    print("\nYou can see that each successive code differs by exactly")
    print("one bit, including the final code and first code:")
    print()
    visualize_bit_changes_animated(gray_codes)
    print(f"\nThus we have successfully created Binary Reflected Gray Code for {n} bits!")

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''    
    Funciton: print_procedure()
    Purpose: Used in demonstration() to print the procedure 
             we will be following in plain english
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def print_procedure():
    print("\nIn this demonstration we will be using a recursive implementation of BRGC generation.")
    print("\nThe procedure is as follows:")
    print("\t1. Start with a single bit Gray code (base case): [\"0\", \"1\"].")
    print("\t2. For each subsequent bit:")
    print("\t\t- Reflect the current list (reverse it).")
    print("\t\t- Prefix the original list with 0 and the reflected list with 1.")
    print("\t3. Repeat until you reach the desired number of bits (recursive step).\n")

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''    
    Funcitons: print_node(), print_node_inline(), delayed_symbol()
    Purpose: Helper functions used in generate_gray_codes() to 
             create clear visuals to trace recursion tree in 
             generating gray codes.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def print_node(prefix, last, text):
    branch = "└── " if last else "├── "
    print(prefix + branch + text)
    return prefix + ("    " if last else "│   ")

def print_node_inline(prefix, last, text):
    branch = "└── " if last else "├── "
    print(prefix + branch + text, end="", flush=True)
    return prefix + ("    " if last else "│   ")

def delayed_symbol(condition):
    # This prints a green ✓ or a red ✕ with a short visual delay
    time.sleep(1)
    print(f" {GREEN}✓{END}" if condition else f" {RED}✕{END}")


def generate_gray_code(n, prefix="", last=True):
    # High-level explanation:
    # Gray code ensures only ONE bit changes between successive numbers. The recursive
    # construction mirrors the previous list (BRGC), prefixing 0s to the original and 1s
    # to the reversed copy. This guarantees minimal bit flips.

    new_prefix = print_node(prefix, last, f"generate_gray_code({n})")

    # --- Base Case: n == 0 ---
    check_prefix = print_node_inline(new_prefix, False, "Check if n == 0 ")
    delayed_symbol(n == 0)
    if n == 0:
        print(f"{new_prefix}" + "├── " + "Return ['0']")
        return ["0"]

    # --- Base Case: n == 1 ---
    check_prefix = print_node_inline(new_prefix, False, "Check if n == 1 ")
    delayed_symbol(n == 1)
    if n == 1:
        print(f"{new_prefix}" + "├── " + "Return ['0', '1']")
        return ["0", "1"]

    # --- Recursive Case ---
    next_prefix = print_node(new_prefix, False, f"Recursing on n-1 = {n-1}")
    smaller = generate_gray_code(n-1, next_prefix, True)


    # --- Construct Gray codes ---

    # Prefixing "0" keeps the first half in order.
    original = [f"{BLUE}0{END}" + x for x in smaller]

    # Prefixing "1" to the *reversed* list ensures the bit-flip adjacency is preserved,
    # connecting last of original and first of reflected with exactly one bit change.
    reflected = [f"{ORANGE}1{END}" + x for x in reversed(smaller)]

    reflect_prefix = print_node(new_prefix, True, "Reflect and prefix results:")
    print_node(reflect_prefix, False, f"Original ({BLUE}prefix 0{END}):  ['" + "', '".join(original) + "']")
    print_node(reflect_prefix, False, f"Reflected ({ORANGE}prefix 1{END}): ['" + "', '".join(reflected) + "']")

    return original + reflected

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''    
    Funciton: strip_ansi_codes_list()
    Purpose: Helper function used in visualize_bit_changes_animated()
             to strip ANSI codes from a list of strings.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def strip_ansi_codes_list(code_list):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return [ansi_escape.sub('', str(code)) for code in code_list]

def visualize_bit_changes_animated(gray_codes, delay=0.8):
    plain_codes = strip_ansi_codes_list(gray_codes)
    n = len(plain_codes)
    # Prepare all highlight steps as before
    steps = []
    # Initial line (no coloring)
    steps.append(["'" + code + "'" for code in plain_codes])
    # Highlight changed bits for each transition
    for i in range(1, n):
        prev = plain_codes[i-1]
        curr = plain_codes[i]
        changed_indices = [j for j in range(len(prev)) if prev[j] != curr[j]]
        for idx in changed_indices:
            highlighted = []
            for k, code in enumerate(plain_codes):
                code_chars = list(code)
                if k == i or k == i-1:
                    code_chars[idx] = f"{RED}{code_chars[idx]}{END}"
                highlighted.append("'" + "".join(code_chars) + "'")
            steps.append(highlighted)
    # Final wrap-around step
    first = plain_codes[0]
    last = plain_codes[-1]
    wrap_indices = [j for j in range(len(first)) if first[j] != last[j]]
    for idx in wrap_indices:
        highlighted = []
        for k, code in enumerate(plain_codes):
            code_chars = list(code)
            if k == 0 or k == n-1:
                code_chars[idx] = f"{RED}{code_chars[idx]}{END}"
            highlighted.append("'" + "".join(code_chars) + "'")
        steps.append(highlighted)
    # Animate by updating the same line
    import sys
    for _ in range(2):
        for step in steps:
            sys.stdout.write("\r[" + ", ".join(step) + "]")
            sys.stdout.flush()
            time.sleep(delay)
        #time.sleep(delay)
    print()  # Move to next line after animation

if __name__ == "__main__":
    main()