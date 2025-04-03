def estimate_revenue(visits, pages_per_visit, rpm):
    """
    מחשב את ההכנסה המשוערת על בסיס:
      visits: מספר ביקורים חודשיים,
      pages_per_visit: ממוצע עמודים לכל ביקור,
      rpm: הכנסה (USD) לכל 1000 צפיות.
    """
    page_views = visits * pages_per_visit
    revenue = (page_views / 1000) * rpm
    return page_views, round(revenue, 2)






