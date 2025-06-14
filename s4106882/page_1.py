def get_page_html(form_data):
    page_html="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="/s4106882/css/style.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="/s4106882/js/page_one.js" defer></script>
        <title>Home Page</title>
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
            <section aria-label="Current Graphs">
                <div class="graph-container" data-graph-container>
                    <button class="graph-button prev" data-graph-button="prev"><i class="glyphicon glyphicon-chevron-left"></i></button>
                    <button class="graph-button next" data-graph-button="next"><i class="glyphicon glyphicon-chevron-right"></i></button>
                    <ul data-slides>
                        <li class="slide" data-active>
                            <img src="/s4106882/images/a.png">
                            <p>This is a fact realting to the first graph</p>
                        </li>
                        <li class="slide" data-next>
                            <img src="/s4106882/images/b.jpg">
                            <p>This is a fact relating to the second graph</p>
                        </li>
                        <li class="slide" data-prev>
                            <img src="/s4106882/images/c.png">
                            <p>This is a fact relating to the third graph</p>
                        </li>
                    </ul>
                </div>
        </main>
    </body>
    </html>
    """
    return page_html