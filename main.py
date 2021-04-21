from fractions import Fraction
import numpy as np

#Absorbing Markov Chain
def solution(m):
    m = np.asarray(m)
    #Input is square matrix
    n = m.shape[0]
    # Special case where we only have 1 state
    if n < 2:
        return [1,1]

    #divide matrix into R and Q submatrices
    sub_r, sub_q = split_martix(m)

    #find F
    sub_f = calc_f(sub_q)
    sub_fr = np.dot(sub_f, sub_r)
    #Return Fractions
    return dfrac(sub_fr[0])


def split_martix(m):
    absorbing = set()

    #If row is all 0's then it is an absorbing row.
    [absorbing.add(row_i) for row_i in range(len(m)) if sum(m[row_i]) == 0]

    sub_r = []
    sub_q = []
    #Algorithm to find R sub matrix and Q sub matrix
    #We also convert the matrix into a probability matrix here
    for row_i in range(len(m)):
        if row_i not in absorbing:
            row_total = float(sum(m[row_i]))
            temp_r = []
            temp_q = []
            for col_i in range(len(m[row_i])):
                if col_i in absorbing:
                    temp_r.append(m[row_i][col_i]/row_total)
                else:
                    temp_q.append(m[row_i][col_i]/row_total)
            sub_r.append(temp_r)
            sub_q.append(temp_q)
    return sub_r, sub_q

#Find Fundamental matrix F = (I-B)^-1
def calc_f(q_subm):
    return np.linalg.inv(np.subtract(np.identity(len(q_subm)), q_subm))

#Return fraction
def dfrac(l):
    top = []
    bottom = []
    for num in l:
        frac = Fraction(num).limit_denominator()
        top.append(frac.numerator)
        bottom.append(frac.denominator)
    lcd = 1
    for bots in bottom:
        lcd = lcm(lcd,bots)
    for i in range(len(top)):
        top[i] *= int(lcd/bottom[i])
    top.append(lcd)
    return top

def lcm(x,y):
    #Least Common Multiple
    return x // gcd(x,y) * y

def gcd(x,y):
    #Greatest Common Denominator
    while y:
        x, y = y, x % y
    return x
