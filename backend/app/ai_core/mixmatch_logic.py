# Phase 2: AI System 3 - Mix & Match Recommendation Engine
# Handles: Color theory, outfit curation, weekly planning

from typing import List, Dict, Any
import json
from datetime import datetime, timedelta


class ColorTheory:
    """Color theory and harmony calculations"""
    
    WARM_COLORS = ["#FF6B35", "#FF8C3A", "#FFA500", "#FFD700", "#FF4500"]
    COOL_COLORS = ["#0066CC", "#0099FF", "#00CCFF", "#6600FF", "#9933FF"]
    NEUTRAL_COLORS = ["#808080", "#A9A9A9", "#FFFFFF", "#000000", "#D3D3D3"]
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb: tuple) -> str:
        """Convert RGB tuple to hex color"""
        return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    @staticmethod
    def get_color_temperature(hex_color: str) -> str:
        """
        Determine if color is warm, cool, or neutral.
        
        Returns: 'warm', 'cool', or 'neutral'
        """
        r, g, b = ColorTheory.hex_to_rgb(hex_color)
        
        # Calculate warm/cool score
        warm_score = r + g
        cool_score = b
        
        if abs(warm_score - cool_score) < 30:
            return "neutral"
        return "warm" if warm_score > cool_score else "cool"
    
    @staticmethod
    def get_complementary_colors(hex_color: str) -> List[str]:
        """
        Find complementary colors for styling suggestions.
        
        Returns list of hex colors that match well
        """
        temp = ColorTheory.get_color_temperature(hex_color)
        
        if temp == "warm":
            return ColorTheory.COOL_COLORS[:3]
        elif temp == "cool":
            return ColorTheory.WARM_COLORS[:3]
        else:
            return ColorTheory.NEUTRAL_COLORS[:3]


class MixMatchEngine:
    """Outfit recommendation engine"""
    
    def __init__(self):
        self.color_theory = ColorTheory()
    
    async def generate_instant_match(
        self,
        item_color: str,
        skin_tone: str,
        user_garments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate instant outfit match suggestions.
        
        Args:
            item_color: Hex color of current item
            skin_tone: User's skin tone ID
            user_garments: List of user's garment items
        
        Returns:
            Matching outfit suggestions
        """
        complementary = self.color_theory.get_complementary_colors(item_color)
        
        # Filter user's garments by complementary colors
        matches = []
        for garment in user_garments:
            garment_color = garment.get("color_hex", "#808080")
            if garment_color in complementary:
                matches.append({
                    "garment_id": garment.get("id"),
                    "color_hex": garment_color,
                    "type": garment.get("garment_type"),
                    "match_score": 0.85
                })
        
        return {
            "primary_item": {
                "color": item_color,
                "temperature": self.color_theory.get_color_temperature(item_color)
            },
            "complementary_colors": complementary,
            "matched_items": matches[:5],
            "suggested_mood": "Stylish & Coordinated"
        }
    
    async def generate_weekly_plan(
        self,
        user_garments: List[Dict[str, Any]],
        skin_tone: str
    ) -> Dict[str, Any]:
        """
        Generate AI-curated weekly outfit plan.
        
        Args:
            user_garments: List of all user garments
            skin_tone: User's skin tone
        
        Returns:
            Weekly curation plan (7 outfits)
        """
        if len(user_garments) < 3:
            return {"error": "Not enough garments for weekly plan"}
        
        weekly_plan = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Simple algorithm: rotate through garments and suggest complements
        for i, day in enumerate(days):
            selected_item = user_garments[i % len(user_garments)]
            item_color = selected_item.get("color_hex", "#808080")
            
            # Get complementary items
            complements = self.color_theory.get_complementary_colors(item_color)
            matching_items = [
                g for g in user_garments 
                if g.get("color_hex") in complements
            ]
            
            outfit = {
                "day": day,
                "primary": {
                    "id": selected_item.get("id"),
                    "type": selected_item.get("garment_type"),
                    "color": item_color
                },
                "complements": [
                    {
                        "id": m.get("id"),
                        "type": m.get("garment_type"),
                        "color": m.get("color_hex")
                    }
                    for m in matching_items[:2]
                ],
                "styling_note": f"Harmonious {self.color_theory.get_color_temperature(item_color)} palette"
            }
            
            weekly_plan.append(outfit)
        
        return {
            "week_of": (datetime.now() + timedelta(days=1)).date().isoformat(),
            "outfits": weekly_plan,
            "generated_at": datetime.now().isoformat()
        }


# Initialize engine
engine = MixMatchEngine()
