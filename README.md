# Second-Order Dynamic System Step Response Simulator

<img width="554" height="275" alt="5 6" src="https://github.com/user-attachments/assets/052da141-4b53-4383-afc8-9908cc438abe" />
<img width="554" height="283" alt="5 7" src="https://github.com/user-attachments/assets/6cde74d7-43ed-4150-8882-0d199601f1d9" />


This project models and analyzes the response of a second-order dynamic system to a unit-step input:

<img width="365" height="59" alt="image" src="https://github.com/user-attachments/assets/be515f29-0056-4b4a-8f85-d286b6686533" />

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
