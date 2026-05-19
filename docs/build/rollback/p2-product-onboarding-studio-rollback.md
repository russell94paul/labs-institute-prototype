# Rollback Plan — P2 Product Onboarding Studio

**Phase:** P2-onboarding
**Risk:** Low — P2 is a standalone dashboard page with no engine changes

## Rollback Steps

1. **Delete** `dashboard/pages/onboarding-studio.html`
2. **Revert** `dashboard/index.html`:
   - Remove the "Onboarding" nav link (`<a class="topnav-link" data-route="onboarding">...</a>`)
   - Remove the `'onboarding'` entry from the `routes` object in the SPA router
3. **Revert** `config/phase-status.json`:
   - Set P2-onboarding status back to `"not_started"`
   - Restore `"blockedBy": ["P1-build-studio"]`
   - Clear `expectedFiles`, `reportPath`, `lastUpdated`
4. **Delete** build tracking docs:
   - `docs/build/p2-product-onboarding-studio-build-report.md`
   - `docs/build/rollback/p2-product-onboarding-studio-rollback.md`
   - `docs/build/session-handoffs/p2-product-onboarding-studio-handoff.md`
5. **Revert** `docs/build/change-manifest.md` — remove P2 section
6. **Revert** `docs/build/approval-requests.md` — remove P2 entry
7. **Revert** `docs/build/parallelization-status.md` — revert to P1-complete state

## Impact Assessment

- **No engine code to revert** — P2 added no Python files or API routes
- **No data migration** — P2 uses client-side state only
- **Build Studio unaffected** — P2 is in a separate page with isolated CSS namespace (`onb-`)
- **Bootstrap Console unaffected** — no shared code
- **All existing API endpoints unchanged**

## Verification After Rollback

- `python -c "import json; json.load(open('config/phase-status.json'))"` — valid JSON
- Server starts without error
- Build Studio loads at `#build-studio`
- Bootstrap Console loads at `#bootstrap`
- No `#onboarding` route exists (shows "Page not found")
