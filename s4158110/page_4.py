import sqlite3
import re

def get_page_html(form_data):
    # Connect to database
    conn = sqlite3.connect('s4158110/database/personas.db')
    c = conn.cursor()

    # Fetch personas
    c.execute("SELECT name, background, needs, goals, skills, image_url FROM personas")
    personas = c.fetchall()

    # Fetch team members
    c.execute("SELECT name, student_number FROM team")
    team = c.fetchall()

    conn.close()

    # Static content
    mission = "Our website addresses the social challenge by..."
    usage = "You can use our site to..."

    # Build HTML
    page_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="/s4106882/css/style.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <title>Mission Statement</title>
        <style>
            /* Hide scrollbar for all browsers */
            html, body {{
                -ms-overflow-style: none;  /* IE and Edge */
                scrollbar-width: none;     /* Firefox */
            }}
            html::-webkit-scrollbar, body::-webkit-scrollbar {{
                display: none;             /* Chrome, Safari, Opera */
            }}
            .persona-header {{
                text-align: center;
                margin-top: 32px;
                margin-bottom: 16px;
                font-size: 2.2em;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            .section-card {{
                background: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                width: 60%;
                margin: 24px auto 0 auto;
                padding: 24px 32px;
                text-align: center;
            }}
            .section-card h1, .section-card h2 {{
                margin-top: 0;
                margin-bottom: 12px;
                font-size: 2em;
                font-weight: bold;
                color: #2a4d7a;
            }}
            .section-card p {{
                font-size: 1.1em;
                margin-bottom: 0;
            }}
            .persona-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 24px;
                justify-content: center;
                align-items: center;
            }}
            .persona-card {{
                background: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                width: 320px;
                padding: 16px;
                text-align: center;
            }}
            .persona-card img {{
                border-radius: 50%;
                width: 120px;
                height: 120px;
                object-fit: cover;
                margin-bottom: 12px;
            }}
            .persona-card h2 {{
                margin: 8px 0 4px 0;
                text-align: center;
            }}
            .persona-section {{
                background: #eef2fa;
                border-radius: 6px;
                padding: 8px 12px;
                margin: 8px 0;
                text-align: center;
            }}
            .persona-section-label {{
                font-weight: bold;
                color: #2a4d7a;
                font-size: 1.1em;
                margin-bottom: 2px;
                display: block;
            }}
            .persona-section-content {{
                font-size: 1em;
                color: #222;
                margin-bottom: 0;
            }}
            .needs-list {{
                margin: 0 0 0 18px;
                padding: 0;
                text-align: left;
                display: inline-block;
            }}
            .team-list {{
                text-align: center;
                list-style-position: inside;
                margin-left: 0;
                padding-left: 0;
            }}
            .team-list li {{
                display: inline-block;
                margin: 0 10px;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="/s4106882/images/RMIT-emblem.png" class="logo">
            <nav>
                <i class="glyphicon glyphicon-home"></i><a href="/">Home</a>
                <i class="glyphicon glyphicon-map-marker"></i><a href="/page2">Page 2</a>
                <i class="glyphicon glyphicon-cloud"></i><a href="/page3">Page 3</a>
                <i class="glyphicon glyphicon-star"></i><a href="/page4">Page 4</a>
                <i class="glyphicon glyphicon-heart"></i><a href="/page5">Page 5</a>
                <i class="glyphicon glyphicon-cog"></i><a href="/page6">Page 6</a>
            </nav>
        </header>
        <main>
            <div class="section-card">
                <h1>Purpose</h1>
                <p>{mission}</p>
            </div>
            <div class="section-card">
                <h2>How to Use</h2>
                <p>{usage}</p>
            </div>
            <div class="persona-header">Personas</div>
            <div class="persona-container">
    """.format(mission=mission, usage=usage)
    for p in personas:
        img_html = f'<img src="{p[5]}" alt="{p[0]}">' if p[5] else ""
        # Split needs into a list by numbers or newlines
        needs_items = re.split(r'\d+\. ?', p[2])
        needs_items = [item.strip() for item in needs_items if item.strip()]
        needs_html = '<ul class="needs-list">' + ''.join(f'<li>{item}</li>' for item in needs_items) + '</ul>'
        page_html += f"""
        <div class="persona-card">
            {img_html}
            <h2>{p[0]}</h2>
            <div class="persona-section">
                <span class="persona-section-label">Background</span>
                <span class="persona-section-content">{p[1]}</span>
            </div>
            <div class="persona-section">
                <span class="persona-section-label">Needs</span>
                {needs_html}
            </div>
            <div class="persona-section">
                <span class="persona-section-label">Goals</span>
                <span class="persona-section-content">{p[3]}</span>
            </div>
            <div class="persona-section">
                <span class="persona-section-label">Skills</span>
                <span class="persona-section-content">{p[4]}</span>
            </div>
        </div>
        """
    page_html += """
            </div>
            <h2 style='text-align:center'>Team Members</h2>
            <ul class="team-list">
    """
    for name, num in team:
        page_html += f"<li>{name} ({num})</li>"
    page_html += """
            </ul>
        </main>
    </body>
    </html>
    """
    return page_html