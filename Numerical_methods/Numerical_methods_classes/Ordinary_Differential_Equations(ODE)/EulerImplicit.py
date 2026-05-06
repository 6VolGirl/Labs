import numpy as np
from scipy.optimize import fsolve
from ODEMethodBase import ODEMethodBase

class EulerImplicit(ODEMethodBase):
    """
    Неявный метод Эйлера для решения ОДУ и систем ОДУ
    """

    def __init__(self):
        super().__init__("Неявный метод Эйлера", order=1)
        self.t_values = []
        self.y_values = []
        self.steps_performed = 0

    def solve(self, f, t0: float, t_end: float, y0, h: float):
        """
        Решение ОДУ (системы) dy/dt = f(t, y) неявным методом Эйлера

        Формула: y_{n+1} = y_n + h * f(t_{n+1}, y_{n+1})

        - f: правая часть ОДУ
        - t0, t_end: временной интервал
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
        self.steps_performed = 0

        while t < t_end:
            if t + h > t_end:
                h = t_end - t

            t_next = t + h

            def implicit_equation(y_new):
                f_val = f(t_next, y_new)
                return y_new - y - h * np.atleast_1d(f_val)

            f_val = f(t, y)
            y_guess = y + h * np.atleast_1d(f_val)
            y_new = fsolve(implicit_equation, y_guess)

            t = t_next
            y = y_new

            self.t_values.append(t)
            self.y_values.append(float(y[0]) if is_scalar else y.copy())
            self.steps_performed += 1

        self.t_values = np.array(self.t_values)
        self.y_values = np.array(self.y_values)
        self.result = (self.t_values, self.y_values)

        return self.result

    def get_solution(self):
        return self.t_values, self.y_values

# class EulerImplicit(ODEMethodBase):
#     """Неявный метод Эйлера"""
#
#     def __init__(self):
#         super().__init__("Неявный метод Эйлера", order=1)
#         self.t_values = []
#         self.y_values = []
#         self.steps = 0
#
#     def solve(self, f, t0: float, t_end: float, y0, h: float):
#         """
#         Решение ОДУ dy/dt = f(t, y) неявным методом Эйлера
#
#         Формула: y_{n+1} = y_n + h * f(t_{n+1}, y_{n+1})
#
#         - f: правая часть ОДУ, функция f(t, y)
#         - t0: начальное время
#         - t_end: конечное время
#         - y0: начальное условие
#         - h: шаг интегрирования
#         """
#         # неправильно распознавались просто числа
#         is_scalar = np.isscalar(y0) or (isinstance(y0, np.ndarray) and y0.size == 1)
#
#         if is_scalar:
#             y0_work = float(y0)
#         else:
#             y0_work = np.atleast_1d(y0).copy()
#
#         self._validate_ode_params(t0, t_end, np.atleast_1d(y0), h)
#
#
#         y0 = np.atleast_1d(y0)  #лучше чем array
#         self._validate_ode_params(t0, t_end, y0, h)
#
#         t = t0
#         y = y0_work
#
#         self.t_values = [t]
#         self.y_values = [float(y) if is_scalar else y.copy()]  #[np.atleast_1d(y.copy())]
#         self.steps = 0
#
#         while t < t_end:
#             if t + h > t_end:
#                 h = t_end - t
#
#             t_next = t + h
#
#             def implicit_equation(y_new):
#                 """Уравнение для fsolve"""
#                 return y_new - y - h * f(t_next, y_new)
#
#             # Начальное приближение
#             y_guess = y + h * f(t, y)
#             y_new = fsolve(implicit_equation, y_guess)
#
#             if is_scalar:
#                 y_new = float(y_new[0])  # Для скаляра: берем первый элемент
#             else:
#                 y_new = y_new
#
#             t = t_next
#             y = y_new
#
#             self.t_values.append(t)
#             self.y_values.append(float(y) if is_scalar else y.copy())     #np.atleast_1d(y.copy()))
#             self.steps += 1
#
#         self.t_values = np.array(self.t_values)
#         self.y_values = np.array(self.y_values)
#         self.result = (self.t_values, self.y_values)
#
#         print(f"\n{self.name}: выполнено {self.steps} шагов")
#
#         return self.t_values, self.y_values
#
#     def get_solution(self):
#         """Возвращает полное решение"""
#         return self.t_values, self.y_values
