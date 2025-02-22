from dataclasses import dataclass, field

@dataclass
class Matrix:
    rows: int
    cols: int
    matrix: list[list[float]] = field(init=False)

    def __post_init__(self):
        self.matrix = [[0.0 for _ in range(self.cols)] for _ in range(self.rows)]

    def set_value(self, row, col, value):
        self.matrix[row][col] = value