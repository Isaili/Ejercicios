class DFA:
    def __init__(self):
        self.states = {'q0', 'q1'}
        self.initial_state = 'q0'
        self.accepting_states = {'q0'}
        
       
        self.transitions = {
            'q0': {'0': 'q1', '1': 'q0'},
            'q1': {'0': 'q0', '1': 'q1'}
        }
        
    def process_input(self, input_string):
        current_state = self.initial_state
        for symbol in input_string:
           
            current_state = self.transitions[current_state].get(symbol)
            if current_state is None:
                
                return False

        return current_state in self.accepting_states


dfa = DFA()
input_string = "001100"
if dfa.process_input(input_string):
    print(f"La cadena '{input_string}' es aceptada por el autómata.")
else:
    print(f"La cadena '{input_string}' no es aceptada por el autómata.")
