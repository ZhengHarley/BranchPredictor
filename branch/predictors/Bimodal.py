from predictors import AbstractBasePredictor, Predict


class Bimodal(AbstractBasePredictor):
    """
    A dynamic predictor that uses an n-bit saturating counter to predict the next state. 0 indicates strongly not
    taken, while 2^n-1 indicates strongly taken. Updates decrease or increase the counter based on the actual outcome.
    """
    def __init__(self, counter_bits: int, table_size: int, initial_state: int = 0, **kwargs):
        super().__init__()
        assert 0 <= initial_state < 2 ** counter_bits, f"Initial state must be in range [0, {2 ** counter_bits})"
        self.counter_bits = counter_bits
        self.initial_state = initial_state
        self.prediction_table = [initial_state] * table_size

    def predict(self, opcode: str, current_pc: int, target_pc: int) -> Predict:
        index = current_pc % len(self.prediction_table)
        state = self.prediction_table[index]
        return Predict.TAKEN if state >= 2 ** (self.counter_bits - 1) else Predict.NOT_TAKEN

    def update(self, opcode: str, current_pc: int, target_pc: int, result: Predict):
        index = current_pc % len(self.prediction_table)
        state = self.prediction_table[index]
        if result == Predict.TAKEN:
            self.prediction_table[index] = min(state + 1, (2 ** self.counter_bits) - 1)
        else:
            self.prediction_table[index] = max(state - 1, 0)

    def reset(self):
        self.prediction_table = [self.initial_state] * len(self.prediction_table)
