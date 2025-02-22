class MatrixOperations:
    def calculate_determinant(self, matrix):
        if matrix.rows != matrix.cols:
            raise ValueError("Determinant requires a square matrix!")
        return self._calculate_determinant(matrix.matrix)

    def _calculate_determinant(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        det = 0
        for c in range(len(matrix)):
            det += ((-1)**c) * matrix[0][c] * self._calculate_determinant(self._get_minor(matrix, 0, c))
        return det

    def _get_minor(self, matrix, row, col):
        return [r[:col] + r[col+1:] for r in (matrix[:row] + matrix[row+1:])]

    def triangularize(self, matrix):
        if matrix.rows != matrix.cols:
            raise ValueError("Triangularization requires a square matrix!")
        matrix_data = [row[:] for row in matrix.matrix]
        steps = []

        for i in range(min(matrix.rows, matrix.cols)):
            if matrix_data[i][i] == 0:
                for j in range(i+1, matrix.rows):
                    if matrix_data[j][i] != 0:
                        matrix_data[i], matrix_data[j] = matrix_data[j], matrix_data[i]
                        steps.append(f"Swapped row {i+1} with row {j+1}")
                        break

            for j in range(i+1, matrix.rows):
                if matrix_data[j][i] != 0:
                    factor = matrix_data[j][i] / matrix_data[i][i]
                    matrix_data[j] = [matrix_data[j][k] - factor * matrix_data[i][k] for k in range(matrix.cols)]
                    steps.append(f"Row {j+1} - ({factor:.2f})*Row {i+1}")

        return matrix_data, steps

    def to_string(self, matrix):
        return '\n'.join(['\t'.join([f"{item:.2f}" for item in row]) for row in matrix])