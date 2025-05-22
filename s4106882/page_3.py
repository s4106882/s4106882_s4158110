def get_page_html(form_data):
    page_html="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="/s4106882/style.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <title>Page 3</title>
    </head>
    <body>
        <header>
            <img src="/s4106882/RMIT-emblem.png" class="logo">
            <nav>
                <i class="glyphicon glyphicon-home"></i><a href="/">Home</a>
                <i class="glyphicon glyphicon-map-marker"></i><a href="/page2">Page 2</a>
                <i class="glyphicon glyphicon-cloud"></i><a href="/page3">Page 3</a>
            </nav>
        </header>
    </body>
    """
    return page_html