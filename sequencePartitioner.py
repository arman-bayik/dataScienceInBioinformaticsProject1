# Simulates DNA sequence partitioning
# Inputs:
#      string i: input file name
#      int x : minimum fragment length
#      int y : maximum fragment length
#      string o : output file name

# Sample call: python sequencePartitioner.py "input.txt" 6 20 "output.txt"
#                                                i       x y       o

import sys


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
    # Read in input sequences
    try:
        input_file = open(i, "r")
    except FileNotFoundError:
        print("Error: specified file, " + i + " does not exist.")
        sys.exit(1)

    input_file.close()
    print("Program run completed successfully.")
    return 0


if __name__ == '__main__':
    main()
