import tkinter as tk
from PIL import Image, ImageTk
import cairo
import math
import io

# === Configuration Constants ===
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 700

DEFAULT_RADIUS = 100
DEFAULT_LINE_WIDTH = 2

RADIUS_RANGE = (50, 300)
LINE_WIDTH_RANGE = (1, 20)

# Curve configuration (can be parameterized later)
CURVE_COLOR = (0.1, 0.2, 0.8)
CURVE_LINE_WIDTH = 1.5

PERIMETER_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (1, 1, 1)

# === Drawing Functions ===

def draw_closed_curve(ctx, center_x, center_y, curve_radius=50):
    """
    Draws an example closed Bézier curve around the center point.
    This can be replaced with custom logic later.
    """
    ctx.set_source_rgb(*CURVE_COLOR)
    ctx.set_line_width(CURVE_LINE_WIDTH)

    offset = curve_radius
    ctx.move_to(center_x - offset, center_y - offset)
    ctx.curve_to(center_x - 0.6 * offset, center_y - 1.6 * offset,
                 center_x + 0.6 * offset, center_y + 1.6 * offset,
                 center_x + offset, center_y - offset)
    ctx.curve_to(center_x + 0.6 * offset, center_y + 1.6 * offset,
                 center_x - 0.6 * offset, center_y - 1.6 * offset,
                 center_x - offset, center_y - offset)
    ctx.close_path()
    ctx.stroke()

def generate_image(width, height, perimeter_radius, perimeter_width):
    """
    Generates a Pycairo image with a circular perimeter and one interior curve.
    """
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)

    # Background
    ctx.set_source_rgb(*BACKGROUND_COLOR)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()

    center_x, center_y = width / 2, height / 2

    # Clip to circle
    ctx.arc(center_x, center_y, perimeter_radius, 0, 2 * math.pi)
    ctx.clip()

    # Draw curve inside
    draw_closed_curve(ctx, center_x, center_y)

    # Draw perimeter
    ctx.reset_clip()
    ctx.set_source_rgb(*PERIMETER_COLOR)
    ctx.set_line_width(perimeter_width)
    ctx.arc(center_x, center_y, perimeter_radius, 0, 2 * math.pi)
    ctx.stroke()

    # Convert to PIL Image
    buf = io.BytesIO()
    surface.write_to_png(buf)
    buf.seek(0)
    return Image.open(buf)

# === GUI Application ===

class CurveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Closed Curves in Circular Perimeter")

        # Display canvas
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.grid(row=0, column=0, columnspan=2)

        # Sliders for radius and perimeter line width
        self.radius_slider = tk.Scale(root, from_=RADIUS_RANGE[0], to=RADIUS_RANGE[1],
                                      orient=tk.HORIZONTAL, label="Radius (r)",
                                      command=self.update_image)
        self.radius_slider.set(DEFAULT_RADIUS)
        self.radius_slider.grid(row=1, column=0, padx=10, sticky="ew")

        self.line_width_slider = tk.Scale(root, from_=LINE_WIDTH_RANGE[0], to=LINE_WIDTH_RANGE[1],
                                          orient=tk.HORIZONTAL, label="Line Width (w)",
                                          command=self.update_image)
        self.line_width_slider.set(DEFAULT_LINE_WIDTH)
        self.line_width_slider.grid(row=1, column=1, padx=10, sticky="ew")

        # Canvas image reference
        self.image_on_canvas = None
        self.update_image()

    def update_image(self, event=None):
        radius = self.radius_slider.get()
        line_width = self.line_width_slider.get()
        pil_image = generate_image(CANVAS_WIDTH, CANVAS_HEIGHT, radius, line_width)
        self.tk_image = ImageTk.PhotoImage(pil_image)

        if self.image_on_canvas is None:
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        else:
            self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)

# === Run GUI ===
if __name__ == "__main__":
    root = tk.Tk()
    app = CurveApp(root)
    root.mainloop()
