// Wardrobe gallery component with state management

"use client";

import { useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useUserStore } from "@/store/user-store";
import { createClient } from "@/lib/supabase/client";
import Link from "next/link";

export function WardrobeGallery() {
  const { user, garments, setGarments, isLoading } = useUserStore();

  useEffect(() => {
    if (!user) return;

    const loadGarments = async () => {
      const supabase = createClient();
      const { data } = await supabase
        .from("garments")
        .select("*")
        .eq("user_id", user.id);

      if (data) {
        setGarments(data);
      }
    };

    loadGarments();
  }, [user, setGarments]);

  if (isLoading) {
    return (
      <div className="text-center text-muted-foreground">
        Loading your wardrobe...
      </div>
    );
  }

  if (garments.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground mb-4">Your wardrobe is empty</p>
        <Link href="/pindai">
          <Button>Scan Your First Item</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {garments.map((garment) => (
        <Card
          key={garment.id}
          className="overflow-hidden hover:shadow-lg transition cursor-pointer"
        >
          <CardContent className="p-0">
            <div className="aspect-square bg-muted overflow-hidden">
              {garment.file_url ? (
                <img
                  src={garment.file_url || "/placeholder.svg"}
                  alt={garment.garment_type}
                  className="w-full h-full object-cover hover:scale-105 transition"
                />
              ) : (
                <div
                  className="w-full h-full flex items-center justify-center"
                  style={{ backgroundColor: garment.color_hex || "#ccc" }}
                />
              )}
            </div>
            <div className="p-4">
              <p className="font-medium text-sm text-balance">
                {garment.garment_type || "Garment"}
              </p>
              <p className="text-xs text-muted-foreground">
                {garment.status}
              </p>
              {garment.color_hex && (
                <div className="flex items-center gap-2 mt-2">
                  <div
                    className="w-4 h-4 rounded"
                    style={{ backgroundColor: garment.color_hex }}
                  />
                  <span className="text-xs">{garment.color_hex}</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
