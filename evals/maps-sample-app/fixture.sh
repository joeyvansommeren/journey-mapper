#!/usr/bin/env bash
# Writes a tiny Next.js invoicing app ("Tally") into the empty eval workspace.
set -euo pipefail

mkdir -p app/signup app/verify-email app/login "app/(dashboard)/invoices/new" app/settings/team \
         "app/pay/[invoiceId]" app/api/invoices app/api/webhooks/stripe lib emails

cat > package.json <<'EOF'
{ "name": "tally", "private": true, "dependencies": { "next": "15.0.0", "stripe": "16.0.0", "resend": "4.0.0" } }
EOF

cat > lib/auth.ts <<'EOF'
// Roles: owners manage billing, admins invite teammates, members create invoices.
export type Role = "owner" | "admin" | "member";
export async function requireRole(role: Role) {
  const session = await getSession();
  if (!session) redirect("/login?next=" + encodeURIComponent(currentPath()));
  if (!hasRole(session.user, role)) redirect("/invoices?error=forbidden");
  return session;
}
EOF

cat > app/signup/page.tsx <<'EOF'
export default function SignUp() {
  return (
    <form action="/api/signup" method="post">
      <h1>Create your Tally account</h1>
      <input name="email" type="email" required />
      <input name="password" type="password" minLength={12} required />
      <input name="company" required />
      <button>Sign up</button>
      <a href="/api/auth/google">Continue with Google</a>
    </form>
  );
}
// On success: createUser() -> sendEmail("verify-email") -> redirect("/verify-email")
EOF

cat > app/verify-email/page.tsx <<'EOF'
export default function VerifyEmail() {
  // No resend button yet; link expires after 15 minutes (lib/tokens.ts).
  return <p>Check your inbox for a verification link.</p>;
}
EOF

cat > app/login/page.tsx <<'EOF'
export default function Login() {
  // Magic link only: POST /api/auth/magic-link -> Resend email -> /invoices
  return <form action="/api/auth/magic-link" method="post"><input name="email" /><button>Email me a link</button></form>;
}
EOF

cat > "app/(dashboard)/invoices/page.tsx" <<'EOF'
export default async function Invoices() {
  await requireRole("member");
  const invoices = await db.invoice.findMany();
  if (invoices.length === 0) return <EmptyState title="No invoices yet" />; // no CTA to create one
  return <InvoiceTable invoices={invoices} />;
}
EOF

cat > "app/(dashboard)/invoices/new/page.tsx" <<'EOF'
// 9-field form: client name, client email, VAT number, line items, currency, due date, notes, PO number, tax rate.
export default function NewInvoice() {
  return <InvoiceForm onSubmit={(data) => fetch("/api/invoices", { method: "POST", body: JSON.stringify(data) })} />;
}
EOF

cat > app/api/invoices/route.ts <<'EOF'
export async function POST(req: Request) {
  await requireRole("member");
  const invoice = await db.invoice.create({ data: await req.json() });
  await stripe.invoices.create({ customer: invoice.stripeCustomerId, collection_method: "send_invoice" });
  await resend.emails.send({ template: "invoice-sent", to: invoice.clientEmail });
  return Response.json(invoice);
}
EOF

cat > app/api/webhooks/stripe/route.ts <<'EOF'
export async function POST(req: Request) {
  const event = stripe.webhooks.constructEvent(await req.text(), req.headers.get("stripe-signature"), secret);
  if (event.type === "invoice.paid") await db.invoice.update({ status: "paid" });
  if (event.type === "invoice.payment_failed") {
    await db.invoice.update({ status: "overdue" });
    await resend.emails.send({ template: "payment-failed", to: event.data.object.customer_email });
  }
}
EOF

cat > "app/pay/[invoiceId]/page.tsx" <<'EOF'
// Public page for the CLIENT receiving an invoice. No login. Stripe Checkout redirect.
export default async function Pay({ params }) {
  const invoice = await db.invoice.findUnique({ where: { id: params.invoiceId } });
  if (!invoice) return <p>This invoice link is invalid.</p>; // no contact info shown
  return <a href={await createCheckoutUrl(invoice)}>Pay {invoice.total}</a>;
}
EOF

cat > app/settings/team/page.tsx <<'EOF'
export default async function Team() {
  await requireRole("admin");
  // Invite by email -> resend "team-invite" template; invite expires after 48h.
  return <InviteForm />;
}
EOF

cat > emails/payment-failed.tsx <<'EOF'
export const PaymentFailed = ({ amount }) => <p>Your payment of {amount} failed. Please try another card.</p>;
EOF
cat > emails/invoice-sent.tsx <<'EOF'
export const InvoiceSent = ({ link }) => <p>You have a new invoice. <a href={link}>View and pay</a></p>;
EOF
