# UC-001 — Launchpad Rebuild vs. Refactor Framework

**Use case:** UC-001 ALDC Launchpad
**Date:** 2026-05-19
**Status:** Analysis only — no implementation decision made

---

## Migration Strategy Options

### Option A: Incremental Refactor

Modify Launchpad in-place to call Conductor APIs for specific capabilities while keeping Launchpad as the primary runtime.

**Pros:**
- Zero downtime during transition
- Each change is small and reversible
- Launchpad continues working throughout
- Lowest initial investment

**Cons:**
- Creates coupling between two codebases
- Launchpad accumulates tech debt from dual-mode operation
- "Refactored" Launchpad is neither fish nor fowl
- Hard to know when you're done

**Risk:** Medium — coupling risk and "perpetual refactor" risk
**Timeline:** 2-4 weeks per capability swap
**Complexity:** Medium per swap, high overall
**Expected value:** Medium — better than status quo, but doesn't unlock Conductor's full value
**When to choose:** When Launchpad must remain fully operational and Conductor APIs are already stable
**When NOT to choose:** When Conductor's APIs are still changing (they are — P3 hasn't started)

---

### Option B: Module-by-Module Extraction

Extract Launchpad's reusable modules into shared libraries that both Launchpad and Conductor import.

**Pros:**
- Code reuse without duplication
- Both systems benefit from improvements
- Clean interface boundaries enforced by module design

**Cons:**
- Shared library maintenance overhead
- Version coordination between two consumers
- Launchpad's modules were not designed for extraction (monolithic orchestrator.py)
- Python packaging overhead

**Risk:** High — shared library coupling is a well-known antipattern for small teams
**Timeline:** 4-6 weeks for extraction + packaging + integration
**Complexity:** High — requires significant refactoring of Launchpad before extraction
**Expected value:** Low — the effort of making Launchpad modular is better spent building Conductor directly
**When to choose:** When multiple products share truly stable, well-defined modules
**When NOT to choose:** When the source code was not designed for extraction (Launchpad wasn't)

---

### Option C: Strangler Migration into Conductor-Managed Workflows

Progressively route Launchpad workflows through Conductor's engine. Launchpad's dashboard continues to work but gradually reads from Conductor's APIs instead of its own. New workflows are built in Conductor from the start. Old workflows migrate one at a time. Launchpad components are retired as Conductor subsumes them.

**Pros:**
- No big bang — each migration is a small, testable step
- Launchpad remains operational throughout
- New capabilities only built in Conductor (no dual-build)
- Natural forcing function for validating Conductor's APIs
- Launchpad becomes the first real proof that Conductor works

**Cons:**
- Requires maintaining both systems during transition
- Launchpad dashboard needs to learn to read from Conductor APIs
- Transition period may last months
- Need clear criteria for when to retire each Launchpad component

**Risk:** Low-Medium — well-understood pattern (Martin Fowler's strangler fig), and both systems are owned by the same developer
**Timeline:** 6-12 weeks total, but each migration step is 1-2 weeks
**Complexity:** Medium per step, medium overall
**Expected value:** High — validates Conductor with real workflows while maintaining operations
**When to choose:** When the replacement system is being built progressively (Conductor P3-P10), and the existing system must keep running
**When NOT to choose:** When you need Conductor to be complete before any migration (not the case — P3 is enough to start)

**Recommended migration sequence:**
1. After P3: migrate pipeline template definitions (Launchpad's 4 pipeline types → Conductor YAML templates)
2. After P4: migrate agent dispatch (Launchpad's inline agents → Conductor agent runtime)
3. After P5: migrate context enrichment (Launchpad's 6-source assembly → Conductor context packs)
4. After P7: migrate credential handling (Launchpad's direct Key Vault → Conductor broker)
5. After P10: migrate the full connector-migration workflow end-to-end

---

### Option D: Full Rebuild

Rewrite all Launchpad functionality as Conductor features from scratch. Retire Launchpad entirely.

**Pros:**
- Clean architecture from the start
- No legacy compromise
- Single codebase to maintain
- Conductor gets battle-tested against real requirements

**Cons:**
- Long blackout period where Launchpad is retired but Conductor isn't ready
- Risks rebuilding Launchpad's quirks that actually solve real problems
- High effort — Launchpad has 15+ dashboard pages, 4 pipeline types, 5 agents, 6 API functions
- Loses Launchpad's operational history and learnings

**Risk:** High — "second system syndrome" and operational gap
**Timeline:** 12-20 weeks for feature parity
**Complexity:** Very high
**Expected value:** High if Conductor reaches parity, but delayed and risky
**When to choose:** When Launchpad is fundamentally broken and can't be used during transition
**When NOT to choose:** When Launchpad works well enough and a gradual migration is feasible (current situation)

---

### Option E: Leave Launchpad as Domain Plugin / Config Pack

Don't migrate Launchpad. Instead, define a "domain pack" format for Conductor that packages domain-specific pipeline templates, agent definitions, context routing rules, and dashboard views. Launchpad becomes a config pack that runs on Conductor's engine.

**Pros:**
- Cleanest separation of concerns
- Launchpad's domain knowledge is preserved as data
- Other domains (not just ALDC) can create their own packs
- Conductor stays general-purpose

**Cons:**
- Requires Conductor to support a plugin/pack system (not in current roadmap)
- Launchpad's code doesn't cleanly separate into "domain config" and "platform engine"
- The pack format needs to be designed and validated
- Adds complexity to Conductor's architecture

**Risk:** Medium — clean in theory, but the pack format is speculative
**Timeline:** Pack format design: 2-4 weeks. Launchpad pack creation: 4-6 weeks. Requires P3+P4+P5 at minimum.
**Complexity:** High — requires designing the pack abstraction
**Expected value:** Very high if the pack format works — enables Conductor's multi-domain thesis
**When to choose:** After Conductor has proven the core engine (P3-P5 complete) and the pack format has been validated with at least one real domain
**When NOT to choose:** Before the core engine is stable (current situation)

---

## Recommendation

**Option C (Strangler Migration)** is the recommended approach for UC-001.

**Rationale:**
- Conductor is being built progressively (P3-P15), which aligns perfectly with the strangler pattern
- Launchpad must keep running for daily ALDC operations
- Each Conductor phase naturally enables migration of a specific Launchpad capability
- Paul owns both codebases, minimizing coordination overhead
- The migration validates Conductor with real workflows at each step

**Long-term:** After the strangler migration is complete (approximately P10), consider extracting the ALDC-specific parts into a domain pack (Option E) as a formalization of what was built during migration. This creates the template for other domains.

---

## Comparison Matrix

| Criterion | A: Refactor | B: Extract | C: Strangler | D: Rebuild | E: Pack |
|---|:---:|:---:|:---:|:---:|:---:|
| Operational continuity | High | Medium | High | Low | High |
| Initial effort | Low | High | Medium | Very High | High |
| Total effort | High | High | Medium | High | Medium |
| Risk | Medium | High | Low-Medium | High | Medium |
| Conductor validation | Low | Low | High | High | High |
| Time to first value | 2-4 weeks | 4-6 weeks | 1-2 weeks | 12-20 weeks | 8-12 weeks |
| Clean architecture | Low | Medium | Medium | High | Very High |
| Reusability | Low | Medium | Medium | Medium | Very High |
| Recommended timing | Now | Never | **Now (after P3)** | Never | After P5 |
