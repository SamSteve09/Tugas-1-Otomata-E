import sys


def is_balanced(s):
    stack = []
    brackets = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in brackets.values():  # Jika karakter adalah tanda kurung pembuka
            stack.append(char)
        elif char in brackets.keys():  # Jika karakter adalah tanda kurung penutup
            if not stack or stack.pop() != brackets[char]:
                return False

    return not stack


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0  # Menunjukkan posisi token saat ini

    def peek(self):
        # Mengembalikan token saat ini tanpa memajukan index.
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return None

    def consume(self):
        # Mengambil token saat ini dan memajukan index.
        token = self.peek()
        self.index += 1
        return token

    def parse_expression(self):
        node = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            if self.peek() == '-':  # Cek aturan x + (-y) tidak boleh
                print("Ekspresi tidak valid")
                sys.exit(0)
            right = self.parse_term()
            node = (op, node, right)
        return node

    def parse_term(self):
        # Memproses term → factor (("*" | "/") factor)
        node = self.parse_exponent()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_exponent()
            node = (op, node, right)
        return node

    def parse_exponent(self):
        # Menangani pangkat ** yang memiliki prioritas lebih tinggi
        node = self.parse_factor()
        while self.peek() == '**':
            op = self.consume()
            right = self.parse_factor()
            node = (op, node, right)
        return node

    def parse_factor(self):
        # Memproses factor → ("-" factor) | NUMBER | "(" expr ")"
        if self.peek() == '-':  # Negasi tunggal diperbolehkan
            self.consume()
            if self.peek() == '-':  # Tidak boleh lebih dari satu tanda minus
                print("Ekspresi tidak valid")
                sys.exit(0)
            return -self.parse_factor()

        token = self.consume()
        if token.isdigit():  # Jika angka, kembalikan sebagai daun pohon
            return int(token)
        elif token == '(':  # Jika tanda kurung buka, parsing sub-ekspresi
            node = self.parse_expression()
            if self.consume() != ')':  # Harus diikuti dengan tanda tutup kurung
                print("Ekspresi tidak valid")
                sys.exit(0)
            return node
        print("Ekspresi tidak valid")
        sys.exit(0)


def tokenize(expression):
    # Memecah ekspresi menjadi token (angka dan operator)
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isdigit():
            num = ""
            while i < len(expression) and expression[i].isdigit():
                num += expression[i]
                i += 1
            tokens.append(num)
        elif expression[i:i+2] == "**":  # Tangani operator pangkat
            tokens.append("**")
            i += 2
        elif expression[i] in "+-*/()":
            tokens.append(expression[i])
            i += 1
        elif expression[i] == " ":
            i += 1  # Lewati spasi
        else:
            print(f"Karakter tidak dikenal: {expression[i]}")
            sys.exit(0)

    for j in range(len(tokens) - 1):
        if tokens[j] == ')' and (tokens[j + 1].isdigit() or tokens[j + 1] == '('):
            print(
                "Ekspresi tidak valid: tanda kurung diikuti angka atau tanda kurung tanpa operator.")
            sys.exit(0)
        if tokens[j].isdigit() and tokens[j + 1] == '(':
            print(
                "Ekspresi tidak valid: angka langsung diikuti tanda kurung tanpa operator.")
            sys.exit(0)

    return tokens


# Contoh penggunaan:
def evaluate(expr):
    if not is_balanced(expr):
        print("Ekspresi Tidak Valid")
        sys.exit(0)

    tokens = tokenize(expr)
    parser = Parser(tokens)
    ast = parser.parse_expression()

    if bool(ast):
        print("Ekspresi Valid")


exs = ["(2 + 4) ** (7 * (9 - 3)/4) / 4 * (2 + 8) - 1",
       "(((2 + 4) * (7 * (9 - 3)/4) / 4) (* (2 + 8) - 1))",
       "(-2 + 4) ** (7 * (-9 * -3)/-4) / -4 * (2 - -8) - 1"]


evaluate(exs[2])
