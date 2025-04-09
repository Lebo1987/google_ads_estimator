from flask import Flask, render_template, request
from utils.bulk_traffic import get_traffic_estimate
from utils.estimate import estimate_revenue

app = Flask(__name__)

@app.template_filter('commafy')
def commafy(value):
    try:
        return "{:,}".format(int(value))
    except:
        return value

# ערכי ברירת מחדל
DEFAULT_VISITS = 1000000
DEFAULT_PAGES_PER_VISIT = 1.5
DEFAULT_RPM = 10.0

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        use_api = request.form.get("use_api")  # "on" אם מסומן, אחרת None
        domain = request.form.get("domain", "").strip().lower()

        if use_api == "on" and domain:
            # מצב API
            api_data = get_traffic_estimate(domain)
            print("📡 API Response:", api_data)

            try:
                visits = api_data["tasks"][0]["result"][0]["items"][0]["metrics"]["organic"]["count"]
            except Exception as e:
                print("❗ Failed to parse API response:", e)
                visits = DEFAULT_VISITS

            pages_per_visit = DEFAULT_PAGES_PER_VISIT
            rpm = DEFAULT_RPM
            mode = "API"
        else:
            # מצב ידני
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
            "domain": domain or "manual input",
            "visits": visits,
            "pages_per_visit": pages_per_visit,
            "page_views": page_views,
            "rpm": rpm,
            "revenue": revenue
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
# Force redeploy test

