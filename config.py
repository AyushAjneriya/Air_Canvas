import cv2

# Webcam Configurations
CAMERA_INDEX = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
FPS_TARGET = 30

# BGR Colors
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_BLACK = (0, 0, 0)      # Eraser color
COLOR_WHITE = (255, 255, 255)  # Background/Text
COLOR_GRAY = (200, 200, 200)   # UI Borders

# Toolbar Settings
TOOLBAR_HEIGHT = 80
TOOLS = ["RED", "BLUE", "GREEN", "YELLOW", "ERASER"]

# Mapping tool names to BGR colors
TOOL_COLORS = {
    "RED": COLOR_RED,
    "BLUE": COLOR_BLUE,
    "GREEN": COLOR_GREEN,
    "YELLOW": COLOR_YELLOW,
    "ERASER": COLOR_BLACK
}

# Drawing Settings
DEFAULT_BRUSH_THICKNESS = 5
ERASER_THICKNESS_MULTIPLIER = 3  # Eraser is 3x normal brush thickness

# Canvas Blending
SEMI_TRANSPARENT_STROKES = True  # If True, drawn lines are semi-transparent; otherwise solid
BLEND_ALPHA = 0.6               # Transparency factor (0.0 to 1.0) when blending

# Keyboard Controls
KEY_CLEAR = ord('c')
KEY_SAVE = ord('s')
KEY_QUIT_Q = ord('q')
KEY_QUIT_ESC = 27  # ESC key ASCII code
