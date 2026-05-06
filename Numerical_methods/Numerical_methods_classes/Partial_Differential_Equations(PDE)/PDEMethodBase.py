import numpy as np
from BaseMethod import NumericalMethod

class PDEMethodBase(NumericalMethod):
    def __init__(self, name: str):
        super().__init__(name)
        self.u = None
        self.x = None
        self.t = None
        self.dx = None
        self.dt = None


    def solve(self, f_init, f_bound, x_domain, t_domain, nx: int, nt: int):
        """
        f_init(x): начальное условие u(x,0)
        f_bound(t): граничные условия (можно сделать абстрактнее)
        x_domain = (x0, xL)
        t_domain = (t0, tEnd)
        """
        raise NotImplementedError


    def get_solution(self):
        return self.x, self.t, self.u

    def compute_error(self, u_exact, L):
        """
        u_exact(x, t, L): аналитическое решение u(x,t).
        self.u : shape (nt+1, nx+1), порядок (t, x)
        """
        if self.u is None or self.x is None or self.t is None:
            raise ValueError("Сначала вызови solve().")

        nt_plus_1, nx_plus_1 = self.u.shape

        # сетка
        T, X = np.meshgrid(self.t, self.x, indexing="ij")  # (nt+1, nx+1)

        u_ex = u_exact(X, T, L)
        err = np.abs(self.u - u_ex)
        abs_err = np.abs(err)

        max_abs_error = np.max(abs_err)
        l2_abs_error = np.sqrt(np.mean(abs_err ** 2))

        abs_u_ex = np.abs(u_ex)
        max_u_ex = np.max(abs_u_ex)
        l2_u_ex = np.sqrt(np.mean(abs_u_ex ** 2))

        max_rel_error = max_abs_error / max_u_ex if max_u_ex != 0 else np.nan
        l2_rel_error = l2_abs_error / l2_u_ex if l2_u_ex != 0 else np.nan

        return {
            "max_abs_error": max_abs_error,
            "l2_abs_error": l2_abs_error,
            "max_rel_error": max_rel_error,
            "l2_rel_error": l2_rel_error,
            "error_field": err,
        }

    def compute_error_slice(self, u_exact, L, axis="y", index=None):
        """
        Если self.u имеет форму
          (nt+1, nx+1)  -> считаем 1D-ошибку напрямую.
          (nt+1, ny+1, nx+1) -> берём срез по axis (x или y) и считаем ошибку.
        """
        if self.u.ndim == 2:
            u_slice = self.u  # (nt+1, nx+1)
            x = self.x
        elif self.u.ndim == 3:
            nt1, ny1, nx1 = self.u.shape
            if axis == "y":
                if index is None:
                    index = ny1 // 2
                u_slice = self.u[:, index, :]  # (nt+1, nx+1)
                x = self.x
            else:
                # по x-срезу аналогично
                ...
        else:
            raise ValueError("Неожиданная размерность self.u")

        T, X = np.meshgrid(self.t, x, indexing="ij")
        u_ex = u_exact(X, T, L)

        err = np.abs(u_slice - u_ex)
        abs_err = np.abs(err)
        max_abs_error = np.max(abs_err)
        l2_abs_error = np.sqrt(np.mean(abs_err ** 2))

        abs_u_ex = np.abs(u_ex)
        max_u_ex = np.max(abs_u_ex)
        l2_u_ex = np.sqrt(np.mean(abs_u_ex ** 2))

        max_rel_error = max_abs_error / max_u_ex if max_u_ex != 0 else np.nan
        l2_rel_error = l2_abs_error / l2_u_ex if l2_u_ex != 0 else np.nan

        return {
            "max_abs_error": max_abs_error,
            "l2_abs_error": l2_abs_error,
            "max_rel_error": max_rel_error,
            "l2_rel_error": l2_rel_error,
            "error_field": err,
        }
