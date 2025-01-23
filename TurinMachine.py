class TuringMachine:
    def __init__(self):
        self.tape = []
        self.head = 0
        self.state = 'q0'
        self.accept_states = {'q_accept'}
        self.reject_states = {'q_reject'}

    def initialize_tape(self, input_string):
        self.tape = list(input_string) + ['_']  
        self.head = 0

    def transition(self):
        current_symbol = self.tape[self.head]
        if self.state == 'q0':
            if current_symbol == '0':
                self.tape[self.head] = 'X'
                self.head += 1
                self.state = 'q1'
            elif current_symbol == '1':
                self.tape[self.head] = 'X'
                self.head += 1
                self.state = 'q2'
            elif current_symbol == '_':
                self.state = 'q_accept'
        elif self.state == 'q1':
            if self.tape[self.head] == '0':
                self.head += 1
                self.state = 'q0'
            elif self.tape[self.head] == '_':
                self.state = 'q_reject'
        elif self.state == 'q2':
            if self.tape[self.head] == '1':
                self.head += 1
                self.state = 'q0'
            elif self.tape[self.head] == '_':
                self.state = 'q_reject'

    def run(self):
        while self.state not in self.accept_states and self.state not in self.reject_states:
            self.transition()
        return self.state


input_string = input("Ingresa una cadena de 0s y 1s: ")

tm = TuringMachine()
tm.initialize_tape(input_string)

result = tm.run()

if result == 'q_accept':
    print(f"La cadena '{input_string}' es aceptada por la máquina de Turing.")
else:
    print(f"La cadena '{input_string}' no es aceptada por la máquina de Turing.")
