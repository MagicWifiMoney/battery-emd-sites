# Affiliate applications — battery EMD sites (prepped 2026-11-20)

## Live sites (use these in every application)
- https://48vlifepo4battery.com — 48V LiFePO4 battery price tracker
- https://12vlifepo4battery.com — 12V LiFePO4 battery price tracker
- https://24vlifepo4battery.com — 24V LiFePO4 battery price tracker (added 2026-11-21)
- https://serverrackbatteries.com — server rack battery price tracker

## Application status — 2026-11-21

### Impact — COMPLETE
- Account 8279972 (Quiet Coyote LLC, login magicwifimoney@gmail.com).
- All four sites added as properties and verified "Connected" (24V property ID 9204903, verified 2026-11-21).
- Marketplace application declined earlier (does not block direct brand partnerships).
- Payout setup (bank, tax, identity verification, email-verify click) is Jay-only and still open — blocks payouts, not applications.

### Awin — applications COMPLETE 2026-11-21
- Existing publisher account 3113529 (login jake.giebel@gmail.com; approved 2026-10-03). Password reset by Jay 2026-11-21.
- Promotional spaces added for all four battery sites (sectors: DIY, Green (Eco friendly), Home & Garden).
- Brand applications (Advertisers → Join Programs), each with a tailored message naming all four trackers:
  - Dakota Lithium (79634) — SUBMITTED, pending approval. 7% / 30-day cookie, ~$1,000 AOV, no product feed. Contact bjohnson@dakotalithium.com.
  - Vatrer (119703) — JOINED (auto-accepted on application). Tracking link: https://www.awin1.com/cread.php?awinmid=119703&awinaffid=3113529 (deep links append &ued=<url-encoded target>). Product feed = Yes — future path to automate Vatrer prices instead of manual re-pulls.
  - BLUETTI US (59271) — SUBMITTED, pending approval. Tiered 5–10%, 30-day cookie, data feed. Terms bar TM bidding (consistent with our no-brand-bidding stance).
  - EcoFlow (59181) — SUBMITTED, pending approval. 5–8%, covers the US store.
  - Jackery US (59183) — SUBMITTED, pending approval.
  - Redodo Power (97969) — SUBMITTED, pending approval. 5–8%, 30-day cookie. Redodo is not yet in the catalog; the application asks to add its 12V/24V lineup.
  - Eco-Worthy (73461) — SUBMITTED, pending approval. Product feed = Yes.
- Join-dialog note: the Promotion dropdown cannot be set via automation; applications were filed under the default "Content" with the four sites named in the message.
- Payout setup (W-9/tax, bank) is Jay-only and still open.
- Not applied (spotted in directory, candidates only): Powerurus, YOSE POWER US.

### Awin — battery-leftover sweep, 2026-11-21 evening (Jay's ask)
- Directory searched for every catalog brand + adjacent brands (battery, solar, Renogy, LiTime, Anker, Battle Born, BougeRV, Rich Solar, WindyNation, HQST, SunGoldPower, Goal Zero, Victron, Ruixu, EG4).
- NEW applications filed, all SUBMITTED / pending approval:
  - LiTime (82429, US) — directory: 12.21% conv, 86.27% approval, USD 1.28 EPC, 72-day payment, product feed = No. Already in the catalog; on approval, swap its product links to Awin deep links. Contact aptshopmkt02@amperetime.com. (A second "litime" program for another region, feed = Yes, also exists.)
  - Powerurus (79302) — 7% / 30-day cookie, product feed = Yes, 50% conv, 100% approval, USD 13.30 EPC. Not in the catalog yet; application offered to add its lineup via the feed.
  - BougeRV (52765) — 6–10% / 30-day cookie, ~$500 AOV, product feed = Yes, 2.48% conv, USD 0.53 EPC. Not in the catalog yet; RV/trolling-motor fit. Contact affiliate@bougerv.com.
  - Sun Gold Power Co.,Ltd (66184) — 6%, ~$1,000 AOV, product feed = No, 2.12% conv, USD 2.20 EPC. Already in the catalog (SG48200T); on approval, swap links to deep links.
- Candidates only (not applied): YOSE POWER US (launched 2026-11-11, stats n/a, e-bike battery focus), Shop Solar (kit retailer, no feed, USD 0.30 EPC), Better Battery Co. (consumer battery subscription, USD 0.10 EPC — not LiFePO4).
- NO Awin program exists for: Renogy, Anker/Anker SOLIX, Battle Born, Rich Solar, WindyNation, HQST, Goal Zero, Victron, Ruixu, EG4. Their programs (where they exist) live off-Awin.
- Session note: the Awin web session expires within hours; Chrome's saved password on oldie (Jay's reset password) signs back in cleanly in one attempt.

### Amazon Associates — blocked on Jay
- magicwifimoney@gmail.com has no Amazon account; Jay must create it himself, then the Associates application runs from oldie. Stop at the tax interview and bank details.

## Promotional method (paste-ready)
"Price-comparison / price-tracking websites. We collect prices directly from
manufacturers' own online stores several times a day and rank LiFePO4 batteries
by price per watt-hour ($/Wh) in sortable tables with buying guides. Traffic is
organic search (SEO) on exact-match domains. No paid search on brand terms, no
coupon/deal aggregation, no email marketing to purchased lists, no incentivized
clicks. Affiliate links are disclosed on every page."

## Applicant entity
Quiet Coyote LLC (per project plan). Note: domains are registered to
Jacob Giebel / SBFX LLC — if a network asks for site ownership proof, the
Vercel domain dashboard + this repo are the evidence. Jay confirms entity at signup.

## Order of applications
1. **Awin** (one account unlocks most of the catalog) — join at awin.com as a
   Publisher, type "Comparison / Price Comparison". $1 refundable verification
   deposit. Then apply inside Awin to: Dakota Lithium (7%/30d), BLUETTI (5–10%),
   EcoFlow (5–8%), Jackery (5%), Redodo (5–8%), Eco-Worthy.
   JAY-ONLY: W-9 (payment details) — payout floor $20, paid 1st & 15th.
2. **Impact** — BLUETTI, Jackery, Eco-Worthy backups + Walmart/Home Depot (low
   priority). JAY-ONLY: tax document. Payout floor $10.
3. **Amazon Associates** — links render as no-price "Check price on Amazon"
   buttons until Creators API unlocks (needs final Associates acceptance +
   10 qualifying sales in trailing 30 days). JAY-ONLY: tax interview + bank info.
   Mandatory disclosure line: "As an Amazon Associate I earn from qualifying purchases."

## After approval (agent does this)
- Map each brand's product URLs to network deep links in the fetcher config
  (single swap point — product `url` field), rebuild, redeploy.
- Direct-first routing: Awin/Impact links preferred over Amazon (blended
  ~$27.40 vs $17.97 per $599 sale).
