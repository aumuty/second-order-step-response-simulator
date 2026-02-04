import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button

# ---------- math ----------
def wn(a0):                     # ωn = 1/sqrt(a0)
    return 1.0 / np.sqrt(a0)

def analytic(a0, a1, b, t):
    s = a1 / 2.0
    y_inf = b / a0
    disc = a1*a1 - 4.0*a0
    if disc < -1e-12:                      # Case 1 (under-damped)
        w = np.sqrt(a0 - (a1*a1)/4.0)
        y = y_inf * (1 - np.exp(-s*t)*(np.cos(w*t) + (s/w)*np.sin(w*t)))
        case = 1
    elif abs(disc) <= 1e-12:               # Case 2 (critical)
        y = y_inf * (1 - np.exp(-s*t)*(1 + s*t))
        case = 2
    else:                                   # Case 3 (over-damped)
        r  = np.sqrt(s*s - a0)
        r1 = -s + r
        r2 = -s - r
        A = r2/(r2 - r1)
        B = -r1/(r2 - r1)
        y = y_inf * (1 + A*np.exp(r1*t) + B*np.exp(r2*t))
        case = 3
    return y, case, y_inf

def f_rhs(a0, a1, b, y, z):
    # y' = z ; z' = (b - a1*z - y)/a0  (unit step u(t)=1)
    return z, (b - a1*z - y) / a0

def euler(a0, a1, b, T, t_end):
    n = int(np.ceil(t_end / T)) + 1
    t = np.linspace(0.0, T*(n-1), n)
    y = np.zeros(n); z = np.zeros(n)
    for i in range(n-1):
        dy, dz = f_rhs(a0, a1, b, y[i], z[i])
        y[i+1] = y[i] + T*dy
        z[i+1] = z[i] + T*dz
    return t, y

def rk4(a0, a1, b, T, t_end):
    n = int(np.ceil(t_end / T)) + 1
    t = np.linspace(0.0, T*(n-1), n)
    y = np.zeros(n); z = np.zeros(n)
    for i in range(n-1):
        k1y, k1z = f_rhs(a0, a1, b, y[i], z[i])
        k2y, k2z = f_rhs(a0, a1, b, y[i]+0.5*T*k1y, z[i]+0.5*T*k1z)
        k3y, k3z = f_rhs(a0, a1, b, y[i]+0.5*T*k2y, z[i]+0.5*T*k2z)
        k4y, k4z = f_rhs(a0, a1, b, y[i]+T*k3y,   z[i]+T*k3z)
        y[i+1] = y[i] + (T/6.0)*(k1y + 2*k2y + 2*k3y + k4y)
        z[i+1] = z[i] + (T/6.0)*(k1z + 2*k2z + 2*k3z + k4z)
    return t, y

def rms(a, b):
    n = min(len(a), len(b))
    return float(np.sqrt(np.mean((a[:n]-b[:n])**2)))

# ---------- UI ----------
plt.close("all")
fig, ax = plt.subplots(figsize=(9, 5))
fig.subplots_adjust(top=0.70, left=0.08, right=0.98, bottom=0.10)

# widgets (top band)
tb_w, tb_h, top_y = 0.16, 0.08, 0.86
ax_a0 = fig.add_axes([0.08, top_y, tb_w, tb_h])
ax_a1 = fig.add_axes([0.28, top_y, tb_w, tb_h])
ax_b  = fig.add_axes([0.48, top_y, tb_w, tb_h])
ax_up = fig.add_axes([0.68, top_y, 0.12, tb_h])

tb_a0 = TextBox(ax_a0, "a₀ (>0)", initial="1.0")
tb_a1 = TextBox(ax_a1, "a₁ (>0)", initial="1.0")
tb_b  = TextBox(ax_b,  "b  (>0)", initial="1.0")
btn   = Button(ax_up, "Update")

ax.set_title("Unit-Step Response • a₀ ÿ + a₁ ẏ + y = b·u(t)")
ax.grid(True, alpha=0.3)

def parse_pos(tb):
    try:
        v = float(tb.text)
        return v if v > 0 else None
    except Exception:
        return None

def render(_=None):
    a0 = parse_pos(tb_a0)
    a1 = parse_pos(tb_a1)
    b  = parse_pos(tb_b)

    ax.cla(); ax.grid(True, alpha=0.3)
    ax.set_title("Unit-Step Response • a₀ ÿ + a₁ ẏ + y = b·u(t)")

    # Strict validation (Q1)
    if a0 is None or a1 is None or b is None:
        ax.text(0.02, 0.02, "Invalid input: require a₀>0, a₁>0, b>0",
                transform=ax.transAxes, color="#b91c1c", weight="bold")
        fig.canvas.draw_idle()
        return
    else:
        ax.text(0.02, 0.02, "Inputs OK (a₀>0, a₁>0, b>0) ✓",
                transform=ax.transAxes, color="#16a34a", weight="bold")

    w = wn(a0)
    T0 = 0.1 * (2*np.pi / w)        # Q5 rule: initial step from formula
    T  = T0
    t_end = max(6.0, 6.0 / w)

    # Analytic reference
    t_dense = np.linspace(0, t_end, 2001)
    ya, case, yinf = analytic(a0, a1, b, t_dense)

    # Auto-halving (Q7)
    tried = 0
    while True:
        te, ye = euler(a0, a1, b, T, t_end)
        tr, yr = rk4(a0, a1, b, T, t_end)
        ya_e = np.interp(te, t_dense, ya)
        ya_r = np.interp(tr, t_dense, ya)
        err_e = rms(ya_e, ye)
        err_r = rms(ya_r, yr)
        if (err_e <= 1e-3 and err_r <= 1e-3) or tried >= 5:
            break
        T *= 0.5
        tried += 1

    # Plot
    ax.plot(t_dense, ya, lw=2.0, label="Analytic")
    ax.plot(te, ye, ".", ms=3, label=f"Euler (T={T:.3g})")
    ax.plot(tr, yr, "-", lw=1.2, label=f"RK4 (T={T:.3g})")
    ax.axhline(yinf, ls="--", lw=1.0, label="b/a₀")
    ax.set_xlabel("Time (s)"); ax.set_ylabel("y(t)")
    ax.legend(loc="best")

    # Case badge (bottom-right) + Q5 rule text (top-left)
    names = {1:"Case 1 – Under-damped", 2:"Case 2 – Critically-damped", 3:"Case 3 – Over-damped"}
    ax.text(0.98, 0.02,
            f"{names[case]}\nωₙ={w:.4g}  y(∞)={yinf:.4g}\n"
            f"T₀={T0:.4g}  T(final)={T:.4g}  halves={tried}\n"
            f"RMS(E)={err_e:.2e}  RMS(RK4)={err_r:.2e}",
            transform=ax.transAxes, ha="right", va="bottom",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.95, lw=0.6))

    # *** Q5 rule shown explicitly ***
    ax.text(0.02, 0.98,
            "Rule (Q5):  T₀ = 0.1 × 2π / ωₙ   with   ωₙ = 1/√a₀",
            transform=ax.transAxes, ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9, lw=0.6))

    fig.canvas.draw_idle()

tb_a0.on_submit(render)
tb_a1.on_submit(render)
tb_b.on_submit(render)
btn.on_clicked(render)

render()
plt.show()

    
