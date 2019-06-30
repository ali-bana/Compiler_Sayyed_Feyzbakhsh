from .lexicalanalyser import LexicalAnalyser, reader_writer


class ParseNode:
    def __init__(self, n):
        self.name = n
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class Parser:
    def __init__(self, program_name):
        self.parse_tree_name = 'parse_tree.txt'
        self.errors_path = 'parse_errors.txt'
        f = open(self.parse_tree_name, 'w')
        f.write('')
        f.close()
        f = open(self.errors_path, 'w')
        f.write('')
        f.close()
        self.la = LexicalAnalyser(program_name)
        self.firsts = {
            'Pro': ['EOF', 'int', 'void'],
            'Dec': ['int', 'void'],
            'Var_or_fun': ['(', '[', ';'],
            'Fun_d': ['('],
            'Var_d': ['[', ';'],
            'Pars': ['int', 'void'],
            'Pars1': ['id'],
            'Par_l': ['int', 'void'],
            'Par_l1': [','],
            'Par': ['int', 'void'],
            'Ty_s': ['int', 'void'],
            'Par1': ['['],
            'Dec_l': ['int', 'void'],
            'Com_s': ['{'],
            'Ex_s': ['continue', 'break', ';', '+', '-', 'num', '(', 'id'],
            'Sel_s': ['if'],
            'It_s': ['while'],
            'St': ['continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-', 'num', '(', 'id'],
            'Re_s': ['return'],
            'Re_s1': [';', '+', '-', 'num', '(', 'id'],
            'Sw_s': ['switch'],
            'Ca_ss': ['case'],
            'Ca_s': ['case'],
            'De_s': ['default'],
            'St_l': ['continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-', 'num', '(', 'id'],
            'Ex1': ['(', '[', '=', '*', '+', '-', '>', '=='],
            'Ex2': ['=', '*', '+', '-', '>', '=='],
            'Si_ex': ['+', '-', '(', 'id', 'num'],
            'Si_ex1': ['>', '=='],
            'Relop': ['>', '=='],
            'Ad_ex': ['+', '-', '(', 'id', 'num'],
            'Ad_ex1': ['+', '-'],
            'Addop': ['+', '-'],
            'Term': ['+', '-', '(', 'id', 'num'],
            'Term1': ['*'],
            'Si_fa': ['+', '-', '(', 'id', 'num'],
            'Fa': ['(', 'id', 'num'],
            'Fa1': ['(', '['],
            'Call': ['('],
            'Var': ['id'],
            'Var1': ['['],
            'Args': ['+', '-', 'num', '(', 'id'],
            'Arg_l': ['+', '-', 'num', '(', 'id'],
            'Ex': ['+', '-', 'num', '(', 'id'],
            'Arg_l1': [',']
        }
        self.follows = {
            'Pro': [],
            'Dec': ['int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
                    'num', '(', 'id', '}'],
            'Var_or_fun': ['int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+',
                           '-', 'num', '(', 'id', '}'],
            'Fun_d': ['int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
                      'num', '(', 'id', '}'],
            'Var_d': ['int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
                      'num', '(', 'id', '}'],
            'Pars': [')'],
            'Pars1': [')'],
            'Par_l': [],
            'Par_l1': [')'],
            'Par': [',', ')'],
            'Ty_s': ['id'],
            'Par1': [',', ')'],
            'Dec_l': ['EOF', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-', 'num', '(',
                      'id', '}'],
            'Com_s': ['case', 'default', 'else', 'int', 'void', 'EOF', 'continue', 'break', ';', '{', 'if', 'while',
                      'return', 'switch', '+', '-', 'num', '(', 'id', '}'],
            'Ex_s': ['case', 'default', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
                     'num', '(', 'id', '}'],
            'Sel_s': ['case', 'default', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
                      'num', '(', 'id', '}'],
            'It_s': ['case', 'default', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
                     'num', '(', 'id', '}'],
            'St': ['case', 'default', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-', 'num',
                   '(', 'id', '}'],
            'Re_s': ['case', 'default', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
                     'num', '(', 'id', '}'],
            'Re_s1': ['case', 'default', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
                      'num', '(', 'id', '}'],
            'Sw_s': ['case', 'default', 'continue', 'break', ';', '{', 'if', 'while', 'return', 'switch', '+', '-',
                     'num', '(', 'id', '}'],
            'Ca_ss': ['default', '}'],
            'Ca_s': ['case', 'default', '}'],
            'De_s': ['}'],
            'St_l': ['case', 'default', '}'],
            'Ex1': [';', ')', '}', ','],
            'Ex2': [';', ')', '}', ','],
            'Si_ex': [],
            'Si_ex1': [';', ')', ']', ','],
            'Relop': ['+', '-', '(', 'id', 'num'],
            'Ad_ex': ['>', '==', ';', ')', ']', ','],
            'Ad_ex1': ['>', '==', ';', ')', ']', ','],
            'Addop': ['+', '-', '(', 'id', 'num'],
            'Term': ['+', '-', '>', '==', ';', ')', ']', ','],
            'Term1': ['+', '-', '>', '==', ';', ')', ']', ','],
            'Si_fa': ['*', '+', '-', '>', '==', ';', ')', ']', ','],
            'Fa': ['*', '+', '-', '>', '==', ';', ')', ']', ','],
            'Fa1': ['*', '+', '-', '>', '==', ';', ')', ']', ','],
            'Call': ['*', '+', '-', '>', '==', ';', ')', ']', ','],
            'Var': [],
            'Var1': ['=', '*', '+', '-', '>', '==', ';', ')', ']', ','],
            'Args': [')'],
            'Arg_l': [')'],
            'Ex': [';', ')', ']', ','],
            'Arg_l1': [')']
        }

        self.firsts['Pars1'].extend(self.follows['Pars1'])
        self.firsts['Par_l1'].extend(self.follows['Par_l1'])
        self.firsts['Par1'].extend(self.follows['Par1'])
        self.firsts['Dec_l'].extend(self.follows['Dec_l'])
        self.firsts['Ca_ss'].extend(self.follows['Ca_ss'])
        self.firsts['De_s'].extend(self.follows['De_s'])
        self.firsts['St_l'].extend(self.follows['St_l'])
        self.firsts['Ex1'].extend(self.follows['Ex1'])
        self.firsts['Ex2'].extend(self.follows['Ex2'])
        self.firsts['Si_ex1'].extend(self.follows['Si_ex1'])
        self.firsts['Ad_ex1'].extend(self.follows['Ad_ex1'])
        self.firsts['Term1'].extend(self.follows['Term1'])
        self.firsts['Fa1'].extend(self.follows['Fa1'])
        self.firsts['Var1'].extend(self.follows['Var1'])
        self.firsts['Args'].extend(self.follows['Args'])
        self.firsts['Arg_l1'].extend(self.follows['Arg_l1'])

        self.parse_stack = []
        self.make_i = True
        self.variable_list = []
        self.break_list = []
        self.var_section = 500
        self.temp_section = 700
        self.heap = 1000

    def write_error(self, error):
        f = open(self.errors_path, 'a')
        f.write(error + '\n')
        f.close()
        pass

    def parse(self):
        return self.Pro()

    def print_parsed(self):
        root = self.parse()
        self.dfs(root, 0)

    def dfs(self, root, level):
        f = open(self.parse_tree_name, 'a')
        f.write(('  |' * level) + root.name + '\n')
        f.close()
        for c in root.children:
            self.dfs(c, level + 1)

    def pass_nonterminal_edge(self, node, non_terminal, function):
        # print(non_terminal)
        # print(self.firsts[non_terminal])
        # print(self.la.look_next())
        # print('...............\n')
        if self.in_checker(self.la.look_next(), self.firsts[non_terminal]):
            # print('going to func')
            c = function()
            node.add_child(c)
        else:
            # print('non tem')
            if self.non_terminal_error_handler(non_terminal) == 'continue':
                c = function()
                node.add_child(c)

    def pass_terminal_edge(self, node, terminal):
        next = self.la.look_next()
        if self.terminal_checker(next, terminal):
            node.add_child(ParseNode(terminal))
            self.la.get_next()
            return
        self.write_error(str(next[2]) + ' :Syntax Error! Missing ' + terminal)
        node.add_child(ParseNode(terminal))
        return

    def terminal_checker(self, terminal, correct):
        if correct == 'id' or correct == 'num':
            return terminal[1] == correct
        else:
            return terminal[0] == correct

    def non_terminal_error_handler(self, non_terminal):
        first = self.firsts[non_terminal]
        follow = self.follows[non_terminal]
        if self.in_checker(self.la.look_next(), first):
            return 'continue'
        elif self.in_checker(self.la.look_next(), follow):
            self.write_error(str(self.la.look_next()[2]) + ': Syntax Error! Missing ' + non_terminal)
            return 'jump'
        self.write_error(str(self.la.look_next()[2]) + ' : Syntax Error! Unexpected ' + self.la.look_next()[0])

        if self.terminal_checker(self.la.look_next(), 'EOF'):
            self.write_error('Unexpected EOF')
            return 'Jump'

        self.la.get_next()
        return self.non_terminal_error_handler(non_terminal)

    def in_checker(self, terminal, set):
        if terminal[1] == 'id' or terminal[1] == 'num':
            return terminal[1] in set
        else:
            return terminal[0] in set

    def Pro(self):
        root = ParseNode('Program')
        # if self.in_checker(self.la.look_next(), self.firsts['Dec_l']):
        #     c1 = self.Dec_l()
        #     root.add_child(c1)
        # else:
        #     if self.non_terminal_error_handler('Dec_l') == 'continue':
        #         c1 = self.Dec_l()
        #         root.add_child(c1)
        #
        self.pass_nonterminal_edge(root, 'Dec_l', self.Dec_l)

        next = self.la.get_next()
        if next[1] != 'EOF':
            self.write_error(str(next[2]) + ': Syntax Error! Malformed Input')
        c2 = ParseNode('EOF')
        root.add_child(c2)
        return root

    def Dec_l(self):
        node = ParseNode('Dec_l')

        if self.in_checker(self.la.look_next(), self.firsts['Dec']):
            self.pass_nonterminal_edge(node, 'Dec', self.Dec)

            self.pass_nonterminal_edge(node, 'Dec_l', self.Dec_l)
            return node

        if self.in_checker(self.la.look_next(), self.follows['Dec_l']):
            return node

        self.pass_nonterminal_edge(node, 'Dec', self.Dec)

        self.pass_nonterminal_edge(node, 'Dec_l', self.Dec_l)
        return node

    def Dec(self):
        node = ParseNode('Dec')

        self.pass_nonterminal_edge(node, 'Ty_s', self.Ty_s)
        self.pass_terminal_edge(node, 'id')
        self.pass_nonterminal_edge(node, 'Var_or_fun', self.Var_or_fun)
        return node

    def Var_or_fun(self):
        node = ParseNode('Var_or_fun')
        if self.in_checker(self.la.look_next(), self.firsts['Fun_d']):
            self.pass_nonterminal_edge(node, 'Fun_d', self.Fun_d)
            return node
        else:
            self.pass_nonterminal_edge(node, 'Var_d', self.Var_d)
            return node

    def Fun_d(self):
        node = ParseNode('Fun_d')

        self.pass_terminal_edge(node, '(')
        self.pass_nonterminal_edge(node, 'Pars', function=self.Pars)
        self.pass_terminal_edge(node, ')')
        self.pass_nonterminal_edge(node, 'Com_s', function=self.Com_s)
        return node

    def Var_d(self):
        node = ParseNode('Var_d')
        if self.la.look_next()[0] == '[':
            self.pass_terminal_edge(node, '[')
            self.pass_terminal_edge(node, 'num')
            self.pass_terminal_edge(node, ']')
            self.pass_terminal_edge(node, ';')
        else:
            self.pass_terminal_edge(node, ';')
        return node

    def Pars(self):
        node = ParseNode('Pars')
        if self.la.look_next()[0] == 'int':
            self.pass_terminal_edge(node, 'int')
            self.pass_terminal_edge(node, 'id')
            self.pass_nonterminal_edge(node, 'Par1', self.Par1)
            self.pass_nonterminal_edge(node, 'Par_l1', self.Par_l1)
        else:
            self.pass_terminal_edge(node, 'void')
            self.pass_nonterminal_edge(node, 'Pars1', self.Pars1)

        return node

    def Pars1(self):
        node = ParseNode('Pars1')
        if self.terminal_checker(self.la.look_next(), 'id'):
            self.pass_terminal_edge(node, 'id')
            self.pass_nonterminal_edge(node, 'Par1', self.Par1)
            self.pass_nonterminal_edge(node, 'Par_l1', self.Par_l1)

        return node

    def Par_l(self):
        node = ParseNode('Par_l')
        self.pass_nonterminal_edge(node, 'Par', self.Par)
        self.pass_nonterminal_edge(node, 'Par_l1', self.Par_l1)
        return node

    def Par_l1(self):
        node = ParseNode('Par_l1')
        if self.terminal_checker(self.la.look_next(), ','):
            self.pass_terminal_edge(node, ',')
            self.pass_nonterminal_edge(node, 'Par', self.Par)
            self.pass_nonterminal_edge(node, 'Par_l1', self.Par_l1)
        return node

    def Par(self):
        node = ParseNode('Par')
        self.pass_nonterminal_edge(node, 'Ty_s', self.Ty_s)
        self.pass_terminal_edge(node, 'id')
        self.pass_nonterminal_edge(node, 'Par1', self.Par1)
        return node

    def Ty_s(self):
        node = ParseNode('Ty_s')
        if self.terminal_checker(self.la.look_next(), 'int'):
            self.pass_terminal_edge(node, 'int')
        else:
            self.pass_terminal_edge(node, 'void')
        return node

    def Par1(self):
        node = ParseNode('Par1')
        if self.terminal_checker(self.la.look_next(), '['):
            self.pass_terminal_edge(node, '[')
            self.pass_terminal_edge(node, ']')
        return node

    def Com_s(self):
        node = ParseNode('Com_s')
        self.pass_terminal_edge(node, '{')
        self.pass_nonterminal_edge(node, 'Dec_l', self.Dec_l)
        self.pass_nonterminal_edge(node, 'St_l', self.St_l)
        self.pass_terminal_edge(node, '}')
        return node

    def Ex_s(self):
        node = ParseNode('Ex_s')
        if self.in_checker(self.la.look_next(), self.firsts['Ex']):
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            self.pass_terminal_edge(node, ';')
        elif self.terminal_checker(self.la.look_next(), 'continue'):
            self.pass_terminal_edge(node, 'continue')
            self.pass_terminal_edge(node, ';')
        elif self.terminal_checker(self.la.look_next(), 'break'):
            self.pass_terminal_edge(node, 'break')
            self.pass_terminal_edge(node, ';')
        else:
            self.pass_terminal_edge(node, ';')
        return node

    def Sel_s(self):
        node = ParseNode('Sel_s')
        self.pass_terminal_edge(node, 'if')
        self.pass_terminal_edge(node, '(')
        self.pass_nonterminal_edge(node, 'Ex', self.Ex)
        self.pass_terminal_edge(node, ')')
        self.pass_nonterminal_edge(node, 'St', self.St)
        self.pass_terminal_edge(node, 'else')
        self.pass_nonterminal_edge(node, 'St', self.St)
        return node

    def It_s(self):
        node = ParseNode('It_s')
        self.pass_terminal_edge(node, 'while')
        self.pass_terminal_edge(node, '(')
        self.pass_nonterminal_edge(node, 'Ex', self.Ex)
        self.pass_terminal_edge(node, ')')
        self.pass_nonterminal_edge(node, 'St', self.St)
        return node

    def St(self):
        node = ParseNode('St')
        if self.in_checker(self.la.look_next(), self.firsts['Com_s']):
            self.pass_nonterminal_edge(node, 'Com_s', self.Com_s)
        elif self.in_checker(self.la.look_next(), self.firsts['Sel_s']):
            self.pass_nonterminal_edge(node, 'Sel_s', self.Sel_s)

        elif self.in_checker(self.la.look_next(), self.firsts['It_s']):
            # print('into while eeeee.......................................................')
            self.pass_nonterminal_edge(node, 'It_s', self.It_s)

        elif self.in_checker(self.la.look_next(), self.firsts['Re_s']):
            self.pass_nonterminal_edge(node, 'Re_s', self.Re_s)


        elif self.in_checker(self.la.look_next(), self.firsts['Sw_s']):
            self.pass_nonterminal_edge(node, 'Sw_s', self.Sw_s)
        else:
            self.pass_nonterminal_edge(node, 'Ex_s', self.Ex_s)

        return node

    def Re_s(self):
        node = ParseNode('Re_s')
        self.pass_terminal_edge(node, 'return')
        self.pass_nonterminal_edge(node, 'Re_s1', self.Re_s1)
        return node

    def Re_s1(self):
        node = ParseNode('Re_s1')
        if self.terminal_checker(self.la.look_next(), ';'):
            self.pass_terminal_edge(node, ';')
        else:
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            self.pass_terminal_edge(node, ';')

        return node

    def Sw_s(self):
        node = ParseNode('Sw_s')
        self.pass_terminal_edge(node, 'switch')
        self.pass_terminal_edge(node, '(')
        self.pass_nonterminal_edge(node, 'Ex', self.Ex)
        self.pass_terminal_edge(node, ')')
        self.pass_terminal_edge(node, '{')
        self.pass_nonterminal_edge(node, 'Ca_ss', self.Ca_ss)
        self.pass_nonterminal_edge(node, 'De_s', self.De_s)
        self.pass_terminal_edge(node, '}')
        return node

    def Ca_ss(self):
        node = ParseNode('Ca_ss')
        if self.in_checker(self.la.look_next(), self.firsts['Ca_s']):
            self.pass_nonterminal_edge(node, 'Ca_s', self.Ca_s)
            self.pass_nonterminal_edge(node, 'Ca_ss', self.Ca_ss)
        return node

    def Ca_s(self):
        node = ParseNode('Ca_s')
        self.pass_terminal_edge(node, 'case')
        self.pass_terminal_edge(node, 'num')
        self.pass_terminal_edge(node, ':')
        self.pass_nonterminal_edge(node, 'St_l', self.St_l)
        return node

    def De_s(self):
        node = ParseNode('De_s')
        if self.terminal_checker(self.la.look_next(), 'default'):
            self.pass_terminal_edge(node, 'default')
            self.pass_terminal_edge(node, ':')
            self.pass_nonterminal_edge(node, 'St_l', self.St_l)
        return node

    def St_l(self):
        node = ParseNode('St_l')
        if self.in_checker(self.la.look_next(), self.firsts['St']):
            self.pass_nonterminal_edge(node, 'St', self.St)
            self.pass_nonterminal_edge(node, 'St_l', self.St_l)
        return node

    def Ex(self):
        node = ParseNode('Ex')
        if self.terminal_checker(self.la.look_next(), '+'):
            self.pass_terminal_edge(node, '+')
            self.pass_nonterminal_edge(node, 'Fa', self.Fa)
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
            self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
        elif self.terminal_checker(self.la.look_next(), '-'):
            self.pass_terminal_edge(node, '-')
            self.pass_nonterminal_edge(node, 'Fa', self.Fa)
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
            self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
        elif self.terminal_checker(self.la.look_next(), 'num'):
            self.pass_terminal_edge(node, 'num')
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
            self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
        elif self.terminal_checker(self.la.look_next(), '('):
            self.pass_terminal_edge(node, '(')
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            self.pass_terminal_edge(node, ')')
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
            self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
        else:
            # print('correct expression')
            # print(self.la.look_next())
            self.pass_terminal_edge(node, 'id')
            self.pass_nonterminal_edge(node, 'Ex1', self.Ex1)
        return node

    def Ex1(self):
        node = ParseNode('Ex1')
        if self.in_checker(self.la.look_next(), self.firsts['Call']):
            self.pass_nonterminal_edge(node, 'Call', self.Call)
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
            self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
        else:
            self.pass_nonterminal_edge(node, 'Var1', self.Var1)
            self.pass_nonterminal_edge(node, 'Ex2', self.Ex2)
        return node

    def Ex2(self):
        node = ParseNode('Ex2')
        if self.terminal_checker(self.la.look_next(), '='):
            self.pass_terminal_edge(node, '=')
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
        else:
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
            self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
        return node

    def Si_ex(self):
        node = ParseNode('Si_ex')
        self.pass_nonterminal_edge(node, 'Ad_ex', self.Ad_ex)
        self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
        return node

    def Si_ex1(self):
        node = ParseNode('Si_ex1')
        if self.in_checker(self.la.look_next(), self.firsts['Relop']):
            self.pass_nonterminal_edge(node, 'Relop', self.Relop)
            self.pass_nonterminal_edge(node, 'Ad_ex', self.Ad_ex)
        return node

    def Relop(self):
        node = ParseNode('Relop')
        if self.terminal_checker(self.la.look_next(), '>'):
            self.pass_terminal_edge(node, '>')
        else:
            self.pass_terminal_edge(node, '==')
        return node

    def Ad_ex(self):
        node = ParseNode('Ad_ex')
        self.pass_nonterminal_edge(node, 'Term', self.Term)
        self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
        return node

    def Ad_ex1(self):
        node = ParseNode('Ad_ex1')
        if self.in_checker(self.la.look_next(), self.firsts['Addop']):
            self.pass_nonterminal_edge(node, 'Addop', self.Addop)
            self.pass_nonterminal_edge(node, 'Term', self.Term)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
        return node

    def Addop(self):
        node = ParseNode('Addop')
        if self.terminal_checker(self.la.look_next(), '+'):
            self.pass_terminal_edge(node, '+')
        else:
            self.pass_terminal_edge(node, '-')
        return node

    def Term(self):
        node = ParseNode('Term')

        self.pass_nonterminal_edge(node, 'Si_fa', self.Si_fa)
        self.pass_nonterminal_edge(node, 'Term1', self.Term1)
        return node

    def Term1(self):
        node = ParseNode('Term1')
        if self.terminal_checker(self.la.look_next(), '*'):
            self.pass_terminal_edge(node, '*')
            self.pass_nonterminal_edge(node, 'Si_fa', self.Si_fa)
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
        return node



    def Si_fa(self):
        node = ParseNode('Si_fa')
        if self.terminal_checker(self.la.look_next(), '+'):
            self.pass_terminal_edge(node, '+')
            self.pass_nonterminal_edge(node, 'Fa', self.Fa)
        elif self.terminal_checker(self.la.look_next(), '-'):
            self.pass_terminal_edge(node, '-')
            self.pass_nonterminal_edge(node, 'Fa', self.Fa)
        else:
            self.pass_nonterminal_edge(node, 'Fa', self.Fa)

        return node

    def Fa(self):
        node = ParseNode('Fa')
        if self.terminal_checker(self.la.look_next(), '('):
            self.pass_terminal_edge(node, '(')
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            self.pass_terminal_edge(node, ')')
        elif self.terminal_checker(self.la.look_next(), 'id'):
            self.pass_terminal_edge(node, 'id')
            self.pass_nonterminal_edge(node, 'Fa1', self.Fa1)

        else:
            self.pass_terminal_edge(node, 'num')
        return node

    def Fa1(self):
        node = ParseNode('Fa1')
        if self.in_checker(self.la.look_next(), self.firsts['Call']):
            self.pass_nonterminal_edge(node, 'Call', self.Call)
        else:
            self.pass_nonterminal_edge(node, 'Var1', self.Var1)
        return node

    def Call(self):
        node = ParseNode('Call')
        self.pass_terminal_edge(node, '(')
        self.pass_nonterminal_edge(node, 'Args', self.Args)
        self.pass_terminal_edge(node, ')')
        return node

    def Var(self):
        node = ParseNode('Var')
        self.pass_terminal_edge(node, 'id')
        self.pass_nonterminal_edge(node, 'Var1', self.Var1)
        return node

    def Var1(self):
        node = ParseNode('Var1')
        if self.terminal_checker(self.la.look_next(), '['):
            self.pass_terminal_edge(node, '[')
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            self.pass_terminal_edge(node, ']')
        return node

    def Args(self):
        node = ParseNode('Args')
        if self.in_checker(self.la.look_next(), self.firsts['Arg_l']):
            self.pass_nonterminal_edge(node, 'Arg_l', self.Arg_l)
        return node

    def Arg_l(self):
        node = ParseNode('Arg_l')
        self.pass_nonterminal_edge(node, 'Ex', self.Ex)
        self.pass_nonterminal_edge(node, 'Arg_l1', self.Arg_l1)
        return node

    def Arg_l1(self):
        node = ParseNode('Arg_l1')
        if self.terminal_checker(self.la.look_next(), ','):
            self.pass_terminal_edge(node, ',')
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            self.pass_nonterminal_edge(node, 'Arg_l1', self.Arg_l1)
        return node
