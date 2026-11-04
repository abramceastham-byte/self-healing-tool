# Planted bugs

The self-healing agent must NOT read this file. It is the answer key for evaluating the tool.

## 1. ZeroDivisionError on products with no reviews

- **Where:** `demo-app/app/main.py`, `average_rating()`, called by `GET /products/{id}/rating`.
- **What:** `sum(ratings) / len(ratings)` divides by zero when the product has no reviews, so the endpoint returns HTTP 500 and Sentry receives a `ZeroDivisionError`.
- **Why tests pass:** every test that checks the average first adds at least one review. No test requests the rating of a product with zero reviews.
- **Trigger (browser):** start the app, open `http://localhost:8000`, and click **Show average rating** on "Desk Lamp" (seeded with no reviews). Or visit `http://localhost:8000/products/3/rating`.
- **Expected fix:** handle the empty case, e.g. return `0.0` (or `None`) with `review_count: 0` when there are no ratings. The UI should keep working.
- **Expected test:** create a product with no reviews, `GET /products/{id}/rating`, assert 200 and `review_count == 0`.
