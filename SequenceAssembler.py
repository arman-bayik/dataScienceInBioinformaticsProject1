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


def align_fragments(s1, s2, match_penalty, replace_penalty, indel_penalty):
    # m: 0-m are the column indexes
    # n: 0-n are the row indexes
    n = len(s1)
    m = len(s2)

    max_i = 0
    max_j = 0

    # Scenario 1 prefix is the left sequence and the top sequence is the suffix
    scenario_1 = False
    # Scenario 2 prefix is the top sequence and the left sequence is the suffix
    scenario_2 = False

    # The DP Matrix v which helps store and compute alignment score
    # v is an n x m matrix
    v = np.zeros((n + 1, m + 1))

    # backtrack is a matrix that stores the traceback path
    backtrack = np.zeros((n + 1, m + 1))

    # This is the maximum score in the Matrix. We start traceback from here
    max_score = 0

    # Calculates score
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            insert_score = v[i][j - 1] + indel_penalty
            delete_score = v[i - 1][j] + indel_penalty
            if s1[i - 1] == s2[j - 1]:
                match_score = v[i - 1][j - 1] + match_penalty
            else:
                match_score = v[i - 1][j - 1] + replace_penalty
            v[i][j] = max(insert_score, delete_score, match_score)

            # if the score at v(i,j) is the same as the match score then we backtrack diagonally
            if v[i][j] == match_score:
                backtrack[i][j] = 1
            # if the score at v(i,j) is the same as the insert score then we backtrack to the left
            if v[i][j] == insert_score:
                backtrack[i][j] = 2
            # if the score at v(i,j) is the same as the delete score then we backtrack upwards
            if v[i][j] == delete_score:
                backtrack[i][j] = 3
            # if the score at v(i,j) is zero then we have finished backtracking
            if v[i][j] == 0:
                backtrack[i][j] = 0

            if v[i][j] >= max_score:
                max_i = i
                max_j = j
                max_score = v[i][j]
    # Stores the aligned versions of the sequences
    aligned_one = []
    aligned_two = []
    contig = ""
    prefix = []
    suffix = []

    # Allows us to start from the backtracking path's beginning
    i = max_i
    j = max_j

    # INFINITE LOOP WHEN THERE ARE 2 BACKTRACKS THAT EQUAL 4
    while backtrack[i][j] != 0:
        # If we backtracked diagonally from this index
        if backtrack[i][j] == 1:
            # aligned_one.append(s1[i - 1])
            # aligned_two.append(s2[j - 1])
            i -= 1
            j -= 1
        # If we backtracked diagonally from this index
        elif backtrack[i][j] == 2:
            # aligned_one.append('-')
            # aligned_two.append(s2[j - 1])
            j -= 1
        elif backtrack[i][j] == 3:
            # aligned_one.append(s1[i - 1])
            # aligned_two.append('-')
            i -= 1
    if max_i == n:
        scenario_1 = True
    else:
        scenario_2 = True

    if scenario_1:
        prefix.append(s1[0:i])
        suffix.append(s2)
        for element in prefix:
            contig += element
        for element in suffix:
            contig += element

    if scenario_2:
        prefix.append(s2[0:j])
        suffix.append(s1)
        for element in prefix:
            contig += element
        for element in suffix:
            contig += element

    # aligned_one.reverse()
    # aligned_two.reverse()
    # print(aligned_one)
    # print(aligned_two)

    return contig, max_score


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
    # Read in the sequence fragments and assembling them based off of their alignment score.
    try:
        input_file = open(i, "r")
    except FileNotFoundError:
        print("Error: specified input file, '" + i + "', does not exist.")
        sys.exit(1)

    # Place the fragments in the list
    sequence_fragments = []
    for fragment in input_file:
        fragment = fragment[0:len(fragment) - 1]
        if fragment != '>':
            sequence_fragments.append(fragment)

    # Compute Alignment Score
    # alignment_result = align_fragments('ede', 'sed', s, r, d)
    # contig = alignment_result[0]
    # alignment_score = alignment_result[1]
    # print(contig)
    # print(alignment_score)

    # Build 2D scoring matrix to calculate maximum score between all fragment combinations
    scoring_matrix = np.full((len(sequence_fragments), len(sequence_fragments)), None)

    stop_flag = False
    while not stop_flag:

        # Populate upper triangle with results of all fragment alignment combinations
        for j in range(0, (len(sequence_fragments) - 1), 1):
            for k in range(j+1, len(sequence_fragments), 1):
                scoring_matrix[j][k] = align_fragments(sequence_fragments[j], sequence_fragments[k], s, r, d)
                print("[" + str(scoring_matrix[j][k][0]) + "," + str(scoring_matrix[j][k][1]) + "]")

        # Find the fragment with the highest score
        max_score = -sys.maxsize
        max_score_index_j = -1
        max_score_index_k = -1
        for j in range(0, len(scoring_matrix) - 1, 1):
            for k in range(j+1, len(scoring_matrix[j + 1]), 1):
                score = scoring_matrix[j][k][1]
                if score > max_score:
                    max_score = score
                    max_score_index_j = -1
                    max_score_index_k = -1
    # Write score to output file
    # output_file = open(o, "w")
    # output_file.write(str(score))

    # Close all files
    # output_file.close()
    input_file.close()
    print("Program run completed successfully.")

    return 0


if __name__ == '__main__':
    main()
