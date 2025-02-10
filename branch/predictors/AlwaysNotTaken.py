from . import AbstractBasePredictor, Predict


class AlwaysNotTaken(AbstractBasePredictor):
    """
    A static predictor that assumes no branches are ever taken.
    """
    def __init__(self, **kwargs):
        super().__init__()

    def predict(self, opcode: str, current_pc: int, target_pc: int) -> Predict:
        return Predict.NOT_TAKEN

    def update(self, opcode: str, current_pc: int, target_pc: int, result: Predict):
        return

    def reset(self):
        return
