import pyhtml

def get_page_html(form_data):
    # Get data from forms
    start_lat = form_data.get("start_lat", [""])[0]
    end_lat = form_data.get("end_lat", [""])[0]
    state = form_data.get("state", [""])[0]

    # Build query
    query = """
    SELECT s.name, ws.name, ws.latitude, ws.site_id
    FROM state s
    JOIN weather_station ws ON s.id = ws.state_id
    """
    conditions = []
    
    if state and state != "":
        conditions.append(f"s.name = '{state}'")
    
    # Handle latitude range with optional values
    if start_lat or end_lat:
        lat_condition = []
        if start_lat:
            lat_condition.append(f"ws.latitude >= {float(start_lat)}")
        if end_lat:
            lat_condition.append(f"ws.latitude <= {float(end_lat)}")
        if lat_condition:
            conditions.append(" AND ".join(lat_condition))
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Get data from database
    results = pyhtml.get_results_from_query("s4106882/Database/climate_test.db", query)

    page_html="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="/s4106882/css/style.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="/s4106882/js/page_two.js" defer></script>
        <title>Weather Data Selection</title>
    </head>
    <body>
        <header>
            <img src="/s4106882/images/RMIT-emblem.png" class="logo">
            <nav>
                <i class="glyphicon glyphicon-home"></i><a href="/">Home</a>
                <i class="glyphicon glyphicon-map-marker"></i><a href="/page2">Page 2</a>
                <i class="glyphicon glyphicon-cloud"></i><a href="/page3">Page 3</a>
            </nav>
        </header>
        <div class="container">
            <div class="row filter-row">
                <div class="col-md-3">
                    <form id="filterForm" method="GET" action="/page2">
                        <label for="state">State</label>
                        <select name="state" id="states" class="form-control">
                            <option value="">All States</option>
                            <option value="A.A.T." """ + ('selected' if state == 'A.A.T.' else '') + """>AAT</option>
                            <option value="A.E.T." """ + ('selected' if state == 'A.E.T.' else '') + """>AET</option>
                            <option value="N.S.W." """ + ('selected' if state == 'N.S.W.' else '') + """>NSW</option>
                            <option value="N.T." """ + ('selected' if state == 'N.T.' else '') + """>NT</option>
                            <option value="QLD" """ + ('selected' if state == 'QLD' else '') + """>QLD</option>
                            <option value="S.A." """ + ('selected' if state == 'S.A.' else '') + """>SA</option>
                            <option value="TAS" """ + ('selected' if state == 'TAS' else '') + """>TAS</option>
                            <option value="VIC" """ + ('selected' if state == 'VIC' else '') + """>VIC</option>
                            <option value="W.A." """ + ('selected' if state == 'W.A.' else '') + """>WA</option>
                        </select>
                </div>
                <div class="col-md-6">
                    <!-- For Tags -->
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label>Latitude Range:</label>
                        <div class="row" style="margin-bottom: 15px;">
                            <div class="col-md-6">
                                <input type="number" name="start_lat" id="start_lat" class="form-control" step="1" placeholder="Start Latitude" value=""" + start_lat + """>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <input type="number" name="end_lat" id="end_lat" class="form-control" step="1" placeholder="End Latitude" value=""" + end_lat + """>
                            </div>
                        </div>
                        <div class="row" style="margin-top: 15px;">
                            <div class="col-md-6">
                                <button type="submit" class="btn btn-primary">Filter</button>
                            </div>
                        </div>
                    </div>
                    </form>
                </div>
            </div>
            <div id="results" class="mt-4">
                <table id="data-table" class="table table-striped">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)" class="sortable" data-sort="state">State</th>
                            <th onclick="sortTable(1)" class="sortable" data-sort="name">Site Name</th>
                            <th onclick="sortTable(2)" class="sortable" data-sort="latitude">Latitude</th>
                            <th onclick="sortTable(3)" class="sortable" data-sort="site_id">Site ID</th>
                        </tr>
                    </thead>
                    <tbody id="data-table">
    """
    
    # Add data rows
    for row in results:
        page_html += "<tr>"
        for value in row:
            page_html += f"<td>{value}</td>"
        page_html += "</tr>"
    
    page_html += """
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    return page_html