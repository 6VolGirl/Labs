import numpy as np
from ODEMethodBase import ODEMethodBase
import sys
sys.path.append ("C:\\Users\\6anna\\PycharmProjects\\Labs\\Numerical_methods\\Numerical_methods_classes\\Nonlinear_Equations")
from NewtonMethod import NewtonMethod
from RungeKuttaMethod import RungeKuttaMethod


class GearMethod(ODEMethodBase):
    BDF_COEFFICIENTS = {
        1: {'a': [1, -1], 'b': 1},
        2: {'a': [3, -4, 1], 'b': 2},
        3: {'a': [11, -18, 9, -2], 'b': 6},
        4: {'a': [25, -48, 36, -16, 3], 'b': 12}
    }

    def __init__(self, name: str = "BDF", order: int = 2, integration_method = RungeKuttaMethod, integration_order: int = 4):
        if order < 1 or order > 4:
            raise ValueError(f"Порядок должен быть от 1 до 4, получен {order}")
        super().__init__(name, order)
        self.order = order
        self.t_values = []
        self.y_values = []
        self.steps = 0
        self.newton_iterations = []
        self.integration_method = integration_method
        self.integration_order = integration_order

    def solve(self, f, t0: float, t_end: float, y0, h: float,
              tol_newton: float = 1e-8, max_newton_iter: int = 20, **kwargs):
        y0 = np.atleast_1d(y0).astype(float)
        dim = len(y0)
        is_scalar = (dim == 1)
        self._validate_ode_params(t0, t_end, y0, h)

        self.t_values = [t0]
        self.y_values = [y0.copy()]
        self.steps = 0
        self.newton_iterations = []

        t = t0
        y = y0.copy()
        y_history = [y.copy()]

        test = self.order

        if self.order > 1:
            solver = self.integration_method(order = self.integration_order)
            for s in range(1, self.order):
                if t >= t_end - 1e-10:
                    break

                # Интервал для RK
                h_startup = min(h, t_end - t)
                t_startup = t + h_startup

                t_vals, y_vals = solver.solve(f, t, t_startup, y, h_startup)

                y = np.atleast_1d(y_vals[-1]).astype(float)
                t = t_vals[-1]
                y_history.append(y.copy())
                self.t_values.append(t)
                self.y_values.append(y.copy())
                self.steps += 1

        a = self.BDF_COEFFICIENTS[self.order]['a']
        b = self.BDF_COEFFICIENTS[self.order]['b']


        while t < t_end - 1e-10:
            h_actual = min(h, t_end - t)

            linear_part = np.zeros(dim)
            hist_cut = y_history[-self.order:]

            for i in range(1, len(a)):
                idx = len(hist_cut) - i
                if idx >= 0:
                    linear_part += a[i] * hist_cut[idx]

            t_new = t + h_actual

            # Неявное уравнение
            def g(y_new):
                y_new = np.atleast_1d(y_new).astype(float)
                f_val = np.atleast_1d(f(t_new, y_new)).astype(float)
                return a[0] * y_new + linear_part - h_actual * b * f(t_new, y_new)

            #Якобиан
            def dg(y_new):
                y_new = np.atleast_1d(y_new).astype(float)
                eps = 1e-8
                g_y = g(y_new)
                jac = np.zeros((dim, dim))

                for j in range(dim):
                    y_eps = y_new.copy()
                    y_eps[j] += eps
                    g_y_eps = g(y_eps)
                    jac[:, j] = (g_y_eps - g_y) / eps

                return jac

            newton = NewtonMethod()
            y_new = newton.solve(hist_cut[-1], g, dg, tol=tol_newton, max_iter=max_newton_iter)
            y_new = np.asarray(y_new)

            self.newton_iterations.append(newton.iterations)

            y_history.append(y_new.copy())
            if len(y_history) > self.order:
                y_history.pop(0)

            t = t_new
            y = y_new
            self.t_values.append(t)
            self.y_values.append(y_new.copy())
            self.steps += 1

        self.t_values = np.array(self.t_values)

        y_unified = [np.atleast_1d(np.asarray(y)).flatten() for y in self.y_values]

        if is_scalar:
            self.y_values = np.array([y[0] for y in y_unified])
        else:
           self.y_values = np.array(y_unified)

        self.result = (self.t_values, self.y_values)
        return self.result

