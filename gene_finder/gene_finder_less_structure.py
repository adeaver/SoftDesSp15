# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Andrew Deaver

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids_less_structure import aa, codons
import random
from load import load_seq

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###

def get_complement(base):
    """ returns the complement for a base

    >>> get_complement("A")
    'T'

    >>> get_complement("T")
    'A'

    >>> get_complement("C")
    'G'

    >>> get_complement("G")
    'C'"""

    # iterates through a two dimensional list, returns the complement if the given base is equal to the first entry in the list
    return ''.join([pair[1] for pair in [["A", "T"], ["T", "A"], ["G", "C"], ["C", "G"]] if (base == pair[0])])


def reverse_complement(dna):
    """
    >>> reverse_complement("ATGCTACATTCGCAT")
    'ATGCGAATGTAGCAT'

    >>> reverse_complement("GTACCCATAGGGATT")
    'AATCCCTATGGGTAC'
    """

    # iterates backwards through the list and gets the complement of each letter in list
    return ''.join([get_complement(dna[x]) for x in range(len(dna)-1, -1, -1)])

def get_ORFS(dna):
    """ Gets the ORFS from one strand"""

    # define starting variables
    ORFS = []
    currentORF = []
    slice_position = 0

    # iterate through the different frames
    for start in range(0, 3):
        # initialize slice position for every iteration
        slice_position = 0

        # iterate through starting positions for slices
        for slice in range(start, len(dna), 3):

            # determine if the slice is a start codon and if the codon has already been recorded (slice >= slice_position)
            if(dna[slice:slice+3] == "ATG" and slice >= slice_position):

                # cycle through the dna sequence until it gets to end codon
                for slice_position in range(slice, len(dna), 3):
                    if(dna[slice_position:slice_position+3] != "TAG" and dna[slice_position:slice_position+3] != "TAA" and dna[slice_position:slice_position+3] != "TGA"):
                        # append to the list of codons that are in the reading frame
                        currentORF.append(dna[slice_position:slice_position+3])
                    else:
                        # append to the list of all ORFs
                        ORFS.append(''.join(currentORF))

                        # reset the variable that reads the current ORF
                        currentORF = []
                        break
                # Handles if the ORF is at the end of the strand
                if(len(currentORF) > 0):
                    ORFS.append(''.join(currentORF))
                    currentORF = []
            elif(slice < slice_position):
                continue
            
    return ORFS


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    # TODO: implement this
    # get the ORFS for both dna and its reverse complement
    return get_ORFS(dna) + get_ORFS(reverse_complement(dna))

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    # TODO: implement this 
    try:
        # find the longest ORF in both strands using max function
        return max(find_all_ORFs_both_strands(dna), key=len)
    except ValueError:
        # max throws value error if there are no ORFs
        return ""


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    # TODO: implement this
    lengths = []

    # shuffle DNA sequence
    for x in range(num_trials):
        new_dna = [i for i in dna]
        random.shuffle(new_dna)
        lengths.append(len(longest_ORF(new_dna)))

    # return the maximum in the lengths
    return max(lengths)


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    # TODO: implement this
    return ''.join([''.join([aa[x] for x in range(0, len(codons)) if (dna[slice:slice+3] in codons[x])]) for slice in range(0, len(dna), 3)])

def gene_finder(dna):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    # TODO: implement this

    # determine threshold
    threshold = longest_ORF_noncoding(dna, 1500)

    # call coding_strand_to_AA on each of the ORFs
    return [coding_strand_to_AA(ORF) for ORF in (find_all_ORFs_both_strands(dna)) if (len(ORF) > threshold)]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    dna = load_seq("./data/X73525.fa")
    
    print gene_finder(dna)