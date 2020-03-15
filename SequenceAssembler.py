# Simulates Shotgun Sequencing
# inputs:
#      string i: input file name
#      integer: s = score for match (positive integer)
#      integer: r = penalty for replace(negative integer)
#      integer: d = penalty for delete/insert(negative integer)
#      string o: output file name

# Sample call: python sequenceAssembler.py "input.txt" 5 -2 2  "output.txt"

import sys
import numpy as np
import random


def align_fragments(seq1, seq2, match_penalty, replace_penalty, indel_penalty):
    # m: 0-m are the column indexes
    # n: 0-n are the row indexes
    n = len(seq1)
    m = len(seq2)

    # The DP Matrix V which helps store and compute alignment score
    # V is an n x m matrix
    V = np.zeros((n + 1, m + 1))

    # backtrack is a matrix that stores the traceback path
    backtrack = np.zeros((n + 1, m + 1))

    # This is the maximum score in the Matrix. We start traceback from here
    max_score = 0

    # Calculates score
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            insert_score = V[i][j - 1] + indel_penalty
            delete_score = V[i - 1][j] + indel_penalty
            if seq1[i - 1] == seq2[j - 1]:
                match_score = V[i - 1][j - 1] + match_penalty
            else:
                match_score = V[i - 1][j - 1] + replace_penalty
            V[i][j] = max(insert_score, delete_score, match_score)

            # if the score at V(i,j) is the same as the match score then we backtrack diagonally
            if V[i][j] == match_score:
                backtrack[i][j] = 1
            # if the score at V(i,j) is the same as the insert score then we backtrack to the left
            if V[i][j] == insert_score:
                backtrack[i][j] = 2
            # if the score at V(i,j) is the same as the delete score then we backtrack upwards
            if V[i][j] == delete_score:
                backtrack[i][j] = 3
            # if the score at V(i,j) is zero then we have finished backtracking
            if V[i][j] == 0:
                backtrack[i][j] = 4

            if V[i][j] >= max_score:
                max_i = i
                max_j = j
                max_score = V[i][j]

    # Stores the aligned versions of the sequences
    aligned_one = []
    aligned_two = []

    # Allows us to start from the backtracking path's beginning
    i = max_i
    j = max_j

    while backtrack[i][j] != 0:
        # If we backtracked diagonally from this index
        if backtrack[i][j] == 1:
            aligned_one = aligned_one.append(seq1[i-1])
            aligned_two = aligned_two.append(seq2[j-1])
            i -= 1
            j -= 1
        # If we backtracked diagonally from this index
        elif backtrack[i][j] == 2:
            aligned_one = aligned_one.append('-')
            aligned_two = aligned_two.append(seq2[j-1])
            j -= 1
        elif backtrack[i][j] == 3:
            aligned_one = aligned_one.append(seq1[i-1])
            aligned_two = aligned_two.append('-')
            i -= 1



    return max_score


def main():
    # -------------------INPUT VERIFICATION AND RECORDING-------------------
    if len(sys.argv) < 6:  # Verifying there aren't too few inputs
        print("Error: Too few inputs.\n")
        print("Inputs should be in the form of [run program] \"i\" s r d \"o\"")
        sys.exit(1)
    if len(sys.argv) > 6:  # Verifying there aren't too many inputs
        print("Error: Too many inputs.\n")
        print("Inputs should be in the form of [run program] \"i\" s r d \"o\"")
        sys.exit(1)
    try:  # Verifying input of i is correct and storing it in variable i
        i = str(sys.argv[1])
    except ValueError:
        print("Error: input for 'i' must be of type string.")
        sys.exit(1)
    try:  # Verifying input of s is correct and storing it in variable s
        s = int(sys.argv[2])
    except ValueError:
        print("Error: input for 's' must be of type int.")
        sys.exit(1)
    try:  # Verifying input of r is correct and storing it in variable r
        r = int(sys.argv[3])
    except ValueError:
        print("Error: input for 'r' must be of type int.")
        sys.exit(1)
    try:  # Verifying input of d is correct and storing it in variable d
        d = int(sys.argv[4])
    except ValueError:
        print("Error: input for 'd' must be of type int.")
        sys.exit(1)
    try:  # Verifying input of o is correct and storing it in variable o
        o = str(sys.argv[5])
    except ValueError:
        print("Error: input for 'o' must be of type string.")
        sys.exit(1)

    #  -------------------CREATE A FASTA FILE WITH REASSEMBLED SEQUENCE-------------------
    # Read in the sequence fragments and assembling them based off of their aligment score.
    try:
        input_file = open(i, "r")
    except FileNotFoundError:
        print("Error: specified input file, '" + i + "', does not exist.")
        sys.exit(1)

    # Place the fragments in the list
    sequenceFragments = []
    for fragment in input_file:
        fragment = fragment[0:len(fragment) - 1]
        if fragment != '>':
            sequenceFragments.append(fragment)

    # Compute Alignment Score
    score = calculate_score('GTTACTGT', 'ACTGTTA', s, r, d)
    print(score)

    # Write score to output file
    output_file = open(o, "w")
    output_file.write(str(score))

    # Close all files
    output_file.close()
    input_file.close()
    print("Program run completed successfully.")

    return 0


if __name__ == '__main__':
    main()
