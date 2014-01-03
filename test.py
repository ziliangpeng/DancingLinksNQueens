from nqueens import NQueens, convert_to_string
import sys


def validate(solution):
    n = len(solution)
    if set(map(len, solution)) != set([n]):
        return False
    positions = filter(lambda p: solution[p[0]][p[1]] == '*', [(x, y) for x in range(n) for y in range(n)])

    for i in range(n):
        if len(filter(lambda p: p[1]==i, positions)) != 1:
            return False
        if len(filter(lambda p: p[0]==i, positions)) != 1:
            return False
    for i in range(-n+1, n):
        if len(filter(lambda p: p[1]-p[0]==i, positions)) > 1:
            return False
    for i in range(n*2-1):
        if len(filter(lambda p: p[0]+p[1]==i, positions)) > 1:
            return False

    return True


def test(n):
    solver = NQueens(n)
    result_count = 0
    error_count = 0
    for solution in solver.get_solutions():
        if not validate(solution):
            error_count += 1
        result_count += 1

    print 'validate result for N =', n,
    if error_count == 0:
        print 'number of answers:', result_count, 'all valid!!!'
    else:
        print 'number of answers:', result_count, 'invalid answers:', error_count


if __name__ == '__main__':
    for n in xrange(1, 13):
        test(n)
