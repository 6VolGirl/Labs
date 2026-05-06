import numpy as np
from ODEMethodBase import ODEMethodBase

class EulerExplicit(ODEMethodBase):
    """
    Явный метод Эйлера для решения ОДУ и систем ОДУ
    """

    def __init__(self):
        super().__init__("Явный метод Эйлера", order=1)
        self.t_values = []
        self.y_values = []
        self.steps = 0

    def solve(self, f, t0: float, t_end: float, y0, h: float):
        """
        Решение ОДУ (системы) dy/dt = f(t, y) явным методом Эйлера

        Формула: y_{n+1} = y_n + h * f(t_n, y_n)

        - f: правая часть ОДУ, функция f(t, y)
          - Для скалярного ОДУ: f(t, y) возвращает число
          - Для системы: f(t, y) возвращает вектор
        - t0: начальное время
        - t_end: конечное время
        - y0: начальное условие
          - Скаляр для скалярного ОДУ
          - Вектор (список/массив) для системы
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

            f_val = f(t, y)
            y_new = y + h * np.atleast_1d(f_val)

            t = t + h
            y = y_new

            self.t_values.append(t)
            self.y_values.append(float(y[0]) if is_scalar else y.copy())
            self.steps += 1

        self.t_values = np.array(self.t_values)
        self.y_values = np.array(self.y_values)
        self.result = (self.t_values, self.y_values)

        return self.t_values, self.y_values

    def get_solution(self):
        return self.t_values, self.y_values

