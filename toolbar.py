import cv2
import config

def draw_toolbar(frame, active_tool, frame_width):
    """
    Renders a premium-looking toolbar UI on top of the frame.
    Divides the toolbar into 5 sections with modern button styling.
    """
    num_tools = len(config.TOOLS)
    block_width = frame_width // num_tools
    padding_x = 10
    padding_y = 10

    # Draw semi-transparent background bar for the toolbar
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame_width, config.TOOLBAR_HEIGHT), (30, 30, 30), cv2.FILLED)
    # Blend the background bar with the frame (alpha = 0.8)
    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)

    for i, tool_name in enumerate(config.TOOLS):
        # Calculate coordinates for each button
        x_start = i * block_width + padding_x
        x_end = (i + 1) * block_width - padding_x
        y_start = padding_y
        y_end = config.TOOLBAR_HEIGHT - padding_y

        # Determine button colors
        if tool_name == "ERASER":
            # Eraser has a white button with black text
            btn_color = config.COLOR_WHITE
            text_color = config.COLOR_BLACK
            label = "ERASER"
        else:
            # Color buttons have their respective color as background, white text
            btn_color = config.TOOL_COLORS[tool_name]
            text_color = config.COLOR_WHITE
            # Red/Yellow/Blue/Green look better with white/black text depending on brightness
            # For Yellow, black text is more readable
            if tool_name == "YELLOW":
                text_color = config.COLOR_BLACK
            label = tool_name

        # Draw the button rectangle
        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), btn_color, cv2.FILLED)

        # Draw a border for the active tool
        if tool_name == active_tool:
            # Highlight with a double border (black inner, white outer) for visibility
            cv2.rectangle(frame, (x_start - 3, y_start - 3), (x_end + 3, y_end + 3), config.COLOR_WHITE, 3)
            cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), config.COLOR_BLACK, 1)

        # Draw label text centered inside the button
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2
        (text_width, text_height), _ = cv2.getTextSize(label, font, font_scale, font_thickness)
        
        # Center coordinates
        text_x = x_start + ((x_end - x_start) - text_width) // 2
        text_y = y_start + ((y_end - y_start) + text_height) // 2
        
        cv2.putText(frame, label, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

def detect_tool_selection(x, y, frame_width):
    """
    Checks if a given coordinate (usually the index fingertip) lies in the toolbar
    and returns the selected tool name.
    """
    if y < config.TOOLBAR_HEIGHT:
        num_tools = len(config.TOOLS)
        block_width = frame_width // num_tools
        tool_idx = x // block_width
        if 0 <= tool_idx < num_tools:
            return config.TOOLS[tool_idx]
    return None
