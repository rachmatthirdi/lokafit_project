# LokaFit - AI-Powered Fashion Styling Assistant

LokaFit adalah aplikasi **PWA (Progressive Web App)** yang menggunakan AI untuk membantu pengguna mengelola lemari pakaian mereka, menganalisis warna pakaian, dan mendapatkan rekomendasi outfit berdasarkan skin tone mereka.

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Tech Stack](#tech-stack)
- [Prasyarat Sistem](#prasyarat-sistem)
- [Instalasi & Setup](#instalasi--setup)
- [Struktur Proyek](#struktur-proyek)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Panduan Pengembang](#panduan-pengembang)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Fitur Utama

### 1. **Autentikasi & Profil Pengguna**
- Sign up dengan email dan password
- Verifikasi email otomatis
- Onboarding flow untuk setup profil
- Analisis skin tone dari foto

### 2. **Pindai & Upload Pakaian (Sistem AI 1)**
- **Mode Akurat**: Pindai pakaian dengan coin sebagai kalibrasi ukuran
  - White balance correction
  - Background removal
  - Kalkulasi dimensi dalam CM
- **Mode Cepat**: Upload foto dan ekstrak warna pakaian
  - KMeans color extraction
  - WebP compression untuk performa

### 3. **Manajemen Lemari Pakaian**
- Gallery view untuk semua item pakaian
- Filter dan search berdasarkan warna, tipe, dll
- Draft items yang belum diproses
- Metadata penyimpanan (tipe, warna, skin tone match)

### 4. **Rekomendasi Outfit (Sistem AI 3)**
- **Instant Match**: Rekomendasi outfit berdasarkan item terpilih
  - Teori warna (complementary, analogous, triadic)
  - Skin tone compatibility
- **Weekly Curation**: Kurasi outfit mingguan otomatis
  - Plan for 7 days
  - Berbasis color harmony dan skin tone

### 5. **Virtual Try-On**
- 2D manekin dengan scaling logic
- Preview outfit sebelum dipakai
- Visualisasi warna pada manekin

---

## 🛠 Tech Stack

### **Frontend (Next.js PWA)**
- **Framework**: Next.js 16 (App Router)
- **Bahasa**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui (Radix UI)
- **State Management**: Zustand
- **Form Handling**: React Hook Form + Zod
- **Database**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth (Email/Password)

### **Backend (FastAPI)**
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Image Processing**: OpenCV, Pillow, rembg
- **ML Libraries**: NumPy
- **API Docs**: Swagger/OpenAPI

### **Database**
- **PostgreSQL** (Supabase)
- **Row Level Security (RLS)** untuk keamanan data

### **Deployment**
- **Frontend**: Vercel
- **Backend**: Railway
- **Storage**: Supabase (PostgreSQL + Auth)

---

## 📦 Prasyarat Sistem

### Untuk Development:
- Node.js 18+ & pnpm
- Python 3.9+
- Git
- Supabase account
- Railway account (untuk backend)

### Dependencies:
\`\`\`bash
# Frontend
node_modules (lihat package.json)

# Backend
Python packages (lihat backend/requirements.txt)
\`\`\`

---

## 🚀 Instalasi & Setup

### 1. Setup Database (Supabase)

\`\`\`bash
# Jalankan SQL scripts untuk membuat schema
# File: scripts/001_create_lokafit_schema.sql

# Jalankan seed data untuk skin tones
# File: scripts/002_seed_skin_tones.sql
\`\`\`

**Tables yang dibuat:**
- `profiles` - Data profil pengguna
- `garments` - Data pakaian di lemari
- `skin_tone_palettes` - Palet warna untuk setiap skin tone
- `weekly_curations` - Kurasi outfit mingguan
- `try_on_logs` - History virtual try-on

### 2. Setup Environment Variables

**Frontend (.env.local):**
\`\`\`
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEV_SUPABASE_REDIRECT_URL=http://localhost:3000
\`\`\`

**Backend (.env):**
\`\`\`
DATABASE_URL=your_postgres_connection_string
FASTAPI_PORT=8000
ENVIRONMENT=development
\`\`\`

### 3. Install & Run Frontend

\`\`\`bash
# Install dependencies
pnpm install

# Run development server
pnpm dev

# Build untuk production
pnpm build
pnpm start
\`\`\`

Frontend akan berjalan di `http://localhost:3000`

### 4. Install & Run Backend

\`\`\`bash
# Navigate ke backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload --port 8000
\`\`\`

Backend akan berjalan di `http://localhost:8000`

---

## 📂 Struktur Proyek

\`\`\`
/
├── app/                          # Next.js App Router
│   ├── api/                      # API routes (proxy ke FastAPI)
│   │   ├── auth/
│   │   └── v1/
│   ├── auth/                     # Authentication pages
│   │   ├── login/
│   │   ├── sign-up/
│   │   └── confirm/
│   ├── dashboard/                # Main dashboard
│   ├── pindai/                   # Garment scanning page
│   ├── lemari/                   # Wardrobe gallery
│   ├── onboarding/               # User onboarding flow
│   ├── page.tsx                  # Home page
│   ├── layout.tsx                # Root layout
│   └── globals.css               # Global styles
│
├── components/
│   ├── ui/                       # shadcn/ui components
│   ├── auth-provider.tsx         # Auth context provider
│   ├── garment-capture.tsx       # Camera capture component
│   ├── wardrobe-gallery.tsx      # Gallery view
│   └── user-menu.tsx             # User menu dropdown
│
├── hooks/
│   ├── use-auth.ts              # Auth hook
│   ├── use-garment-scan.ts      # Scanning logic
│   ├── use-recommendations.ts   # Recommendations engine
│   └── use-skin-tone.ts         # Skin tone analysis
│
├── lib/
│   ├── supabase/
│   │   ├── client.ts            # Client-side Supabase
│   │   ├── server.ts            # Server-side Supabase
│   │   └── middleware.ts        # Supabase middleware
│   ├── api-client.ts            # API client untuk FastAPI
│   └── utils.ts                 # Utility functions
│
├── store/
│   └── user-store.ts            # Zustand store
│
├── middleware.ts                 # Route middleware
│
├── backend/                       # FastAPI Backend
│   ├── main.py                  # FastAPI entry point
│   ├── requirements.txt          # Python dependencies
│   ├── app/
│   │   ├── ai_core/
│   │   │   ├── garment_processor.py    # Sistem AI 1
│   │   │   └── mixmatch_logic.py       # Sistem AI 3
│   │   └── api/
│   │       └── v1/
│   │           ├── scan.py             # Scanning endpoints
│   │           ├── profile.py          # Profile endpoints
│   │           └── recommend.py        # Recommendation endpoints
│
├── scripts/
│   ├── 001_create_lokafit_schema.sql   # Database schema
│   └── 002_seed_skin_tones.sql         # Seed data
│
├── public/                       # Static assets
├── package.json
├── tsconfig.json
└── next.config.mjs
\`\`\`

---

## 💾 Database Schema

### Users & Profiles
\`\`\`sql
-- profiles: Menyimpan informasi profil pengguna
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  full_name TEXT,
  skin_tone TEXT,
  photo_url TEXT,
  created_at TIMESTAMP
);
\`\`\`

### Garments (Pakaian)
\`\`\`sql
-- garments: Menyimpan data item pakaian
CREATE TABLE garments (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES profiles(id),
  name TEXT,
  image_url TEXT,
  color_hex TEXT,
  color_name TEXT,
  category TEXT,
  material TEXT,
  dimensions_cm JSON,
  created_at TIMESTAMP
);
\`\`\`

### Skin Tone Palettes
\`\`\`sql
-- skin_tone_palettes: Palet warna untuk setiap skin tone
CREATE TABLE skin_tone_palettes (
  id UUID PRIMARY KEY,
  skin_tone TEXT UNIQUE,
  complementary_colors JSON,
  analogous_colors JSON,
  triadic_colors JSON
);
\`\`\`

### Weekly Curations
\`\`\`sql
-- weekly_curations: Kurasi outfit mingguan
CREATE TABLE weekly_curations (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES profiles(id),
  day_of_week INT,
  recommended_garments JSON,
  created_at TIMESTAMP
);
\`\`\`

**RLS Policies**: Semua table memiliki RLS yang memastikan pengguna hanya bisa mengakses data mereka sendiri.

---

## 🔌 API Documentation

### Frontend API Routes (Next.js)

#### `POST /api/v1/scan`
Proxy ke FastAPI `/scan` endpoint
- Request: FormData dengan file gambar
- Response: JSON dengan garment data

#### `POST /api/v1/profile`
Proxy ke FastAPI `/profile` endpoint
- Request: JSON dengan profile data
- Response: Updated profile data

### Backend Endpoints (FastAPI)

#### 1. **Scanning Endpoints**

**`POST /api/v1/scan/accurate`** - Mode akurat dengan kalibrasi coin
\`\`\`json
Request:
{
  "file": <binary_image>,
  "coin_diameter_px": 50,
  "skin_tone": "warm"
}

Response:
{
  "garment_id": "uuid",
  "dimensions_cm": { "width": 40, "length": 65 },
  "color_hex": "#FF6B6B",
  "color_name": "Red",
  "image_webp_url": "s3://..."
}
\`\`\`

**`POST /api/v1/scan/quick`** - Mode cepat tanpa kalibrasi
\`\`\`json
Request:
{
  "file": <binary_image>
}

Response:
{
  "color_hex": "#FF6B6B",
  "color_name": "Red"
}
\`\`\`

#### 2. **Profile Endpoints**

**`POST /api/v1/profile/skin-tone`** - Analisis skin tone dari foto
\`\`\`json
Request:
{
  "file": <binary_image>
}

Response:
{
  "skin_tone": "warm",
  "confidence": 0.92
}
\`\`\`

#### 3. **Recommendation Endpoints**

**`GET /api/v1/recommend/instant?item_id=uuid`** - Instant outfit match
\`\`\`json
Response:
{
  "item_id": "uuid",
  "matching_items": [
    { "id": "uuid2", "color_name": "Beige", "match_score": 0.95 },
    { "id": "uuid3", "color_name": "Brown", "match_score": 0.88 }
  ],
  "color_theory": "complementary"
}
\`\`\`

**`GET /api/v1/recommend/weekly?user_id=uuid`** - Weekly curation
\`\`\`json
Response:
{
  "week_plan": [
    {
      "day": "Monday",
      "outfit": [
        { "id": "uuid1", "name": "Blue Shirt" },
        { "id": "uuid2", "name": "Black Pants" }
      ]
    },
    // ... 6 more days
  ]
}
\`\`\`

---

## 👨‍💻 Panduan Pengembang

### State Management (Zustand)

**File**: `store/user-store.ts`

\`\`\`typescript
// Global state untuk user dan garments
const userStore = create((set) => ({
  user: null,
  garments: [],
  skinTone: null,
  
  // Actions
  setUser: (user) => set({ user }),
  addGarment: (garment) => set((state) => ({
    garments: [...state.garments, garment]
  })),
  setSkinTone: (tone) => set({ skinTone: tone })
}));

// Usage dalam components
const { user, garments } = userStore();
\`\`\`

### Hooks

#### `useAuth()` - Autentikasi
\`\`\`typescript
const { user, loading, login, logout } = useAuth();
\`\`\`

#### `useGarmentScan()` - Scanning
\`\`\`typescript
const { scan, scanning, error } = useGarmentScan();
const result = await scan(file, mode);
\`\`\`

#### `useRecommendations()` - Rekomendasi
\`\`\`typescript
const { getInstantMatch, getWeeklyPlan } = useRecommendations();
\`\`\`

#### `useSkinTone()` - Skin tone analysis
\`\`\`typescript
const { analyzeSkinTone, analyzing } = useSkinTone();
const tone = await analyzeSkinTone(photoFile);
\`\`\`

### API Client

**File**: `lib/api-client.ts`

\`\`\`typescript
// POST dengan FormData
const result = await apiClient.post('/scan/quick', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});

// GET dengan query params
const recommendations = await apiClient.get('/recommend/instant', {
  params: { item_id: 'uuid' }
});
\`\`\`

### Komponen Utama

#### `<GarmentCapture />`
- Camera capture component
- Bisa mode akurat (dengan coin) atau quick (tanpa)
- Return: FormData ready untuk API

#### `<WardrobeGallery />`
- Display grid garments
- Support filter & search
- Click untuk select & rekomendasi

#### `<AuthProvider />`
- Context wrapper untuk app
- Manage session & user state
- Auto-redirect jika belum login

---

## 🚢 Deployment

### Frontend ke Vercel

\`\`\`bash
# 1. Push ke GitHub
git push origin main

# 2. Connect ke Vercel dari vercel.com
# Vercel otomatis build & deploy saat ada push

# 3. Set environment variables di Vercel dashboard
# NEXT_PUBLIC_SUPABASE_URL
# NEXT_PUBLIC_SUPABASE_ANON_KEY
# NEXT_PUBLIC_API_URL
\`\`\`

### Backend ke Railway

\`\`\`bash
# 1. Create Railway account
# 2. Connect GitHub repo
# 3. Railway otomatis deploy

# 4. Set environment variables di Railway
# DATABASE_URL
# FASTAPI_PORT
# ENVIRONMENT
\`\`\`

### Database (Supabase)

Database sudah hosted di Supabase - tidak perlu deploy ulang, hanya maintain data & schema.

---

## 🔧 Troubleshooting

### Frontend Issues

#### Error: "NEXT_PUBLIC_SUPABASE_URL is not defined"
**Solution**: Cek `.env.local` file dan pastikan semua environment variables tersedia

#### Error: "Failed to fetch from API"
**Solution**: 
- Pastikan backend berjalan di `http://localhost:8000`
- Cek `NEXT_PUBLIC_API_URL` di `.env.local`
- Cek CORS settings di FastAPI

#### PWA tidak install
**Solution**: Pastikan `next.config.mjs` memiliki PWA config dan HTTPS diaktifkan (production)

### Backend Issues

#### ImportError: "No module named 'rembg'"
**Solution**: Jalankan `pip install -r requirements.txt` di virtual environment

#### "Address already in use :8000"
**Solution**: Kill process di port 8000 atau ubah port di `.env`

#### Database connection error
**Solution**: 
- Verifikasi `DATABASE_URL` di `.env`
- Pastikan Supabase server aktif
- Cek firewall/network settings

### Database Issues

#### RLS Policy blocking queries
**Solution**: 
- Pastikan user sudah login (Supabase auth)
- Check RLS policies di Supabase dashboard
- Verify `user_id` match dengan authenticated user

---

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.io/docs)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)

---

## 📝 License

MIT License - Silakan gunakan & modifikasi

---

## 📧 Support

Jika ada pertanyaan atau issues:
- Buat issue di GitHub
- Email: support@lokafit.app

---

**LokaFit © 2025** - AI Fashion Styling Assistant
