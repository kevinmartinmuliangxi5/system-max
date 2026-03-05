---
title: "Supabase Edge Function JWT Verification and CORS Security"
category: "security-issues"
tags:
  - jwt-authentication
  - cors-configuration
  - edge-function
  - supabase
  - api-security
  - rate-limiting
  - nextjs
module: "zen-garden-ui/supabase/functions/ai-processor"
symptom: |
  - Edge Function accepts requests without JWT verification
  - CORS fallback to localhost allows unauthorized origins
  - API rate limiting not enforced per authenticated user
  - User ID spoofing possible via request body
  - Generic error messages expose internal implementation details
root_cause: |
  Security was not implemented from the start during initial development:
  1. Edge Function lacked authentication middleware
  2. CORS was configured with permissive fallback during development
  3. Client-side was sending anon key instead of user's access token
  4. Rate limiting was only implemented client-side, not server-side
  5. Type definitions were duplicated between client and server
date: 2026-02-16
severity: "critical"
status: "resolved"
related_files:
  - "supabase/functions/ai-processor/index.ts"
  - "lib/api/plant-service.ts"
  - "lib/supabase/client.ts"
  - "hooks/usePlantIdentification.ts"
  - "next.config.mjs"
---

# Supabase Edge Function JWT Verification and CORS Security

## Problem Summary

During code review, multiple critical security vulnerabilities were identified in the ZenGarden AI application's Edge Function and client-side API implementation:

1. **No JWT Verification** - Edge Function accepted requests without authentication
2. **Permissive CORS** - Fallback to localhost allowed unauthorized origins
3. **User ID Spoofing** - Client-provided user IDs were trusted
4. **Missing Rate Limiting** - No server-side quota enforcement
5. **Type Safety Issues** - Duplicate type definitions between client/server

## Investigation Steps

### 1. Security Audit Findings

| Severity | Issue | Location |
|----------|-------|----------|
| Critical | No JWT verification | `ai-processor/index.ts` |
| High | CORS fallback to localhost | `ai-processor/index.ts` |
| High | Client sends anon key, not access token | `plant-service.ts` |
| High | User ID from request body trusted | `plant-service.ts` |
| Medium | No server-side rate limiting | Edge Function |
| Medium | Type duplication | Multiple files |

### 2. OWASP Top 10 Assessment

| Category | Status | Notes |
|----------|--------|-------|
| A01: Broken Access Control | ❌ FAIL | No authentication on Edge Function |
| A07: Auth Failures | ❌ FAIL | No JWT verification |

## Solution

### 1. JWT Verification (Edge Function)

```typescript
// supabase/functions/ai-processor/index.ts

interface AuthResult {
  success: boolean
  userId?: string
  error?: string
}

async function verifyAuth(
  req: Request,
  supabase: ReturnType<typeof createClient>
): Promise<AuthResult> {
  const authHeader = req.headers.get('Authorization')

  // Check for Bearer token
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return { success: false, error: 'Missing or invalid Authorization header' }
  }

  const token = authHeader.replace('Bearer ', '')

  try {
    const { data: { user }, error } = await supabase.auth.getUser(token)

    if (error || !user) {
      return { success: false, error: 'Invalid or expired token' }
    }

    return { success: true, userId: user.id }
  } catch (error) {
    console.error('Auth verification error:', error)
    return { success: false, error: 'Authentication failed' }
  }
}

// Usage in handler
const authResult = await verifyAuth(req, supabase)
if (!authResult.success) {
  return jsonResponse({ error: authResult.error }, 401, corsHeaders)
}
const verifiedUserId = authResult.userId!
```

### 2. CORS Fix (Reject Instead of Fallback)

```typescript
// BEFORE (INSECURE)
function getCorsHeaders(origin: string | null): HeadersInit {
  const allowedOrigin = origin && ALLOWED_ORIGINS.includes(origin)
    ? origin
    : ALLOWED_ORIGINS[0]  // DANGEROUS: Fallback to localhost

  return { 'Access-Control-Allow-Origin': allowedOrigin }
}

// AFTER (SECURE)
function getCorsHeaders(origin: string | null): HeadersInit | null {
  // Reject requests from unauthorized origins
  if (!origin || !ALLOWED_ORIGINS.includes(origin)) {
    return null  // Returns null = reject
  }

  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
  }
}

// Handler rejects unauthorized origins
if (!corsHeaders) {
  return new Response(JSON.stringify({ error: 'Origin not allowed' }), {
    status: 403,
    headers: { 'Content-Type': 'application/json' },
  })
}
```

### 3. Client-Side Authentication

```typescript
// BEFORE (INSECURE)
const response = await fetch(FUNCTION_URL, {
  headers: {
    'Authorization': `Bearer ${process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY}`,
  },
  body: JSON.stringify({
    task,
    imageBase64,
    userId: session?.user?.id,  // DANGEROUS: Trusted client-provided ID
  }),
})

// AFTER (SECURE)
const session = await getOrCreateSession()
const accessToken = session?.access_token
if (!accessToken) {
  return { error: 'Please login first' }
}

const response = await fetch(FUNCTION_URL, {
  headers: {
    'Authorization': `Bearer ${accessToken}`,  // User's JWT token
  },
  body: JSON.stringify({
    task,
    imageBase64,
    // SECURITY: userId NOT sent - server extracts from verified JWT
  }),
})
```

### 4. Server-Side Rate Limiting

```typescript
const RATE_LIMITS: Record<string, number> = {
  identify: 10,  // 10 requests per day
  analyze: 5,    // 5 requests per day
}

async function checkRateLimit(
  supabase: ReturnType<typeof createClient>,
  userId: string,
  endpoint: string
): Promise<{ allowed: boolean; remaining: number }> {
  const limit = RATE_LIMITS[endpoint] || 10
  const now = new Date()
  const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate())

  const { count } = await supabase
    .from('api_usage_log')
    .select('*', { count: 'exact', head: true })
    .eq('user_id', userId)
    .eq('endpoint', endpoint)
    .eq('success', true)
    .gte('created_at', startOfDay.toISOString())

  const used = count || 0
  return {
    allowed: used < limit,
    remaining: Math.max(0, limit - used),
  }
}

// Usage
const rateLimit = await checkRateLimit(supabase, verifiedUserId, payload.task)
if (!rateLimit.allowed) {
  return jsonResponse({ error: 'Daily limit exceeded' }, 429, corsHeaders)
}
```

### 5. Type Safety (Eliminate Duplication)

```typescript
// BEFORE: Types duplicated in multiple files
// hooks/usePlantIdentification.ts
interface FengShuiAnalysisResult { ... }  // Weaker types

// AFTER: Import from central types
// hooks/usePlantIdentification.ts
import type { PlantIdentification, FengShuiAnalysis } from '@/lib/types'
```

### 6. Security Headers (Next.js)

```javascript
// next.config.mjs
async headers() {
  return [{
    source: '/:path*',
    headers: [
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(*), microphone=(), geolocation=()' },
    ],
  }]
}
```

## Prevention Strategies

### Code Review Checklist for Edge Functions

- [ ] JWT verification is the FIRST operation in handler
- [ ] User ID extracted from verified JWT, NEVER from request body
- [ ] 401 response for missing/invalid tokens
- [ ] CORS whitelist defined, NO wildcards
- [ ] Unauthorized origins receive 403, not CORS headers
- [ ] Rate limiting implemented for expensive operations
- [ ] 429 response when rate limit exceeded
- [ ] Error messages don't leak internal details
- [ ] API keys via headers, not URL params

### Client-Side Patterns

- [ ] Use user's `access_token`, not `anon_key`
- [ ] Don't send userId in request body
- [ ] Handle 401 (re-auth), 403 (CORS), 429 (rate limit)
- [ ] Import types from central `@/lib/types`

## Test Cases

```typescript
// Unit test: JWT verification
it('should reject requests without Authorization header', async () => {
  const req = new Request('https://example.com/api', { method: 'POST' })
  const result = await verifyAuth(req, mockSupabase)
  expect(result.success).toBe(false)
  expect(result.error).toBe('Missing or invalid Authorization header')
})

// Unit test: CORS
it('should reject OPTIONS requests from unauthorized origins', async () => {
  const response = await fetch(FUNCTION_URL, {
    method: 'OPTIONS',
    headers: { Origin: 'https://malicious-site.com' },
  })
  expect(response.status).toBe(403)
})

// Unit test: Rate limiting
it('should reject requests at the limit', async () => {
  mockSupabase.select.mockResolvedValue({ count: 10 })
  const result = await checkRateLimit(mockSupabase, 'user-123', 'identify')
  expect(result.allowed).toBe(false)
})
```

## References

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Next.js Security Headers](https://nextjs.org/docs/advanced-features/security-headers)

## Related Issues

- Security Review Report: `docs/plans/2026-02-15-zengarden-technical-review.md`
- Security Patch Documentation: `docs/plans/2026-02-15-security-patch.md`

---

**Compounded on:** 2026-02-16
**Files affected:** 5
**Severity reduction:** Critical → Resolved
