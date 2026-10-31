# ImportGuard — Application Interior Visual Specification

**Document:** `IMPORTGUARD_APP_INTERIOR_VISUAL_SPEC.md`  
**Scope:** Product interior, guest workspace, account flows, and authenticated application  
**Status:** Design and implementation reference  
**Priority:** Preserve the existing public landing page and hero section.

---

## 1. Design objective

ImportGuard should feel like a serious data-processing product built for people who work with real CSV files and depend on accurate results.

The interface must communicate:

- Precision and reliability.
- Clear data structure and readable tables.
- Confidence in validation and export results.
- A professional workflow rather than a collection of unrelated pages.
- A consistent experience from guest use through account creation and authenticated use.

This is not a request to apply a generic dashboard template.

Every screen must have a clear purpose. Every metric must represent real data. Every action must have a defined result. Empty states, errors, loading states, and permission restrictions must receive the same design attention as successful states.

## 2. Scope boundaries

### Explicitly excluded

Do not redesign or replace:

- The public landing page.
- The existing landing page hero section.
- The existing public marketing content.
- The current public website navigation unless a genuine functional issue requires a change.

The existing hero is already part of the website. It is not part of this design task.

### Included

Design and implement the application experience:

1. Guest workspace.
2. CSV upload and preview.
3. Column mapping.
4. Validation and correction results.
5. Export authentication gate.
6. Sign-up and sign-in.
7. Authenticated home.
8. Dashboard.
9. Import history.
10. Export history.
11. Billing and plans.
12. Customer payments.
13. Enterprise team management.
14. Account settings.
15. Help and support.

The owner/admin financial dashboard is a separate restricted interface. It must not be exposed to ordinary customers.

## 3. Visual direction

### Design concept: The Data Workshop

The application should resemble a carefully designed professional data workspace.

It should feel structured, calm, precise, and technically credible.

Use the existing visualization as the initial visual reference, but refine it into a consistent interface system.

**Primary visual characteristics**

- Deep ink or navy application shell.
- Carefully controlled blue and violet accents.
- Neutral, high-contrast working surfaces.
- Clear typography and strong information hierarchy.
- Subtle borders and restrained shadows.
- Distinctive status indicators.
- Dense but readable data tables.
- Consistent spacing and alignment.

Avoid:

- Excessive gradients.
- Glowing borders around ordinary components.
- Decorative dashboard charts with no useful information.
- Random floating cards.
- Oversized empty metric cards.
- Excessive rounded containers.
- Unnecessary animations.
- Generic AI-generated SaaS layouts.
- Emoji as interface icons.

The product should look distinctive through composition, typography, information hierarchy, and interaction quality, not through decorative effects.

### Design principle

**The data is the main visual element.**

The workspace must prioritize the CSV, its columns, mapping decisions, validation results, and export status. The interface must never make the actual data harder to read.

## 4. Application shell

All authenticated pages should share one consistent application shell.

### Desktop layout

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ImportGuard                                      Search   Help  User │
├───────────────┬──────────────────────────────────────────────────────┤
│               │                                                      │
│  WORKSPACE    │  Page title                         Primary action   │
│               │  Short contextual description                      │
│  Home         │                                                      │
│  Dashboard    │  Main page content                                  │
│  Workspace    │                                                      │
│               │                                                      │
│  YOUR DATA    │                                                      │
│  Import       │                                                      │
│  History      │                                                      │
│  Exports      │                                                      │
│               │                                                      │
│  ACCOUNT      │                                                      │
│  Plans        │                                                      │
│  Payments     │                                                      │
│  Settings     │                                                      │
│  Help         │                                                      │
│               │                                                      │
│  Plan usage   │                                                      │
│  Account      │                                                      │
└───────────────┴──────────────────────────────────────────────────────┘
```

### Sidebar

The sidebar should have three visually distinct groups:

**Workspace**
- Home
- Dashboard
- Workspace

**Your data**
- Import History
- Exports

**Account**
- Billing & Plans
- Payments
- Settings
- Help & Support

At the bottom:

- Current subscription.
- Usage indicator.
- Account/profile access.

The sidebar must clearly identify the active page.

Do not make every navigation item visually identical. Use restrained active-state treatment.

### Top bar

Include:

- Current page context or breadcrumb where useful.
- Search only if it performs a real search.
- Help access.
- Notifications only if real notifications exist.
- Account/profile menu.

Do not add nonfunctional controls simply to fill space.

## 5. Guest workspace

This is one of the most important screens.

A visitor must be able to experience the core product before creating an account.

### Primary workflow

```text
Upload CSV
    ↓
Preview data
    ↓
Map columns
    ↓
Review mapping
    ↓
Validate and process
    ↓
Review results
    ↓
Click Export
    ↓
Sign in or create account
    ↓
Restore pending work
    ↓
Download corrected CSV
```

The authentication gate must not appear before the visitor has experienced the actual workflow.

### Workspace layout

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Workspace                                      Guest session         │
│ Prepare, map, and validate your CSV                                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  STEP 01          STEP 02          STEP 03          STEP 04          │
│  Upload      →    Mapping     →    Validation  →   Export            │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  YOUR FILE                                                           │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                                                                │  │
│  │             Upload CSV or drop your file here                  │  │
│  │                                                                │  │
│  │             Supported format and file limits                  │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  FILE PREVIEW                                                        │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ #    Name           Email                 Status                │  │
│  │ 1    Example        example@mail.com      Valid                 │  │
│  │ 2    Example        invalid-email          Needs review          │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

The layout above describes the hierarchy, not fixed dimensions.

### Upload state

Show:

- Upload area.
- Supported file types.
- Maximum file size and other actual limits.
- Upload progress.
- Clear error feedback.
- File name and size after upload.

Do not display invented upload limits.

### CSV preview

The preview is a core product component.

Requirements:

- High contrast between text and background.
- Readable column headings.
- Alternating row treatment where appropriate.
- Horizontal scrolling for wide datasets.
- Sticky column headers when useful.
- Clear distinction between valid, invalid, missing, and suspicious values.
- Pagination or virtualization for larger datasets.
- No white text on white surfaces.
- No clipping of values without a way to inspect them.

The preview must work in both light and dark themes if both themes are supported.

### Column mapping

Display source columns and destination fields clearly.

```text
SOURCE COLUMN                 TARGET FIELD

customer_email       ───────→ Email Address
full_name            ───────→ Full Name
phone_no             ───────→ Phone Number
created              ───────→ Created At
```

Include:

- Mapping confidence only when a real confidence value exists.
- Unmapped field warnings.
- Duplicate mapping warnings.
- Invalid mapping feedback.
- Manual correction.
- Optional Meta suggestions, clearly identified as suggestions.

Meta suggestions must never silently become approved mappings.

### Validation results

Separate the results into meaningful categories:

- Valid records.
- Records requiring correction.
- Missing required values.
- Invalid formats.
- Duplicate records, if supported.
- Other detected issues.

Every result must be traceable to the actual processing output.

Provide a way to inspect affected rows and understand why they were flagged.

### Export action

The export button should be visually prominent when the workflow is ready.

When a guest clicks Export, preserve the pending work and initiate the authentication gate.

Do not silently discard the uploaded file, mapping, or validation results.

## 6. Authentication gate

This is a critical transition, not an unrelated popup.

### Export gate design

```text
┌───────────────────────────────────────────────────────┐
│                                                       │
│              Your file is ready                       │
│                                                       │
│  Create an account to save your work and download     │
│  your corrected CSV.                                  │
│                                                       │
│  [ Continue with sign in ]                            │
│                                                       │
│  [ Create free account ]                              │
│                                                       │
│  Your current workspace will be restored after        │
│  authentication.                                      │
│                                                       │
└───────────────────────────────────────────────────────┘
```

The exact copy may be refined, but the meaning must remain clear.

### Sign-up

Include:

- Name, if required.
- Email.
- Password.
- Password confirmation only if needed.
- Terms/privacy acknowledgement where required.
- Clear validation errors.
- Password visibility control.
- Loading and success states.

### Sign-in

Include:

- Email.
- Password.
- Password visibility control.
- Forgot password flow.
- Clear error feedback.

### Pending-work restoration

After authentication:

1. Verify the account.
2. Retrieve the pending guest workspace securely.
3. Associate it with the authenticated account.
4. Restore the file, mappings, and processing results.
5. Allow the user to download the corrected export.
6. Apply retention and expiry rules to temporary guest data.

The implementation must define secure ownership, expiration, cleanup, and failure handling.

If restoration fails, provide a clear recovery path. Never pretend that the work was restored when it was not.

## 7. Authenticated home

The authenticated home page should be an operational starting point.

It should answer:

- What can I do next?
- What happened recently?
- How much of my plan have I used?
- Where can I continue my work?

Suggested structure:

```text
Welcome back

[ Start a new import ]                  [ View dashboard ]

Recent activity
---------------------------------------------------------
File                  Status             Date
customers.csv         Completed          ...
leads.csv             Needs review       ...

Plan usage
---------------------------------------------------------
Exports used          Remaining quota
Current plan          Renewal information
```

Only show information that exists in the database.

If there is no activity, show a useful empty state with a direct route to the workspace.

## 8. Dashboard

The dashboard should summarize actual user activity.

### Information hierarchy

**Primary section**
- Total imports.
- Successful exports.
- Files requiring attention.
- Current plan usage.

**Secondary section**
- Recent activity.
- Recent imports and exports.
- Validation outcomes.
- Usage over time, if sufficient real data exists.

**Contextual section**
- Current plan.
- Usage allowance.
- Upgrade information when relevant.

Do not show fabricated growth percentages, fake revenue, fake activity, or meaningless charts.

A dashboard with three useful real metrics is better than a dashboard with twelve invented ones.

## 9. Import History

This page should make previous work easy to find.

Table fields:

| Field | Purpose |
|---|---|
| File name | Identify the original file |
| Date | When the import occurred |
| Records | Actual number of processed records |
| Status | Completed, failed, or requires attention |
| Validation | Actual result summary |
| Actions | Open, review, or download where permitted |

Include:

- Search.
- Date filtering where supported.
- Status filtering.
- Pagination.
- Empty state.
- Loading state.
- Error state.

Clicking an item should open its details, subject to the data retention policy.

## 10. Exports

This page is separate from import history.

It should show files that were actually exported.

Suggested columns:

- Export name.
- Related import.
- Export date.
- File format.
- Processing status.
- Download availability.

Do not offer expired or deleted files as downloadable.

Clearly distinguish an export that was generated from one that was successfully downloaded, if that distinction is tracked.

## 11. Billing & Plans

All subscription amounts and billing currencies must be in USD.

There are three plans:

### Free

For individual users testing or using the core product.

Potential limits:

- Limited successful exports.
- Standard file-size limits.
- Basic mapping and validation.
- Shorter history retention.

The suggested allowance is three successful exports per month. Treat this as a proposed product rule until explicitly approved.

### Pro

For individuals with regular CSV workflows.

Potential benefits:

- Higher export allowance.
- Larger files.
- Extended history.
- More advanced mapping and validation.
- Higher processing capacity.

### Enterprise / Business

For teams working together.

Potential benefits:

- Team accounts.
- Shared workspaces.
- Member invitations.
- Role-based permissions.
- Shared history.
- Centralized billing.
- Team usage controls.
- Administrative management.

### Plan comparison design

Do not simply create three identical pricing cards.

Use a clear comparison structure that makes the differences understandable.

```text
YOUR CURRENT PLAN

FREE
Individual use
Current usage: ...

------------------------------------------------------------

PRO
For individual professionals

Features
Usage allowance
File limits
History retention

[ Upgrade to Pro ]

------------------------------------------------------------

ENTERPRISE
For teams and organizations

Team members
Shared workspace
Permissions
Centralized billing

[ Explore Enterprise ]
```

Prices remain unapproved. Do not invent final subscription prices.

Show a clear current-plan state and explain what happens when a quota is reached.

## 12. Customer Payments

This page is for the customer, not the platform owner.

Include:

- Current subscription.
- Billing status.
- Next renewal date, if available.
- Payment history.
- Transaction status.
- Receipts or invoices, if supported.
- Cancellation or plan-change controls, when implemented.

### Payment states

Design clear states for:

- No payment method.
- No payment history.
- Successful payment.
- Pending payment.
- Failed payment.
- Refunded payment.
- Cancelled subscription.
- Expired subscription.

A provider has not yet been selected.

Therefore:

- Do not create fake checkout.
- Do not collect card details.
- Do not imply that payments are available when they are not.
- Keep provider integration separate from the visual interface.
- Use honest unavailable states until a real payment provider is configured.

## 13. Enterprise Team Management

This is a dedicated product capability, not merely another pricing card.

### Team overview

Show:

- Team name.
- Current plan.
- Member count.
- Shared usage.
- Team workspace access.
- Pending invitations.

### Member management

Suggested table:

| Member | Role | Status | Actions |
|---|---|---|---|
| Member name | Owner | Active | Manage |
| Member name | Admin | Active | Manage |
| Member name | Member | Invited | Resend |

### Roles

Define permissions explicitly.

At minimum:

- Owner.
- Admin.
- Member.

Do not assume all team members can access billing, invite members, or manage other users.

### Shared workspace

Team users should be able to distinguish:

- Their own imports.
- Shared team imports.
- Team exports.
- Items they have permission to access.

Tenant isolation must be enforced by the backend, not merely by hiding interface elements.

## 14. Settings

Use clear sections rather than one enormous form.

Suggested categories:

**Profile**
- Name.
- Email.
- Profile details.

**Security**
- Password.
- Active sessions, if supported.
- Account security controls.

**Preferences**
- Theme.
- Display preferences.

**Data and privacy**
- Export account data, if supported.
- Delete account.
- Retention information.

**Team settings**
- Team details.
- Member management, for authorized roles.

All settings must be backed by real functionality.

## 15. Owner/Admin financial dashboard

This is a separate restricted area.

It must not appear in the normal customer sidebar.

Access must be enforced by backend authorization and appropriate administrative roles.

### Main overview

Show actual data for:

- Total revenue.
- Active subscriptions.
- Subscription distribution.
- Successful payments.
- Failed payments.
- Refunds.
- Cancelled subscriptions.

### Transactions

Include:

- Transaction ID.
- Customer.
- Plan.
- Amount in USD.
- Payment status.
- Date.
- Provider reference.

### Subscription management

Authorized administrators may need to inspect:

- Customer subscription status.
- Plan.
- Renewal status.
- Payment history.
- Cancellation status.

Only implement controls that have a defined, secure backend action.

Do not invent revenue or transaction records to make the dashboard look populated.

## 16. Interaction and state design

Every major component must define the states below where applicable:

| State | Expected behavior |
|---|---|
| Default | Normal usable state |
| Hover | Clear interaction feedback |
| Focus | Visible keyboard focus |
| Loading | Progress indication |
| Success | Clear confirmation |
| Empty | Useful next action |
| Error | Understandable explanation |
| Disabled | Explain why unavailable |
| Restricted | Explain permission requirement |

Buttons must have real actions.

Forms must validate input.

Navigation must work.

Dialogs must be dismissible where appropriate.

No decorative button, fake chart, or dead-end screen should remain in the finished product.

## 17. Responsive behavior

Design for:

- Large desktop.
- Standard laptop.
- Tablet.
- Mobile.

### Desktop

- Persistent sidebar.
- Main content uses a readable maximum width.
- Data tables use available space effectively.

### Tablet

- Sidebar can collapse.
- Tables may scroll horizontally.
- Forms remain readable.

### Mobile

- Sidebar becomes a drawer or compact navigation.
- Important actions remain accessible.
- Tables have deliberate mobile behavior.
- No horizontal page overflow.
- Forms use appropriate input widths.
- Dialogs fit within the viewport.
- Upload and preview remain usable.

Do not simply shrink the desktop layout.

## 18. Accessibility

Requirements:

- Sufficient text contrast.
- Visible keyboard focus.
- Semantic headings and landmarks.
- Proper form labels.
- Accessible error messages.
- Keyboard-operable navigation and dialogs.
- Reduced-motion support.
- No status communicated through color alone.
- Appropriate table semantics.

Run automated accessibility checks and manually inspect critical workflows.

## 19. Design system and component library

Build reusable components rather than styling each page independently.

Expected shared components:

- Application shell.
- Sidebar.
- Top bar.
- Page header.
- Buttons.
- Inputs.
- Selects.
- Dialogs.
- Toasts.
- Status indicators.
- Tables.
- Pagination.
- Empty states.
- Loading states.
- Error states.
- Usage indicators.
- Plan comparison.
- File upload.
- CSV preview.
- Mapping rows.
- Validation summary.

Define consistent design tokens for:

- Colors.
- Typography.
- Spacing.
- Borders.
- Radius.
- Shadows.
- Focus states.
- Breakpoints.

Avoid introducing several competing visual systems.

## 20. Implementation acceptance criteria

A screen is not complete merely because it renders.

Each screen must pass these checks:

1. The layout follows this specification.
2. The screen uses the shared design system.
3. All displayed information is grounded in actual application data.
4. Every visible control has a working action or an honest unavailable state.
5. Loading, empty, error, and success states are handled.
6. Desktop and mobile layouts work.
7. Keyboard navigation and focus are usable.
8. Existing functionality has not regressed.
9. Backend authorization is enforced where required.
10. Automated tests and browser checks pass.

### Required visual review

Capture browser screenshots at representative desktop, tablet, and mobile widths.

Review:

- Alignment.
- Spacing.
- Typography.
- Contrast.
- Table readability.
- Responsive navigation.
- Component consistency.
- Visual hierarchy.

Compare the actual implementation against this specification, not against a vague impression of what a SaaS dashboard should look like.

## 21. Final design rule

ImportGuard should look like one carefully designed product.

The guest workspace, authenticated workspace, dashboard, history, billing, payments, and team experience must share the same visual language.

The public landing page and hero remain separate and unchanged during this phase.

**Do not optimize for the number of screens completed. Optimize for a coherent, usable, trustworthy product experience.**