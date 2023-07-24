import string

string.whitespace = " \n"

class LexicalAnalyzer:
    def __init__(self):
        self.transitions = {}
        self.accepted_states = set()
        self.init_state = None
        self.current_state = None
        self.current_token = ''

    def add_init_state(self, state):
        self.init_state = state
    
    def add_transition(self, state, read, target_state):
        for char in read:
            self.transitions[(state, char)] = target_state

    def add_accepted_state(self, state):
        self.accepted_states.add(state)
    
    def analyze(self, input_str, verbose=False):
        if not input_str.endswith('#'):
            input_str = input_str + '#'

        cursor_pos = 0
        self.current_state = self.init_state
        self.current_token = ''

        while cursor_pos < len(input_str):
            is_accepted = self.current_state in self.accepted_states

            if verbose:
                print({
                    'current_state': self.current_state,
                    'current_token': self.current_token,
                    'input': input_str[cursor_pos]
                })

            if is_accepted and input_str[cursor_pos] in string.whitespace + '#':
                print(f'Current Token: {self.current_token}')
                self.current_token = ''

            if input_str[cursor_pos] not in string.whitespace:
                self.current_token += input_str[cursor_pos]

            self.current_state = self.transitions.get((self.current_state, input_str[cursor_pos]))
            
            if not self.current_state:
                print(f'Invalid Token: {input_str[cursor_pos]}')
                break

            cursor_pos += 1
            
        if self.current_state == 'accept':
            print("Your code is valid!")


def main():
    lexical = LexicalAnalyzer()
    
    # add init state
    lexical.add_init_state('q0')
    
    # handle 'for' statement
    lexical.add_transition('q0', 'f', 'q1')
    lexical.add_transition('q1', 'o', 'q2')
    lexical.add_transition('q2', 'r', 'q3')

    # space or tab after 'for' statement
    lexical.add_transition('q3', string.whitespace, 'q3')

    lexical.add_accepted_state('q3')

    # handle variable name
    lexical.add_transition('q3', string.ascii_letters, 'q4')
    lexical.add_transition('q4', string.ascii_letters + string.digits + '_', 'q4')

    # space or tab after variable name
    lexical.add_transition('q4', string.whitespace, 'q5')

    lexical.add_accepted_state('q4')

    # handle '<>=!' operator
    lexical.add_transition('q5', '<>=!', 'q6')
    lexical.add_transition('q6', '=', 'q6')
    lexical.add_transition('q6', string.whitespace, 'q7')

    lexical.add_accepted_state('q6')

    # handle variable name
    lexical.add_transition('q6', string.ascii_letters, 'q7')
    lexical.add_transition('q7', string.ascii_letters + string.digits + '_', 'q7')

    # space or tab after variable name
    lexical.add_transition('q7', string.whitespace, 'q8')
    lexical.add_accepted_state('q7')

    # handle '{' symbol
    lexical.add_transition('q8', '{', 'q9')
    lexical.add_transition('q9', string.whitespace, 'q10')

    lexical.add_accepted_state('q9')

    lexical.add_transition('q9', string.ascii_letters + '_', 'q10')
    lexical.add_transition('q10', string.ascii_letters + string.digits + '_', 'q10')
    lexical.add_transition('q10', string.whitespace, 'q11')

    lexical.add_accepted_state('q10')

    lexical.add_transition('q11', '=', 'q12')
    lexical.add_transition('q12', string.whitespace, 'q13')

    lexical.add_accepted_state('q12')

    lexical.add_transition('q12', string.ascii_letters + '_', 'q13')
    lexical.add_transition('q13', string.ascii_letters + string.digits + '_', 'q13')
    lexical.add_transition('q13', string.whitespace, 'q14')

    lexical.add_accepted_state('q13')

    lexical.add_transition('q14', '+-', 'q15')
    lexical.add_transition('q15', string.whitespace, 'q16')

    lexical.add_accepted_state('q15')

    lexical.add_transition('q15', string.ascii_letters + '_', 'q16')
    lexical.add_transition('q16', string.ascii_letters + string.digits + '_', 'q16')
    lexical.add_transition('q16', string.whitespace, 'q17')

    lexical.add_accepted_state('q16')
    
    lexical.add_transition('q17', '}', 'q18')
    lexical.add_transition('q18', '#', 'accept')
    lexical.add_accepted_state('q18')


    # analyze input string
    # input_str = input('Enter your code: ')
    # Yang harus diinputkan = 'for j < k { j = j + 1 }'
    print("Enter/Paste your content. Ctrl-Z ( windows ) to save it. After Ctrl-Z, press Enter to run the code")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    input_str = '\n'.join(contents)
    lexical.analyze(input_str, verbose=True)


if __name__ == '__main__':
    main()