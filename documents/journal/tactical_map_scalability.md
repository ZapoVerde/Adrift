### 📍 Tactical Map Scalability – RimWorld-Sized Environments

**Status:** Locked

* The current architecture supports maps up to 250×250 tiles (\~62,500 tiles), consistent with RimWorld-style tactical zones.
* No major structural changes are needed, but strict safeguards are required to avoid catastrophic performance failures.

**🎯 Rationale**

* The project embraces tactical environments that feature:

  * Large, contiguous indoor/outdoor spaces
  * Long-range visibility (100m+)
  * Dozens of actors operating asynchronously
  * Environmental hazards and memory-aware fog-of-war

* These features demand a map architecture that is:

  * Efficient for localized logic
  * Compatible with sparse tile access
  * Scalable without heavy memory mutation or rendering loads

**🧱 Architectural Principles**

* Tiles are stored as a `Dict[(x, y), Dict]` — allowing sparse and direct spatial access
* Actors store individual `seen_tiles` and `visible_tiles` — enabling fog-of-war
* Vision is trace-based and range-limited, not flood-fill
* No nested zones — all logic works directly on `(x, y)` coordinates
* This structure scales well provided access is localized and global sweeps are avoided

**🔥 Red Flag Patterns (Must Be Avoided)**

| 🚫 Pattern                         | 🤔 Why It’s Bad                            | ✅ Preferred Strategy                      |
| ---------------------------------- | ------------------------------------------ | ----------------------------------------- |
| `for tile in floorplan.tiles`      | Iterates 10k+ tiles per tick               | Loop over `visible_tiles` only            |
| `for a in actors: for b in actors` | O(n²) visibility checks with 50+ actors    | Check only within RoP distance            |
| `deepcopy(floorplan.tiles)`        | Massive memory cost, triggers GC churn     | Mutate in-place, track diffs if needed    |
| `draw_all_tiles()`                 | Renders offscreen/unseen tiles             | Slice to visible viewport + margin        |
| Global fire/gas propagation        | Re-evaluates entire map                    | Use event queue or tile-local tick logic  |
| Full-map pathfinding               | Path queries grow quadratically with range | Scope-limited A\* or abort-on-range-limit |

**✅ Structural Safeguards In Place**

**🛡️ Enforcement Guidelines**

* Whenever modifying tactical systems, scan for these anti-patterns:

  * Global tile iteration
  * Actor-to-actor nested loops
  * Unscoped pathfinding or propagation
  * Unbounded rendering

* If detected, refactor or isolate behind batching mechanisms.

* Future enhancements may introduce spatial indexes (quadtrees, chunking), but are not required for MVP.

**📝 Notes**

* This entry is a standing directive. All tactical logic proposals and refactors must be checked against this scalability matrix.
* Flagged red patterns should be discussed before merge or prototype commits.
