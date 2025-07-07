import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math
import random
from shapely.geometry import Polygon
from shapely.affinity import translate

# Canvas and visual settings
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 700
BACKGROUND_COLOR = (255, 255, 255)
PERIMETER_COLOR = (0, 0, 0)
POLY1_COLOR = (25, 51, 204)

# Default and allowed parameter ranges
DEFAULT_RADIUS = 100
DEFAULT_LINE_WIDTH = 2
DEFAULT_MARGIN = 10
DEFAULT_LAYERS = 3

RADIUS_RANGE = (50, 300)
LINE_WIDTH_RANGE = (1, 20)
MARGIN_RANGE = (1, 50)
LAYER_RANGE = (1, 50)


def draw_random_polygon_inside_circle(radius, margin, sides=50):
    """Create a random polygon within a circle of radius - margin."""
    points = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides
        r = radius - random.uniform(margin, margin + 1)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x, y))
    return points


def to_absolute(points, offset):
    """Translate points from local (0,0) to absolute (cx, cy)."""
    return [(x + offset[0], y + offset[1]) for x, y in points]


def color_from_index(i):
    """Generate distinguishable colors for each polygon layer."""
    hue = (i * 37) % 360
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(hue / 360.0, 0.6, 0.9)
    return (int(r * 255), int(g * 255), int(b * 255))


def generate_image(width, height, perimeter_radius, perimeter_width, margin, num_layers):
    image = Image.new("RGB", (width, height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    cx, cy = width // 2, height // 2

    # Draw perimeter
    bbox = [cx - perimeter_radius, cy - perimeter_radius,
            cx + perimeter_radius, cy + perimeter_radius]
    draw.ellipse(bbox, outline=PERIMETER_COLOR, width=perimeter_width)

    # poly1: initial random polygon
    poly1_local = draw_random_polygon_inside_circle(perimeter_radius, margin, sides=50)
    poly1_abs = to_absolute(poly1_local, (cx, cy))
    poly = Polygon(poly1_abs)

    # Draw poly1
    draw.polygon(poly1_abs, outline=POLY1_COLOR, fill=None)

    # Generate and draw nested inner polygons
    for i in range(1, num_layers):
        poly = poly.buffer(-margin)
        if poly.is_empty or poly.geom_type != 'Polygon':
            break
        color = color_from_index(i)
        coords = list(poly.exterior.coords)
        draw.polygon(coords, outline=color, fill=None)

    return image


class CurveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nested Polygons with Margin")

        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.radius_slider = self.create_slider("Radius (r)", RADIUS_RANGE, DEFAULT_RADIUS, 0)
        self.line_width_slider = self.create_slider("Line Width (w)", LINE_WIDTH_RANGE, DEFAULT_LINE_WIDTH, 1)
        self.margin_slider = self.create_slider("Margin", MARGIN_RANGE, DEFAULT_MARGIN, 2)
        self.layer_slider = self.create_slider("Inner Layers", LAYER_RANGE, DEFAULT_LAYERS, 3)

        self.image_on_canvas = None
        self.update_image()

    def create_slider(self, label, range_vals, default_val, col):
        slider = tk.Scale(self.root, from_=range_vals[0], to=range_vals[1],
                          orient=tk.HORIZONTAL, label=label,
                          command=self.update_image)
        slider.set(default_val)
        slider.grid(row=1, column=col, sticky="ew", padx=5)
        return slider

    def update_image(self, event=None):
        r = self.radius_slider.get()
        w = self.line_width_slider.get()
        m = self.margin_slider.get()
        n = self.layer_slider.get()
        pil_img = generate_image(CANVAS_WIDTH, CANVAS_HEIGHT, r, w, m, n)
        self.tk_image = ImageTk.PhotoImage(pil_img)
        if self.image_on_canvas is None:
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        else:
            self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)


if __name__ == "__main__":
    root = tk.Tk()
    app = CurveApp(root)
    root.mainloop()
