

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
    - Diverse ground truths — NOT dominated by technical/critical/engineering
    """
    return [
        {
            "id": "HARD-001",
            "subject": "URGENT: SSO down, admin deleted, exports broken",
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
            "subject": "GDPR Article 17 - formal data deletion request",
            "body": "Per GDPR Article 17, I'm formally requesting the complete deletion of all personal data associated with my account (user ID: EU-78432) and any associated sub-accounts. This includes backups, logs, analytics data, and any third-party systems where my data may have been shared. I need written confirmation within 30 days as required by regulation. Please also provide a list of all third parties who have received my data. Note: I still want to keep using the service with a fresh account afterward.",
            "customer_name": "Hans Mueller",
            "customer_tier": "pro",
         
            "ground_truth": {
                "category": "account",
                "priority": "critical",
                "department": "admin",
            }
        },
        {
            "id": "HARD-003",
            "subject": "Our contract says unlimited storage but you're throttling us",
            "body": "I'm extremely frustrated. Our Enterprise contract (signed Jan 2023, 3-year term) explicitly states 'unlimited cloud storage' in Section 4.2. Yesterday we received an email saying we've exceeded a '5TB fair use limit' that appears nowhere in our contract, and our upload speeds have been throttled to 1 Mbps. Our legal counsel has reviewed the contract and confirms there is no fair use clause. We demand immediate restoration of full upload speeds and a written acknowledgment that no storage limits apply to our account. If not resolved by EOD Friday, we'll be filing a formal breach of contract claim.",
            "customer_name": "Victoria Sterling",
            "customer_tier": "enterprise",
         
            "ground_truth": {
                "category": "billing",
                "priority": "critical",
                "department": "finance",
            }
        },
        {
            "id": "HARD-004",
            "subject": "Need to consolidate 3 separate company accounts after merger",
            "body": "Following our acquisition of TechCorp and DataFlow Inc last month, we now have 3 separate enterprise accounts on your platform (IDs: ENT-001, ENT-445, ENT-892) that need to be merged into one. Combined we have 800+ users, 15TB of data, and hundreds of custom integrations. We need: 1) All data migrated to a single account without any loss, 2) User permissions preserved from all three accounts, 3) Billing consolidated to a single invoice, 4) API keys and webhooks remapped. Our CTO wants this done within 60 days. What's the process?",
            "customer_name": "Richard Yamamoto",
            "customer_tier": "enterprise",
        .
            "ground_truth": {
                "category": "account",
                "priority": "high",
                "department": "customer_success",
            }
        },
        {
            "id": "HARD-005",
            "subject": "Frustrated with ongoing performance - SLA violation",
            "body": "This is my FOURTH ticket about the same issue. Every day between 2-4 PM EST, our dashboard becomes unusably slow (30+ second load times). Previous tickets #1234, #1567, and #1890 were all closed with 'resolved' but NOTHING has changed. Your support team keeps blaming our network but I've done traceroutes, tested from 3 different ISPs and offices. We're in month 2 of a 3-year contract and I'm talking to our legal team about the SLA violation clause. If this isn't fixed this week, we're escalating to your VP of Engineering.",
            "customer_name": "Robert Kim",
            "customer_tier": "enterprise",
    
            "ground_truth": {
                "category": "technical",
                "priority": "critical",
                "department": "engineering",
            }
        },
        {
            "id": "HARD-006",
            "subject": "Your sales rep promised features that don't exist",
            "body": "Before signing our $120k/year enterprise contract, your sales rep Jake (ext 4421) specifically demonstrated a 'real-time collaboration' feature during our eval. He showed us live co-editing of documents with presence indicators and conflict resolution. We signed largely because of this capability. Now that we're onboarded, this feature doesn't exist anywhere in the product. When I asked support, they said it's 'on the roadmap for Q4.' We signed a contract based on a feature demo that was apparently faked. I want either: a) the feature delivered within 30 days as demonstrated, or b) a full contract refund. Our legal team is preparing a misrepresentation claim.",
            "customer_name": "Natasha Volkov",
            "customer_tier": "enterprise",
         
            "ground_truth": {
                "category": "account",
                "priority": "critical",
                "department": "customer_success",
            }
        },
        {
            "id": "HARD-007",
            "subject": "International shipping nightmare - customs seizure",
            "body": "Our bulk order of 200 units (PO #INTL-7789, value $340,000) has been seized by German customs because the commercial invoice lists the wrong HS tariff code and the country of origin is missing. The customs broker says the shipment will be destroyed if proper documentation isn't provided within 10 business days. We also discovered the declared value on the export docs shows $50,000 instead of $340,000 — this looks like it could be flagged as customs fraud. We need corrected commercial invoices, proper certificates of origin, and someone to liaise with our customs broker in Frankfurt IMMEDIATELY. This is a potential criminal matter if not resolved.",
            "customer_name": "Klaus Weber",
            "customer_tier": "enterprise",
       
            "ground_truth": {
                "category": "shipping",
                "priority": "critical",
                "department": "logistics",
            }
        },
        {
            "id": "HARD-008",
            "subject": "Webhook PII exposure - SOC2 compliance violation",
            "body": "After your last release (v4.2.1), webhooks now include PII fields (email, phone) in the payload that weren't there before. We're sending these webhooks to a third-party analytics tool that is NOT approved for PII in our security policy. Was this an intentional feature addition or a regression? Either way, we need to either: a) roll back the webhook schema, or b) add field-level filtering. This is a potential compliance violation for us under SOC2 requirements and we need it resolved within 48 hours.",
            "customer_name": "Samantha Wright",
            "customer_tier": "enterprise",
       
            "ground_truth": {
                "category": "technical",
                "priority": "critical",
                "department": "engineering",
            }
        },
        {
            "id": "HARD-009",
            "subject": "Renewal pricing dispute - competitor offering 60% less",
            "body": "Our 3-year enterprise contract is up for renewal next month. Your renewal quote came in at $180k/year — a 20% increase. Meanwhile, CompetitorX is offering equivalent functionality at $72k/year with free migration support. Before we make a decision, I need: 1) Justification for the price increase when we've had 4 major outages this year, 2) A revised quote that's competitive, 3) An account credit of $15k for the SLA violations we documented but never received compensation for, 4) Written commitment to the feature roadmap items your PM promised us last quarter. We've been a loyal customer for 5 years but loyalty doesn't pay the bills.",
            "customer_name": "Angela Morrison",
            "customer_tier": "enterprise",
  
            "ground_truth": {
                "category": "billing",
                "priority": "high",
                "department": "finance",
            }
        },
        {
            "id": "HARD-010",
            "subject": "Need to revoke ex-contractor access - security exposure",
            "body": "We just discovered that a contractor we terminated 3 months ago (user: mike.contractor@external.com) still has active access to our enterprise account. He has admin-level permissions, can see all our client data, and his API key is still active. We terminated him for cause (data policy violations) and this is a massive security exposure. We need: 1) His access revoked immediately across all systems, 2) A complete audit log of everything he accessed in the last 90 days, 3) Confirmation his API key has been invalidated, 4) An explanation for why your platform didn't auto-revoke when we disabled his SSO. Our CISO is furious and wants a written incident report.",
            "customer_name": "Patricia Wong",
            "customer_tier": "enterprise",

            "ground_truth": {
                "category": "account",
                "priority": "critical",
                "department": "admin",
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
