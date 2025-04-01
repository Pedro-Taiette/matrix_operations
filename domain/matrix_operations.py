from fractions import Fraction

class MatrixOperations:
    def calculate_determinant(self, matrix):
        if matrix.rows != matrix.cols:
            raise ValueError("O determinante requer uma matriz quadrada!")
        return self._calculate_determinant(matrix.matrix)

    def _calculate_determinant(self, matrix):
        matrix = [row[:] for row in matrix]  # Faz uma cópia da matriz
        n = len(matrix)
        det = Fraction(1)

        for i in range(n):
            if matrix[i][i] == 0:
                if not self._pivot(matrix, i, n):
                    return Fraction(0)
                det *= -1  # Trocas de linha alteram o sinal do determinante

            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    self._eliminate_row(matrix, i, j, factor)

            det *= matrix[i][i]  # O determinante é o produto dos elementos da diagonal principal
        return det

    def _pivot(self, matrix, i, n):
        for j in range(i + 1, n):
            if matrix[j][i] != 0:
                matrix[i], matrix[j] = matrix[j], matrix[i]  # Troca de linha
                return True
        return False

    def _eliminate_row(self, matrix, i, j, factor):
        for k in range(len(matrix)):
            matrix[j][k] -= factor * matrix[i][k]

    def triangularize(self, matrix):
        if matrix.rows != matrix.cols:
            raise ValueError("A triangularização requer uma matriz quadrada!")

        matrix_data = [row[:] for row in matrix.matrix]
        steps = []
        swap_count = 0  # Contador de trocas de linha
        step_counter = 1  # Contador de passos para exibição correta

        steps.append(f"Passo {step_counter}: Matriz inicial\n{self.to_string(matrix_data)}\n")
        step_counter += 1

        for i in range(len(matrix_data)):
            max_row = self._find_max_row(matrix_data, i)
            if max_row != i:
                matrix_data[i], matrix_data[max_row] = matrix_data[max_row], matrix_data[i]
                swap_count += 1  # Conta cada troca de linha
                steps.append(f"Passo {step_counter}: Troca da linha {i+1} com a linha {max_row+1}\n{self.to_string(matrix_data)}")
                step_counter += 1

            if matrix_data[i][i] == 0:
                continue

            for j in range(i + 1, len(matrix_data)):
                if matrix_data[j][i] != 0:
                    factor = Fraction(matrix_data[j][i], matrix_data[i][i])
                    steps.append(f"Passo {step_counter}: Linha {j+1} = Linha {j+1} - ({self.format_fraction(factor)}) * Linha {i+1}")
                    self._eliminate_row(matrix_data, i, j, factor)
                    steps.append(f"Após a operação:\n{self.to_string(matrix_data)}")
                    step_counter += 1

        # O determinante é calculado pela multiplicação dos elementos da diagonal principal
        determinant = Fraction(1)
        for i in range(len(matrix_data)):
            determinant *= matrix_data[i][i]

        # Ajusta o sinal do determinante com base no número de trocas de linha
        if swap_count % 2 != 0:
            determinant *= -1

        # Determina a flag de sinal do determinante
        determinant_sign = "(Positivo)" if determinant >= 0 else "(Negativo)"
        steps.append(f"Passo {step_counter}: Determinante final = {determinant} {determinant_sign}")

        return matrix_data, steps, determinant

    def _find_max_row(self, matrix_data, i):
        return max(range(i, len(matrix_data)), key=lambda r: abs(matrix_data[r][i]))

    def to_string(self, matrix):
        return '\n'.join(['\t'.join([self.format_value(item) for item in row]) for row in matrix])

    def format_value(self, value):
        if isinstance(value, Fraction):
            return self.format_fraction(value)
        return str(value)

    def format_fraction(self, value):
        if value.denominator == 1:
            return str(value.numerator)  # Se o denominador for 1, mostra apenas o numerador
        return f"{value.numerator}/{value.denominator}"
