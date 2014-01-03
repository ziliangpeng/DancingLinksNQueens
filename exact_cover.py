"""
    Copied from https://github.com/benma/sudoku-exactcover.
"""


class SparseBooleanMatrix(object):
    head = None
    def __init__(self):
        self.head = Column()

    def add_column(self, column):
        self.head.left.right = column
        column.left = self.head.left
        self.head.left = column
        column.right = self.head

    def __iter__(self):
        cursor = self.head.right
        while cursor is not self.head:
            yield cursor
            cursor = cursor.right
    
    def exact_cover(self, callback=None):
        """
        Dancing Links implementation of Algorithm X.
        http://lanl.arxiv.org/pdf/cs/0011047
        """
        def cover(column):
            column.remove_h()
            for i in column:
                j = i.right
                while j is not i:
                    j.remove_v()            
                    j = j.right
                      
        def uncover(column):
            for i in reversed(list(column)):
                j = i.left
                while j is not i:
                    j.insert_v()
                    j = j.left
            column.insert_h()
            
        def exact_cover(row_stack, callback=None):
            if self.head.right is self.head:
                solution = row_stack[:]
                if callback is not None:
                    callback(solution)
                yield solution
            else:
                c = min(self)
                cover(c)

                for r in c:
                    j = r.right
                    while j is not r:
                        cover(j.column)
                        j = j.right

                    row_stack.append(r)
                    for solution in exact_cover(row_stack, callback=callback):
                        yield solution

                    row_stack.pop()

                    j = r.left
                    while j is not r:
                        uncover(j.column)
                        j = j.left

                uncover(c)

        return exact_cover([], callback)


class Node(object):
    left = None
    top = None
    right = None
    bottom = None
    column = None
    
    def __init__(self):
        self.top = self
        self.bottom = self
        self.left = self
        self.right = self

    def remove_h(self):
        if self.left is not None:
            self.left.right = self.right
        if self.right is not None:
            self.right.left = self.left
            
    def remove_v(self):
        if self.top is not None:
            self.top.bottom  = self.bottom
        if self.bottom is not None:
            self.bottom.top = self.top
        self.column.size -= 1

    def insert_h(self):
        if self.left is not None:
            self.left.right = self
        if self.right is not None:
            self.right.left = self
            
    def insert_v(self):
        if self.top is not None:
            self.top.bottom = self
        if self.bottom is not None:
            self.bottom.top = self
        self.column.size += 1

class Column(Node):
    size = 0
        
    def __lt__(self, other):
        return self.size < other.size

    def __eq__(self, other):
        return self.size == other.size
    
    def __iter__(self):
        cursor = self.bottom
        while cursor is not self:
            yield cursor
            cursor = cursor.bottom

    def add_data_object(self, data_object):
        self.top.bottom = data_object
        data_object.top = self.top
        self.top = data_object
        data_object.bottom = self
        data_object.column = self
        self.size += 1       
