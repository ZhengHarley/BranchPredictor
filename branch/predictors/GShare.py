from . import AbstractBasePredictor, Predict
from predictors.TwoLevel import TwoLevel


class GShare(TwoLevel):
    """
    A dynamic predictor similar to the Two-Level predictor that uses the XOR of the PC address and the global BHR
    to index into a PHT. The PHT houses a bimodal saturating counter which predicts the outcome of that branch.
    """
    def __init__(self,
                 history_size_bits: int,
                 pht_counter_bits: int = 2,
                 initial_bhr_state: int = 0,
                 initial_pht_state: int = 0, **kwargs
                 ):
        super().__init__(
            num_bhrs=1,
            history_size_bits=history_size_bits,
            num_pht_entries=2 ** history_size_bits,
            pht_counter_bits=pht_counter_bits,
            initial_pht_state=initial_bhr_state,
            initial_bhr_state=initial_pht_state,
            **kwargs)
        # no need to change anything in init

    def predict(self, opcode: str, current_pc: int, target_pc: int) -> Predict:
        bhr_index = 0
        history = self.bhr[bhr_index]       # Set bhr_index to 0?           
        pht_index = ((history << self.pc_bits) ^ (current_pc & ((2 ** self.pc_bits) - 1))) % len(self.pht)
        pht_state = self.pht[pht_index]
        return Predict.TAKEN if pht_state >= 2 ** (self.pht_counter_bits - 1) else Predict.NOT_TAKEN

    def update(self, opcode: str, current_pc: int, target_pc: int, result: Predict):
        bhr_index = 0
        history = self.bhr[bhr_index]
        pht_index = ((history << self.pc_bits) ^ (current_pc & ((2 ** self.pc_bits) - 1))) % len(self.pht)
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
