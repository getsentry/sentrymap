import random

SEA = 0
LAND = 1
COUNTRY = 2

CHAR = {
    SEA: "~",
    LAND: "#",
    COUNTRY: "x",
}

class HexGrid:
    grid = []

    NE = 1
    E = 2
    SE = 3
    SW = 4
    W = 5
    NW = 6
    
    def __init__(self, rows=15, cols=30):
        self.rows = rows
        self.cols = cols

        for _ in range(rows):
            self.grid.append([0] * cols)

    def grow_chunk1(self, num):
        startx = int(self.rows / 2)
        starty = int(self.cols / 2)

        currx = startx
        curry = starty
        self.grid[currx][curry] = 1

        for i in range(num-1):
            painted = False
            while not painted:
                direction = random.randint(1, 6) 
                currx, curry = self.get_neighbor(currx, curry, direction)
                
                if currx < 0 or curry < 0 or currx >= self.rows-1 or curry >= self.cols-1:
                    continue

                if self.grid[currx][curry] == SEA:
                    painted = True
                    self.grid[currx][curry] = LAND

    def grow_chunk2(self, num):
        startx = int(self.rows / 2)
        starty = int(self.cols / 2)

        self.grid[startx][starty] = 1

        currx = startx
        curry = starty

        for i in range(0, num+1):           
            # calculate painted neigbors
            if self.all_neighbors_painted(startx, starty):
                startx, starty = self.get_random_neighbor(startx, starty)

            for direction in range(1, 7):
                currx, curry = self.get_neighbor(startx, starty, direction)

                if currx < 0 or curry < 0 or currx >= self.rows-1 or curry >= self.cols-1:
                    continue

                if self.grid[currx][curry] == LAND:
                    continue

                if self.grid[currx][curry] == SEA:
                    self.grid[currx][curry] = LAND
                    break


    def get_neighbor(self, x, y, direction):
        match direction:
            case HexGrid.NE:
                neighbor_x = x+1 if y%2==0 else x
                neighbor_y = y - 1
            case HexGrid.E:
                neighbor_x = x + 1
                neighbor_y = y
            case HexGrid.SE:
                neighbor_x = x+1 if y%2==0 else x
                neighbor_y = y + 1
            case HexGrid.SW:
                neighbor_x = x if y%2==0 else x-1
                neighbor_y = y + 1
            case HexGrid.W:
                neighbor_x = x - 1
                neighbor_y = y
            case HexGrid.NW:
                neighbor_x = x if y%2==0 else x-1
                neighbor_y = y - 1

        return neighbor_x, neighbor_y

    def get_random_neighbor(self, x, y):
        direction = random.randint(1, 6)
        return self.get_neighbor(x, y, direction)
            
    def all_neighbors_painted(self, x, y):
        painted = 0
        for direction in range(1, 7):
            neighbor_x, neighbor_y = self.get_neighbor(x, y, direction)
            if self.grid[neighbor_x][neighbor_y] == LAND:
                painted += 1

        return painted == 6

    def print(self):
        for i in range(self.rows):
            delimiter = " " if i%2 == 0 else ""
            row = ' '.join([CHAR[b] for x in self.grid[i]])
            print(f"{delimiter}{row}")
                
    def print2(self):
        for y in range(self.cols):
            row = []
            for x in range(self.rows):
                row.append(self.grid[x][y])
            
            delimiter = " " if y%2 == 0 else ""
            rowstr = ' '.join([CHAR[b] for b in row])
            print(f"{delimiter}{rowstr}")
                    

def main():
    grid = HexGrid()
    grid.grow_chunk2(60)
    # grid.add_country(10)
    print("===============================")
    grid.print2()


if __name__ == "__main__":
    main()