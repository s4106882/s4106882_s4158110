import sqlite3

def get_page_html(form_data):
    # Connect to your database
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
            .persona-header {{
                text-align: center;
                margin-top: 32px;
                margin-bottom: 16px;
                font-size: 2.2em;
                font-weight: bold;
                letter-spacing: 1px;
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
            }}
            .persona-section {{
                background: #eef2fa;
                border-radius: 6px;
                padding: 8px 12px;
                margin: 8px 0;
                text-align: left;
            }}
            .persona-section b {{
                color: #2a4d7a;
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
            <h1>Mission Statement</h1>
            <p>{mission}</p>
            <h2>How to Use</h2>
            <p>{usage}</p>
            <div class="persona-header">Personas</div>
            <div class="persona-container">
    """.format(mission=mission, usage=usage)
    for p in personas:
        img_html = f'<img src="{p[5]}" alt="{p[0]}">' if p[5] else ""
        page_html += f"""
        <div class="persona-card">
            {img_html}
            <h2>{p[0]}</h2>
            <div class="persona-section"><b>Background:</b> {p[1]}</div>
            <div class="persona-section"><b>Needs:</b> {p[2]}</div>
            <div class="persona-section"><b>Goals:</b> {p[3]}</div>
            <div class="persona-section"><b>Skills:</b> {p[4]}</div>
        </div>
        """
    page_html += """
            </div>
            <h2>Team Members</h2>
            <ul>
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