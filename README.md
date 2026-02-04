# Second-Order Dynamic System Step Response Simulator

This project models and analyzes the response of a second-order dynamic system to a unit-step input:

<img width="419" height="84" alt="image" src="https://github.com/user-attachments/assets/850784ef-fa5b-4d1d-b368-a36d2763d141" />

---

## Damping Conditions

The tool evaluates system behavior under all damping conditions:

- Underdamped  
- Critically damped  
- Overdamped  

---

## Features

It provides:

- Analytical closed-form solutions for each damping case  
- Numerical approximations using:
  - Euler Method  
  - 4th-order Runge–Kutta (RK4) Method  
- Automatic adaptive time-step refinement based on RMS error thresholds  
- Interactive GUI built with **Matplotlib widgets** for real-time parameter input  
- Graphical comparison of analytical vs numerical responses  

---

## Technologies Used

- Python  
- NumPy  
- Matplotlib  
- Matplotlib Widgets (TextBox, Button)  
- Numerical Integration Methods (Euler & RK4)  

---

## Important Note

This project was developed as part of the **Real-Time System Design Course Laboratory Work**.

---
