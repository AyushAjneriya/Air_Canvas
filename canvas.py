import cv2
import numpy as np
import datetime
import os
import config

class Canvas:
    def __init__(self, width, height):
        """
        Initializes a black canvas of specified width and height.
        """
        self.width = width
        self.height = height
        self.clear()

    def clear(self):
        """
        Resets the canvas to all black.
        """
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)

    def draw_stroke(self, prev_point, curr_point, color, thickness):
        """
        Draws a line on the canvas from prev_point to curr_point.
        """
        if prev_point is not None and curr_point is not None:
            cv2.line(self.canvas, prev_point, curr_point, color, thickness, lineType=cv2.LINE_AA)

    def blend_canvas(self, webcam_frame):
        """
        Blends the canvas drawings onto the webcam frame.
        Drawn strokes will be blended according to configuration (semi-transparent or solid).
        """
        # Convert canvas to grayscale
        canvas_gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        
        # Threshold to create a mask of the drawing (any non-black pixel is part of drawing)
        _, mask = cv2.threshold(canvas_gray, 1, 255, cv2.THRESH_BINARY)
        
        # Inverse mask for background
        mask_inv = cv2.bitwise_not(mask)

        if config.SEMI_TRANSPARENT_STROKES:
            alpha = config.BLEND_ALPHA
            # Blend the entire frame and canvas
            blended = cv2.addWeighted(webcam_frame, 1.0 - alpha, self.canvas, alpha, 0)
            
            # Mask the blended strokes (foreground)
            fg = cv2.bitwise_and(blended, blended, mask=mask)
            # Mask the original frame outside the strokes (background)
            bg = cv2.bitwise_and(webcam_frame, webcam_frame, mask=mask_inv)
            
            # Combine them
            blended_frame = cv2.add(bg, fg)
        else:
            # Solid strokes overlay
            fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
            bg = cv2.bitwise_and(webcam_frame, webcam_frame, mask=mask_inv)
            blended_frame = cv2.add(bg, fg)

        return blended_frame

    def save_canvas(self, output_dir="."):
        """
        Saves the persistent canvas (only drawing on black background) as a PNG with timestamp.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        # Save to disk
        success = cv2.imwrite(filepath, self.canvas)
        return success, filepath
