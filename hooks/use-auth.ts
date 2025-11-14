// Authentication Hook with User Management

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { useUserStore } from "@/store/user-store";

export function useAuth() {
  const [isReady, setIsReady] = useState(false);
  const { setUser, setIsLoggedIn, user } = useUserStore();

  useEffect(() => {
    const checkAuth = async () => {
      const supabase = createClient();

      try {
        // Get current session
        const {
          data: { session },
        } = await supabase.auth.getSession();

        if (session?.user) {
          // Fetch user profile
          const { data: profile } = await supabase
            .from("profiles")
            .select("*")
            .eq("id", session.user.id)
            .single();

          if (profile) {
            setUser(profile);
            setIsLoggedIn(true);
          } else {
            // Create profile if it doesn't exist
            await supabase.from("profiles").insert({
              id: session.user.id,
              email: session.user.email,
              full_name: session.user.user_metadata?.full_name || "",
            });

            setUser({
              id: session.user.id,
              email: session.user.email || "",
              full_name: session.user.user_metadata?.full_name || "",
            });
            setIsLoggedIn(true);
          }
        } else {
          setIsLoggedIn(false);
        }
      } catch (error) {
        console.error("[useAuth] Error checking auth:", error);
      } finally {
        setIsReady(true);
      }
    };

    checkAuth();

    // Subscribe to auth changes
    const supabase = createClient();
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(async (event, session) => {
      if (session?.user) {
        const { data: profile } = await supabase
          .from("profiles")
          .select("*")
          .eq("id", session.user.id)
          .single();

        if (profile) {
          setUser(profile);
          setIsLoggedIn(true);
        }
      } else {
        setUser(null);
        setIsLoggedIn(false);
      }
    });

    return () => {
      subscription?.unsubscribe();
    };
  }, [setUser, setIsLoggedIn]);

  return {
    isReady,
    user,
  };
}
