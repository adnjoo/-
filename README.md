# 🧠 Emergent Cellular Automaton (CA)

This is a minimal Python simulation of a 2D emergent system, inspired by biological cellular automata, neural activity, and artificial life.

## 🌱 Features

- **5-channel float grid**
  - Channel 0: Structure
  - Channel 1: Support
  - Channel 2: Memory (persistent trace)
  - Channel 3: Oscillator (heartbeat)
  - Channel 4: Identity mask (fixed cell types)
- **Convolution-based updates**
- **Memory-action feedback loop**
- **Inertia (to create smooth temporal transitions)**
- **Spontaneous energy injections**
- **Contrast-stretched RGB visualization**

## 🧪 Installation

```bash
pip install -r requirements.txt
````

## ▶️ Run the Simulation

```bash
python a.py
```

A `matplotlib` window will open and animate the evolving CA.

## 📦 Dependencies

* `numpy`
* `scipy`
* `matplotlib`

These are listed in `requirements.txt`.

## 📸 Screenshot

*(Optional: insert a screenshot here using `![](screenshot.png)`)*

## 📚 Inspired By

* Neural cellular automata (Google Brain)
* Turing patterns & morphogenesis
* Synthetic biology + minimal cognition

---

Pull requests and mutations welcome.
