// Hook for outfit recommendations

import { useCallback, useState } from "react";
import {
  generateInstantMatch,
  generateWeeklyPlan,
} from "@/lib/api-client";
import { useUserStore } from "@/store/user-store";

export function useRecommendations() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user, garments, skinToneResult } = useUserStore();

  const getInstantMatches = useCallback(
    async (itemColor: string) => {
      if (!user || !skinToneResult) {
        setError("Missing user or skin tone data");
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const result = await generateInstantMatch(
          itemColor,
          skinToneResult.skin_tone_class,
          garments
        );
        return result.data;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Failed to generate matches";
        setError(errorMessage);
      } finally {
        setIsLoading(false);
      }
    },
    [user, skinToneResult, garments]
  );

  const getWeeklyPlan = useCallback(async () => {
    if (!user || !skinToneResult) {
      setError("Missing user or skin tone data");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await generateWeeklyPlan(
        garments,
        skinToneResult.skin_tone_class
      );
      return result.data;
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to generate weekly plan";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [user, skinToneResult, garments]);

  return {
    getInstantMatches,
    getWeeklyPlan,
    isLoading,
    error,
  };
}
