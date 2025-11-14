// Global User State Management with Zustand
// Handles: User profile, wardrobe cache, authentication state

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  height_cm?: number;
  weight_kg?: number;
  skin_tone_id?: string;
  avatar_url?: string;
}

export interface Garment {
  id: string;
  file_url: string;
  color_hex: string;
  measurements_json?: Record<string, any>;
  garment_type: string;
  status: "DRAF" | "PERMANEN";
}

interface UserStore {
  // State
  user: UserProfile | null;
  garments: Garment[];
  skinToneResult: Record<string, any> | null;
  isLoggedIn: boolean;
  isLoading: boolean;

  // Actions
  setUser: (user: UserProfile | null) => void;
  setGarments: (garments: Garment[]) => void;
  addGarment: (garment: Garment) => void;
  setSkinTone: (result: Record<string, any>) => void;
  setIsLoggedIn: (isLoggedIn: boolean) => void;
  setIsLoading: (isLoading: boolean) => void;
  clearStore: () => void;
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      user: null,
      garments: [],
      skinToneResult: null,
      isLoggedIn: false,
      isLoading: false,

      setUser: (user) => set({ user }),
      setGarments: (garments) => set({ garments }),
      addGarment: (garment) =>
        set((state) => ({ garments: [garment, ...state.garments] })),
      setSkinTone: (result) => set({ skinToneResult: result }),
      setIsLoggedIn: (isLoggedIn) => set({ isLoggedIn }),
      setIsLoading: (isLoading) => set({ isLoading }),
      clearStore: () =>
        set({
          user: null,
          garments: [],
          skinToneResult: null,
          isLoggedIn: false,
        }),
    }),
    {
      name: "lokafit-user-store",
    }
  )
);
