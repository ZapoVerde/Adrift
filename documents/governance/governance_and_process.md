# 🏛️ Governance & Process

This document defines the rules that govern the design journal, audit tracking, versioning, assistant behavior, and implementation flow.

---

## 🔒 What “Locked” Means

A system marked as `Locked` is:
- Fully designed and reviewed
- No longer open to spontaneous redesign or exploratory change
- Governed by change control: must be updated in the Design Journal + Changelog

Locked status **does not** mean implemented. It means *canonical design* is complete.

---

## ✅ What “Implemented” Means

A system marked as `Implemented` is:
- Fully coded in appropriate modules
- Tested for both normal and edge behavior
- Confirmed either by audit or explicit implementation milestone

---

## 🛡️ Change Control Rules

To modify any `Locked` system:
1. Create a new Design Changelog entry with:
   - Old → New summary
   - Rationale for change
   - Audit impact (if any)
2. Update the relevant section in the Design Journal
3. Mark in the Version Delta Log with version tag (e.g., v1.3 → v1.4)
4. If system behavior changes, flag for test regeneration

No Locked system may be altered informally.

---

## 📓 Design Changelog Standards

Each entry must include:
- Timestamp (UTC)
- Author (default: user)
- Section or system changed
- Summary of what changed
- Reason (narrative, tactical, technical)
- Implementation follow-up needed?

Example:
```
2025-06-23 — Changed Stealth to include `search()` boost mechanic. Enables active detection. Locked section updated. Requires update to test_search_vs_stealth().
```

---

## 📚 Version Delta Log Standards

Track each meaningful revision to a system or spec. Include:
- Affected system name
- Old version tag → new version tag
- Summary of delta (mechanical, narrative, data, or flow)
- Reference to journal diff (if available)

---

## 📋 Testing Standards

All systems must be testable via:
- Core behavior (normal usage)
- Edge cases (extreme inputs, invalid data)
- Probabilistic behavior (combat rolls, stealth checks)
- Growth behavior (e.g., skill/attribute progression)

Test cases should live alongside implementation files or in `test/`.

---

## 🤖 Assistant Interaction Rules

- Must **not** prompt user to move on unless explicitly invited
- Must **ask for missing documentation** if new system is discussed
- All summaries must be structured, not interpretive
- Will never delete or rewrite design logic without changelog entry
- Will auto-create journal entries, audit flags, and changelogs on user request

---

## 🧱 Summary: Governance Pillars

| Aspect             | Rule                                                                 |
|--------------------|----------------------------------------------------------------------|
| Locking            | Design frozen, cannot be altered without changelog and audit update |
| Implementation     | Must be coded + tested + verified                                    |
| Change Process     | Requires changelog + journal + delta log                            |
| Testing            | Required for all core, edge, and growth behaviors                   |
| Assistant Behavior | Must obey interaction and doc generation rules                      |
