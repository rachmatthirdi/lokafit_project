// Frontend API Client for FastAPI Backend Communication

interface ScanRequest {
  file: File;
  coinCoords: {
    x: number;
    y: number;
    diameter_pixels: number;
    type: string;
  };
  whiteTapCoords: {
    x: number;
    y: number;
    radius: number;
  };
}

interface ScanResponse {
  status: string;
  webp_url: string;
  metadata: {
    color_hex: string;
    measurements: {
      width_cm: number;
      height_cm: number;
      area_cm2: number;
    };
    scale_ratio: number;
  };
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function scanGarmentAccurate(
  request: ScanRequest
): Promise<ScanResponse> {
  const formData = new FormData();
  formData.append("file", request.file);
  formData.append("coin_coords", JSON.stringify(request.coinCoords));
  formData.append("white_tap_coords", JSON.stringify(request.whiteTapCoords));

  const response = await fetch(`${API_BASE}/api/v1/scan/accurate`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Scan failed: ${response.statusText}`);
  }

  return response.json();
}

export async function scanGarmentQuick(file: File): Promise<ScanResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/api/v1/scan/quick`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Quick scan failed: ${response.statusText}`);
  }

  return response.json();
}

export async function analyzeSkinTone(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/api/v1/profile/skin-tone`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Skin tone analysis failed: ${response.statusText}`);
  }

  return response.json();
}

export async function generateInstantMatch(
  itemColor: string,
  skinTone: string,
  userGarments: any[]
) {
  const response = await fetch(`${API_BASE}/api/v1/recommend/instant`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      item_color: itemColor,
      skin_tone: skinTone,
      user_garments: userGarments,
    }),
  });

  if (!response.ok) {
    throw new Error(`Match generation failed: ${response.statusText}`);
  }

  return response.json();
}

export async function generateWeeklyPlan(userGarments: any[], skinTone: string) {
  const response = await fetch(`${API_BASE}/api/v1/recommend/weekly`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_garments: userGarments,
      skin_tone: skinTone,
    }),
  });

  if (!response.ok) {
    throw new Error(`Weekly plan generation failed: ${response.statusText}`);
  }

  return response.json();
}
