BASE_BLOCKS = [
    [[1, 1]],  # 2x1 block

    [[1, 1, 1]],  # 3x1 block

    [[1, 1, 1, 1]],  # 4x1 block

    [[1, 1, 1, 1, 1]],  # 5x1 block

    [[1, 1], 
     [1, 1]],  # 2x2 block

    [[1, 1, 1, 1], 
     [1, 1, 1, 1]],  # 4x2 block

    [[1, 1, 1], 
     [1, 1, 1], 
     [1, 1, 1]],  # 3x3 block

    [[1, 1, 1], 
     [1, 0, 0], 
     [1, 0, 0]],  # 3x3 - 2x2 block

    [[1, 1], 
     [1, 0]],  # 2x2 - 2x1 block

    [[1, 1, 1], 
     [1, 0, 0]],  # Tetris L block

    [[1, 1, 1], 
     [0, 0, 1]],  # Tetris J block

    [[1, 1, 1], 
     [0, 1, 0]],  # Tetris T block

    [[1, 1, 0], 
     [0, 1, 1]],  # Tetris S block

    [[0, 1, 1], 
     [1, 1, 0]],  # Tetris Z block

    [[1, 0], 
     [0, 1]], # Diagonal 2x2 block

    [[1, 0, 0], 
     [0, 1, 0], 
     [0, 0, 1]], # Diagonal 3x3 block
]