# Simulates DNA sequence partitioning
# Inputs:
#      string i: input file name
#      int x : minimum fragment length
#      int y : maximum fragment length
#      string o : output file name

# Sample call: python sequencePartitioner.py "input.txt" 6 20 "output.txt"

import sys


def main():
    #  -------------------INPUT VERIFICATION AND RECORDING-------------------
    if (len(sys.argv) < 9):  # Verifying there aren't too few inputs
        print("Error: Too few inputs.\n")
        print("Inputs should be in the form of [run program] n a c g t k p \"o\"")
        sys.exit()
    if (len(sys.argv) > 9):  # Verifying there aren't too many inputs
        print("Error: Too many inputs.\n")
        print("Inputs should be in the form of [run program] n a c g t k p \"o\"")
        sys.exit()

    print("Program run completed successfully.")
    return 0


if __name__ == '__main__':
    main()
