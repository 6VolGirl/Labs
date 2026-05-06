import numpy as np
from ODEMethodBase import ODEMethodBase


class ImprovedEuler(ODEMethodBase):
    """
    Усовершенствованный метод Эйлера

    Δy_i = h * f(t_i + h/2, y_i + (h/2)*f(t_i, y_i))
    y_{i+1} = y_i + Δy_i
    """

    def __init__(self):
        super().__init__("Усовершенствованный метод Эйлера (2-й порядок)", order=2)
        self.t_values = []
        self.y_values = []
        self.steps = 0

    def solve(self, f, t0: float, t_end: float, y0, h: float):
        """
        Решение ОДУ (системы) методом средней точки

        - f: правая часть ОДУ, функция f(t, y)
        - t0: начальное время
        - t_end: конечное время
        - y0: начальное условие (скаляр или вектор)
        - h: шаг интегрирования
        """
        y0 = np.atleast_1d(y0).astype(float)
        dim = len(y0)
        is_scalar = (dim == 1)

        self._validate_ode_params(t0, t_end, y0, h)

        t = t0
        y = y0.copy()

        self.t_values = [t]
        self.y_values = [float(y[0]) if is_scalar else y.copy()]
        self.steps = 0

        while t < t_end:
            if t + h > t_end:
                h = t_end - t

            k1 = np.atleast_1d(f(t, y))
            y_half = y + (h / 2.0) * k1
            k_mid = np.atleast_1d(f(t + h / 2.0, y_half))
            y_new = y + h * k_mid

            t = t + h
            y = y_new

            self.t_values.append(t)
            self.y_values.append(float(y[0]) if is_scalar else y.copy())
            self.steps += 1

        self.t_values = np.array(self.t_values)
        self.y_values = np.array(self.y_values)
        self.result = (self.t_values, self.y_values)

        #if is_scalar:
        #    print(f"\n{self.name}: скалярное ОДУ, выполнено {self.steps_performed} шагов")
        #else:
        #   print(f"\n{self.name}: система из {dim} ОДУ, выполнено {self.steps_performed} шагов")
        #print(f"Форма результата: t{self.t_values.shape}, y{self.y_values.shape}")

        return self.t_values, self.y_values

    def get_solution(self):
        """Возвращает полное решение"""
        return self.t_values, self.y_values
