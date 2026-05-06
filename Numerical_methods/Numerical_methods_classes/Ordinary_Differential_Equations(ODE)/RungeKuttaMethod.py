import numpy as np
from ODEMethodBase import ODEMethodBase

class RungeKuttaMethod(ODEMethodBase):
    """
    Метод Рунге-Кутты для решения ОДУ и систем ОДУ
    """
    RUNGE_COEFFICIENTS = {
        1: {
            'c': [0],
            'a': [[0]],
            'b': [1]
        },
        2: {
            'c': [0, 1],
            'a': [[0, 0],
                  [1, 0]],
            'b': [1 / 2, 1 / 2]
        },
        3: {
            'c': [0, 1 / 2, 1],
            'a': [[0, 0, 0],
                  [1 / 2, 0, 0],
                  [-1, 2, 0]],
            'b': [1 / 6, 2 / 3, 1 / 6]
        },
        4: {
            'c': [0, 1 / 2, 1 / 2, 1],
            'a': [[0, 0, 0, 0],
                  [1 / 2, 0, 0, 0],
                  [0, 1 / 2, 0, 0],
                  [0, 0, 1, 0]],
            'b': [1 / 6, 1 / 3, 1 / 3, 1 / 6]
        },
    }

    def __init__(self, order = 4):
        if order not in self.RUNGE_COEFFICIENTS:
            raise ValueError(f"Порядок должен быть от 1 до 5, получен {order}")
        super().__init__("Метод Рунге-Кутты {order}-го порядка", order=order)
        self.order = order
        self.tabl = self.RUNGE_COEFFICIENTS[order]
        self.t_values = []
        self.y_values = []
        self.steps = 0

    def solve(self, f, t0: float, t_end: float, y0, h: float):
        """
        Решение ОДУ методом Рунге-Кутты

        - f: правая часть ОДУ, функция f(t, y)
        - t0, t_end: промежуток времени
        - y0: начальное условие
        - h: шаг интегрирования
        """

        y0 = np.atleast_1d(y0).astype(float)
        dim = len(y0)
        is_scalar = (dim == 1)

        #self._validate_ode_params(t0, t_end, y0, h)

        a = np.array(self.tabl['a'])
        b = np.array(self.tabl['b'])
        c = np.array(self.tabl['c'])

        t = t0
        y = y0.copy()

        self.t_values = [t0]
        self.y_values = [float(y[0]) if is_scalar else y.copy()]
        self.steps = 0

        while t < t_end:
            if t + h > t_end:
                h = t_end - t

            k = []
            for i in range(self.order):
                arg_1 = t + c[i] * h
                arg_2 = y + h * sum(a[i][j]*k[j] for j in range(i))
                k_i = np.atleast_1d(f(arg_1, arg_2))
                k.append(k_i)

            y_new = y + h * sum(b[i] * k[i] for i in range(self.order))

            t += h
            y = y_new

            self.t_values.append(t)
            self.y_values.append(float(y[0]) if is_scalar else y.copy())
            self.steps += 1

        self.t_values = np.array(self.t_values)
        self.y_values = np.array(self.y_values)
        self.result = (self.t_values, self.y_values)

        return self.t_values, self.y_values

    def solve_with_precision(self, f, t0: float, t_end: float, y0, target_error=1e-6):
        """
        Решение ОДУ с автоматическим выбором шага для достижения заданной точности

        - f: правая часть ОДУ
        - t0, t_end: промежуток времени
        - y0: начальное условие
        - target_error: допустимая локальная ошибка на шаге
        """

        y0 = np.atleast_1d(y0).astype(float)
        dim = len(y0)
        is_scalar = (dim == 1)

        t = t0
        y = y0.copy()
        h = (t_end - t0) / 100 # начальный шаг

        self.t_values = [t0]
        self.y_values = [float(y[0]) if is_scalar else y.copy()]
        self.steps = 0

        accepted_steps = 0
        rejected_steps = 0

        while t < t_end - 1e-10:
            if t + h > t_end:
                h = t_end - t

            y_h = self.single_step(f, t, y, h)

            y_half_1 = self.single_step(f, t, y, h / 2)
            y_half_2 = self.single_step(f, t + h / 2, y_half_1, h / 2)

            error = np.max(np.abs(y_h - y_half_2))

            if error < target_error or h < 1e-10:
                t += h
                y = y_half_2.copy() #более точное

                self.t_values.append(t)
                self.y_values.append(float(y[0]) if is_scalar else y.copy())

                # Увеличиваем шаг, если ошибка намного меньше допуска
                if error < 0.1 * target_error:
                    h = min(h * 1.5, (t_end - t0) / 10)

                accepted_steps += 1
                self.steps += 1
            else:
                h = h / 2
                rejected_steps += 1

        self.t_values = np.array(self.t_values)
        self.y_values = np.array(self.y_values)
        self.result = (self.t_values, self.y_values)

        print(f"RK{self.order} с точностью {target_error:.0e}:")
        print(f"  Шагов принято: {accepted_steps}")
        print(f"  Шагов отклонено: {rejected_steps}")
        print(f"  Всего точек: {len(self.t_values)}")

        return self.t_values, self.y_values

    def get_solution(self):
        return self.t_values, self.y_values

    def single_step(self, f, t: float, y: np.ndarray, h: float) -> np.ndarray:
        """
        Выполнить один шаг интегрирования методом Рунге-Кутты

        - t: текущее время
        - y: текущее значение
        """
        y = np.atleast_1d(y).astype(float)

        a = np.array(self.tabl['a'])
        b = np.array(self.tabl['b'])
        c = np.array(self.tabl['c'])

        k = []
        for i in range(self.order):
            arg_1 = t + c[i] * h
            arg_2 = y + h * sum(a[i][j] * k[j] for j in range(i))
            k_i = np.atleast_1d(f(arg_1, arg_2))
            k.append(k_i)

        y_new = y + h * sum(b[i] * k[i] for i in range(self.order))

        return y_new.flatten() if len(y_new) == 1 else y_new






