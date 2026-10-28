# VentureLink

Full-stack investor / business membership network built with React, Vinext, Cloudflare D1 and R2.

## Pages
`/` marketing; `/register` onboarding; `/dashboard` top-five matches; `/discovery` filtered profiles; `/inbox` requests and conversations; `/settings` profile, uploads and billing; `/admin` owner administration; `/privacy` privacy and trust.

## Configuration before public launch
- Set `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` as secret Sites runtime variables. Never place them in browser code or source.
- Configure a Stripe Customer Portal with cancellation enabled.
- Register `/api/stripe/webhook` for snapshot events: `checkout.session.completed`, `invoice.paid`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted`, `customer.subscription.paused`, `customer.subscription.resumed`.
- The deployment initially stays owner-private. Stripe webhooks and external visitors require a public, reachable deployment before live onboarding; sharing must be explicitly changed by the owner.
- `ADMIN_EMAILS` is a comma-separated server-side administrator allowlist. The owner email is configured in Sites.
- Membership is implemented as **$10 monthly OR $10 yearly**, as selected. No separate initial registration charge is added. Confirm commercial pricing before launch.
- Add your business identity, support contact, terms, and document-retention policy before accepting real customers.

## Behavior
Authentication uses platform-owned ChatGPT sign-in and sign-out. A signed-in user can prepare a profile; paid and manually approved members can connect and message. Document verification is a separate manual decision. Changing a profile submits it for re-approval and clears its verification badge. Identity documents are private to their owner and admins. PDF/JPG/PNG uploads are limited to 10 MB and checked for file signatures.

Inbox uses authenticated Server-Sent Events, checking for conversation changes every two seconds, with a 15-second refresh fallback. Streams reconnect automatically after 50 seconds. Match scores weight sector 40%, stage 20%, country 15%, and proportional funding alignment 25%; only opposite-party profiles are suggested. Matches are recomputed from current preferences. Profile review reminders appear in the dashboard after 30 or 365 days, not by email.

The homepage and pre-membership Discovery show clearly identified illustrative profiles. No demo data is seeded into production. Saved-profile bookmarks last for the current page session.

## Local development
`npm run dev` starts the loopback preview. Local platform sign-in simulates `seedy@sites.test`; this shim is excluded from production. Run `npm run db:generate` after schema changes. Apply generated migrations to local D1 using the starter README commands. Production migrations are applied by Sites publication.

Checks: `npx tsc --noEmit`, `npm run build`. Use the Sites packaging workflow for deployment.

## Stripe references
- https://docs.stripe.com/webhooks
- https://docs.stripe.com/billing/subscriptions/webhooks
