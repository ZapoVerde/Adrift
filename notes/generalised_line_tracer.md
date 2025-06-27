Design Journal Update: trace_visibility_path() is a Generalized Line Tracer
📌 Status: Locked
🧠 Rationale
The trace_visibility_path() function was originally introduced for vision line-of-sight checks, but we've agreed that:

A generic grid line tracer — that steps tile-to-tile between an origin and target — has broad tactical utility, including:

Actor vision pathing (visibility logic)

Projectile trajectory modeling (hit/collision checks)

Environmental effect spread (gas, sound, fire)

AI awareness propagation (e.g. alert sentry calling nearby units)

Trap and field detection (e.g. laser tripwires or mines)

📐 Architectural Implications
The function must remain pure and logic-only — no side effects, no actor logic baked in.

The function should return a list of tiles/zones (or optionally terminate early on hit), not just True/False.

All context-specific logic (e.g. “can this actor see through fog?” or “is this thing penetrable by bullets?”) must be handled by the calling function, not inside trace_visibility_path() itself.

Core output format:

python
Copy
Edit
[
    {"coord": (x, y), "tile": {...}, "blocking": False},
    {"coord": (x2, y2), "tile": {...}, "blocking": True},
    ...
]
🧱 Design Philosophy
Build once, use everywhere: don't fork logic between “projectile” and “vision” paths.

Modular priority: enable tactical systems to query the same path and apply different interpretations.

Avoid game-specific terms in function naming or logic. It should work for heat, lasers, arrows, or sound equally well.

🔧 Implementation Constraints
Must support both 8-way diagonal and grid-accurate Bresenham-like paths.

Must respect both tiles and objects with blocks_sight, blocks_projectiles, or custom fields.

Return value must be stable and serializable for debug/testing.

📎 Integration Points
observe() (vision): filters this trace with visibility penalties

resolve_projectile_hit(): stops at first blocking object

apply_environmental_spread(): uses full trace, possibly with falloff

tactical_debug_draw(): renders path for diagnostics

🧪 Test Coverage Requirements
Must test pure tracing behavior across:

straight and diagonal lines

complex terrain

tile and thing overlays

Tests should validate return content, not just True/False.