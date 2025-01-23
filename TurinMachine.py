class TuringMachine:
    def __init__(self):
        self.state = 'q0'

    def transition(self, symbol):
        if self.state == 'q0':
            if symbol == '1':
                self.state = 'q1'
        elif self.state == 'q1':
            if symbol == '1':
                self.state = 'q0'

    def run(self, input_string):
        for symbol in input_string:
            if symbol not in ['0', '1']:  # Si hay un carácter no válido
                return 'q_reject'
            self.transition(symbol)
        return 'q_accept' if self.state == 'q0' else 'q_reject'


input_string = input("Ingresa una cadena de 0s y 1s: ")

tm = TuringMachine()
result = tm.run(input_string)

if result == 'q_accept':
    print(f"La cadena '{input_string}' es aceptada por la máquina de Turing.")
else:
    print(f"La cadena '{input_string}' no es aceptada por la máquina de Turing.")
