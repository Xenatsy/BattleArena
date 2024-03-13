Random r = new Random();
char[,] board(int width = 5, int height = 5) {
    char[,] b = new char[width, height];
    for (int i = 0; i < width; i++)
        for (int j = 0; j < height; j++)
            b[i, j] = '1';
    return b;
}

void printBoard(char[,] board) { 
    for (int i = 0; i < board.GetLength(0); i++)
    {
        for (int j = 0; j < board.GetLength(1); j++)
            Console.Write($"{board[i, j]} ");
        Console.WriteLine();
    }
}
// Game Cycle
while (true)
{
    switch (Console.ReadLine())
    {
        case "show": {
                Console.Clear();
                Unit u1 = new Unit(
                    "hero",
                    r.Next(1, 10), 
                    r.Next(1, 10),
                    r.Next(1, 10)
                );
                u1.getInfo();
                break;
            }
        case "exit": { return; }
    }
}

