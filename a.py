import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import convolve2d

# === PARAMETERS ===
grid_size = 32
num_channels = 5  # 0: structure, 1: support, 2: memory, 3: oscillator, 4: identity mask
num_ticks = 300
decay_rate = 0.01
inertia = 0.85

# === CONVOLUTION KERNEL ===
kernel = np.array([
    [0.0,  0.25, 0.0],
    [0.25, 0.0,  0.25],
    [0.0,  0.25, 0.0]
], dtype=np.float32)

# === INITIAL STATE ===
grid = np.random.rand(grid_size, grid_size, num_channels).astype(np.float32)

# Cell identity mask: fixed "type" channel, 0 or 1
identity_mask = (np.random.rand(grid_size, grid_size) > 0.5).astype(np.float32)
grid[:, :, 4] = identity_mask

# === UPDATE FUNCTION ===
def update(grid, tick):
    new_grid = np.copy(grid)

    # Convolutional update for channels 0–2
    for ch in range(3):
        channel = grid[:, :, ch]
        convolved = convolve2d(channel, kernel, mode='same', boundary='wrap')
        new_grid[:, :, ch] = np.tanh(channel + 0.1 * convolved - decay_rate * channel)

    # Memory reinforcement: channel 0 boosts channel 2
    new_grid[:, :, 2] = 0.98 * grid[:, :, 2] + 0.05 * grid[:, :, 0]

    # Memory feeds back into structure (loop)
    new_grid[:, :, 0] += 0.02 * new_grid[:, :, 2]

    # Oscillator channel (heartbeat)
    osc = np.sin(tick * 0.1 + np.linspace(0, np.pi * 2, grid_size)).reshape(-1, 1)
    new_grid[:, :, 3] = 0.8 * grid[:, :, 3] + 0.2 * osc

    # Identity mask modulates structural reinforcement
    new_grid[:, :, 0] += 0.03 * (grid[:, :, 4] - 0.5)

    # Energy injection if flatlining
    if np.mean(grid[:, :, 0]) < 0.3:
        x, y = np.random.randint(0, grid_size, 2)
        new_grid[x, y, :3] += np.random.normal(0, 0.4, size=3)

    # Inertia: blend with previous state
    return np.clip(inertia * grid + (1 - inertia) * new_grid, 0, 1)

# === VISUALIZATION ===
def normalize_for_display(data):
    """Contrast-stretched RGB for better visibility"""
    stretched = (data - np.min(data)) / (np.max(data) - np.min(data) + 1e-5)
    return stretched

fig, ax = plt.subplots()
im = ax.imshow(normalize_for_display(grid[:, :, :3]), vmin=0, vmax=1)
ax.set_title("Emergent CA v5 – Feedback, Identity, Persistence")

def animate(i):
    global grid
    grid = update(grid, i)
    vis = normalize_for_display(grid[:, :, :3])
    im.set_array(vis)
    return [im]

ani = FuncAnimation(fig, animate, frames=num_ticks, interval=100, blit=False)
plt.show()
