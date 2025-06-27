### 💥 Overkill Weapons

**Status:** Locked

* Some weapons are designed for single-use or high-risk deployment with extreme power.
* These weapons have disproportionate damage, special handling requirements, and dramatic side effects.
* They are rare, heavy, or impractical for regular carry but viable in desperate or scripted moments.
* Rationale: Introduces narrative drama, supports tactical high-stakes decisions, and rewards opportunistic play.

**📐 Architectural Implications**

* Defined in `ITEM_DB` with flags like `overkill: true`.
* Often include high stat requirements (especially STR or DEX).
* Critical failures are more severe — e.g. explosion, blindness, injury to self.
* Usage may apply permanent penalties (e.g. recoil injury, deafening).
* May feature limited ammo or be one-use only.

**🔄 Flow Integration**

* Treated as normal weapons in terms of roll resolution, but:
  - Higher base damage + multiplier ceiling
  - Special messaging for unique effect (e.g. `vaporize`, `detonate`, `crush`)
  - Apply narrative consequences if roll fails badly
* Integrated into loot table as rare tier or one-off scenario reward.

**🧠 Design Philosophy**

* Weapons are not balanced for fairness, but for drama and choice tension.
* Players are not expected to use overkill weapons routinely.
* Useful for boss fights, enemy sieges, or clutch reversals.
* Risk and cost ensure overkill use is memorable, not trivial.

**📝 Unstructured Notes**

* Examples: rocket launcher, orbital flare, unstable plasma core.
* Carrying may make actor a target or impose combat penalty.
* Messaging may differ by target size — e.g. `obliterates` small, `maims` large.
* Some may damage environment (e.g. breach walls, collapse floor).
* May be used in AI scripting for shock troops or suicide enemies.
