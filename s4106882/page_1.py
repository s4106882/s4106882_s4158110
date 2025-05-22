def get_page_html(form_data):
    print("About to return the home page...")
    page_html="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="/New folder/style.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="/New folder/.js" defer></script>
        <title>Home Page</title>
    </head>
    <body>
        <header>
            <nav>
                <i class="glyphicon glyphicon-home"></i><a href="/">Home</a>
                <i class="glyphicon glyphicon-map-marker"></i><a href="/page2">Page 2</a>
                <i class="glyphicon glyphicon-cloud"></i><a href="/page3">Page 3</a>
            </nav>
        </header>
        <main>
            <section aria-label="Current Graphs">
                <div class="graph-container" data-graph-container>
                    <button class="graph-button prev" data-graph-button="prev"><i class="glyphicon glyphicon-chevron-left"></i></button>
                    <button class="graph-button next" data-graph-button="next"><i class="glyphicon glyphicon-chevron-right"></i></button>
                    <ul data-slides>
                        <li class="slide" data-active>
                            <img src="/New folder/a.png">
                            <p>This is a fact about the first graph</p>
                        </li>
                        <li class="slide" data-next>
                            <img src="/New folder/b.jpg">
                            <p>This is a fact about the second graph</p>
                        </li>
                        <li class="slide" data-prev>
                            <img src="/New folder/c.png">
                            <p>This is a fact about the third graph</p>
                        </li>
                    </ul>
                </div>
        </main>
    </body>
    </html>
    """
    return page_html