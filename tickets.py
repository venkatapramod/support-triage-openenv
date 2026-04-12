# Support Ticket Datasets - Easy, Medium, Hard
# Each ticket has ground truth labels for grading

from typing import List, Dict, Any


def get_easy_tickets() -> List[Dict[str, Any]]:
    """Simple, clear-cut tickets with obvious categorization.
    
    These tickets have unambiguous signals:
    - Single clear issue
    - Category, priority, and department are all obvious from the text
    - No cross-domain confusion
    """
    return [
        {
            "id": "EASY-001",
            "subject": "I was charged twice for my subscription",
            "body": "Hello, I just noticed that my credit card was charged $29.99 twice on March 1st for my Pro subscription. Can you please refund the duplicate charge? My account email is john@example.com.",
            "customer_name": "John Smith",
            "customer_tier": "pro",
            "ground_truth": {
                "category": "billing",
                "priority": "high",
                "department": "finance",
            }
        },
        {
            "id": "EASY-002",
            "subject": "App crashes when I open settings",
            "body": "Every time I click on the settings icon, the app crashes immediately. I'm using version 3.2.1 on Android 14. This happens every single time without fail. I can't access any settings at all.",
            "customer_name": "Mike Chen",
            "customer_tier": "pro",
            "ground_truth": {
                "category": "technical",
                "priority": "high",
                "department": "engineering",
            }
        },
        {
            "id": "EASY-003",
            "subject": "Where is my order?",
            "body": "I placed order #98765 five days ago and the tracking still shows 'Processing'. When will my package ship? I need it by Friday.",
            "customer_name": "Lisa Park",
            "customer_tier": "free",
            "ground_truth": {
                "category": "shipping",
                "priority": "medium",
                "department": "logistics",
            }
        },
        {
            "id": "EASY-004",
            "subject": "How do I export my data to CSV?",
            "body": "Hi, I'd like to know how to export all my project data to CSV format. Is there a built-in export feature? I checked the docs but couldn't find anything. Thanks!",
            "customer_name": "Tom Wilson",
            "customer_tier": "pro",
            "ground_truth": {
                "category": "general",
                "priority": "low",
                "department": "customer_success",
            }
        },
        {
            "id": "EASY-005",
            "subject": "Cancel my subscription please",
            "body": "I would like to cancel my monthly subscription effective immediately. Please confirm the cancellation and let me know if I'll receive a prorated refund for the remaining days.",
            "customer_name": "Emily Davis",
            "customer_tier": "pro",
            "ground_truth": {
                "category": "billing",
                "priority": "medium",
                "department": "finance",
            }
        },
        {
            "id": "EASY-006",
            "subject": "Package arrived damaged",
            "body": "My order #11234 arrived today but the box was crushed and the product inside is broken. I need a replacement or refund please. I took photos of the damage.",
            "customer_name": "Nina Patel",
            "customer_tier": "pro",
            "ground_truth": {
                "category": "shipping",
                "priority": "high",
                "department": "logistics",
            }
        },
        {
            "id": "EASY-007",
            "subject": "Cannot log into my account",
            "body": "I've been trying to log in for the past hour but keep getting 'Invalid password' error. I'm sure my password is correct. I tried resetting it but never received the reset email. Please help me regain access.",
            "customer_name": "Sarah Johnson",
            "customer_tier": "free",
            "ground_truth": {
                "category": "account",
                "priority": "medium",
                "department": "customer_success",
            }
        },
        {
            "id": "EASY-008",
            "subject": "Broken link on your website",
            "body": "The 'Pricing' link in the footer of your website leads to a 404 error page. Just thought I'd let you know!",
            "customer_name": "Kevin Brown",
            "customer_tier": "free",
            "ground_truth": {
                "category": "technical",
                "priority": "low",
                "department": "engineering",
            }
        },
    ]


def get_medium_tickets() -> List[Dict[str, Any]]:
    """Tickets with moderate ambiguity requiring careful reasoning."""
    return [
        {
            "id": "MED-001",
            "subject": "Upgrade not reflected after payment",
            "body": "I paid for the Enterprise plan yesterday via wire transfer (confirmation #WT-44892). However, my dashboard still shows the Pro plan with Pro limits. My team of 50 needs access to the enterprise API endpoints by tomorrow for a product launch. This is blocking our entire release.",
            "customer_name": "David Rodriguez",
            "customer_tier": "enterprise",
            # Trap: looks technical (dashboard not updating) but root cause is billing
            "ground_truth": {
                "category": "billing",
                "priority": "critical",
                "department": "finance",
            }
        },
        {
            "id": "MED-002",
            "subject": "Can't access features I'm paying for",
            "body": "I upgraded to Pro three weeks ago and I'm being charged $29/month. However, the advanced analytics tab still shows a lock icon and says 'Upgrade to Pro to unlock'. I've logged out and back in, cleared my cache, tried different browsers. My billing page confirms I'm on the Pro plan. Is this a billing sync issue or a bug?",
            "customer_name": "Alex Kumar",
            "customer_tier": "pro",
            # Trap: mentions billing AND technical symptoms. Root cause is technical.
            "ground_truth": {
                "category": "technical",
                "priority": "high",
                "department": "engineering",
            }
        },
        {
            "id": "MED-003",
            "subject": "Need to transfer ownership of team workspace",
            "body": "Our team lead Emily Watson (emily@corp.com) is leaving the company next week. We need to transfer ownership of the 'Product Team' workspace to me (carlos@corp.com) before her last day. We have 30 active projects in there. Also, please make sure her access is revoked after the transfer but keep her historical contributions visible.",
            "customer_name": "Carlos Mendez",
            "customer_tier": "enterprise",
            "ground_truth": {
                "category": "account",
                "priority": "high",
                "department": "customer_success",
            }
        },
        {
            "id": "MED-004",
            "subject": "Refund for undelivered order and reshipment",
            "body": "Order #45231 has been stuck in 'In Transit' for 18 days now — the carrier says it's likely lost. I need two things: 1) a full refund for the $450 charge since I never received the item, and 2) a new shipment of the same order sent via expedited shipping at no extra cost. My credit card was charged on day one. This is unacceptable for the premium I pay.",
            "customer_name": "Jennifer Lee",
            "customer_tier": "enterprise",
            # Trap: involves both shipping (lost package) AND billing (refund).
            # Primary action needed is shipping/logistics.
            "ground_truth": {
                "category": "shipping",
                "priority": "high",
                "department": "logistics",
            }
        },
        {
            "id": "MED-005",
            "subject": "Data discrepancy in analytics dashboard",
            "body": "The numbers in our analytics dashboard don't match what we see in the raw API export. For example, the dashboard shows 15,420 events on March 5th but the CSV export shows 14,892. This 3.5% discrepancy is causing issues with our quarterly reporting. We've noticed this pattern for the last 2 weeks. Our finance team is asking questions.",
            "customer_name": "Rachel Green",
            "customer_tier": "enterprise",
            "ground_truth": {
                "category": "technical",
                "priority": "high",
                "department": "engineering",
            }
        },
        {
            "id": "MED-006",
            "subject": "Cancellation and data export before account closes",
            "body": "I've decided to cancel my Pro subscription at the end of this billing cycle. Before my account is deactivated, I need to export all my project data, client records, and report history. Can you walk me through the export process and confirm my cancellation date? Also, will I get a prorated refund for the unused portion?",
            "customer_name": "Brian Foster",
            "customer_tier": "pro",
            # Trap: mentions cancellation (billing), data export (general/account),
            # and refund (billing). Primary need is account lifecycle management.
            "ground_truth": {
                "category": "account",
                "priority": "medium",
                "department": "customer_success",
            }
        },
        {
            "id": "MED-007",
            "subject": "Integration with Slack not working after update",
            "body": "After updating to version 4.0, our Slack integration stopped sending notifications. I've reconnected the OAuth token, verified the webhook URL, and tested with a fresh Slack workspace. The integration status page shows 'Connected' but no messages are being delivered. Our team relies on these notifications for incident response. Logs show the webhook POST returns 200 but Slack never receives the payload.",
            "customer_name": "Priya Patel",
            "customer_tier": "pro",
            "ground_truth": {
                "category": "technical",
                "priority": "high",
                "department": "engineering",
            }
        },
        {
            "id": "MED-008",
            "subject": "Charged for seats of departed employees",
            "body": "Looking at my latest invoice, I'm being billed for 45 seats but we only have 32 active employees. The extra 13 seats are from people who left over the past few months. I assumed inactive accounts would stop being billed automatically. Can you remove those seats and credit us for the overcharges? Also, is there a way to set up automatic seat deprovisioning when we disable accounts in our SSO?",
            "customer_name": "Sandra Kim",
            "customer_tier": "enterprise",
            # Trap: mentions billing AND account management (SSO).
            # Primary issue is billing — they're being overcharged.
            "ground_truth": {
                "category": "billing",
                "priority": "high",
                "department": "finance",
            }
        },
        {
            "id": "MED-009",
            "subject": "Slow response times - is this a known outage?",
            "body": "For the past 2 hours our entire team has been experiencing extremely slow load times (15-20 seconds per page). I checked your status page and it says 'All Systems Operational'. But clearly something is wrong because this is affecting all 8 of our users across different locations and networks. We have a client demo in 90 minutes. Is there an undisclosed incident?",
            "customer_name": "Daniel Wright",
            "customer_tier": "pro",
            "ground_truth": {
                "category": "technical",
                "priority": "critical",
                "department": "engineering",
            }
        },
    ]


def get_hard_tickets() -> List[Dict[str, Any]]:
    """Complex, ambiguous tickets requiring nuanced judgment.
    
    These tickets are designed to be genuinely tricky:
    - Multiple overlapping domains where the "obvious" categorization is wrong
    - Emotional language that biases toward wrong priority levels
    - Cross-departmental issues where routing is non-obvious
    - Subtle distinctions between similar categories
    """
    return [
        {
            "id": "HARD-001",
            "subject": "Multiple issues - urgent help needed",
            "body": "URGENT: We're having a total meltdown here. First, our enterprise SSO stopped working at 2 AM, locking out 200+ employees. Second, while trying to fix it, someone accidentally deleted the admin account. Third, we have a board presentation at 9 AM today using data from your platform and the export feature is returning blank files. We're a Fortune 500 customer paying $50k/year. I need someone on the phone NOW.",
            "customer_name": "Margaret Thompson",
            "customer_tier": "enterprise",
            "ground_truth": {
                "category": "technical",
                "priority": "critical",
                "department": "engineering",
            }
        },
        {
            "id": "HARD-002",
            "subject": "Compliance concern - GDPR data deletion request",
            "body": "Per GDPR Article 17, I'm formally requesting the complete deletion of all personal data associated with my account (user ID: EU-78432) and any associated sub-accounts. This includes backups, logs, analytics data, and any third-party systems where my data may have been shared. I need written confirmation within 30 days as required by regulation. Please also provide a list of all third parties who have received my data. Note: I still want to keep using the service with a fresh account afterward.",
            "customer_name": "Hans Mueller",
            "customer_tier": "pro",
            # Trap: LLMs often classify this as "general" or "technical".
            # It's an account/legal matter routed to admin (compliance team).
            # Priority is critical due to legal deadline.
            "ground_truth": {
                "category": "account",
                "priority": "critical",
                "department": "admin",
            }
        },
        {
            "id": "HARD-003",
            "subject": "Potential security breach detected",
            "body": "Our security team has detected unusual API activity on our enterprise account. Between 1 AM and 4 AM UTC, someone made 50,000+ API calls from an IP address in a country where we have no employees (185.234.xxx.xxx). The calls were reading customer records from our database via your API. We've rotated our API keys but need to know: 1) Was there a breach on your end? 2) What data was accessed? 3) Do we need to file an incident report? Our legal team is standing by. We may also need to notify affected customers under breach notification laws.",
            "customer_name": "James O'Brien",
            "customer_tier": "enterprise",
            # Trap: legal language may bias toward admin/legal department.
            # But this is a security incident — engineering must investigate first.
            "ground_truth": {
                "category": "technical",
                "priority": "critical",
                "department": "engineering",
            }
        },
        {
            "id": "HARD-004",
            "subject": "Invoice dispute and contract renewal question",
            "body": "Hi, three things: 1) Invoice #INV-2024-0892 includes charges for 75 seats but we only have 52 active users. Your own docs say inactive seats are auto-released after 30 days. Please credit $2,875. 2) Our contract renewal is in 6 weeks and we'd like to discuss volume pricing for scaling to 200 seats. 3) Can we get the educational discount? We're a university research lab but signed up under our department's corporate entity.",
            "customer_name": "Dr. Patricia Huang",
            "customer_tier": "enterprise",
            "ground_truth": {
                "category": "billing",
                "priority": "high",
                "department": "finance",
            }
        },
        {
            "id": "HARD-005",
            "subject": "Frustrated with ongoing performance issues - SLA violation",
            "body": "This is my FOURTH ticket about the same issue. Every day between 2-4 PM EST, our dashboard becomes unusably slow (30+ second load times). Previous tickets #1234, #1567, and #1890 were all closed with 'resolved' but NOTHING has changed. Your support team keeps blaming our network but I've done traceroutes, tested from 3 different ISPs and offices. We're in month 2 of a 3-year contract and I'm talking to our legal team about the SLA violation clause. If this isn't fixed this week, we're escalating to your VP of Engineering. I have all the evidence documented.",
            "customer_name": "Robert Kim",
            "customer_tier": "enterprise",
            # Trap: the legal/SLA/contract language may bias toward "account" or
            # "billing" or "admin". But the root issue is a recurring technical
            # performance problem.
            "ground_truth": {
                "category": "technical",
                "priority": "critical",
                "department": "engineering",
            }
        },
        {
            "id": "HARD-006",
            "subject": "Webhook schema change exposing PII - compliance risk",
            "body": "After your last release (v4.2.1), webhooks now include PII fields (email, phone) in the payload that weren't there before. We're sending these webhooks to a third-party analytics tool that is NOT approved for PII in our security policy. Was this an intentional feature addition or a regression? Either way, we need to either: a) roll back the webhook schema, or b) add field-level filtering. This is a potential compliance violation for us under SOC2 requirements and we need it resolved within 48 hours.",
            "customer_name": "Samantha Wright",
            "customer_tier": "enterprise",
            # Trap: SOC2/compliance language biases toward admin department.
            # But this is a code change (webhook schema) that engineering must fix.
            "ground_truth": {
                "category": "technical",
                "priority": "critical",
                "department": "engineering",
            }
        },
        {
            "id": "HARD-007",
            "subject": "Migration stalled - sales promises unfulfilled",
            "body": "We're migrating from Competitor X to your platform. We have 2TB of historical data, 500 custom workflows, and 150 integrations. Your sales rep promised 'white-glove migration support' but it's been 3 weeks and we haven't been assigned a migration engineer. Our contract with Competitor X ends in 45 days and if we don't start NOW we'll have to renew with them for another year at $200k. Can someone please take ownership of this? We need a migration plan, a dedicated engineer, and weekly check-ins.",
            "customer_name": "Amanda Foster",
            "customer_tier": "enterprise",
            # Trap: mentions sales promises and costs ($200k), biasing toward
            # billing/finance. But this is an account management / onboarding
            # issue for customer_success. The $200k is competitor cost, not a
            # billing dispute.
            "ground_truth": {
                "category": "account",
                "priority": "critical",
                "department": "customer_success",
            }
        },
        {
            "id": "HARD-008",
            "subject": "Bulk order damaged in transit - insurance claim needed",
            "body": "We received our bulk hardware order (PO #BLK-2024-445, 50 units, total value $125,000) and 12 units arrived with cracked screens. We need: 1) Immediate replacement of the 12 damaged units, 2) Info on filing an insurance claim with the carrier, 3) A credit for the shipping cost since the damage was due to inadequate packaging, 4) An expedited reshipping timeline because we have a deployment deadline in 2 weeks. Photos of the damage attached. Our warehouse team has preserved all original packaging.",
            "customer_name": "Victor Nakamura",
            "customer_tier": "enterprise",
            # Trap: $125k value and "credit" language bias toward billing/finance.
            # But the primary action is shipping/logistics (replacements, insurance,
            # reshipment).
            "ground_truth": {
                "category": "shipping",
                "priority": "critical",
                "department": "logistics",
            }
        },
        {
            "id": "HARD-009",
            "subject": "Audit log gaps - SOC2 compliance at risk",
            "body": "During our SOC2 audit preparation, we discovered gaps in the audit logs your platform provides. Specifically: 1) User deletion events from January are missing entirely. 2) Permission change logs don't include the 'changed by' field for bulk operations. 3) API access logs have a 4-hour gap on Feb 14th with no explanation. Our auditors need a complete, unbroken chain of evidence. If we can't get clean logs, we'll fail our SOC2 Type II audit next month, which will cost us three major enterprise clients. We need your compliance team to investigate and provide corrected logs within 2 weeks.",
            "customer_name": "Christine Palmer",
            "customer_tier": "enterprise",
            # Trap: "compliance team" and "SOC2 audit" strongly bias toward
            # admin department. But the actual fix requires engineering to
            # investigate log gaps and provide corrected data.
            "ground_truth": {
                "category": "technical",
                "priority": "critical",
                "department": "engineering",
            }
        },
        {
            "id": "HARD-010",
            "subject": "Conflicting information from sales and support about data retention",
            "body": "I'm extremely frustrated. Your sales rep (Jake, ext 4421) told us in writing that our Enterprise plan includes unlimited data retention. But now support is telling us data older than 90 days will be purged next week under some new policy. We have 3 years of critical business data on your platform. We made our purchasing decision based on Jake's promise. I have the email thread saved. If our data gets purged, we'll be pursuing legal action. Please escalate this to someone who can actually make decisions and honor the commitments your sales team made.",
            "customer_name": "Gregory Santos",
            "customer_tier": "enterprise",
            # Trap: legal threats and data purging language may bias toward
            # admin (legal) or technical (data). But this is fundamentally
            # an account management escalation — resolving conflicting promises
            # and protecting the customer relationship.
            "ground_truth": {
                "category": "account",
                "priority": "critical",
                "department": "customer_success",
            }
        },
    ]


TASK_CONFIGS = {
    "easy_triage": {
        "description": "Triage 8 straightforward support tickets with clear categories",
        "tickets_fn": get_easy_tickets,
        "num_tickets": 8,
    },
    "medium_triage": {
        "description": "Triage 9 moderately complex tickets requiring careful reading",
        "tickets_fn": get_medium_tickets,
        "num_tickets": 9,
    },
    "hard_triage": {
        "description": "Triage 10 complex, multi-issue tickets requiring nuanced judgment",
        "tickets_fn": get_hard_tickets,
        "num_tickets": 10,
    },
}
