from . import AbstractBasePredictor, Predict


class BackTakeForwardNot(AbstractBasePredictor):
    """
    A static predictor that assumes backward branches (usually loops) are taken, while forward branches
    (e.g., if conditions) are not taken.
    """
    def __init__(self, **kwargs):
        super().__init__()

    def predict(self, opcode: str, current_pc: int, target_pc: int) -> Predict:
        offset = target_pc - current_pc
        return Predict.TAKEN if offset < 0 else Predict.NOT_TAKEN

    def update(self, opcode: str, current_pc: int, target_pc: int, result: Predict):
        return

    def reset(self):
        return
