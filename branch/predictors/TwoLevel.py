from predictors import AbstractBasePredictor, Predict


class TwoLevel(AbstractBasePredictor):
    """
    A dynamic predictor that uses a two-level table to predict outcomes. PCs index into a Branch History Register
    (or BHR) which stores the history of that branch. The history of the branch is then used to index into a Pattern
    History Table (or PHT) which stores a bimodal saturating counter for each pattern.
    """
    def __init__(self,
                 num_bhrs: int,
                 history_size_bits: int,
                 num_pht_entries: int,
                 pht_counter_bits: int = 2,
                 initial_bhr_state: int = 0,
                 initial_pht_state: int = 0, **kwargs
                 ):
        super().__init__()
        assert 0 <= initial_pht_state < 2 ** pht_counter_bits, \
            f"Initial Pattern History Table (PHT) state must be in range [0, {2 ** pht_counter_bits})"
        assert 0 <= initial_bhr_state < 2 ** history_size_bits, \
            f"Initial Branch History Register (BHR) state must be in range [0, {2 ** history_size_bits})"
        assert num_pht_entries >= 2 ** history_size_bits, \
            f"The number of PHT entries must be greater than or equal to the number of history bits"

        self.bhr = [initial_bhr_state] * num_bhrs
        self.pht = [initial_pht_state] * num_pht_entries
        self.pc_bits = num_pht_entries - (2 ** history_size_bits)
        self.history_size_bits = history_size_bits
        self.pht_counter_bits = pht_counter_bits
        self.initial_bhr_state = initial_bhr_state
        self.initial_pht_state = initial_pht_state

    def predict(self, opcode: str, current_pc: int, target_pc: int) -> Predict:
        bhr_index = current_pc % len(self.bhr)
        history = self.bhr[bhr_index]
        pht_index = ((history << self.pc_bits) | (current_pc & ((2 ** self.pc_bits) - 1))) % len(self.pht)
        pht_state = self.pht[pht_index]
        return Predict.TAKEN if pht_state >= 2 ** (self.pht_counter_bits - 1) else Predict.NOT_TAKEN

    def update(self, opcode: str, current_pc: int, target_pc: int, result: Predict):
        bhr_index = current_pc % len(self.bhr)
        history = self.bhr[bhr_index]
        pht_index = ((history << self.pc_bits) | (current_pc & ((2 ** self.pc_bits) - 1))) % len(self.pht)
        pht_state = self.pht[pht_index]

        if result == Predict.TAKEN:
            self.pht[pht_index] = min(pht_state + 1, (2 ** self.pht_counter_bits) - 1)
        else:
            self.pht[pht_index] = max(pht_state - 1, 0)

        history <<= 1
        history |= 1 if result == Predict.TAKEN else 0
        history &= (2 ** self.history_size_bits) - 1
        self.bhr[bhr_index] = history

    def reset(self):
        self.bhr = [self.initial_bhr_state] * len(self.bhr)
        self.pht = [self.initial_pht_state] * len(self.pht)
