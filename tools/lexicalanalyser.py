class reader_writer:
    def __init__(self, program_name):
        f = open('lexical_errors.txt', 'w')
        f.write('')
        f.close()
        f = open('scanner.txt', 'w')
        f.write('')
        f.close()
        self.program = ''
        f = open(program_name, 'r')
        for l in f:
            self.program += l
        # print(self.program)
        self.i = 0
        self.errors = []

    def read(self):
        if self.i < len(self.program):
            return self.program[self.i]

    def next(self):
        if self.i < len(self.program):
            self.i += 1

    def back(self):
        if self.i > 0:
            self.i -= 1

    def add_error(self, error):
        self.errors.append(error)

    def print_errors(self):
        f = open('lexical_errors.txt', 'a')
        max_line = 0
        for e in self.errors:
            max_line = max(max_line, e[1])

        for i in range(max_line + 1):
            f.write(str(i+1) + '. ')
            for e in self.errors:
                if e[1] == i:
                    f.write(e[0] + ' ')
            f.write('\n')
    def print_lexical_scanner(self, l):
        f = open('scanner.txt', 'a')
        max_line = 0
        for e in l:
            max_line = max(max_line, e[2])

        for i in range(max_line + 1):
            f.write(str(i + 1) + '. ')
            for e in l:
                if e[2] == i:
                    f.write('(' + e[1] + ', ' + e[0] + ') ')
            f.write('\n')
        pass
    def has_next(self):
        return self.i < len(self.program)


class LexicalAnalyser:
    def __init__(self, program_name):
        self.rw = reader_writer(program_name)
        self.parse_result = self.parse()
        self.t = 0

        self.is_comment = False
        self.line = 0
        self.one_line = False


    def get_next(self):
        # print('next')
        if self.t >= len(self.parse_result):
            return self.parse_result[len(self.parse_result) - 1]
        else:
            result =  self.parse_result[self.t]
            self.t += 1
            return result

    def look_next(self):
        if self.t >= len(self.parse_result):
            return self.parse_result[len(self.parse_result) - 1]
        else:
            return self.parse_result[self.t]



    def parse(self):
        simbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '>']
        white_space = [' ', '\n', '\t', '\v', '\r', '\f']
        key_words = ['if', 'else', 'while', 'void', 'int', 'break', 'continue', 'switch', 'default', 'case', 'return']
        result = []
        token = ''
        line = 0
        is_comment = False
        one_line = False
        while self.rw.has_next():
            c = self.rw.read()
            # print(c, end='')
            if c == '/':
                self.rw.next()
                if self.rw.read() == '/':
                    is_comment = True
                    one_line = True
                if self.rw.read() == '*':
                    is_comment = True
                    one_line = False
                else:
                    self.rw.back()
            if is_comment:
                if c == '\n' and one_line:
                    is_comment = False
                    line += 1
                elif c == '*':
                    self.rw.next()
                    if self.rw.read() == '/':
                        is_comment = False
                        one_line = False
                self.rw.next()
                c = self.rw.read()
            if not is_comment:
                if c == '=':
                    if token in key_words:
                        result.append([token, 'keyword', line])
                    elif token.isnumeric():
                        result.append([token, 'num', line])
                    elif token != '':
                        result.append([token, 'id', line])
                    token = ''
                    if self.rw.has_next():
                        self.rw.next()
                        if self.rw.read() == '=':
                            result.append(['==', 'symbol', line])
                            self.rw.next()
                            continue
                    result.append(['=', 'symbol', line])

                elif c in simbols:
                    if token in key_words:
                        result.append([token, 'keyword', line])
                    elif token.isnumeric():
                        result.append([token, 'num', line])
                    elif token != '':
                        result.append([token, 'id', line])
                    token = ''
                    result.append([c, 'symbol', line])
                elif c in white_space:
                    if token in key_words:
                        result.append([token, 'keyword', line])
                    elif token.isnumeric():
                        result.append([token, 'num', line])
                    elif token != '':
                        result.append([token, 'id', line])
                    token = ''
                    if c == '\n':
                        line += 1

                elif c.isalpha():
                    if token.isnumeric():
                        self.rw.add_error(['(' + token + ', names should start with letters)', line])
                        token = '' + c
                    else:
                        token += c

                elif c.isnumeric():
                    token += c
                    pass
                else:
                    self.rw.add_error(['(' + c + ', invalid input)', line])
                    token = ''
                self.rw.next()
        if token != '':
            if token in key_words:
                result.append([token, 'keyword', line])
            elif token.isnumeric():
                result.append([token, 'num', line])
            elif token != '':
                result.append([token, 'id', line])

        result.append(['EOF', 'EOF', line])
        self.rw.print_lexical_scanner(result)
        self.rw.print_errors()
        # print(result)
        return result
