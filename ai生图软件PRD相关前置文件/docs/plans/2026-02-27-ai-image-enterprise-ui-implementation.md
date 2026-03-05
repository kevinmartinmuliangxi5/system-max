# AI Image Enterprise UI Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build two enterprise-grade, PRD-aligned `.pen` UI files for AI image app MVP.

**Architecture:** Use Pencil MCP to generate two separate design files with identical IA and distinct visual systems. Each file contains three core screens and explicit loading/error/empty states. Validate by screenshot capture and layout checks.

**Tech Stack:** Pencil MCP (`open_document`, `batch_design`, `get_screenshot`, `snapshot_layout`)

---

### Task 1: Requirement Lock

**Files:**
- Modify: `ai生图软件PRD相关前置文件/AI生图软件PRD（MVP）.md`
- Create: `ai生图软件PRD相关前置文件/docs/plans/2026-02-27-ai-image-enterprise-ui-design.md`

**Step 1: Define acceptance checklist**
- Confirm 2 style systems + 3 core pages + state screens.

**Step 2: Verify mapping to PRD core pages**
Run: Manual checklist against PRD section 9
Expected: All pages mapped.

### Task 2: Create Pen File A (Enterprise Calm)

**Files:**
- Create: `ai生图软件PRD相关前置文件/ai-image-ui-enterprise-calm.pen`

**Step 1: Build screen frames and structure**
- Insert app shell, cards, input areas, toolbar, actions.

**Step 2: Apply style tokens and hierarchy**
- Colors, type scale, spacing, radii.

**Step 3: Screenshot verify**
Run: `get_screenshot` for each main frame
Expected: No overlap/clipping, enterprise calm style clear.

### Task 3: Create Pen File B (Neo Tech Ops)

**Files:**
- Create: `ai生图软件PRD相关前置文件/ai-image-ui-neo-tech-ops.pen`

**Step 1: Rebuild same IA with dark technical style**
- Keep structure parity with File A.

**Step 2: Apply contrast-safe dark palette**
- High readability, neon accent usage constrained.

**Step 3: Screenshot verify**
Run: `get_screenshot` for each main frame
Expected: Strong tech identity, no readability regression.

### Task 4: Final Verification

**Files:**
- Verify: both `.pen` files

**Step 1: Layout snapshot check**
Run: `snapshot_layout` with `problemsOnly=true`
Expected: No critical layout issues.

**Step 2: Delivery summary**
- Provide change summary, evidence, residual risks.
