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

    def parse_expression(self, allow_unary=True):
        node = self.parse_term(allow_unary=allow_unary)
        while self.peek() in ('+', '-'):
            op = self.consume()
            
            # Operand kanan tidak boleh dimulai dengan unary minus
            right = self.parse_term(allow_unary=False)
            node = (op, node, right)
        return node

    def parse_term(self, allow_unary=True):
        # Memproses term → factor (("*" | "/") factor)
        node = self.parse_exponent(allow_unary=allow_unary)
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_exponent(allow_unary=False)
            node = (op, node, right)
        return node

    def parse_exponent(self, allow_unary=True):
        # Menangani pangkat ** yang memiliki prioritas lebih tinggi
        node = self.parse_factor(allow_unary=allow_unary)
        while self.peek() == '**':
            op = self.consume()
            right = self.parse_factor(allow_unary=False)
            node = (op, node, right)
        return node

    def parse_factor(self, allow_unary=True):
        # Memproses factor → ("-" factor) | NUMBER | "(" expr ")"
        if self.peek() == '-':  # Negasi tunggal diperbolehkan
                if not allow_unary:
                print("Unary minus tidak diizinkan")
                sys.exit(0)
            self.consume()
            result = self.parse_factor(allow_unary=True)
            if result == 0:
                print("0 pada awal expresi aritmatika tidak boleh diawali dengan tanda \"-\" ")
                sys.exit(0)
            return -result

        token = self.consume()
        if token.isdigit():  # Jika angka, kembalikan sebagai daun pohon
            return int(token)
        elif token == '(':  # Jika tanda kurung buka, parsing sub-ekspresi
            node = self.parse_expression(allow_unary=True)
            if self.consume() != ')':  # Harus diikuti dengan tanda tutup kurung
                print("Ekspresi tidak valid")
                sys.exit(0)
            return node
        print("Tanda tidak seimbang")
        sys.exit(0)

def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isdigit():
            num = ""
            while i < len(expression) and expression[i].isdigit():
                num += expression[i]
                i += 1
            if len(num) > 1 and num[0] == '0':
                print("Digit tidak diawali dengan 0")
                sys.exit(0)
            tokens.append(num)
        elif expression[i:i+2] == "**":
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
        if tokens[j] == ')' and (tokens[j+1].isdigit() or tokens[j+1] == '('):
            print("Tanda kurung diikuti angka atau tanda kurung tanpa operator.")
            sys.exit(0)
        if tokens[j].isdigit() and tokens[j+1] == '(':
            print("Angka langsung diikuti tanda kurung tanpa operator.")
            sys.exit(0)
    return tokens


# Contoh penggunaan:
def evaluate(expr):
    if not is_balanced(expr):
        print("Ekspresi Tidak Valid")
        sys.exit(0)

    tokens = tokenize(expr)
    parser = Parser(tokens)
    parser.parse_expression()
    print("Ekspresi Valid")

testc = int(input("Masukkan jumlah ekspresi: "))

for i in range(testc):
    AE = input("Contoh (2+5-4**3): ")
    try:
        evaluate(AE)
    except SystemExit:
        print("Ekspresi tidak valid")
