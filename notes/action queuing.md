✅ Design Principle: Queuing Is for Control Load, Not for Strategic Execution
🔒 Implications for Player-Controlled Actors
Queuing is a quality-of-life tool for controlling many actors

It reduces micromanagement burden, especially in squad or colony-scale play

Repeat actions, patrol loops, and chained attacks are for reducing friction, not optimal tactics

“If I’m only controlling one character, I’d probably just issue one action at a time.”

🔒 Implications for AI-Controlled Actors
AI should prefer single-action decision loops, unless queuing provides a clear benefit

Queuing for AI is only used when:

Committing to multi-part maneuvers (e.g. charge + swing)

Creating perceived intent or personality

Reducing overhead for frequently repeated actions

📜 Revised Queue Design Ethos
Actor Type	Queue Role
Player (solo)	Rare use; direct, moment-to-moment control
Player (multi)	Queueing is a control scaling tool
Basic AI	Mostly reacts tick-by-tick
Advanced AI	May queue short tactical chains, but reassess often

🧠 Architectural Response
All actors must support queuing (engine-level)

AI should default to single-action logic

Tactical AI can inject queue chains if needed

Interruptions only flush player queues if they’re clearly invalidated, because the player probably didn’t want them continuing blindly anyway

Player queued actions can optionally include “continue if still valid” checkboxes or flags

Would you like to revisit queue flushing rules now in light of this (e.g., flushing becomes the default unless explicitly marked as persistent)?






You said:
Yes let's revisit


ChatGPT said:
Perfect. Let’s reframe the queue flushing policy in light of your principle:

“Queueing is for reducing control load, not for committing to strategic plans.”

This shifts our default posture toward clearing invalid queues, especially for players.

🧹 Revised Queue Flushing Policy
✅ Default Rule:
Flush invalidated queues unless explicitly marked persistent.

🔁 Who Can Persist?
Actor Type	Can Preserve Queue Post-Interrupt?	Default Behavior
Player-controlled	🔴 No — flush unless explicitly flagged	Clarity and control-first
Basic AI	🔴 No — always reassess	Keeps logic reactive
Advanced AI	🟡 Optional — may requeue behavior chains	If action was part of compound tactic

🔁 Repeat Actions (e.g. fire loop, patrol, suppress)
Are flushed on:

Weapon/tool loss

Status effect that prevents the action (e.g. stunned, restrained)

May resume automatically only if:

Actor is AI with a persistent intent model (e.g. berserker still wants to charge)

Or the action was flagged repeat_if_possible

🧠 Implementation Tags (Internal Use)
We tag queued actions with:

repeat: requeue this same action

tactical_chain: part of multi-step plan

flush_on_interrupt: default unless overridden

resume_if_possible: only if all preconditions still valid

These allow future extensions without cluttering the player experience.

🧾 Messaging Implications
Players always receive:

“Action cancelled: weapon lost.”

“Queue flushed: stunned mid-execution.”

AI can skip explicit feedback unless debugging is enabled.

✅ This model gives you a player-transparent, AI-flexible, and tactically neutral queue system.

Lock this in and proceed to C: Repeat Action Modeling, or review examples where resume-if-possible might apply (like overwatch, patrols)?