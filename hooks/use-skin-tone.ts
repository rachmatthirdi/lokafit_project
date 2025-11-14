// Skin Tone Analysis Hook

import { useState, useCallback } from "react";
import { analyzeSkinTone } from "@/lib/api-client";
import { useUserStore } from "@/store/user-store";
import { createClient } from "@/lib/supabase/client";

export function useSkinTone() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user, setSkinTone } = useUserStore();

  const analyzeTone = useCallback(
    async (file: File) => {
      if (!user) {
        setError("User not authenticated");
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const result = await analyzeSkinTone(file);

        // Save to database
        const supabase = createClient();
        await supabase
          .from("profiles")
          .update({
            skin_tone_id: result.skin_tone_class,
          })
          .eq("id", user.id);

        // Update store
        setSkinTone(result);

        return result;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Analysis failed";
        setError(errorMessage);
      } finally {
        setIsLoading(false);
      }
    },
    [user, setSkinTone]
  );

  return {
    analyzeTone,
    isLoading,
    error,
  };
}
