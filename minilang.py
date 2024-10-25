class Operator:
    """Superclasse représentant un opérateur générique."""
    def apply(self, left, right):
        raise NotImplementedError("La méthode apply doit être implémentée par les sous-classes.")

class MathOperator(Operator):
    """Sous-classe pour les opérateurs mathématiques comme +, -, *, /."""
    def __init__(self, symbol):
        self.symbol = symbol

    def apply(self, left, right):
        match self.symbol:
            case '+':
                return left + right
            case '-':
                return left - right
            case '*':
                return left * right
            case '/':
                return left // right if right != 0 else 'Division par zéro'

    def __repr__(self):
        return f"MathOperator('{self.symbol}')"

class ComparisonOperator(Operator):
    """Sous-classe pour les opérateurs de comparaison comme >, <, ==, !=, >=, <=."""
    def __init__(self, symbol):
        self.symbol = symbol

    def apply(self, left, right):
        match self.symbol:
            case '>':
                return left > right
            case '<':
                return left < right
            case '==':
                return left == right
            case '!=':
                return left != right
            case '>=':
                return left >= right
            case '<=':
                return left <= right

    def __repr__(self):
        return f"ComparisonOperator('{self.symbol}')"

class Func:
    """Représente une fonction avec 1 ou plusieurs paramètres."""
    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def execute(self):
        match self.name:
            case 'print':
                for arg in self.args:
                    print(arg)
            case 'max':
                return max(self.args)
            case 'min':
                return min(self.args)

    def __repr__(self):
        return f"Func('{self.name}', {self.args})"

class Interpreter:
    """Interprète un mini-langage de programmation."""
    def __init__(self):
        self.variables = {}

    def get_value(self, token):
        """Renvoie la valeur d'un token, soit un entier, soit une variable stockée."""
        try:
            return int(token)
        except ValueError:
            return self.variables.get(token, token)

    def execute_line(self, line):
        # Analyse et exécute une seule ligne de code
        tokens = line.split()
        match tokens:
            # Affectation d'une variable avec une opération mathématique
            case [var, '=', left, symbol, right] if symbol in ['+', '-', '*', '/']:
                left_value = self.get_value(left)
                right_value = self.get_value(right)
                operator = MathOperator(symbol)
                self.variables[var] = operator.apply(left_value, right_value)

            # Fonction print avec une seule variable ou valeur
            case ['print', var]:
                func = Func('print', self.get_value(var))
                func.execute()

            # Fonction max/min avec plusieurs arguments
            case [func_name, *args] if func_name in ['max', 'min']:
                func_args = [self.get_value(arg) for arg in args]
                func = Func(func_name, *func_args)
                result = func.execute()
                print(result)

            # Condition if avec un opérateur de comparaison
            case ['if', left, op, right, ':'] if op in ['>', '<', '==', '!=', '>=', '<=']:
                left_value = self.get_value(left)
                right_value = self.get_value(right)
                operator = ComparisonOperator(op)
                if operator.apply(left_value, right_value):
                    return 'if_true'
                else:
                    return 'if_false'
            case ['else', ':']:
                return 'else'

    def run(self, program):
        # Traite un programme complet ligne par ligne
        lines = program.splitlines()
        i = 0
        while i < len(lines):
            result = self.execute_line(lines[i])
            if result == 'if_true':
                i += 1  # Exécute la ligne suivante si la condition est vraie
                self.execute_line(lines[i].strip())
                i += 1  # Ignorer le bloc else
            elif result == 'if_false':
                i += 2  # Sauter le bloc else si la condition est fausse
            else:
                i += 1

program = """
x = 5 + 3
y = x * 2
if x > 5 :
    print y
else :
    print 0
"""

interpreter = Interpreter()
interpreter.run(program)
