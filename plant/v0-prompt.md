# V0.dev Prompt for ZenGarden AI (灵犀园)

## 完整提示词 (复制以下内容到 v0.app/chat)

---

Create a mobile-first React app for "ZenGarden AI" (灵犀园) - a feng shui plant placement assistant with Japanese zen aesthetics. Use Next.js, Tailwind CSS, and Framer Motion.

## Design System

### Colors (CSS Variables)
```
--zen-bg: #FAF8F5 (warm off-white background)
--zen-surface: #FFFFFF (card surfaces)
--zen-text: #1C1C1C (primary text)
--zen-text-secondary: #6B6B6B
--zen-text-muted: #9A9A9A
--zen-border: #E8E5E0
--zen-primary: #4A7C59 (sage green)
--zen-primary-light: #8FBC8F
--zen-primary-dark: #2D5A3D
--zen-accent-gold: #C9A962 (feng shui gold)
```

### Typography
- Font: Inter
- Headlines: 300 weight (light, airy)
- Body: 400-500 weight
- Chinese text support required

### Design Tokens
- Border radius: 16px (cards), 12px (buttons), 80px (pill nav)
- Shadows: subtle, soft (0 4px 16px rgba(74,124,89,0.15))

## 5 Screens to Build

### Screen 1: Home (首页)
- Status bar simulation (9:41, signal, wifi, battery icons)
- Header: Leaf icon + "灵犀园" logo (Inter 300, 24px) + notification bell button (white circle, 40px)
- Hero card: Green gradient (135deg, primary-light → primary → primary-dark), 200px height, rounded-20px
  - Title: "与自然灵犀相通" (white, 28px, weight 300)
  - Subtitle: "发现植物之美，营造风水佳境" (white 80% opacity)
- Section title: "核心功能" (13px, secondary color, 0.3 letter-spacing)
- 2x2 Feature cards grid (gap 12px):
  1. "慧眼识草" - scan-eye icon, green tint bg, "AI识别植物"
  2. "风水罗盘" - compass icon, gold tint bg, "场景分析"
  3. "灵犀推荐" - box icon, green tint bg, "智能匹配"
  4. "AR虚实" - layers icon, green tint bg, "虚实共生"
- Bottom: Floating pill tab bar (iOS 18 style)
  - White pill container (80px radius, 56px height)
  - 4 tabs: home (active, green fill), scan, compass, user
  - Active tab: green pill background with white icon
  - Inactive: muted gray icons

### Screen 2: Plant Identify (植物识别 - 慧眼识草)
- Nav bar: back arrow button + "慧眼识草" title (centered)
- Camera preview area: Dark green gradient (radial), 360px height, rounded-24px
  - Center: Dashed white border frame (200x200, 20px radius)
  - Hint text: "将植物置于取景框内" (white 60% opacity)
- Result card (white, rounded-20px, padding 20px):
  - Plant thumbnail: Green gradient circle (64px) with leaf icon
  - Plant name: "龟背竹" (20px, weight 500)
  - Latin name: "Monstera deliciosa" (italic, secondary color)
  - Confidence badge: "97%" (green bg tint, green text)
  - Divider line
  - Tags row: "净化空气" (muted bg), "耐阴" (muted bg), "招财" (gold bg, gold text)
- Action buttons row:
  - "重拍" - outline style, refresh-cw icon
  - "确认" - primary green fill, check icon

### Screen 3: Feng Shui Analysis (风水分析 - 风水罗盘)
- Nav bar: back button + "风水罗盘" title
- Scene preview placeholder: Gray gradient, rounded-20px, 200px, image icon + "客厅场景"
- Section: "环境分析"
  - 4-column grid in white card:
    - Sun icon (gold) + "光照充足"
    - Droplets icon (blue) + "湿度适中"
    - Thermometer icon (red) + "温度22°C"
    - Wind icon (green) + "通风良好"
- Section: "风水建议"
  - White card with 2 items:
    1. Gold gem icon + "财位·东南角" + "适合放置发财树、金钱树"
    2. Green heart icon + "健康位·正东" + "适合放置绿萝、虎皮兰"
  - Indented dividers (left padding 48px)
- Section: "推荐植物" + "查看全部" link
  - Horizontal scroll cards (120px width each):
    - Circular green gradient image (64px)
    - Plant name: "发财树", "龟背竹", "绿萝"
    - Tag: "招财旺运" (gold), "净化空气" (green), "好养护" (green)

### Screen 4: AR Editor (AR编辑 - AR虚实共生)
- Full screen gray gradient background (simulating camera view)
- Header: X close button + "AR 布置" title + help button (semi-transparent white bg)
- AR Canvas area with:
  - Primary ghost zone: Semi-transparent green (60% opacity), dashed border, 100x120px
    - Label badge at bottom: "财位" (green pill)
  - Secondary ghost zone: Very light green (20% opacity), smaller, dashed border
  - Draggable plant: Green gradient rectangle with shadow (represents the plant being placed)
- Bottom toolbar:
  - 3 tool buttons (white semi-transparent): "缩放" (maximize-2), "旋转" (rotate-cw), "换植物" (repeat)
  - CTA button: Green gradient, "完成布置" with sparkles icon, shadow

### Screen 5: Ceremony Complete (仪式完成)
- Full screen radial gradient: #4A7C59 center → #2D5A3D → #1a3d28 edges
- Center composition:
  - Outer glow: Large ellipse with green gradient (40% → 0% opacity)
  - Inner glow: Medium ellipse with white gradient (30% → 0% opacity)
  - Plant circle: 100px, white 20% fill, white 40% stroke, leaf icon (white, 44px)
- Text area (centered):
  - Poem: "「青叶入室，生机以此为始」" (white, 20px, weight 300, letter-spacing 1px)
  - Subtitle: "愿这一抹绿意，为您带来好运与安宁" (white 60% opacity)
  - Result badge: Semi-transparent white card with check-circle icon (gold) + "龟背竹 · 财位东南" + "已成功布置"
- Bottom buttons:
  - "分享成果" - white fill, green text, share-2 icon
  - "返回首页" - transparent with white border, white text, grid icon

## Interactions & Animations (Framer Motion)

1. **Page transitions**: Slide left/right between screens
2. **Tab bar**: Active tab pill animates with spring physics
3. **Ghost zones in AR**: Subtle pulsing/breathing animation (opacity oscillation)
4. **Ceremony screen**:
   - Glow rings slowly pulse outward
   - Plant icon fades in with scale animation
   - Text fades in sequentially with stagger
5. **Cards**: Subtle hover lift effect
6. **Buttons**: Press scale down to 0.97

## Component Structure

```
/components
  /ui
    - Button.tsx (primary, outline, ghost variants)
    - Card.tsx
    - Badge.tsx
    - TabBar.tsx (floating pill style)
    - NavBar.tsx
  /screens
    - HomeScreen.tsx
    - IdentifyScreen.tsx
    - FengShuiScreen.tsx
    - AREditorScreen.tsx
    - CeremonyScreen.tsx
  /icons
    - Use Lucide React icons
```

## Key Requirements

1. Mobile-first (390px width viewport)
2. Smooth 60fps animations
3. Chinese language support
4. Dark/light text contrast on gradients
5. Consistent 16px border radius on cards
6. Use CSS variables for theming
7. Floating iOS 18-style tab bar

Build all 5 screens as a cohesive mobile app prototype with working navigation between screens.

---

## 简短版提示词 (如果需要更简洁)

---

Build a mobile React app "ZenGarden AI" (灵犀园) - a feng shui plant placement app with Japanese zen aesthetics.

**Tech**: Next.js + Tailwind + Framer Motion + Lucide icons

**Colors**: Sage green (#4A7C59), warm white (#FAF8F5), gold accent (#C9A962)

**5 Screens**:
1. **Home**: Logo, green gradient hero card "与自然灵犀相通", 2x2 feature grid, iOS 18 floating pill tab bar
2. **Plant ID**: Camera preview (dark green), scan frame, result card with plant "龟背竹" + 97% confidence + tags
3. **Feng Shui**: Environment analysis (light/humidity/temp/airflow), feng shui positions (财位·东南角), plant recommendations scroll
4. **AR Editor**: Ghost zones with dashed borders (primary "财位" labeled), draggable plant, bottom tools + "完成布置" CTA
5. **Ceremony**: Radial green gradient, glowing plant icon, poem "青叶入室，生机以此为始", share/home buttons

**Style**: Zen minimal, 16px rounded cards, Inter font (300 weight headlines), soft shadows, Chinese text support.

Add Framer Motion animations: page transitions, pulsing ghost zones, ceremony glow effects.
