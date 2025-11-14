// Hook for garment scanning with API integration

import { useState, useCallback } from "react";
import {
  scanGarmentAccurate,
  scanGarmentQuick,
} from "@/lib/api-client";
import { useUserStore } from "@/store/user-store";
import { createClient } from "@/lib/supabase/client";

interface ScanCoordinates {
  coinCoords?: {
    x: number;
    y: number;
    diameter_pixels: number;
    type: string;
  };
  whiteTapCoords?: {
    x: number;
    y: number;
    radius: number;
  };
}

export function useGarmentScan() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user, addGarment, setIsLoading: setStoreLoading } = useUserStore();

  const performAccurateScan = useCallback(
    async (file: File, coordinates: ScanCoordinates) => {
      if (!user) {
        setError("User not authenticated");
        return;
      }

      setIsLoading(true);
      setError(null);
      setStoreLoading(true);

      try {
        // Call FastAPI backend
        const result = await scanGarmentAccurate({
          file,
          coinCoords: coordinates.coinCoords || {
            x: 0,
            y: 0,
            diameter_pixels: 100,
            type: "generic",
          },
          whiteTapCoords: coordinates.whiteTapCoords || {
            x: 0,
            y: 0,
            radius: 0,
          },
        });

        // Upload image to Supabase Storage
        const supabase = createClient();
        const fileName = `garments/${user.id}/${Date.now()}.webp`;

        // Convert webp URL to blob and upload
        const response = await fetch(result.webp_url);
        const blob = await response.blob();

        const { data: uploadData, error: uploadError } = await supabase.storage
          .from("garments")
          .upload(fileName, blob);

        if (uploadError) throw uploadError;

        // Get public URL
        const {
          data: { publicUrl },
        } = supabase.storage.from("garments").getPublicUrl(fileName);

        // Save to database
        const { data: garment, error: dbError } = await supabase
          .from("garments")
          .insert({
            user_id: user.id,
            file_url: publicUrl,
            storage_path: fileName,
            color_hex: result.metadata.color_hex,
            measurements_json: result.metadata.measurements,
            garment_type: "Unknown",
            status: "DRAF",
          })
          .select()
          .single();

        if (dbError) throw dbError;

        // Update local state
        addGarment(garment);

        return garment;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Scan failed";
        setError(errorMessage);
        console.error("[useGarmentScan]", errorMessage);
      } finally {
        setIsLoading(false);
        setStoreLoading(false);
      }
    },
    [user, addGarment, setStoreLoading]
  );

  const performQuickScan = useCallback(
    async (file: File) => {
      if (!user) {
        setError("User not authenticated");
        return;
      }

      setIsLoading(true);
      setError(null);
      setStoreLoading(true);

      try {
        const result = await scanGarmentQuick(file);

        // Upload to Supabase
        const supabase = createClient();
        const fileName = `garments/${user.id}/${Date.now()}.webp`;

        const response = await fetch(result.webp_url);
        const blob = await response.blob();

        await supabase.storage.from("garments").upload(fileName, blob);

        const {
          data: { publicUrl },
        } = supabase.storage.from("garments").getPublicUrl(fileName);

        const { data: garment, error: dbError } = await supabase
          .from("garments")
          .insert({
            user_id: user.id,
            file_url: publicUrl,
            storage_path: fileName,
            color_hex: result.metadata.color_hex,
            measurements_json: result.metadata.measurements,
            garment_type: "Unknown",
            status: "DRAF",
          })
          .select()
          .single();

        if (dbError) throw dbError;

        addGarment(garment);
        return garment;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Quick scan failed";
        setError(errorMessage);
      } finally {
        setIsLoading(false);
        setStoreLoading(false);
      }
    },
    [user, addGarment, setStoreLoading]
  );

  return {
    performAccurateScan,
    performQuickScan,
    isLoading,
    error,
  };
}
