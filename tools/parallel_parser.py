from tools.parallel_lexical import LexicalAnalyser


class ParseNode:
    def __init__(self, n):
        self.name = n
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class Variable:
    def __init__(self, id, address, type, int_or_void):
        self.id = id
        self.address = address
        self.type = type
        self.accessable = True
        self.int_or_void = int_or_void

    def to_string(self):
        return '(' + 'id=' + self.id + ' ' + 'address=' + str(self.address) + ' ' + 'type=' + self.type + ')' + ' '




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
            'Ex1': [';', ')', ']', ','],
            'Ex2': [';', ')', ']', ','],
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
        self.fun_name = ''
        self.int_stack = []
        self.make_i = True
        self.id_list = []
        self.break_list = []
        self.var_section = 500
        self.start_temp = 700
        self.temp_i = 700
        self.heap = 1004
        self.pb = []
        self.word_length = 4
        self.vars = []
        self.functions = []
        self.heap_reg = 1000
        self.semantic_errors = []
        self.stack_start = 2004
        self.sp = 2000
        self.return_register = 3000
        self.has_main = False

        self.continues = []

        self.temp_call_params = []
        self.number_of_while = 0
        self.number_of_switch = 0


    def get_temp(self):
        result = self.temp_i
        self.temp_i += self.word_length
        # self.vars.append(Variable('', result, 'temp', 'int'))
        return result

    def add_var(self, id, type, int_or_void):
        self.check_define_var_or_func(id)
        self.check_not_void(int_or_void)
        self.vars.append(Variable(id, self.var_section, type, int_or_void))
        self.var_section += self.word_length
        self.print_vars()

    def sub_scope(self):
        self.vars.append('[')
        self.functions.append('[')

    def close_scope(self):
        while 1:
            if self.vars.pop() == '[':
                break
        while 1:
            if self.functions.pop() == '[':
                break

    def get_var(self, id):
        self.check_use_of_var(id)
        for i in range(len(self.vars)-1, -1, -1):
            if self.vars[i] == '[':
                continue
            if self.vars[i].id == id:
                return self.vars[i].address

    def get_var_type_by_address(self, address):
        for i in range(len(self.vars)-1, -1, -1):
            if self.vars[i] == '[':
                continue
            if self.vars[i].address == address:
                return self.vars[i].type
        if self.start_temp <= address < self.heap_reg or address >= self.return_register or self.heap_reg <= address < self.sp:
            return 'int'
        return 'int'


    def add_command(self, command, add1, add2, add3):
        self.pb.append('(' + command + ', ' + str(add1) + ', ' + str(add2) + ', ' + str(add3) + ')')

    def put_command(self, command, add1, add2, add3, i):
        self.pb[int(i)] = '(' + command + ', ' + str(add1) + ', ' + str(add2) + ', ' + str(add3) + ')'

    def skip_command(self):
        self.pb.append('')

    def get_pbi(self):
        return len(self.pb)

    def get_function(self, id):
        for f in self.functions:
            if f == "[":
                continue
            if f[0] == id:
                return f

    def add_function(self, id, address, type):
        self.functions.append([id, address, type, []])
        # print(self.functions)


    def add_parameter(self, parameter_id, type):
        self.functions[len(self.functions)-2][3].append([parameter_id, type])

    def push_tocken(self):
        self.int_stack.append(self.la.look_next()[0])
        # print('after push', self.int_stack)

    def pop(self):
        # print('poping', self.int_stack)
        return self.int_stack.pop()

    def push(self, obj):
        self.int_stack.append(obj)
        # print('pushed', self.int_stack)

    def allocate(self, n):
        result = self.heap
        self.heap += self.word_length * n
        return result




    def print_vars(self):
        # print('into vars')
        # for v in self.vars:
        #     if v == '[':
        #         print(v, end=' ')
        #     else:
        #         print(v.to_string(), end=' ')
        pass

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
        # print(self.la.look_next())
        # print(self.firsts[non_terminal])
        # print(self.la.look_next())
        # print('...............\n')
        aaa = self.la.look_next()
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
        # print(terminal)
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
        self.la.get_next()

        if self.terminal_checker(self.la.look_next(), 'EOF'):
            self.write_error('Unexpected EOF')
            return 'continue'

        return self.non_terminal_error_handler(non_terminal)

    def in_checker(self, terminal, set):
        if terminal[1] == 'id' or terminal[1] == 'num':
            return terminal[1] in set
        else:
            return terminal[0] in set


    def new_breakable(self):
        self.break_list.append([])

    def new_break(self, address):
        self.break_list[len(self.break_list) - 1].append(address)

    def get_break_addresses(self):
        return self.break_list.pop()

    def print_intermediate(self):
        for i in range(len(self.pb)):
            print(str(i) + '\t' + self.pb[i])

    def get_function_address(self, id):
        for f in self.functions:
            if f[0] == id:
                return f[1]


    def Pro(self):
        root = ParseNode('Program')
        #########
        self.add_command('ASSIGN', '#'+str(self.heap), self.heap_reg, '')
        self.add_command('ASSIGN', '#'+str(self.stack_start), self.sp, '')
        self.push(self.get_pbi())
        self.skip_command()
        self.functions.append(['output', self.get_pbi(), 'void', [['a', 'int']]])
        self.add_command('SUB', self.sp, '#4', self.sp)
        self.add_command('PRINT', '@'+str(self.sp), '', '')
        self.add_command('SUB', self.sp, '#4', self.sp)
        self.add_command('ASSIGN', '@'+str(self.sp), self.return_register, '')
        # self.add_command('PRINT', self.return_register, '', '')
        self.add_command('JP', '@'+str(self.return_register), '', '')
        self.put_command('JP', self.get_pbi(), '', '', self.pop())
        #######
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

        #############
        self.add_command('JP', self.get_function('main')[1], '', '')
        self.put_command('JP', self.get_pbi(), '', '', int(self.pop()))
        #############
        #testing
        print('...............')
        # print(self.vars)
        # print(self.functions)
        if self.make_i:
            self.print_intermediate()


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
        ######
        self.push_tocken()
        ######
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
        is_main = False
        #
        if self.make_i:
            print('midim too',self.int_stack)
            name = self.pop()
            type = self.pop()
            self.push(self.get_pbi())
            self.push(type)
            self.push(name)
            self.skip_command()
            func_name = self.pop()
            self.add_function(func_name, self.get_pbi(), self.pop())
            self.sub_scope()
            self.check_define_var_or_func(func_name)
        #
        self.pass_terminal_edge(node, '(')
        #####
        if self.make_i:
            if func_name == 'main' and self.la.look_next()[0] == 'void':
                self.has_main = True
                is_main = True
        ####
        self.pass_nonterminal_edge(node, 'Pars', function=self.Pars)
        ######
        if self.make_i:
            for v in self.vars[::-1]:
                if v == '[':
                    break
                self.add_command('SUB', self.sp, '#'+str(self.word_length), self.sp)
                self.add_command('ASSIGN', '@'+str(self.sp), v.address, '')
        ######
        self.pass_terminal_edge(node, ')')

        self.pass_nonterminal_edge(node, 'Com_s', function=self.Com_s)

        ######
        if self.make_i:
            # print(self.int_stack)
            if not is_main:
                self.add_command('SUB', self.sp, '#' + str(self.word_length), self.sp)
                self.add_command('ASSIGN', '@' + str(self.sp), self.return_register, '')
                self.add_command('JP', '@' + str(self.return_register), '', '')
            if is_main:
                self.skip_command()
            add = self.pop()
            self.put_command('JP', str(self.get_pbi()),'', '', int(add))
            if is_main:
                self.push(self.get_pbi()-1)
        ######
        self.close_scope()
        return node

    def Var_d(self):
        node = ParseNode('Var_d')
        if self.la.look_next()[0] == '[':
            self.pass_terminal_edge(node, '[')
            self.push_tocken()
            self.pass_terminal_edge(node, 'num')
            self.pass_terminal_edge(node, ']')
            self.pass_terminal_edge(node, ';')
            ######
            if self.make_i:
                size = int(self.pop()) * self.word_length
                id = self.pop()
                iv_type = self.pop()
                self.add_var(id, 'array', iv_type)
                var_addr = self.get_var(id)
                self.add_command('ASSIGN', self.heap_reg, str(var_addr), '')
                self.add_command('ADD', self.heap_reg, '#'+str(size), self.heap_reg)
            ######
        else:
            #
            if self.make_i:
                t1 = self.pop()
                t2 = self.pop()
                self.add_var(t1, t2, t2)
                add = self.get_var(t1)
                self.add_command('ASSIGN', '#0', add, '')
            #
            self.pass_terminal_edge(node, ';')
        return node

    def Pars(self):
        node = ParseNode('Pars')
        if self.la.look_next()[0] == 'int':
            ######
            self.push_tocken()
            ######
            self.pass_terminal_edge(node, 'int')
            ####
            self.push_tocken()
            ####
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
        #####
        self.push_tocken()
        #####
        self.pass_terminal_edge(node, 'id')
        self.pass_nonterminal_edge(node, 'Par1', self.Par1)
        return node

    def Ty_s(self):
        node = ParseNode('Ty_s')
        ###########
        self.push_tocken()
        ############
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
            ######
            if self.make_i:
                id = self.pop()
                self.add_parameter(id, 'array')
                iv = self.pop()
                self.add_var(id, 'array', iv)
            #######
        else:
            ######
            if self.make_i:
                id = self.pop()
                type = self.pop()
                self.add_parameter(id, type)
                self.add_var(id, type, type)
            #######
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
            ####
            self.pop()
            ####
            self.pass_terminal_edge(node, ';')
        elif self.terminal_checker(self.la.look_next(), 'continue'):
            ##########
            if self.make_i:
                self.continues[len(self.continues)-1].append(self.get_pbi())
                self.skip_command()
            #########
            self.pass_terminal_edge(node, 'continue')
            self.pass_terminal_edge(node, ';')
        elif self.terminal_checker(self.la.look_next(), 'break'):
            #######
            if self.make_i:
                self.new_break(self.get_pbi())
                self.skip_command()
            #######
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
        #######
        if self.make_i:
            ex = self.pop()
            self.push(self.get_pbi())
            self.push(ex)
            self.skip_command()
        #######
        self.pass_nonterminal_edge(node, 'St', self.St)

        self.pass_terminal_edge(node, 'else')
        #########
        if self.make_i:
            i = self.get_pbi()
            self.skip_command()
            self.put_command('JPF', self.pop(), self.get_pbi(), '', self.pop())
            self.push(i)
        ########

        self.pass_nonterminal_edge(node, 'St', self.St)
        #######
        if self.make_i:
            self.put_command('JP', self.get_pbi(), '', '', self.pop())
        ############
        return node

    def It_s(self):
        node = ParseNode('It_s')
        self.pass_terminal_edge(node, 'while')
        self.pass_terminal_edge(node, '(')
        #######
        if self.make_i:
            self.push(self.get_pbi())
            self.new_breakable()
        ######
        self.pass_nonterminal_edge(node, 'Ex', self.Ex)
        self.pass_terminal_edge(node, ')')
        self.continues.append([])
        ######
        if self.make_i:
            self.number_of_while += 1
            ex = self.pop()
            self.push(self.get_pbi())
            self.push(ex)
            self.skip_command()
        ######
        self.pass_nonterminal_edge(node, 'St', self.St)

        ########
        if self.make_i:
            t = self.pop()
            jpf = self.pop()
            jp = self.pop()
            self.add_command('JP', jp, '', '')
            end = self.get_pbi()
            self.put_command('JPF', t, end, '', jpf)
            for i in self.get_break_addresses():
                self.put_command('JP', end, '', '', i)

            for i in self.continues.pop():
                self.put_command('JP', jp, '', '', i)
        ########
        self.number_of_while -= 1
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
            ##############
            self.add_command('SUB', self.sp, '#' + str(self.word_length), self.sp)
            self.add_command('ASSIGN', '@' + str(self.sp), self.return_register, '')
            self.add_command('JP', '@' + str(self.return_register), '', '')
            #############
            self.pass_terminal_edge(node, ';')
        else:
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            ###########
            if self.make_i:
                return_val = self.pop()
                self.add_command('SUB', self.sp, '#'+str(self.word_length), self.sp)
                self.add_command('ASSIGN', '@'+str(self.sp) , self.return_register, '')
                self.add_command('ASSIGN', return_val, '@'+str(self.sp), '')
                self.add_command('ADD', self.sp, '#' + str(self.word_length), self.sp)
                self.add_command('JP', '@'+str(self.return_register), '', '')
            ###########
            self.pass_terminal_edge(node, ';')

        return node

    def Sw_s(self):
        node = ParseNode('Sw_s')
        self.pass_terminal_edge(node, 'switch')
        self.pass_terminal_edge(node, '(')
        self.pass_nonterminal_edge(node, 'Ex', self.Ex)
        self.pass_terminal_edge(node, ')')
        #######
        self.new_breakable()
        #######
        self.number_of_switch += 1
        self.pass_terminal_edge(node, '{')
        self.pass_nonterminal_edge(node, 'Ca_ss', self.Ca_ss)
        self.pass_nonterminal_edge(node, 'De_s', self.De_s)
        self.pass_terminal_edge(node, '}')
        self.number_of_switch -= 1
        #######
        if self.make_i:
            end = self.get_pbi()
            for i in self.get_break_addresses():
                self.put_command('JP', end, '', '', i)
        #######
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
        ##########
        if self.make_i:
            exp = self.pop()
            t = self.get_temp()
            number = self.la.look_next()[0]
            self.add_command('EQ', exp, '#'+number, t)
            self.add_command('JPF', t, self.get_pbi()+2, '')
            self.push(exp)
            self.push(t)
            self.push(self.get_pbi())
            self.skip_command()
        ##########
        self.pass_terminal_edge(node, 'num')
        self.pass_terminal_edge(node, ':')
        self.pass_nonterminal_edge(node, 'St_l', self.St_l)
        #########
        if self.make_i:
            addr = self.pop()
            t = self.pop()
            self.put_command('JP', self.get_pbi(), '', '', addr)
        #########
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
        aaa = self.la.look_next()
        # print('sdfsdfdsf', self.la.look_next())
        if self.terminal_checker(self.la.look_next(), '+'):
            self.pass_terminal_edge(node, '+')
            self.pass_nonterminal_edge(node, 'Fa', self.Fa)
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
            self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
        elif self.terminal_checker(self.la.look_next(), '-'):
            self.pass_terminal_edge(node, '-')
            self.pass_nonterminal_edge(node, 'Fa', self.Fa)
            ######
            if self.make_i:
                var_add = self.pop()
                t = self.get_temp()
                self.add_command('SUB', '#0', var_add, t)
                self.push(t)
            #######
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
            self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
        elif self.terminal_checker(self.la.look_next(), 'num'):
            ########
            self.push('#'+self.la.look_next()[0])
            #######
            self.pass_terminal_edge(node, 'num')
            self.pass_nonterminal_edge(node, 'Term1', self.Term1)
            self.pass_nonterminal_edge(node, 'Ad_ex1', self.Ad_ex1)
            self.pass_nonterminal_edge(node, 'Si_ex1', self.Si_ex1)
            # print(self.int_stack)
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
            ####
            self.push_tocken()
            ####
            self.pass_terminal_edge(node, 'id')
            self.pass_nonterminal_edge(node, 'Ex1', self.Ex1)
        return node

    def Ex1(self):
        node = ParseNode('Ex1')
        aaa = self.la.look_next()
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
        aaa = self.la.look_next()
        if self.terminal_checker(self.la.look_next(), '='):
            self.pass_terminal_edge(node, '=')
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            ######
            if self.make_i:
                ex = self.pop()
                var = self.pop()
                self.check_assign_types(ex, var)
                self.add_command('ASSIGN', ex, var, '')
                self.push(ex)
            ######
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
            #######
            self.push_tocken()
            ##########
            self.pass_nonterminal_edge(node, 'Relop', self.Relop)
            self.pass_nonterminal_edge(node, 'Ad_ex', self.Ad_ex)
            #######
            if self.make_i:
                t = self.get_temp()
                a2 = self.pop()
                relop = self.pop()
                # print(a2)
                # print(relop)
                a1 = self.pop()
                if relop == '==':
                    self.check_assign_types(a1, a2)
                    self.add_command('EQ', a1, a2, t)
                else:
                    self.check_assign_types(a1, a2)
                    self.add_command('LT', a1, a2, t)
                self.push(t)
            ##########
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
            #######
            self.push_tocken()
            #######
            self.pass_nonterminal_edge(node, 'Addop', self.Addop)
            self.pass_nonterminal_edge(node, 'Term', self.Term)
            #######
            if self.make_i:
                t = self.get_temp()
                a2 = self.pop()
                addop = self.pop()
                a1 = self.pop()
                if addop == '+':
                    self.check_assign_types(a1, a2)
                    self.add_command('ADD', a1, a2, t)
                else:
                    self.check_assign_types(a1, a2)
                    self.add_command('SUB', a1, a2, t)
                self.push(t)
            ########
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
            ########
            if self.make_i:
                t = self.get_temp()
                t1 = self.pop()
                t2 = self.pop()
                self.check_assign_types(t1, t2)
                self.add_command('MULT', t1, t2, t)
                self.push(t)
            #########
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
            #######
            if self.make_i:
                fa = self.pop()
                self.add_command('SUB', '#0', fa, fa)
            ######
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
            ######
            self.push_tocken()
            ############
            self.pass_terminal_edge(node, 'id')
            self.pass_nonterminal_edge(node, 'Fa1', self.Fa1)

        else:
            ########
            self.push('#' + self.la.look_next()[0])
            #########
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
        ###########
        if self.make_i:
            for v in self.vars:
                if v == '[':
                    continue
                self.add_command('ASSIGN', v.address, '@'+str(self.sp), '')
                self.add_command('ADD', self.sp, '#'+str(self.word_length), self.sp)
            self.push(self.get_pbi())
            self.skip_command()
            self.skip_command()
        ###########
        self.pass_terminal_edge(node, '(')
        self.temp_call_params = []
        id = self.int_stack[-2]
        self.pass_nonterminal_edge(node, 'Args', self.Args)
        self.check_use_of_func(id)
        self.temp_call_params = []
        self.pass_terminal_edge(node, ')')
        #########
        if self.make_i:
            print(self.int_stack)
            add = self.pop()
            self.put_command('ASSIGN', '#'+str(self.get_pbi() + 1), '@'+str(self.sp), '', add)
            add += 1
            self.put_command('ADD', self.sp, '#'+str(self.word_length), self.sp, add)
            print('in', self.int_stack)
            print(self.functions)
            func = self.get_function(self.pop())
            func_add = func[1]
            self.add_command('JP', func_add, '', '')
            #called the function
            if func[2] != 'void':
                print('doole khar',func)
                t = self.get_temp()
                self.add_command('SUB', self.sp, '#'+str(self.word_length), self.sp)
                self.add_command('ASSIGN', '@'+str(self.sp), t, '')
                self.push(t)
            else:
                self.push(0)
            for v in self.vars[::-1]:
                if v == '[':
                    continue
                self.add_command('SUB', self.sp, '#' + str(self.word_length), self.sp)
                self.add_command('ASSIGN', '@'+str(self.sp), v.address, '')
        #########
        return node

    def Var(self):
        node = ParseNode('Var')
        self.pass_terminal_edge(node, 'id')
        self.pass_nonterminal_edge(node, 'Var1', self.Var1)
        return node

    def Var1(self):
        aaa = self.la.look_next()
        node = ParseNode('Var1')
        if self.terminal_checker(self.la.look_next(), '['):
            self.pass_terminal_edge(node, '[')
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            self.pass_terminal_edge(node, ']')
            ######
            if self.make_i:
                t = str(self.get_temp())
                ex = self.pop()
                var = self.get_var(self.pop())
                self.add_command('ADD', var, ex, t)
                self.push('@'+t)
            ######
        else:
            ########
            if self.make_i:
                var_add = self.get_var(self.pop())
                self.push(var_add)
            ######
        return node

    def Args(self):
        node = ParseNode('Args')
        if self.in_checker(self.la.look_next(), self.firsts['Arg_l']):
            self.pass_nonterminal_edge(node, 'Arg_l', self.Arg_l)
        return node

    def Arg_l(self):
        node = ParseNode('Arg_l')
        self.pass_nonterminal_edge(node, 'Ex', self.Ex)
        #########
        if self.make_i:
            temp = self.pop()
            self.temp_call_params.append(temp)
            self.add_command('ASSIGN', temp, '@'+str(self.sp), '')
            self.add_command('ADD', self.sp, '#'+str(self.word_length), self.sp)
        #########
        self.pass_nonterminal_edge(node, 'Arg_l1', self.Arg_l1)
        return node

    def Arg_l1(self):
        node = ParseNode('Arg_l1')
        if self.terminal_checker(self.la.look_next(), ','):
            self.pass_terminal_edge(node, ',')
            self.pass_nonterminal_edge(node, 'Ex', self.Ex)
            #########
            if self.make_i:
                temp = self.pop()
                self.temp_call_params.append(temp)
                self.add_command('ASSIGN', temp, '@'+str(self.sp), '')
                self.add_command('ADD', self.sp, '#' + str(self.word_length), self.sp)
            #########
            self.pass_nonterminal_edge(node, 'Arg_l1', self.Arg_l1)
        return node

    def check_define_var_or_func(self, id):
        for var in self.vars:
            if var == '[':
                continue
            if var.id == id:
                self.semantic_errors += [id + " is defined."]
                self.make_i = False
        if self.functions.__len__() == 0:
            return
        if self.functions[-1] == '[':
            for func in self.functions[:-2]:
                if func == '[':
                    continue
                if func[0] == id:
                    self.semantic_errors += [id + " is defined."]
                    self.make_i = False
        else:
            for func in self.functions:
                if func == '[':
                    continue
                if func[0] == id:
                    self.semantic_errors += [id + " is defined."]
                    self.make_i = False

    def check_use_of_var(self, id):
        for var in self.vars:
            if var == '[':
                continue
            if var.id == id:
                return
        self.semantic_errors += [id + " is not defined."]
        self.make_i = False

    def check_use_of_func(self, id):
        params = []
        for i in range(len(self.temp_call_params)):
            x = self.temp_call_params[i]
            if x is None:
                return
            if x == id:
                break
            if isinstance(x, str):
                params.append('int')
            else:
                params.append(self.get_var_type_by_address(x))
        for func in self.functions:
            if func == '[':
                continue
            if func[0] == id:
                if len(params) != len(func[3]):
                    self.semantic_errors += ['Mismatch in numbers of arguments of ' + id]
                    self.make_i = False
                    return
                for i in range(len(func[3])):
                    if params[i] != func[3][i][1]:
                        self.semantic_errors += [id + " bad params in " + str(i+1) + "\'th param. expected " +
                                                 func[3][i][1] + " found " + params[i] + "."]
                        self.make_i = False
                        return
                return
        self.semantic_errors += [id + " is not defined."]
        self.make_i = False

    def check_assign_types(self, a, b):
        if isinstance(a, str):
            if a[0] == '#':
                t1 = 'int'
            else:
                t1 = 'int'
        else:
            t1 = self.get_var_type_by_address(a)
        if isinstance(b, str):
            if b[0] == '#':
                t2 = 'int'
            else:
                t2 = 'int'
        else:
            t2 = self.get_var_type_by_address(b)
        if t1 != t2:
            self.semantic_errors += [t1 + ", " + t2 + " type mismatch."]
            self.make_i = False

    def check_not_void(self, type):
        if type == 'void':
            self.semantic_errors += ['Illegal type of void']
            self.make_i = False

    def check_continue_place(self):
        if self.number_of_while <= 0:
            self.semantic_errors += ['No ’while’ found for ’continue’.']
            self.make_i = False

    def check_break_place(self):
        if self.number_of_while <= 0 and self.number_of_switch <= 0:
            self.semantic_errors += ['No ’while’ or ’switch’ found for ’break’.']
            self.make_i = False
