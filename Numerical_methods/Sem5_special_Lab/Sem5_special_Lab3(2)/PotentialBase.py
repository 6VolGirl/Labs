class PotentialBase:
    """Базовый класс для потенциалов"""

    def __call__(self, x):
        raise NotImplementedError

    def derivative(self, x):
        """Производная потенциала"""
        raise NotImplementedError