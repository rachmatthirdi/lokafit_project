# Phase 2: Recommendation API Routes
# POST /api/v1/recommend/instant - Generate instant outfit matches
# POST /api/v1/recommend/weekly - Generate weekly curation plan

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.ai_core.mixmatch_logic import engine

router = APIRouter()


class InstantMatchRequest(BaseModel):
    item_color: str
    skin_tone: str
    user_garments: List[Dict[str, Any]]


class WeeklyPlanRequest(BaseModel):
    user_garments: List[Dict[str, Any]]
    skin_tone: str


@router.post("/instant")
async def generate_instant_match(request: InstantMatchRequest):
    """
    Generate instant outfit match suggestions.
    
    Args:
        request: Item color, skin tone, and available garments
    
    Returns:
        Matching outfit suggestions
    """
    try:
        result = await engine.generate_instant_match(
            request.item_color,
            request.skin_tone,
            request.user_garments
        )
        
        return {"status": "success", "data": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/weekly")
async def generate_weekly_plan(request: WeeklyPlanRequest):
    """
    Generate AI-curated weekly outfit plan.
    
    Args:
        request: User's garments and skin tone
    
    Returns:
        7-day outfit curation plan
    """
    try:
        result = await engine.generate_weekly_plan(
            request.user_garments,
            request.skin_tone
        )
        
        return {"status": "success", "data": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
