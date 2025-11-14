-- LokaFit Database Schema
-- Phase 1: Foundation Data Structure

-- Create profiles table (linked to Supabase Auth users)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  height_cm DECIMAL(5,2),
  weight_kg DECIMAL(5,2),
  measurements_json JSONB,
  skin_tone_id UUID,
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create skin_tone_palettes table
CREATE TABLE IF NOT EXISTS skin_tone_palettes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  hex_values JSONB NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create garments table (user's wardrobe items)
CREATE TABLE IF NOT EXISTS garments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  file_url TEXT NOT NULL,
  storage_path TEXT,
  color_hex TEXT,
  measurements_json JSONB,
  garment_type TEXT,
  status TEXT CHECK (status IN ('DRAF', 'PERMANEN')),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create weekly_curations table (AI-generated outfit recommendations)
CREATE TABLE IF NOT EXISTS weekly_curations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  week_of DATE NOT NULL,
  curated_items JSONB NOT NULL,
  styling_notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create try_on_logs table (user's VTO history)
CREATE TABLE IF NOT EXISTS try_on_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  garment_id UUID NOT NULL REFERENCES garments(id) ON DELETE CASCADE,
  manekin_state JSONB,
  capture_image_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE garments ENABLE ROW LEVEL SECURITY;
ALTER TABLE weekly_curations ENABLE ROW LEVEL SECURITY;
ALTER TABLE try_on_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE skin_tone_palettes ENABLE ROW LEVEL SECURITY;

-- RLS Policies for profiles
CREATE POLICY "profiles_select_own" ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "profiles_insert_own" ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

CREATE POLICY "profiles_update_own" ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- RLS Policies for garments
CREATE POLICY "garments_select_own" ON garments FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "garments_insert_own" ON garments FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "garments_update_own" ON garments FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "garments_delete_own" ON garments FOR DELETE
  USING (auth.uid() = user_id);

-- RLS Policies for weekly_curations
CREATE POLICY "curations_select_own" ON weekly_curations FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "curations_insert_own" ON weekly_curations FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- RLS Policies for try_on_logs
CREATE POLICY "logs_select_own" ON try_on_logs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "logs_insert_own" ON try_on_logs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- RLS Policies for skin_tone_palettes (public read)
CREATE POLICY "palettes_select_all" ON skin_tone_palettes FOR SELECT
  USING (true);

-- Create indexes for performance
CREATE INDEX idx_garments_user_id ON garments(user_id);
CREATE INDEX idx_curations_user_id ON weekly_curations(user_id);
CREATE INDEX idx_logs_user_id ON try_on_logs(user_id);
