# Simulates DNA sequence partitioning
# Inputs:
#      string i: input file name
#      int x : minimum fragment length
#      int y : maximum fragment length
#      string o : output file name

# Sample call: python sequencePartitioner.py "input.txt" 6 20 "output.txt"
#                                                i       x y       o

import sys
import random


def main():
    #  -------------------INPUT VERIFICATION AND RECORDING-------------------
    if len(sys.argv) < 5:  # Verifying there aren't too few inputs
        print("Error: Too few inputs.\n")
        print("Inputs should be in the form of [run program] n a c g t k p \"o\"")
        sys.exit(1)
    if len(sys.argv) > 5:  # Verifying there aren't too many inputs
        print("Error: Too many inputs.\n")
        print("Inputs should be in the form of [run program] n a c g t k p \"o\"")
        sys.exit(1)
    try:  # Verifying input of i is correct and storing it in variable i
        i = str(sys.argv[1])
    except ValueError:
        print("Error: input for 'i' must be of type string.")
        sys.exit(1)
    try:  # Verifying input of x is correct and storing it in variable x
        x = int(sys.argv[2])
        if x <= 0:
            raise ValueError
    except ValueError:
        print("Error: input for 'x' must be positive, nonzero, and of type int.")
        sys.exit(1)
    try:  # Verifying input of y is correct and storing it in variable y
        y = int(sys.argv[3])
        if (y <= 0) or (y <= x):
            raise ValueError
    except ValueError:
        print("Error: input for 'y' must be positive, nonzero, greater than or equal to 'x' and of type int.")
        sys.exit(1)
    try:  # Verifying input of o is correct and storing it in variable o
        o = str(sys.argv[4])
    except ValueError:
        print("Error: input for 'o' must be of type string.")
        sys.exit(1)

    #  -------------------CREATE A FASTA FILE WITH CHOPPED SEQUENCES-------------------
    # Read in input file contents into array of sequences
    try:
        input_file = open(i, "r")
    except FileNotFoundError:
        print("Error: specified input file, '" + i + "', does not exist.")
        sys.exit(1)

    old_sequences_array = []
    for sequence in input_file:
        old_sequences_array.append(sequence)

    j = 0
    while j < len(old_sequences_array):
        if ">" in old_sequences_array[j]:  # remove separation lines from sequences list
            old_sequences_array.remove(old_sequences_array[j])
            j -= 1
        else:  # remove trailing newlines from sequences
            old_sequences_array[j] = old_sequences_array[j].rstrip()
        j += 1

    # Create and fill new sequence array from fragmented old sequences
    new_sequences_array = []
    for j in range(0, len(old_sequences_array), 1):
        while len(old_sequences_array[j]) >= x:
            fragment = "ERROR"
            if len(old_sequences_array[j]) == x:
                new_sequences_array.append(old_sequences_array[j])
                old_sequences_array[j] = ""
            else:
                fragment_length = int(random.uniform(x, y))
                if fragment_length > len(old_sequences_array[j]):
                    fragment_length = len(old_sequences_array[j])
                    fragment = old_sequences_array[j][:fragment_length]
                else:
                    fragment = old_sequences_array[j][:fragment_length]
                new_sequences_array.append(fragment)
                old_sequences_array[j] = old_sequences_array[j][fragment_length:]

    # Write new sequences to output file in FASTA format
    output_file = open(o, "w")
    for j in range(0, len(new_sequences_array), 1):
        output_file.write(">\n" + new_sequences_array[j] + "\n")

    # Close all files
    output_file.close()
    input_file.close()
    print("Program run completed successfully.")
    return 0


if __name__ == '__main__':
    main()
