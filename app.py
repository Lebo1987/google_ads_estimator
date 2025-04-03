from flask import Flask, render_template, request
from utils.bulk_traffic import get_traffic_estimate
from utils.estimate import estimate_revenue

app = Flask(__name__)

# ערכי ברירת מחדל (Fallback)
DEFAULT_VISITS = 1000000         # ביקורים חודשיים
DEFAULT_PAGES_PER_VISIT = 1.5    # עמודים לכל ביקור
DEFAULT_RPM = 10.0             # הכנסה לכל 1000 צפיות (USD)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # האם המשתמש בוחר להשתמש ב-API או במצב ידני
        use_api = request.form.get("use_api")  # "on" אם מסומן, אחרת None
        domain = request.form.get("domain", "").strip().lower() or "manual-input"
        
        if use_api == "on":
            # מצב API: המשתמש מזין רק את הדומיין
            api_data = get_traffic_estimate(domain)
            print("API Data:", api_data)
            if api_data and not api_data.get("error"):
                try:
                    # ניסיון לשלוף את מספר הביקורים מהנתונים שמתקבלים
                    # נניח שמספר הביקורים נמצא ב:
                    visits = api_data["tasks"][0]["result"][0]["items"][0]["metrics"]["organic"]["count"]
                except Exception as e:
                    print("Error parsing API data:", e)
                    visits = DEFAULT_VISITS
            else:
                visits = DEFAULT_VISITS
            pages_per_visit = DEFAULT_PAGES_PER_VISIT
            rpm = DEFAULT_RPM
            mode = "API"
        else:
            # מצב ידני: המשתמש מזין ידנית את הנתונים
            try:
                visits = float(request.form.get("visits", DEFAULT_VISITS))
            except:
                visits = DEFAULT_VISITS
            try:
                pages_per_visit = float(request.form.get("pages_per_visit", DEFAULT_PAGES_PER_VISIT))
            except:
                pages_per_visit = DEFAULT_PAGES_PER_VISIT
            try:
                rpm = float(request.form.get("rpm", DEFAULT_RPM))
            except:
                rpm = DEFAULT_RPM
            mode = "Manual"
        
        page_views, revenue = estimate_revenue(visits, pages_per_visit, rpm)
        result = {
            "mode": mode,
            "domain": domain,
            "visits": visits,
            "pages_per_visit": pages_per_visit,
            "page_views": page_views,
            "rpm": rpm,
            "revenue": revenue
        }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)


