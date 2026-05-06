import numpy as np
from ODEMethodBase import ODEMethodBase
from RungeKuttaMethod import RungeKuttaMethod

import numpy as np
from typing import Callable, Tuple, Optional


class AdamsBashforthMoulton(ODEMethodBase):
    """ Метод прогноз-коррекция Адамса-Башфорта-Моултона 1-4 порядка """

    PREDICTOR_COEFFS = {
        1: (1, [1]),
        2: (2, [3, -1]),
        3: (12, [23, -16, 5]),
        4: (24, [55, -59, 37, -9])
    }
    CORRECTOR_COEFFS = {
        1: (1, [1]),
        2: (2, [1, 1]),
        3: (12, [5, 8, -1]),
        4: (24, [9, 19, -5, 1])
    }

    def __init__(self, order: int = 3, max_iterations: int = 1):
        """
        - order: порядок метода (1, 2, 3 или 4)
        - max_iterations: максимальное число итераций коррекции
        """
        if order not in [1, 2, 3, 4]:
            raise ValueError(f"Порядок метода должен быть 1, 2, 3 или 4. Получено: {order}")

        super().__init__(name=f"Adams-Bashforth-Moulton (order {order})", order=order)

        self.max_iterations = max_iterations
        self.t_values = None
        self.y_values = None
        self.iterations_used = []
        self.pred_denom, self.pred_coeffs = self.PREDICTOR_COEFFS[order]
        self.corr_denom, self.corr_coeffs = self.CORRECTOR_COEFFS[order]

    def _compute_initial_values(self, f, t0: float, y0: np.ndarray, h: float, steps_needed: int):
        """
        Вычисление начальных значений методом Рунге-Кутты

        - steps_needed: количество начальных шагов (равно порядку метода)
        """
        t_init = [t0]
        y_init = [y0.copy()]

        for i in range(steps_needed):
            t_current = t_init[-1]
            y_current = y_init[-1]

            rk_4 = RungeKuttaMethod(order = 4)
            y_next = rk_4.single_step(f, t_current, y_current, h)
            t_next = t_current + h

            t_init.append(t_next)
            y_init.append(y_next)

        return t_init, y_init

    def _predictor_step(self, f_values: list, y_n: np.ndarray, h: float) -> np.ndarray:
        """ Шаг предиктора """
        # f_values = [f_n, f_{n-1}, ..., f_{n-k+1}]
        sum_term = sum(coeff * f_val for coeff, f_val in zip(self.pred_coeffs, f_values))
        y_pred = y_n + (h / self.pred_denom) * sum_term
        return y_pred

    def _corrector_step(self, f_pred: np.ndarray, f_values: list, y_n: np.ndarray, h: float) -> np.ndarray:
        """ Шаг корректора """
        sum_term = self.corr_coeffs[0] * f_pred

        for i, coeff in enumerate(self.corr_coeffs[1:], start=0):
            sum_term += coeff * f_values[i]

        y_corr = y_n + (h / self.corr_denom) * sum_term
        return y_corr

    def solve(self, f: Callable, t0: float, t_end: float, y0: float,
              h: float) -> Tuple[np.ndarray, np.ndarray]:
        """ Решение задачи Коши методом Адамса-Башфорта-Моултона """

        y0_array = self._initialize_vector(None, y0)
        self._validate_ode_params(t0, t_end, y0_array, h)

        steps_needed = self.order
        t_list, y_list = self._compute_initial_values(f, t0, y0_array, h, steps_needed)

        f_history = [f(t, y) for t, y in zip(t_list, y_list)]
        t_current = t_list[-1]

        while t_current < t_end - 1e-12:
            t_next = t_current + h
            y_n = y_list[-1]

            f_prev = f_history[-self.order:]
            y_pred = self._predictor_step(f_prev, y_n, h)
            f_pred = f(t_next, y_pred)
            y_corr = y_pred.copy()
            iterations = 0

            for iteration in range(self.max_iterations):
                y_corr_old = y_corr.copy()
                f_corr = f(t_next, y_corr)

                y_corr = self._corrector_step(f_corr, f_prev, y_n, h)
                iterations += 1

                if np.linalg.norm(y_corr - y_corr_old) < 1e-12:
                    break

            self.iterations_used.append(iterations)
            t_list.append(t_next)
            y_list.append(y_corr)
            f_history.append(f(t_next, y_corr))

            t_current = t_next

        self.t_values = np.array(t_list)
        self.y_values = np.array(y_list)


        if self.y_values.shape[1] == 1:     #Скаляр
            self.y_values = self.y_values.flatten()
        self.result = (self.t_values, self.y_values)

        return self.t_values, self.y_values

    def get_iteration_statistics(self) -> dict:
        """ Получение статистики по числу итераций коррекции """
        if not self.iterations_used:
            return {}

        return {
            'mean_iterations': np.mean(self.iterations_used),
            'max_iterations': np.max(self.iterations_used),
            'min_iterations': np.min(self.iterations_used),
            'total_corrector_calls': sum(self.iterations_used)
        }




