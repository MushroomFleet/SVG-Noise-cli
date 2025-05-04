#!/usr/bin/env python3
"""
SVG_Noise.py - A tool to generate SVG noise patterns for grainy gradients

This script generates SVG files containing noise filters that can be used
to create grainy gradient effects in CSS. The generated SVG files can be
referenced directly in CSS background properties.

Usage:
    python SVG_Noise.py --output noise.svg --width 300 --height 300 --type fractalNoise --frequency 0.65

Author: Claude
License: MIT
"""

import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import sys
from typing import Optional, Tuple, List


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate SVG noise patterns for grainy gradients.')
    
    parser.add_argument('--output', '-o', type=str, default='noise.svg',
                        help='Output SVG file path (default: noise.svg)')
    
    parser.add_argument('--width', '-w', type=int, default=300,
                        help='Width of the SVG in pixels (default: 300)')
    
    parser.add_argument('--height', '-ht', type=int, default=300,
                        help='Height of the SVG in pixels (default: 300)')
    
    parser.add_argument('--type', '-t', type=str, choices=['fractalNoise', 'turbulence'], 
                        default='fractalNoise',
                        help='Type of noise to generate (default: fractalNoise)')
    
    parser.add_argument('--frequency', '-f', type=float, default=0.65,
                        help='Base frequency of the noise (0.1-1.0) (default: 0.65)')
    
    parser.add_argument('--octaves', '-oct', type=int, default=3,
                        help='Number of octaves for the noise (1-5) (default: 3)')
    
    parser.add_argument('--seed', '-s', type=int, default=None,
                        help='Seed for the noise generation (default: random)')
    
    parser.add_argument('--base-color', '-bc', type=str, default='#ffffff',
                        help='Base color for the noise in hex format (default: #ffffff)')
    
    parser.add_argument('--opacity', '-op', type=float, default=0.8,
                        help='Opacity of the noise overlay (0.0-1.0) (default: 0.8)')
    
    parser.add_argument('--gradient', '-g', action='store_true',
                        help='Add a linear gradient to the SVG (default: False)')
    
    parser.add_argument('--gradient-colors', '-gc', type=str, nargs='+', 
                        default=['#ff0080', '#0080ff'],
                        help='Colors for the gradient in hex format (default: "#ff0080 #0080ff")')
    
    parser.add_argument('--gradient-angle', '-ga', type=int, default=45,
                        help='Angle of the gradient in degrees (default: 45)')
    
    parser.add_argument('--inline-css', '-css', action='store_true',
                        help='Include CSS for contrast/brightness in the SVG (default: False)')
    
    parser.add_argument('--contrast', '-c', type=int, default=170,
                        help='Contrast percentage for inline CSS (default: 170)')
    
    parser.add_argument('--brightness', '-b', type=int, default=1000,
                        help='Brightness percentage for inline CSS (default: 1000)')
    
    return parser.parse_args()


def validate_hex_color(color: str) -> bool:
    """Validate a hex color string."""
    if not color.startswith('#'):
        return False
    
    color = color.lstrip('#')
    if len(color) not in [3, 6]:
        return False
    
    try:
        int(color, 16)
        return True
    except ValueError:
        return False


def create_gradient_element(svg: ET.Element, colors: List[str], angle: int, id_name: str = "gradient") -> ET.Element:
    """Create a linear gradient element."""
    # Convert angle to x1,y1,x2,y2 coordinates
    angle_rad = angle * 3.14159 / 180
    if angle <= 90:
        x1, y1 = 0, 0
        x2, y2 = 100 * abs((angle / 90) - 1), 100 * (angle / 90)
    elif angle <= 180:
        x1, y1 = 0, 100
        x2, y2 = 100 * ((angle - 90) / 90), 0
    elif angle <= 270:
        x1, y1 = 100, 100
        x2, y2 = 0, 100 * (1 - ((angle - 180) / 90))
    else:
        x1, y1 = 100, 0
        x2, y2 = 100 * (1 - ((angle - 270) / 90)), 100
    
    # Create defs element if not exists
    defs = svg.find("defs")
    if defs is None:
        defs = ET.SubElement(svg, "defs")
    
    # Create linear gradient
    gradient = ET.SubElement(defs, "linearGradient")
    gradient.set("id", id_name)
    gradient.set("x1", f"{x1}%")
    gradient.set("y1", f"{y1}%")
    gradient.set("x2", f"{x2}%")
    gradient.set("y2", f"{y2}%")
    
    # Add stops
    num_colors = len(colors)
    for i, color in enumerate(colors):
        stop = ET.SubElement(gradient, "stop")
        stop.set("offset", f"{100 * i / (num_colors - 1)}%")
        stop.set("stop-color", color)
    
    return gradient


def create_svg_noise(args):
    """Create an SVG with noise based on the provided arguments."""
    # Create SVG root element
    svg = ET.Element("svg")
    svg.set("xmlns", "http://www.w3.org/2000/svg")
    svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    svg.set("width", str(args.width))
    svg.set("height", str(args.height))
    svg.set("viewBox", f"0 0 {args.width} {args.height}")
    
    # Create defs section for filters
    defs = ET.SubElement(svg, "defs")
    
    # Create the noise filter
    filter_elem = ET.SubElement(defs, "filter")
    filter_elem.set("id", "noiseFilter")
    filter_elem.set("x", "0")
    filter_elem.set("y", "0")
    filter_elem.set("width", "100%")
    filter_elem.set("height", "100%")
    
    # Add turbulence element
    turbulence = ET.SubElement(filter_elem, "feTurbulence")
    turbulence.set("type", args.type)
    turbulence.set("baseFrequency", str(args.frequency))
    turbulence.set("numOctaves", str(args.octaves))
    turbulence.set("stitchTiles", "stitch")
    
    if args.seed is not None:
        turbulence.set("seed", str(args.seed))
    
    # Create base rect with color
    base_rect = ET.SubElement(svg, "rect")
    base_rect.set("width", "100%")
    base_rect.set("height", "100%")
    base_rect.set("fill", args.base_color)
    
    # Create rect with the noise filter
    noise_rect = ET.SubElement(svg, "rect")
    noise_rect.set("width", "100%")
    noise_rect.set("height", "100%")
    noise_rect.set("filter", "url(#noiseFilter)")
    noise_rect.set("opacity", str(args.opacity))
    
    # Add gradient if requested
    if args.gradient:
        # Validate colors
        valid_colors = []
        for color in args.gradient_colors:
            if validate_hex_color(color):
                valid_colors.append(color)
            else:
                print(f"Warning: Invalid color '{color}' will be ignored.")
        
        if len(valid_colors) < 2:
            print("Warning: Need at least 2 valid colors for gradient. Using default colors.")
            valid_colors = ["#ff0080", "#0080ff"]
        
        # Create gradient
        create_gradient_element(svg, valid_colors, args.gradient_angle, "noiseGradient")
        
        # Create rect with gradient
        gradient_rect = ET.SubElement(svg, "rect")
        gradient_rect.set("width", "100%")
        gradient_rect.set("height", "100%")
        gradient_rect.set("fill", "url(#noiseGradient)")
        gradient_rect.set("opacity", "0.7")
    
    # Add inline CSS for contrast/brightness if requested
    if args.inline_css:
        style = ET.SubElement(svg, "style")
        css = f"""
            svg {{
                filter: contrast({args.contrast}%) brightness({args.brightness}%);
            }}
        """
        style.text = css
    
    # Convert to string with pretty formatting
    rough_string = ET.tostring(svg, encoding='utf-8')
    parsed = minidom.parseString(rough_string)
    pretty_xml = parsed.toprettyxml(indent="  ")
    
    # Remove extra whitespace that minidom adds around text content
    pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
    
    return pretty_xml


def save_svg(svg_content: str, output_path: str):
    """Save SVG content to file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"SVG saved to {output_path}")
        
        # Get absolute path for clearer output
        abs_path = os.path.abspath(output_path)
        print(f"Full path: {abs_path}")
        
        file_size = os.path.getsize(output_path)
        print(f"File size: {file_size} bytes")
        
    except IOError as e:
        print(f"Error saving file: {e}")
        sys.exit(1)


def print_css_usage_example(output_filename: str):
    """Print an example of how to use the generated SVG in CSS."""
    print("\nCSS Usage Examples:")
    print("-" * 50)
    
    print("Basic usage:")
    print(f"""
.noise {{
  background-image: url("{output_filename}");
}}
""")
    
    print("With gradient and enhanced contrast/brightness:")
    print(f"""
.grainy-gradient {{
  background: 
    linear-gradient(45deg, #ff0080, #0080ff),
    url("{output_filename}");
  filter: contrast(170%) brightness(1000%);
}}
""")
    
    print("With blending:")
    print(f"""
.noise-with-blending {{
  position: relative;
  isolation: isolate;
}}

.noise-with-blending::before {{
  content: "";
  position: absolute;
  inset: 0;
  background: 
    linear-gradient(45deg, #ff0080, #0080ff),
    url("{output_filename}");
  filter: contrast(170%) brightness(1000%);
}}

.noise-with-blending::after {{
  content: "";
  position: absolute;
  inset: 0;
  background: #f8f0fc;
  mix-blend-mode: color;
  opacity: 0.3;
}}
""")


def main():
    """Main function."""
    args = parse_arguments()
    
    # Check if output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        except OSError as e:
            print(f"Error creating directory: {e}")
            sys.exit(1)
    
    # Create SVG content
    svg_content = create_svg_noise(args)
    
    # Save to file
    save_svg(svg_content, args.output)
    
    # Print usage example
    print_css_usage_example(args.output)


if __name__ == "__main__":
    main()