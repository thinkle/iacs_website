import csv, types,numpy

class Row:

    def __init__ (self, row, handles):
        self.data = row
        self.handles = handles

    def __len__ (self):
        return len(self.data)
        
    def __getattr__ (self, attr):
        if attr in self.handles:
            return self.data[self.handles.index(attr)]
        else:
            raise AttributeError
        
    def __getitem__ (self, attr):
        if type(attr) == int:
            return self.data[attr]
        else:
            return getattr(self,attr)

class Data:

    def __init__ (self, rows=[]):
        self.rows = rows
        if self.rows:
            self.handles = self.titles = self.rows[0].handles

    def __len__ (self):
        return len(self.rows)
        
    def __getitem__ (self, n):
        return self.rows[n]

    def groupby (self, attr):
        unique_values = set([r[attr] for r in self.rows])
        grouped = {}
        for val in unique_values:
            grouped[val] = Data(filter(lambda x: x[attr]==val, self.rows))
        return grouped

    def find (self, attr, value):
        return Data(filter(lambda x: x[attr]==value, self.rows))

class CsvData (Data):

    def __init__ (self, fn):
        Data.__init__(self, [])
        self.fn = fn
        self.read()

    def read (self):
        self.fh = file(self.fn,'rb')
        reader = csv.reader(self.fh)
        self.titles = reader.next(); self.handles = self.titles
        try:
            row = reader.next()
        except:
            row = None
        while row:
            self.rows.append(Row(row,self.titles))
            try:
                row = reader.next()
            except:
                row = None
        self.fh.close()
