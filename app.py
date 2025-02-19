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
mass = st.sidebar.slider("Mass of the Object (kg)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# Compute position, velocity, and force at a given time
def compute_motion(radius, angular_velocity, initial_phase, time, mass):
    x = radius * np.cos(angular_velocity * time + initial_phase)
    y = radius * np.sin(angular_velocity * time + initial_phase)
    vx = -radius * angular_velocity * np.sin(angular_velocity * time + initial_phase)
    vy = radius * angular_velocity * np.cos(angular_velocity * time + initial_phase)
    fx = -mass * x * angular_velocity**2
    fy = -mass * y * angular_velocity**2
    return x, y, vx, vy, fx, fy

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
velocity_arrow = ax.quiver(0, 0, 0, 0, angles='xy', scale_units='xy', scale=0.1, color='green', label='Velocity')
force_arrow = ax.quiver(0, 0, 0, 0, angles='xy', scale_units='xy', scale=1, color='purple', label='Force')
ax.legend()

# Placeholder for updating plot
plot_placeholder = st.empty()
info_placeholder = st.empty()

# Run animation
start_button = st.button("Start Simulation")

if start_button:
    t = 0  # Time starts at 0
    dt = 0.01 / simulation_speed  # Time step based on simulation speed

    while True:
        x, y, vx, vy, fx, fy = compute_motion(radius, angular_velocity, initial_phase, t, mass)

        # Update particle position and arrows
        particle.set_data([x], [y])  # Wrap x and y in lists
        velocity_arrow.set_offsets([x, y])
        velocity_arrow.set_UVC(vx, vy)

        # Ensure force arrow points toward the center without crossing the circle
        force_magnitude = np.sqrt(fx**2 + fy**2)
        fx_adjusted = (fx / force_magnitude) * radius
        fy_adjusted = (fy / force_magnitude) * radius
        force_arrow.set_offsets([x, y])
        force_arrow.set_UVC(fx_adjusted, fy_adjusted)

        # Redraw the plot
        ax.clear()
        ax.set_xlim(-radius - 1, radius + 1)
        ax.set_ylim(-radius - 1, radius + 1)
        ax.set_aspect('equal')
        ax.grid()

        # Re-add elements
        ax.add_artist(plt.Circle((0, 0), radius, color='blue', fill=False, linestyle='--'))
        ax.plot([x], [y], 'ro', label='Particle')
        ax.quiver(x, y, vx, vy, angles='xy', scale_units='xy', scale=0.1, color='green', label='Velocity')
        ax.quiver(x, y, fx_adjusted, fy_adjusted, angles='xy', scale_units='xy', scale=1, color='purple', label='Force')
        ax.legend()

        # Update plot in placeholder
        plot_placeholder.pyplot(fig)

        # Display force and velocity information
        velocity_magnitude = np.sqrt(vx**2 + vy**2)
        info_placeholder.markdown(f"**Velocity Magnitude:** {velocity_magnitude:.2f} m/s  \n**Force Magnitude:** {force_magnitude:.2f} N")

        # Increment time
        t += dt
        time.sleep(dt)
