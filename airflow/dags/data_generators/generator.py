from faker import Faker
from datetime import datetime

fake = Faker()

MAX_USERS = 100
MAX_PRODUCTS = 20
MIN_DATETIME = datetime(2024, 1, 1)
MAX_DATETIME = datetime.now()

def gen_event_logs(id_=1) -> dict:
    return {
        "event_id": fake.uuid4(),
        "timestamp": fake.date_time_between(start_date=MIN_DATETIME, end_date=MAX_DATETIME),
        "event_type": fake.random_element([
            "user_login", "product_view", "order_placed", "user_logout", "cart_update",
            "payment_failed", "user_registration", "product_review", "search_query", "password_reset"]),
        "details": {
            "user_id": fake.random_int(1, MAX_USERS),
            "ip_address": fake.ipv4(),
            "status": fake.random_element(["success", "error"])
        }
    }

def gen_moderation_queue(id_=1) -> dict:
    return {
        "review_id": fake.uuid4(),
        "user_id": fake.random_int(1, MAX_USERS),
        "product_id": fake.random_int(1, MAX_PRODUCTS),
        "review_text": fake.text(),
        "rating": fake.random_int(1, 5),
        "moderation_status": fake.random_element(["pending", "approved"]),
        "flags": fake.random_choices(["price_concern", "defective_product", "low_quality",
                                     "delivery_issue", "misleading_description"],
                                     fake.random_int(0, 2)),
        "submitted_at": fake.date_time_between(start_date=MIN_DATETIME, end_date=MAX_DATETIME)
    }

def gen_product_price_history(id_=1) -> dict:
    price_changes = [
        {
            "timestamp": fake.date_time_between(start_date=MIN_DATETIME, end_date=MAX_DATETIME),
            "price": fake.pyfloat(min_value=1, max_value=1000)
        } for _ in range(fake.random_int(1, 20))
    ]
    return {
        "product_id": id_,
        "price_changes": price_changes,
        "current_price": sorted(price_changes, key=lambda x: x['timestamp'])[-1]['price'],
        "currency": fake.random_element(["USD", "EUR"])
    }


def gen_search_queries(id_=1) -> dict:
    return {
        "query_id": fake.uuid4(),
        "user_id": fake.random_int(1, MAX_USERS),
        "query_text": fake.text(max_nb_chars=30),
        "timestamp": fake.date_time_between(start_date=MIN_DATETIME, end_date=MAX_DATETIME),
        "filters": {
            "category": fake.random_element(["electronics", "audio", "wearables", "cameras", "gaming", "tablets",
                                             "e-readers", "monitors", "printers", "networking", "smartphones"]),
            "price_range": fake.random_element(["0-10", "11-50", "51-100", "101-500", "501-1000", "1001-5000",
                                                "5000+"])
        },
        "results_count": fake.random_int(1, 100)
    }

def gen_support_tickets(id_=1) -> dict:
    return {
        "ticket_id": fake.uuid4(),
        "user_id": fake.random_int(1, MAX_USERS),
        "status": fake.random_element(["open", "resolved", "in_progress", "closed"]),
        "issue_type": fake.random_element(["payment", "technical", "account", "delivery", "refund"]),
        "messages": [
            {
                "sender": fake.random_element(["support", "user"]),
                "message": fake.text(max_nb_chars=100),
                "timestamp": fake.date_time_between(start_date=MIN_DATETIME, end_date=MAX_DATETIME)
            } for _ in range(fake.random_int(1, 6))
        ],
        "created_at": fake.date_time_between(start_date=MIN_DATETIME, end_date=MAX_DATETIME),
        "updated_at": fake.date_time_between(start_date=MIN_DATETIME, end_date=MAX_DATETIME)
    }

def gen_user_recommendations(id_=1) -> dict:
    return {
        "user_id": fake.random_int(1, MAX_USERS),
        "recommended_products": fake.random_elements(list(range(1, MAX_PRODUCTS)), length=3),
        "last_updated": fake.date_time_between(start_date=MIN_DATETIME, end_date=MAX_DATETIME)
    }

def gen_user_sessions(id_=1) -> dict:
    start_time = fake.date_time_between(start_date=MIN_DATETIME, end_date=MAX_DATETIME)
    end_time = fake.date_time_between(start_date=start_time, end_date=MAX_DATETIME)
    return {
        "session_id": fake.uuid4(),
        "user_id": fake.random_int(1, MAX_USERS),
        "start_time": start_time,
        "end_time": end_time,
        "pages_visited": [fake.url() for _ in range(fake.random_int(1, 5))],
        "device": {
            "type": fake.random_element(["desktop", "mobile", "tablet"]),
            "user_agent": fake.user_agent(),
        },
        "actions": [
            {
                "action_type": fake.random_element(["click", "scroll", "comment", "add_to_cart", "form_submit", "like",
                                                    "checkout", "search", "share"]),
                "element": fake.random_element(["product_button", "product_page", "checkout_button", "about_link",
                                                "contact_form", "blog_link", "blog_post", "support_link", "faq_search"]),
                "timestamp": fake.date_time_between(start_date=start_time, end_date=end_time)
            } for _ in range(fake.random_int(1, 10))
        ]
    }

