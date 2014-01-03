from exact_cover import SparseBooleanMatrix, Node, Column 

class QueenCell(Node):
    def __init__(self, row_number, column_number):
        super(QueenCell, self).__init__()
        self.row_number = row_number
        self.column_number = column_number


class NQueens(SparseBooleanMatrix):
    """
    Solving n-queens problems.
    """

    def __init__(self, N):
        super(NQueens, self).__init__()

        self.size = N
        row_count = N
        col_count = N
        diagon_left_count = N * 2 - 1
        diagon_right_count = N * 2 - 1
        for i in xrange(row_count + col_count + diagon_right_count + diagon_left_count):
            if i < N*2:
                self.add_column(Column(True))
            else:
                self.add_column(Column(False))


        columns = list(self)
        for row in range(N):
            for col in range(N):
                args = (row, col)
                r0, r1, r2, r3 = QueenCell(*args), QueenCell(*args), QueenCell(*args), QueenCell(*args)
                r0.left, r0.right = r3, r1
                r1.left, r1.right = r0, r2
                r2.left, r2.right = r1, r3
                r3.left, r3.right = r2, r0
                diag_left = col - row + (N-1)
                diag_right = row + col

                col_index = 0
                columns[col_index + row].add_data_object(r0)
                col_index += row_count
                columns[col_index + col].add_data_object(r1)
                col_index += col_count
                columns[col_index + diag_left].add_data_object(r2)
                col_index += diagon_left_count
                columns[col_index + diag_right].add_data_object(r3)


    def transform(self, solution):
        positions = [None] * self.size
        for cell in solution:
            positions[cell.row_number] = cell.column_number

        ans = []
        for i in range(self.size):
            row = list('.' * self.size)
            row[positions[i]] = '*'
            ans.append(row)
        return ans

    
    def get_solutions(self):
        for solution in self.exact_cover():
            yield self.transform(solution)



def convert_to_string(solution):
    return '\n'.join(map(''.join, solution))

if __name__ == '__main__':
    import sys
    N = int(sys.argv[1])
    print 'N is', N

    solver = NQueens(N)
    solutions = solver.get_solutions()

    for solution in solutions:
        print convert_to_string(solution)
        break


