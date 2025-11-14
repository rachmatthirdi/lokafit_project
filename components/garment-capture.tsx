// Component for capturing garment photos with coordinates

"use client";

import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface GarmentCaptureProps {
  mode: "accurate" | "quick";
  onCapture: (file: File, coordinates?: any) => void;
  isLoading?: boolean;
}

export function GarmentCapture({
  mode,
  onCapture,
  isLoading = false,
}: GarmentCaptureProps) {
  const [photo, setPhoto] = useState<string | null>(null);
  const [coordinates, setCoordinates] = useState<any>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const handlePhotoSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setPhoto(event.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (mode !== "accurate" || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Store coordinates for calibration
    setCoordinates((prev: any) => ({
      ...prev,
      lastClick: { x, y },
    }));
  };

  const handleCapture = () => {
    const fileInput = fileInputRef.current;
    if (fileInput?.files?.[0]) {
      onCapture(fileInput.files[0], coordinates);
    }
  };

  return (
    <Card>
      <CardContent className="p-6 flex flex-col gap-6">
        {!photo ? (
          <div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
            <p className="text-muted-foreground mb-4">Capture or upload a photo</p>
            <Button
              variant="outline"
              onClick={() => fileInputRef.current?.click()}
            >
              Choose Photo
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handlePhotoSelect}
              className="hidden"
            />
          </div>
        ) : (
          <>
            <div className="rounded-lg overflow-hidden bg-muted">
              <canvas
                ref={canvasRef}
                className="w-full cursor-crosshair"
                onClick={handleCanvasClick}
              />
              <img
                src={photo || "/placeholder.svg"}
                alt="Captured"
                className="w-full h-96 object-cover"
                onLoad={(e) => {
                  if (canvasRef.current && e.currentTarget) {
                    const ctx = canvasRef.current.getContext("2d");
                    canvasRef.current.width = e.currentTarget.width;
                    canvasRef.current.height = e.currentTarget.height;
                    ctx?.drawImage(e.currentTarget, 0, 0);
                  }
                }}
              />
            </div>
            {mode === "accurate" && (
              <p className="text-xs text-muted-foreground">
                Click to mark calibration points
              </p>
            )}
            <div className="flex gap-4">
              <Button
                onClick={() => setPhoto(null)}
                variant="outline"
                className="flex-1"
              >
                Retake
              </Button>
              <Button
                onClick={handleCapture}
                disabled={isLoading}
                className="flex-1"
              >
                {isLoading ? "Processing..." : "Scan"}
              </Button>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
