import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# App title
st.title("Uniform Circular Motion Simulation")

# Sidebar for user inputs
st.sidebar.header("Simulation Parameters")
radius = st.sidebar.slider("Radius (m)", min_value=0.5, max_value=10.0, value=5.0, step=0.1)
angular_velocity = st.sidebar.slider("Angular Velocity (rad/s)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
initial_phase = st.sidebar.slider("Initial Phase (radians)", min_value=0.0, max_value=2 * np.pi, value=0.0, step=0.1)
simulation_speed = st.sidebar.slider("Simulation Speed (x Real Time)", min_value=0.5, max_value=5.0, value=1.0, step=0.1)

# Compute position at a given time
def compute_position(radius, angular_velocity, initial_phase, time):
    x = radius * np.cos(angular_velocity * time + initial_phase)
    y = radius * np.sin(angular_velocity * time + initial_phase)
    return x, y

# Animation display
st.header("Circular Motion Animation")
fig, ax = plt.subplots()
ax.set_xlim(-radius - 1, radius + 1)
ax.set_ylim(-radius - 1, radius + 1)
ax.set_aspect('equal')
ax.grid()

# Circle path
circle = plt.Circle((0, 0), radius, color='blue', fill=False, linestyle='--')
ax.add_artist(circle)

# Particle
particle, = ax.plot([], [], 'ro', label='Particle')
ax.legend()

# Run animation
start_button = st.button("Start Simulation")

if start_button:
    st.write("Press 'Stop' to end the simulation.")
    stop_button = st.button("Stop Simulation")

    t = 0  # Time starts at 0
    dt = 0.01 / simulation_speed  # Time step based on simulation speed

    while not stop_button:
        x, y = compute_position(radius, angular_velocity, initial_phase, t)

        # Update particle position
        particle.set_data([x], [y])  # Wrap x and y in lists
        ax.draw_artist(particle)

        # Display updated plot
        st.pyplot(fig)

        # Increment time
        t += dt
        time.sleep(dt)

    st.write("Simulation Stopped.")
