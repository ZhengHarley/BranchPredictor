from . import AbstractBasePredictor, Predict


class AlwaysTaken(AbstractBasePredictor):
    """
    A static predictor that assumes all branches are always taken.
    """
    def __init__(self, **kwargs):
        super().__init__()

    def predict(self, opcode: str, current_pc: int, target_pc: int) -> Predict:
        return Predict.TAKEN

    def update(self, opcode: str, current_pc: int, target_pc: int, result: Predict):
        return

    def reset(self):
        return
