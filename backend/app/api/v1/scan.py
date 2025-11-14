# Phase 2: Scan API Routes
# POST /api/v1/scan/accurate - Accurate garment scan with calibration
# POST /api/v1/scan/quick - Quick scan without calibration

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional
import json
from app.ai_core.garment_processor import processor

router = APIRouter()


@router.post("/accurate")
async def scan_accurate(
    file: UploadFile = File(...),
    coin_coords: str = Form(...),
    white_tap_coords: str = Form(...)
):
    """
    Accurate garment scan with coin calibration and white balance.
    
    Args:
        file: Image file (JPEG/PNG)
        coin_coords: JSON string with coin calibration data
        white_tap_coords: JSON string with white paper coordinates
    
    Returns:
        WebP image bytes and measurement metadata
    """
    try:
        # Parse JSON coordinates
        coin_data = json.loads(coin_coords)
        white_data = json.loads(white_tap_coords)
        
        # Read file bytes
        file_bytes = await file.read()
        
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Process garment
        webp_bytes, metadata = await processor.process_garment_accurate(
            file_bytes, coin_data, white_data
        )
        
        return {
            "status": "success",
            "webp_url": "file://processed_image.webp",  # In production: upload to Supabase Storage
            "metadata": metadata
        }
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in coordinates")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/quick")
async def scan_quick(file: UploadFile = File(...)):
    """
    Quick garment scan without calibration.
    
    Args:
        file: Image file (JPEG/PNG)
    
    Returns:
        Processed image and basic metadata
    """
    try:
        file_bytes = await file.read()
        
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Simplified processing without calibration
        webp_bytes, metadata = await processor.process_garment_accurate(
            file_bytes, 
            {"diameter_pixels": 100, "type": "generic"},
            {"x": 0, "y": 0, "radius": 0}
        )
        
        return {
            "status": "success",
            "webp_url": "file://processed_image.webp",
            "metadata": metadata
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
