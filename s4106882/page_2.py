import pyhtml

def get_page_html(form_data):
    start_lat = form_data.get("start_lat", "")
    end_lat = form_data.get("end_lat", "")

    # Build the query based on selected parameters
    query = f"SELECT State, Lat FROM LOCA"
    conditions = []
    
    if start_lat and end_lat:
        conditions.append(f"Latitude BETWEEN {start_lat} AND {end_lat}")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Get the data from database
    results = pyhtml.get_results_from_query("s4106882/Database/BOM_Weather_Database.db", query)

    page_html="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="/s4106882/style.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <title>Weather Data Selection</title>
        <style>
            .table {
                background: white;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                margin-top: 20px;
            }
            .table th {
                background: var(--primary-color);
                color: white;
                padding: 15px;
            }
            .table td {
                padding: 12px;
                color: var(--secondary-color);
            }
            .form-control {
                border: 2px solid var(--hightlight-color-first);
                border-radius: 5px;
                padding: 8px;
                transition: border-color 0.3s ease;
            }
            .form-control:focus {
                border-color: var(--hightlight-color-second);
                outline: none;
                box-shadow: 0 0 5px var(--hightlight-color-second);
            }
            .filter-row {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                margin: 20px 0;
            }
            label {
                color: var(--primary-color);
                font-weight: bold;
                margin-bottom: 8px;
            }
            .container {
                padding-top: 5vh;
            }
        </style>
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
                    <label for="state">State</label>
                    <select name="state" id="states" class="form-control">
                        <option value="">All States</option>
                        <option value="NSW">NSW</option>
                        <option value="VIC">VIC</option>
                        <option value="QLD">QLD</option>
                        <option value="SA">SA</option>
                        <option value="WA">WA</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <!-- For Tags -->
                </div>
                <div class="col-md-3">
                    <form id="filterForm">
                        <div class="form-group">
                            <label>Latitude Range:</label>
                            <div class="row" style="margin-bottom: 15px;">
                                <div class="col-md-6">
                                    <input type="number" name="start_lat" id="start_lat" class="form-control" step="1" placeholder="Start Latitude" value=""" + start_lat + """ required>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <input type="number" name="end_lat" id="end_lat" class="form-control" step="1" placeholder="End Latitude" value=""" + end_lat + """ required>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div id="results" class="mt-4">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th class="sortable" data-sort="location">Location</th>
                            <th class="sortable" data-sort="latitude">Latitude</th>
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