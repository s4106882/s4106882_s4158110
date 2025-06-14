import pyhtml

def get_page_html(form_data):
    # Get data from forms
    start_lat = form_data.get("start_lat", [""])[0]
    end_lat = form_data.get("end_lat", [""])[0]
    start_long = form_data.get("start_long", [""])[0]
    end_long = form_data.get("end_long", [""])[0]
    state = form_data.get("state", [""])[0]
    site_name = form_data.get("site_name", [""])[0]
    current_page = int(form_data.get("page", ["1"])[0])
    entries_per_page = 20
    weather_tags = form_data.get("weather_tags", [])

    # Get unique site names for the dropdown, filtered by state if selected
    site_names_query = """
    SELECT DISTINCT ws.name 
    FROM weather_station ws 
    JOIN state s ON ws.state_id = s.id
    """
    if state and state != "":
        site_names_query += f" WHERE s.name = '{state}'"
    site_names_query += " ORDER BY ws.name"
    
    site_names = [row[0] for row in pyhtml.get_results_from_query("s4106882/Database/climate_final.db", site_names_query)]

    # Build query
    query = """
    SELECT s.name, ws.name, ws.latitude, ws.longitude, ws.site_id,
           wd.DMY, wd.precipitation, 
           CASE WHEN wd.evaporation = '' OR wd.evaporation IS NULL THEN NULL ELSE CAST(wd.evaporation AS FLOAT) END as evaporation,
           wd.maxtemp, wd.mintemp
    FROM state s
    JOIN weather_station ws ON s.id = ws.state_id
    JOIN weather_data wd ON ws.site_id = wd.location
    """
    conditions = []
    
    if state and state != "":
        conditions.append(f"s.name = '{state}'")
    
    if site_name and site_name != "":
        conditions.append(f"ws.name = '{site_name}'")
    
    if start_lat or end_lat:
        lat_condition = []
        if start_lat:
            lat_condition.append(f"ws.latitude >= {float(start_lat)}")
        if end_lat:
            lat_condition.append(f"ws.latitude <= {float(end_lat)}")
        if lat_condition:
            conditions.append(" AND ".join(lat_condition))

    if start_long or end_long:
        long_condition = []
        if start_long:
            long_condition.append(f"ws.longitude >= {float(start_long)}")
        if end_long:
            long_condition.append(f"ws.longitude <= {float(end_long)}")
        if long_condition:
            conditions.append(" AND ".join(long_condition))

    # Tag conditions
    if weather_tags:
        weather_conditions = []
        for tag in weather_tags:
            if tag == "high_temp":
                weather_conditions.append("wd.maxtemp > 30")
            elif tag == "low_temp":
                weather_conditions.append("wd.mintemp < 10")
            elif tag == "high_precip":
                weather_conditions.append("wd.precipitation > 10")
            elif tag == "high_evap":
                weather_conditions.append("CAST(wd.evaporation AS FLOAT) > 0")
        if weather_conditions:
            conditions.append("(" + " AND ".join(weather_conditions) + ")")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    count_query = f"SELECT COUNT(*) FROM ({query}) as count_table"
    total_entries = pyhtml.get_results_from_query("s4106882/Database/climate_final.db", count_query)[0][0]
    total_pages = (total_entries + entries_per_page - 1) // entries_per_page

    query += f" LIMIT {entries_per_page} OFFSET {(current_page - 1) * entries_per_page}"
    
    # Get data from database
    results = pyhtml.get_results_from_query("s4106882/Database/climate_final.db", query)

    # Get regional summary data
    summary_query = """
    SELECT 
        r.name as region,
        COUNT(DISTINCT ws.site_id) as num_stations,
        ROUND(AVG(wd.maxtemp), 1) as avg_max_temp
    FROM state s
    JOIN weather_station ws ON s.id = ws.state_id
    JOIN region r ON ws.region_id = r.id
    JOIN weather_data wd ON ws.site_id = wd.location
    """
    
    if conditions:
        summary_query += " WHERE " + " AND ".join(conditions)
    
    summary_query += " GROUP BY r.name ORDER BY r.name"
    summary_results = pyhtml.get_results_from_query("s4106882/Database/climate_final.db", summary_query)

    pag_html = generate_pagination_controls(current_page, total_pages, state, start_lat, end_lat, start_long, end_long, weather_tags, site_name)

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
                <i class="glyphicon glyphicon-star"></i><a href="/page4">Page 4</a>
                <i class="glyphicon glyphicon-heart"></i><a href="/page5">Page 5</a>
                <i class="glyphicon glyphicon-cog"></i><a href="/page6">Page 6</a>
            </nav>
        </header>
        <div class="container">
            <div class="row filter-row">
                <div class="col-md-3">
                    <form id="filterForm" method="GET" action="/page2">
                        <label for="state">State</label>
                        <select name="state" id="states" class="form-control" onchange="updateSiteNames(this.value)">
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
                        <label for="site_name" style="margin-top: 15px;">Site Name</label>
                        <select name="site_name" id="site_name" class="form-control">
                            <option value="">All Sites</option>
    """
    
    # Add site name options
    for name in site_names:
        page_html += f'<option value="{name}" ' + ('selected' if site_name == name else '') + f'>{name}</option>'
    
    page_html += """
                        </select>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Weather Conditions</label>
                        <div class="weather-tags">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="checkbox">
                                        <label>
                                            <input type="checkbox" name="weather_tags" value="high_temp" """ + ('checked' if 'high_temp' in weather_tags else '') + """> High Temperature (&gt;30&deg;C)
                                        </label>
                                    </div>
                                    <div class="checkbox">
                                        <label>
                                            <input type="checkbox" name="weather_tags" value="low_temp" """ + ('checked' if 'low_temp' in weather_tags else '') + """> Low Temperature (&lt;10&deg;C)
                                        </label>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="checkbox">
                                        <label>
                                            <input type="checkbox" name="weather_tags" value="high_precip" """ + ('checked' if 'high_precip' in weather_tags else '') + """> High Precipitation (>10mm)
                                        </label>
                                    </div>
                                    <div class="checkbox">
                                        <label>
                                            <input type="checkbox" name="weather_tags" value="high_evap" """ + ('checked' if 'high_evap' in weather_tags else '') + """> High Evaporation (>5mm)
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label>Location Range</label>
                        <div class="row" style="margin-bottom: 15px;">
                            <div class="col-md-6">
                                <input type="number" name="start_lat" id="start_lat" class="form-control" step="1" placeholder="Start Latitude" value=""" + start_lat + """>
                            </div>
                            <div class="col-md-6">
                                <input type="number" name="start_long" id="start_long" class="form-control" step="1" placeholder="Start Longitude" value=""" + start_long + """>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <input type="number" name="end_lat" id="end_lat" class="form-control" step="1" placeholder="End Latitude" value=""" + end_lat + """>
                            </div>
                            <div class="col-md-6">
                                <input type="number" name="end_long" id="end_long" class="form-control" step="1" placeholder="End Longitude" value=""" + end_long + """>
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
                <ul class="nav nav-tabs" id="dataTabs" role="tablist">
                    <li class="active" role="presentation">
                        <a href="#detailed" id="detailed-tab" role="tab" data-toggle="tab" aria-controls="detailed" aria-selected="true">Detailed Data</a>
                    </li>
                    <li role="presentation">
                        <a href="#summary" id="summary-tab" role="tab" data-toggle="tab" aria-controls="summary" aria-selected="false">Regional Summary</a>
                    </li>
                </ul>
                <div class="tab-content" id="dataTabsContent">
                    <div class="tab-pane fade in active" id="detailed" role="tabpanel" aria-labelledby="detailed-tab">
                        <table id="data-table" class="table table-striped">
                            <thead>
                                <tr>
                                    <th onclick="sortTable(0)" class="sortable" data-sort="state">State</th>
                                    <th onclick="sortTable(1)" class="sortable" data-sort="name">Site Name</th>
                                    <th onclick="sortTable(2)" class="sortable" data-sort="latitude">Latitude</th>
                                    <th onclick="sortTable(3)" class="sortable" data-sort="longitude">Longitude</th>
                                    <th onclick="sortTable(4)" class="sortable" data-sort="site_id">Site ID</th>
                                    <th onclick="sortTable(5)" class="sortable" data-sort="DMY">Date</th>
                                    <th onclick="sortTable(6)" class="sortable" data-sort="precipitation">Precipitation (mm)</th>
                                    <th onclick="sortTable(7)" class="sortable" data-sort="evaporation">Evaporation (mm)</th>
                                    <th onclick="sortTable(8)" class="sortable" data-sort="maxtemp">Max Temperature (&deg;C)</th>
                                    <th onclick="sortTable(9)" class="sortable" data-sort="mintemp">Min Temperature (&deg;C)</th>
                                </tr>
                            </thead>
                            <tbody>
    """
    
    # Add detailed data rows
    for row in results:
        page_html += "<tr>"
        for value in row:
            page_html += f"<td>{value}</td>"
        page_html += "</tr>"
    
    page_html += """
                            </tbody>
                        </table>
                        """ + pag_html + """
                    </div>
                    <div class="tab-pane fade" id="summary" role="tabpanel" aria-labelledby="summary-tab">
                        <table id="summary-table" class="table table-striped">
                            <thead>
                                <tr>
                                    <th onclick="sortTable(0)" class="sortable" data-sort="region">Region</th>
                                    <th onclick="sortTable(1)" class="sortable" data-sort="num_stations">Number of Weather Stations</th>
                                    <th onclick="sortTable(2)" class="sortable" data-sort="avg_max_temp">Average Max Temperature (&deg;C)</th>
                                </tr>
                            </thead>
                            <tbody>
    """
    
    # Add summary data rows
    for row in summary_results:
        page_html += "<tr>"
        for value in row:
            page_html += f"<td>{value}</td>"
        page_html += "</tr>"
    
    page_html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </body>
    </html>
    """
    
    return page_html

def generate_pagination_controls(current_page, total_pages, state, start_lat, end_lat, start_long, end_long, weather_tags, site_name):
    # Use current filters
    base_url = "/page2?"
    params = []
    if state:
        params.append(f"state={state}")
    if site_name:
        params.append(f"site_name={site_name}")
    if start_lat:
        params.append(f"start_lat={start_lat}")
    if end_lat:
        params.append(f"end_lat={end_lat}")
    if start_long:
        params.append(f"start_long={start_long}")
    if end_long:
        params.append(f"end_long={end_long}")
    for tag in weather_tags:
        params.append(f"weather_tags={tag}")
    base_url += "&".join(params)
    if params:
        base_url += "&"

    pag_html = '<div class="pagination-container"><ul class="pagination">'
    
    # Previous button
    if current_page > 1:
        pag_html += f'<li><a href="{base_url}page={current_page-1}">&laquo;</a></li>'
    else:
        pag_html += '<li class="disabled"><span>&laquo;</span></li>'

    # Page numbers
    max_visible_pages = 5
    start_page = max(1, current_page - max_visible_pages // 2)
    end_page = min(total_pages, start_page + max_visible_pages - 1)
    
    if start_page > 1:
        pag_html += f'<li><a href="{base_url}page=1">1</a></li>'
        if start_page > 2:
            pag_html += '<li class="disabled"><span>...</span></li>'

    for page in range(start_page, end_page + 1):
        if page == current_page:
            pag_html += f'<li class="active"><span>{page}</span></li>'
        else:
            pag_html += f'<li><a href="{base_url}page={page}">{page}</a></li>'

    if end_page < total_pages:
        if end_page < total_pages - 1:
            pag_html += '<li class="disabled"><span>...</span></li>'
        pag_html += f'<li><a href="{base_url}page={total_pages}">{total_pages}</a></li>'

    # Next button
    if current_page < total_pages:
        pag_html += f'<li><a href="{base_url}page={current_page+1}">&raquo;</a></li>'
    else:
        pag_html += '<li class="disabled"><span>&raquo;</span></li>'

    pag_html += f'''
    </ul>
    <div class="page-input">
        <form method="GET" action="/page2" style="display: inline;">
            <input type="hidden" name="state" value="{state}">
            <input type="hidden" name="site_name" value="{site_name}">
            <input type="hidden" name="start_lat" value="{start_lat}">
            <input type="hidden" name="end_lat" value="{end_lat}">
            <input type="hidden" name="start_long" value="{start_long}">
            <input type="hidden" name="end_long" value="{end_long}">
            <input type="number" name="page" min="1" max="{total_pages}" value="{current_page}" class="form-control" style="width: 60px; display: inline-block;">
            <button type="submit" class="btn btn-primary">Go</button>
        </form>
    </div>
    </div>'''

    return pag_html  

def get_site_names(form_data):
    state = form_data.get("state", [""])[0]
    
    # Get site names for the selected state
    site_names_query = """
    SELECT DISTINCT ws.name 
    FROM weather_station ws 
    JOIN state s ON ws.state_id = s.id
    """
    if state and state != "":
        site_names_query += f" WHERE s.name = '{state}'"
    site_names_query += " ORDER BY ws.name"
    
    site_names = [row[0] for row in pyhtml.get_results_from_query("s4106882/Database/climate_final.db", site_names_query)]
    
    return site_names  