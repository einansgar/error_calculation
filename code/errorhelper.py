""" This module helps to calculate an absolute error from given values. """

from math import sqrt

def calculate_mean_and_error(values: list):
    avg = sum(values)/len(values)
    square_sum = 0
    for val in values:
        square_sum += (val - avg)**2
    variant = square_sum / (len(values)-1)
    derivation = sqrt(variant)
    error = derivation / sqrt(len(values))
    error_of_error = 1 / sqrt(2*(len(values)-1))
    print("Values:", values)
    print("Result:", avg, "+/-", error)
    print("Variant:", variant, "- Derivation:", derivation, "- Error of error:", error_of_error)     
    return avg, error
    
if __name__ == "__main__":
    print("Enter your values seperated by space")
    s = input()
    l = list()
    s = s.split(' ')
    for v in s:
        l.append(float(v))
    calculate_mean_and_error(l)

