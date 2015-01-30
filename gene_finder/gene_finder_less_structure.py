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
    complements =[["A", "T"], ["G", "C"]]

    for pair in complements:
        if(base==pair[0]):
            return pair[1]
        elif(base==pair[1]):
            return pair[0]


def reverse_complement(dna):
    """
    >>> reverse_complement("ATGCTACATTCGCAT")
    'ATGCGAATGTAGCAT'
    """
    return ''.join([get_complement(dna[x]) for x in range(len(dna)-1, -1, -1)])

def get_ORFS(dna):
    """ Gets the ORFS from one strand"""
    ORFS = []

    currentORF = []

    slice_position = 0
    for slice in range(0, len(dna)-3, 1):
        if(dna[slice:slice+3] == "ATG" and slice >= slice_position):
            for slice_position in range(slice, len(dna)-2, 3):
                if(dna[slice_position:slice_position+3] != "TAG" and dna[slice_position:slice_position+3] != "TAA" and dna[slice_position:slice_position+3] != "TGA"):
                    currentORF.append(dna[slice_position:slice_position+3])
                else:
                    ORFS.append(''.join(currentORF))
                    currentORF = []
                    break
            if(len(currentORF) > 0):
                ORFS.append(''.join(currentORF))
        else:
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
    return get_ORFS(dna) + get_ORFS(reverse_complement(dna))

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    # TODO: implement this

    ORF1 = get_ORFS(dna)
    ORF2 = get_ORFS(reverse_complement(dna))

    allORFs = ORF1 + ORF2

    longest = ""
    length = -999

    for ORF in allORFs:
        if(len(ORF) > length):
            longest = ORF

    return longest


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    # TODO: implement this
    pass

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

    codingStrand = ""

    slice = 0
    while(slice <= len(dna)-3):
        codon = dna[slice:slice+3]

        for x in range(0, len(codons)):
            for y in range(0, len(codons[x])):
                if(codon == codons[x][y]):
                    codingStrand += aa[x]
                    break

        slice += 3

    return codingStrand


def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    # TODO: implement this
    
    ORFS = find_all_ORFs_both_strands(dna)
    good_aa = []

    for ORF in ORFS:
        if(len(ORF) >= threshold):
            good_aa.append(coding_strand_to_AA(ORF))

    return good_aa

if __name__ == "__main__":
    import doctest
    doctest.testmod()