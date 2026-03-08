import csv
from collections import defaultdict
from html import escape

CSV_FILE = "Members_-_Members.csv"
OUTPUT_FILE = "alumni.html"
DEFAULT_IMG = "assets/images/members/jane-doe.png"
MEMBERS_IMG_BASE = "assets/images/members/"

def img_src(path):
    """Return image src: use member path if available, else default."""
    if path and path.strip():
        return MEMBERS_IMG_BASE + path.strip()
    return DEFAULT_IMG

def build_html(members_by_semester):
    sections = ""
    for semester, members in members_by_semester.items():
        items = ""
        for i, m in enumerate(members, start=1):
            name = escape(m["name"])
            semesters = escape(m["listofsemesters"])
            quote = m["quote"].strip()
            citation = m["citation"].strip()
            left_img = img_src(m["image"])
            right_img = img_src(m["crazyimage"])

            quote_html = ""
            if quote:
                cite_html = f' <span class="citation">— {escape(citation)}</span>' if citation else ""
                quote_html = f'<p class="member-quote">"{escape(quote)}"{cite_html}</p>'

            items += f"""
        <li class="member-item">
          <img src="{left_img}" alt="{name}" class="member-img-left">
          <div class="member-info">
            <strong>{name}</strong>
            <p><span>Semesters in GamesCrafters:</span> {semesters}</p>
            {quote_html}
          </div>
          <img src="{right_img}" alt="{name} crazy" class="member-img-right">
        </li>"""

        sections += f"""
      <h3 id="{semester.replace(' ', '-').lower()}">Joined in {escape(semester)}</h3>
      <ol class="members-list">{items}
      </ol>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GamesCrafters :: Alumni</title>
  <link rel="stylesheet" href="main.css">
</head>
<body>

  <div class="page-logo">
    <a href="index.html">GamesCrafters</a>
  </div>

  <div class="page-nav">
    <h1>Alumni</h1>
  </div>

  <div class="page-content">
    <div class="page-content-wrapper">
      {sections}
    </div>
  </div>

  <div class="page-footer">
    <div class="page-footer-wrapper">
      <p>© GamesCrafters — UC Berkeley</p>
      <p>A research and development group exploring combinatorial game theory.</p>
    </div>
  </div>

</body>
</html>"""

def main():
    members_by_semester = defaultdict(list)

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            semester = row["semesterjoined"].strip()
            if semester:
                members_by_semester[semester].append(row)

    # Sort semesters: most recent first
    def semester_sort_key(s):
        parts = s.split()
        season, year = parts[0], int(parts[1])
        return (year, 0 if season == "Fall" else 1)

    sorted_semesters = dict(
        sorted(members_by_semester.items(), key=lambda x: semester_sort_key(x[0]), reverse=True)
    )

    html = build_html(sorted_semesters)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    total = sum(len(v) for v in sorted_semesters.values())
    print(f"✅ Generated {OUTPUT_FILE} with {total} members across {len(sorted_semesters)} semesters.")

if __name__ == "__main__":
    main()