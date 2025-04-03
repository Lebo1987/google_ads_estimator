def estimate_earnings_by_category(total_visits, avg_cpc, category):
    """
    מחשב את ההכנסה המשוערת על בסיס:
      total_visits - מספר ביקורים חודשי
      avg_cpc - מחיר ממוצע לקליק (USD)
      category - קטגוריה של האתר
    הערכת CTR מוגדרת לפי הקטגוריה:
      - content: 1.0%
      - niche: 0.7%
      - ecommerce: 1.5%
      - entertainment: 1.2%
      - optimized: 2.0%
    """
    # הגדרת ערכי CTR מומלצים לכל קטגוריה (כעשרוניים)
    category_ctrs = {
        "content": 0.01,
        "niche": 0.007,
        "ecommerce": 0.015,
        "entertainment": 0.012,
        "optimized": 0.02
    }
    # קבלת ערך ה-CTR לפי הקטגוריה; ברירת מחדל: 1%
    ctr = category_ctrs.get(category.lower(), 0.01)
    clicks = total_visits * ctr
    revenue = clicks * avg_cpc
    return revenue, ctr

if __name__ == "__main__":
    # דוגמה: מיליון ביקורים, CPC ממוצע של $0.25
    total_visits = 1_000_000
    avg_cpc = 0.25

    # רשימת קטגוריות לבדיקה
    categories = ["content", "niche", "ecommerce", "entertainment", "optimized"]

    print("Estimated Revenue by Category:")
    for cat in categories:
        revenue, ctr = estimate_earnings_by_category(total_visits, avg_cpc, cat)
        print(f"Category: {cat.capitalize()} - CTR: {ctr*100:.1f}% → Estimated Revenue: ${revenue:,.2f}")
