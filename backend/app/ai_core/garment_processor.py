# Phase 2: AI System 1 - Garment Recognition & Measurement
# Handles: rembg segmentation, coin calibration, color extraction, WebP compression

import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Tuple, Dict, Any
import json


class GarmentProcessor:
    """
    Core AI system for garment processing:
    - Background removal (rembg)
    - Coin-based scale calibration
    - Color extraction (KMeans)
    - Measurement calculation
    - WebP compression
    """

    def __init__(self):
        self.scale_ratio = None  # pixels per millimeter
        self.dominant_color = None
        self.measurements = {}

    def calculate_scale_from_coin(
        self, 
        image_array: np.ndarray, 
        coin_coords: Dict[str, Any]
    ) -> float:
        """
        Calculate scale ratio (pixels/mm) using coin diameter.
        
        Args:
            image_array: OpenCV image (BGR)
            coin_coords: {"x": center_x, "y": center_y, "diameter_pixels": d}
        
        Returns:
            scale_ratio: pixels per millimeter
        """
        # Indonesian coins reference diameters (mm):
        # 500: 27mm, 1000: 26mm, 5000: 33mm
        coin_reference = {
            "500": 27.0,
            "1000": 26.0,
            "5000": 33.0,
            "generic": 27.0  # Default fallback
        }
        
        diameter_px = coin_coords.get("diameter_pixels", 100)
        coin_type = coin_coords.get("type", "generic")
        diameter_mm = coin_reference.get(coin_type, 27.0)
        
        scale_ratio = diameter_px / diameter_mm
        self.scale_ratio = scale_ratio
        return scale_ratio

    def white_balance_calibration(
        self,
        image_array: np.ndarray,
        white_tap_coords: Dict[str, Any]
    ) -> np.ndarray:
        """
        Calibrate white balance using white paper tap coordinates.
        
        Args:
            image_array: OpenCV image (BGR)
            white_tap_coords: {"x": x, "y": y, "radius": r}
        
        Returns:
            Corrected image array
        """
        x = int(white_tap_coords.get("x", 0))
        y = int(white_tap_coords.get("y", 0))
        radius = int(white_tap_coords.get("radius", 30))
        
        # Extract white reference region
        if 0 <= y - radius and y + radius < image_array.shape[0] and \
           0 <= x - radius and x + radius < image_array.shape[1]:
            white_region = image_array[y - radius:y + radius, x - radius:x + radius]
            
            # Calculate mean color in white region
            b_mean, g_mean, r_mean = cv2.mean(white_region)[:3]
            
            # Normalize to white (255, 255, 255)
            scale_b = 255.0 / (b_mean + 1e-5)
            scale_g = 255.0 / (g_mean + 1e-5)
            scale_r = 255.0 / (r_mean + 1e-5)
            
            # Apply white balance
            corrected = image_array.copy().astype(float)
            corrected[:, :, 0] *= scale_b
            corrected[:, :, 1] *= scale_g
            corrected[:, :, 2] *= scale_r
            
            corrected = np.clip(corrected, 0, 255).astype(np.uint8)
            return corrected
        
        return image_array

    def extract_dominant_color(self, segmented_image: np.ndarray) -> str:
        """
        Extract dominant color from segmented garment using KMeans.
        
        Args:
            segmented_image: Image with transparent background (RGBA)
        
        Returns:
            Hex color string (e.g., "#FF5733")
        """
        # Convert to RGB, remove alpha channel, and flatten
        if segmented_image.shape[2] == 4:  # RGBA
            rgb_image = segmented_image[:, :, :3]
            alpha = segmented_image[:, :, 3]
            # Mask out transparent pixels
            mask = alpha > 128
        else:
            rgb_image = segmented_image
            mask = np.ones(segmented_image.shape[:2], dtype=bool)
        
        # Reshape to 2D for KMeans
        pixels = rgb_image[mask].reshape(-1, 3).astype(float)
        
        if len(pixels) == 0:
            return "#808080"  # Gray fallback
        
        # KMeans clustering to find dominant color
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, _, centers = cv2.kmeans(
            pixels, 1, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
        )
        
        dominant_rgb = centers[0].astype(int)
        hex_color = "#{:02x}{:02x}{:02x}".format(
            dominant_rgb[0], dominant_rgb[1], dominant_rgb[2]
        )
        
        self.dominant_color = hex_color
        return hex_color

    def measure_garment_outline(
        self,
        segmented_image: np.ndarray
    ) -> Dict[str, float]:
        """
        Measure garment dimensions from segmented outline.
        
        Args:
            segmented_image: Binary or segmented image
        
        Returns:
            Dictionary with width_cm, height_cm, area_cm2
        """
        if self.scale_ratio is None:
            self.scale_ratio = 3.0  # Default fallback
        
        # Extract alpha channel for mask
        if segmented_image.shape[2] == 4:
            alpha = segmented_image[:, :, 3]
            mask = (alpha > 128).astype(np.uint8) * 255
        else:
            # Convert to grayscale
            mask = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2GRAY)
            mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)[1]
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return {"width_cm": 0, "height_cm": 0, "area_cm2": 0}
        
        # Get bounding box of largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Convert pixels to cm using scale ratio
        width_cm = w / self.scale_ratio / 10  # pixels/mm to cm
        height_cm = h / self.scale_ratio / 10
        area_cm2 = (width_cm * height_cm)
        
        self.measurements = {
            "width_cm": round(width_cm, 2),
            "height_cm": round(height_cm, 2),
            "area_cm2": round(area_cm2, 2),
        }
        
        return self.measurements

    def compress_to_webp(
        self,
        image_array: np.ndarray,
        quality: int = 75
    ) -> bytes:
        """
        Compress image to WebP format.
        
        Args:
            image_array: Image as numpy array
            quality: WebP quality (0-100)
        
        Returns:
            WebP image bytes
        """
        # Convert BGR to RGB
        rgb_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_array)
        
        # Compress to WebP
        webp_buffer = BytesIO()
        pil_image.save(webp_buffer, format="WebP", quality=quality)
        webp_buffer.seek(0)
        
        return webp_buffer.getvalue()

    async def process_garment_accurate(
        self,
        file_bytes: bytes,
        coin_coords: Dict[str, Any],
        white_tap_coords: Dict[str, Any]
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Main processing pipeline for accurate garment scan.
        
        Args:
            file_bytes: Raw image bytes from frontend
            coin_coords: Coin calibration data
            white_tap_coords: White balance calibration data
        
        Returns:
            (webp_bytes, metadata_json)
        """
        # Convert bytes to image
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Invalid image data")
        
        # Step 1: Calculate scale ratio
        self.calculate_scale_from_coin(image, coin_coords)
        
        # Step 2: White balance calibration
        wb_corrected = self.white_balance_calibration(image, white_tap_coords)
        
        # Step 3: Simulate background removal (rembg integration point)
        # In production: segmented = remove_background(wb_corrected)
        segmented = wb_corrected  # Placeholder
        
        # Step 4: Extract dominant color
        color_hex = self.extract_dominant_color(segmented)
        
        # Step 5: Measure garment
        measurements = self.measure_garment_outline(segmented)
        
        # Step 6: Compress to WebP
        webp_bytes = self.compress_to_webp(segmented)
        
        # Step 7: Prepare metadata
        metadata = {
            "color_hex": color_hex,
            "measurements": measurements,
            "scale_ratio": float(self.scale_ratio),
            "file_format": "webp"
        }
        
        return webp_bytes, metadata


# Initialize processor
processor = GarmentProcessor()
