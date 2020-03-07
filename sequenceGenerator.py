# Simulates DNA sequence generation
# Inputs:
#      int n : sequence length
#      int a : % of sequence that should be A nucleotide
#      int c : % of sequence that should be C nucleotide
#      int g : % of sequence that should be G nucleotide
#      int t : % of sequence that should be T nucleotide
#      int k : number of sequences
#      double p : mutation probability (range = [0,1])
#      string o : output file name

# Sample call: python sequenceGenerator.py 50 25 25 25 25 3 .03 "output.txt"
#                                          n  a  c  g  t  k  p       o

import sys
import random


def main():
    #  -------------------INPUT VERIFICATION AND RECORDING-------------------
    if len(sys.argv) < 9:  # Verifying there aren't too few inputs
        print("Error: Too few inputs.\n")
        print("Inputs should be in the form of [run program] n a c g t k p \"o\"")
        sys.exit(1)
    if len(sys.argv) > 9:  # Verifying there aren't too many inputs
        print("Error: Too many inputs.\n")
        print("Inputs should be in the form of [run program] n a c g t k p \"o\"")
        sys.exit(1)

    try:  # Verifying input of n is correct and storing it in variable n
        n = int(sys.argv[1])
        if n < 0:
            raise ValueError
    except ValueError:
        print("Error: input for 'n' must be positive and of type int.")
        sys.exit(1)

    try:  # Verifying input of a is correct and storing it in variable a
        a = int(sys.argv[2])
        if a < 0:
            raise ValueError
    except ValueError:
        print("Error: input for 'a' must be positive and of type int.")
        sys.exit(1)

    try:  # Verifying input of c is correct and storing it in variable c
        c = int(sys.argv[3])
        if c < 0:
            raise ValueError
    except ValueError:
        print("Error: input for 'c' must be positive and of type int.")
        sys.exit(1)

    try:  # Verifying input of g is correct and storing it in variable g
        g = int(sys.argv[4])
        if g < 0:
            raise ValueError
    except ValueError:
        print("Error: input for 'g' must be positive and of type int.")
        sys.exit(1)

    try:  # Verifying input of t is correct and storing it in variable t
        t = int(sys.argv[5])
        if t < 0:
            raise ValueError
    except ValueError:
        print("Error: input for 't' must be positive and of type int.")
        sys.exit(1)

    try:  # Verifying input of k is correct and storing it in variable k
        k = int(sys.argv[6])
        if k < 0:
            raise ValueError
    except ValueError:
        print("Error: input for 'k' must be positive and of type int.")
        sys.exit(1)

    try:  # Verifying input of p is correct and storing it in variable p
        p = float(sys.argv[7])
        if (p < 0) or (p > 1):
            raise ValueError
    except ValueError:
        print("Error: input for 'p' must be in the range [0,1] (inclusive) and of type double.")
        sys.exit(1)

    try:  # Verifying input of o is correct and storing it in variable o
        o = str(sys.argv[8])
    except ValueError:
        print("Error: input for 'o' must be of type string.")
        sys.exit(1)

    #  -------------------CREATING FASTA FILE WITH INPUT SPECIFICATIONS-------------------
    # Calculating s to generate random nucleotides, a c g and t will be valid if this point is reached
    s = a + c + g + t
    # Calculating probabilities and bounds to generate a c g and t nucleotides using a random decimal generator
    a_prob = float(a)/float(s)
    c_prob = float(c)/float(s)
    g_prob = float(g)/float(s)
    t_prob = float(t)/float(s)
    a_lb = 0
    a_ub = a_prob
    c_lb = a_ub
    c_ub = a_ub + c_prob
    g_lb = c_ub
    g_ub = c_ub + g_prob
    t_lb = g_ub
    t_ub = g_ub + t_prob
    a_bounds = [a_lb, a_ub]  # >=, <
    c_bounds = [c_lb, c_ub]  # >=, <
    g_bounds = [g_lb, g_ub]  # >=, <
    t_bounds = [t_lb, t_ub]  # >=, <=
    # Creating the output file and writing sequence information to it
    output_file = open(o, "w")
    for i in range(0, k, 1):
        output_file.write(">\n")
        for j in range(0, n, 1):
            nucleotide_select = random.uniform(0, 1)
            if(nucleotide_select >= a_bounds[0]) and (nucleotide_select < a_bounds[1]):
                output_file.write("A")
            elif(nucleotide_select >= c_bounds[0]) and (nucleotide_select < c_bounds[1]):
                output_file.write("C")
            elif(nucleotide_select >= g_bounds[0]) and (nucleotide_select < g_bounds[1]):
                output_file.write("G")
            elif(nucleotide_select >= t_bounds[0]) and (nucleotide_select <= t_bounds[1]):
                output_file.write("T")
        output_file.write("\n")
    output_file.close()
    print("Program run completed successfully.")
    return 0


if __name__ == '__main__':
    main()
