from datetime import datetime
import csv

class Coordinates():

    def __init__(self):
        self.coords = []
    
    def add(self, x, y):
        self.coords.append([x, y])

    def getSize(self):
        return len(self.coords)

    def save(self):
        with open(str(datetime.now()) + '.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(['n', 'x', 'y'])
            for i in range(len(self.coords)):
                writer.writerow([i, self.coords[i][0], self.coords[i][1]])
