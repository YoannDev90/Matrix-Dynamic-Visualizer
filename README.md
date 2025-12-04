# Linear Transformation Visualizer

An interactive Python application for visualizing 2D linear transformations using Pygame.

## Features

- Interactive matrix editing with keyboard controls
- Real-time visualization of transformations on a square
- Dynamic grid with coordinate labels
- Pan and zoom controls (keyboard and mouse)
- Resizable window
- Auto-adjust view to fit content

## Controls

- **Q/W**: Adjust matrix element (0,0) (+/-)
- **E/T**: Adjust matrix element (0,1) (+/-)
- **A/S**: Adjust matrix element (1,0) (+/-)
- **D/F**: Adjust matrix element (1,1) (+/-)
- **R**: Reset matrix to identity
- **Arrow keys**: Pan view
- **= / -**: Zoom in/out
- **Mouse wheel**: Zoom towards cursor
- **Space**: Auto-adjust view
- **Escape**: Quit

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/linear-transformation-visualizer.git
   cd linear-transformation-visualizer
   ```

2. Install dependencies:

   ```bash
   pip install pygame numpy
   ```

3. Run the application:

   ```bash
   python transformation_visualizer.py
   ```

## Usage

The application displays a square and its transformation by the current matrix. Use the keyboard controls to modify the matrix elements and see the transformation in real-time. The grid helps visualize the coordinate system.

## License

MIT License - see LICENSE file for details.
