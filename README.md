# SVG_Noise.py

SVG_Noise.py is a command-line tool that generates SVG noise patterns for creating beautiful grainy gradients in web design. This tool creates SVG files containing turbulence filters that can be directly referenced in CSS to achieve texture effects like grainy gradients, paper textures, and more.

## Table of Contents

- [What is SVG Noise?](#what-is-svg-noise)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Command Line Options](#command-line-options)
- [Usage Examples](#usage-examples)
- [Using in CSS](#using-in-css)
- [Advanced Techniques](#advanced-techniques)
- [License](#license)

## What is SVG Noise?

SVG Noise utilizes the SVG `<feTurbulence>` filter primitive to generate Perlin noise patterns. When combined with CSS filters and blend modes, these patterns can create stunning grainy gradient effects that add texture and depth to web designs.

The core technique involves:
1. Generating an SVG with a noise filter
2. Using the SVG as a background image in CSS
3. Layering gradients on top of the noise
4. Enhancing with CSS filters like contrast and brightness
5. Further refining with CSS blend modes

## Installation

### Prerequisites

- Python 3.6 or higher

### Installation Steps

1. Clone or download this repository:
   ```bash
   git clone https://github.com/MushroomFleet/SVG-Noise-cli
   cd svg-noise
   ```

2. Make the script executable (on Unix-based systems):
   ```bash
   chmod +x SVG_Noise.py
   ```

3. Install dependencies (if needed):
   ```bash
   pip install -r requirements.txt
   ```
   Note: This tool uses only standard Python libraries, so no additional packages are required.

## Basic Usage

Generate a basic SVG noise pattern with default settings:

```bash
python SVG_Noise.py --output noise.svg
```

This will create a 300x300 pixel SVG file with fractal noise using default parameters.

## Command Line Options

SVG_Noise.py offers numerous options to customize your noise patterns:

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output SVG file path | `noise.svg` |
| `--width` | `-w` | Width of the SVG in pixels | `300` |
| `--height` | `-ht` | Height of the SVG in pixels | `300` |
| `--type` | `-t` | Type of noise (`fractalNoise` or `turbulence`) | `fractalNoise` |
| `--frequency` | `-f` | Base frequency of the noise (0.1-1.0) | `0.65` |
| `--octaves` | `-oct` | Number of octaves for the noise (1-5) | `3` |
| `--seed` | `-s` | Seed for the noise generation | `None` (random) |
| `--base-color` | `-bc` | Base color for the noise in hex format | `#ffffff` |
| `--opacity` | `-op` | Opacity of the noise overlay (0.0-1.0) | `0.8` |
| `--gradient` | `-g` | Add a linear gradient to the SVG | `False` |
| `--gradient-colors` | `-gc` | Colors for gradient in hex format | `#ff0080 #0080ff` |
| `--gradient-angle` | `-ga` | Angle of gradient in degrees | `45` |
| `--inline-css` | `-css` | Include CSS for contrast/brightness | `False` |
| `--contrast` | `-c` | Contrast percentage for inline CSS | `170` |
| `--brightness` | `-b` | Brightness percentage for inline CSS | `1000` |

## Usage Examples

### Basic Noise Pattern

Generate a simple noise pattern:

```bash
python SVG_Noise.py --output basic-noise.svg
```

### Custom Dimensions

Create a larger noise pattern:

```bash
python SVG_Noise.py --output large-noise.svg --width 800 --height 600
```

### Different Noise Types

Generate turbulence-type noise instead of fractal noise:

```bash
python SVG_Noise.py --output turbulence.svg --type turbulence
```

### Adjusting Noise Parameters

Fine-tune the noise appearance:

```bash
python SVG_Noise.py --output fine-noise.svg --frequency 0.9 --octaves 4
```

```bash
python SVG_Noise.py --output coarse-noise.svg --frequency 0.4 --octaves 2
```

### With Fixed Seed

Create reproducible noise patterns with a fixed seed:

```bash
python SVG_Noise.py --output fixed-noise.svg --seed 42
```

### Changing Base Color and Opacity

Change the underlying color and noise opacity:

```bash
python SVG_Noise.py --output colored-noise.svg --base-color "#f5f5f5" --opacity 0.6
```

### Adding Gradients

Include a gradient in the SVG:

```bash
python SVG_Noise.py --output gradient-noise.svg --gradient
```

With custom gradient colors:

```bash
python SVG_Noise.py --output custom-gradient.svg --gradient --gradient-colors "#ff0080" "#0080ff" "#00ff80"
```

Adjust gradient angle:

```bash
python SVG_Noise.py --output angled-gradient.svg --gradient --gradient-angle 135
```

### Including Inline CSS

Add contrast and brightness filters directly in the SVG:

```bash
python SVG_Noise.py --output enhanced-noise.svg --inline-css
```

With custom contrast and brightness:

```bash
python SVG_Noise.py --output custom-enhanced.svg --inline-css --contrast 200 --brightness 800
```

### Combining Multiple Options

Create a highly customized noise pattern:

```bash
python SVG_Noise.py --output custom-complete.svg --width 1200 --height 800 \
  --type fractalNoise --frequency 0.75 --octaves 4 --seed 123 \
  --base-color "#121212" --opacity 0.7 \
  --gradient --gradient-colors "#6b46c1" "#e9d8fd" "#4299e1" --gradient-angle 60 \
  --inline-css --contrast 180 --brightness 900
```

## Using in CSS

After generating your SVG noise file, you can use it in CSS in several ways:

### Basic Background

```css
.noise-background {
  background-image: url('path/to/noise.svg');
}
```

### With Gradient Overlay

```css
.grainy-gradient {
  background: 
    linear-gradient(45deg, #ff0080, #0080ff),
    url('path/to/noise.svg');
  filter: contrast(170%) brightness(1000%);
}
```

### With CSS Blending

```css
.noise-with-blending {
  position: relative;
  isolation: isolate;
}

.noise-with-blending::before {
  content: "";
  position: absolute;
  inset: 0;
  background: 
    linear-gradient(45deg, #ff0080, #0080ff),
    url('path/to/noise.svg');
  filter: contrast(170%) brightness(1000%);
}

.noise-with-blending::after {
  content: "";
  position: absolute;
  inset: 0;
  background: #f8f0fc;
  mix-blend-mode: color;
  opacity: 0.3;
}
```

### Multi-Color Transitions

```css
.multi-color-gradient {
  background: 
    linear-gradient(to right, rgba(255, 0, 128, 0.7) 0%, rgba(255, 0, 128, 0) 50%),
    linear-gradient(to right, rgba(0, 128, 255, 0) 50%, rgba(0, 128, 255, 0.7) 100%),
    url('path/to/noise.svg');
  filter: contrast(170%) brightness(1000%);
}
```

## Advanced Techniques

### Layering Multiple Noise Patterns

For more complex textures, you can layer multiple noise patterns with different frequencies:

```css
.layered-noise {
  background: 
    linear-gradient(45deg, rgba(255, 0, 128, 0.7), rgba(0, 128, 255, 0.7)),
    url('path/to/fine-noise.svg'),
    url('path/to/coarse-noise.svg');
  background-blend-mode: overlay, multiply;
  filter: contrast(170%) brightness(800%);
}
```

### Animated Gradients

Create dynamic effects by animating properties:

```css
@keyframes rotate-hue {
  0% { filter: contrast(170%) brightness(1000%) hue-rotate(0deg); }
  100% { filter: contrast(170%) brightness(1000%) hue-rotate(360deg); }
}

.animated-noise {
  background: 
    linear-gradient(to right, rgba(255, 0, 128, 0.7), rgba(0, 128, 255, 0.7)),
    url('path/to/noise.svg');
  background-blend-mode: overlay;
  animation: rotate-hue 10s linear infinite;
}
```

### Text Effects

Apply noise to text using background-clip:

```css
.grainy-text {
  font-size: 48px;
  font-weight: 900;
  background: linear-gradient(to right, #f00, #00f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: contrast(170%) brightness(150%);
  position: relative;
  z-index: 1;
}

.grainy-text::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('path/to/noise.svg');
  mix-blend-mode: overlay;
  z-index: -1;
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Created by [Your Name]
