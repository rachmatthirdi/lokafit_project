# Phase 2: Profile API Routes
# GET /api/v1/profile - Get user profile
# POST /api/v1/profile/skin-tone - Analyze skin tone from photo

from fastapi import APIRouter, File, UploadFile, HTTPException
import numpy as np
import cv2
from typing import Optional

router = APIRouter()


@router.post("/skin-tone")
async def analyze_skin_tone(file: UploadFile = File(...)):
    """
    Analyze user's skin tone from face photo.
    
    Args:
        file: Face photo image file
    
    Returns:
        Skin tone classification and color palette
    """
    try:
        file_bytes = await file.read()
        
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Decode image
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image")
        
        # Simple skin tone detection (placeholder)
        # In production: use ML model for accurate detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Extract center region (likely face)
        h, w = image.shape[:2]
        center_region = image[h//4:3*h//4, w//4:3*w//4]
        
        # Calculate average skin color
        avg_color_bgr = np.mean(center_region, axis=(0, 1))
        avg_color_rgb = avg_color_bgr[::-1]
        
        # Classify skin tone
        r, g, b = int(avg_color_rgb[0]), int(avg_color_rgb[1]), int(avg_color_rgb[2])
        luminance = 0.299*r + 0.587*g + 0.114*b
        
        if luminance > 180:
            skin_tone_class = "Light"
        elif luminance > 130:
            skin_tone_class = "Medium"
        elif luminance > 80:
            skin_tone_class = "Deep"
        else:
            skin_tone_class = "Very Deep"
        
        # Determine warm/cool undertone
        if r > b:
            undertone = "Warm"
        elif b > r:
            undertone = "Cool"
        else:
            undertone = "Neutral"
        
        return {
            "status": "success",
            "skin_tone_class": skin_tone_class,
            "undertone": undertone,
            "hex_color": "#{:02x}{:02x}{:02x}".format(int(avg_color_rgb[0]), int(avg_color_rgb[1]), int(avg_color_rgb[2])),
            "recommendations": {
                "warm_colors": ["#FF6B35", "#FFD700", "#FF8C3A"],
                "cool_colors": ["#0099FF", "#6600FF", "#0066CC"]
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@router.get("/")
async def get_profile(user_id: str):
    """
    Get user profile information.
    
    In production: fetch from Supabase
    """
    return {
        "status": "success",
        "message": "Profile endpoint ready"
    }
