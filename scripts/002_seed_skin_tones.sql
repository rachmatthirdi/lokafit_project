-- Seed skin tone palettes with Indonesian-focused color theory

INSERT INTO skin_tone_palettes (name, hex_values, description) VALUES
(
  'Warm Undertone',
  '{"primary": "#E8B4A8", "secondary": ["#D4A574", "#C99070", "#B8845C", "#A47548"], "accent": "#F5D4A3"}',
  'Golden, peachy, warm skin tones'
),
(
  'Cool Undertone',
  '{"primary": "#D4A0A0", "secondary": ["#C4949C", "#B488A0", "#A47CA8", "#9876B0"], "accent": "#E8C4D8"}',
  'Pink, rosy, cool skin tones'
),
(
  'Neutral Undertone',
  '{"primary": "#D4A890", "secondary": ["#C49C84", "#B89078", "#A8846C", "#987860"], "accent": "#E8C8A0"}',
  'Balanced, olive, neutral skin tones'
),
(
  'Deep/Dark Skin Tone',
  '{"primary": "#6B4423", "secondary": ["#5C3817", "#4D2C0B", "#3E2000", "#2F1400"], "accent": "#8B6433"}',
  'Deep, dark, warm skin tones'
),
(
  'Light/Fair Skin Tone',
  '{"primary": "#F5D4C4", "secondary": ["#E8C8B8", "#DBBCAC", "#CEB0A0", "#C1A494"], "accent": "#FDE8DC"}',
  'Light, fair, pale skin tones'
);
