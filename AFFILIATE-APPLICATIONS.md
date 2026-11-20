# Affiliate applications — battery EMD sites (prepped 2026-11-20)

## Live sites (use these in every application)
- https://48vlifepo4battery.com — 48V LiFePO4 battery price tracker (33 models)
- https://12vlifepo4battery.com — 12V LiFePO4 battery price tracker (80 models)
- https://serverrackbatteries.com — server rack battery price tracker (9 modules)

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
