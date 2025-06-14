import pyhtml

def get_page_html(form_data):
    # Get highest recorded temperature stations
    highest_temp_query = """
    SELECT ws.name, CAST(MAX(wd.maxtemp) AS FLOAT) as highest_temp
    FROM weather_data wd
    JOIN weather_station ws ON wd.location = ws.site_id
    WHERE wd.maxtemp IS NOT NULL 
    AND wd.maxtemp != 0
    AND wd.maxtemp != ''
    AND wd.maxtemp > 0
    AND trim(wd.maxtemp) != ''
    GROUP BY ws.name
    HAVING highest_temp IS NOT NULL
    AND highest_temp > 0
    ORDER BY highest_temp DESC
    LIMIT 5
    """
    highest_temp_results = pyhtml.get_results_from_query("s4106882/Database/climate_final.db", highest_temp_query)
    highest_temp_labels = [row[0] for row in highest_temp_results]
    highest_temp_values = [row[1] for row in highest_temp_results]

    # Get temperature comparison between 1970 and 2020
    temp_comparison_query = """
    WITH valid_temps AS (
        SELECT 
            substr(DMY, -4) as year,
            CAST(maxtemp AS FLOAT) as maxtemp,
            CAST(mintemp AS FLOAT) as mintemp
        FROM weather_data
        WHERE maxtemp IS NOT NULL 
        AND mintemp IS NOT NULL 
        AND maxtemp != 0 
        AND mintemp != 0
        AND length(DMY) >= 4
    )
    SELECT 
        (SELECT AVG(maxtemp) FROM valid_temps WHERE year = '1970') as avg_max_1970,
        (SELECT AVG(mintemp) FROM valid_temps WHERE year = '1970') as avg_min_1970,
        (SELECT AVG(maxtemp) FROM valid_temps WHERE year = '2020') as avg_max_2020,
        (SELECT AVG(mintemp) FROM valid_temps WHERE year = '2020') as avg_min_2020
    """
    temp_comparison = pyhtml.get_results_from_query("s4106882/Database/climate_final.db", temp_comparison_query)[0]

    # Get top 5 regions with most weather stations
    region_query = """
    SELECT ws.name, COUNT(DISTINCT ws.site_id) as station_count
    FROM weather_station ws
    JOIN weather_data wd ON ws.site_id = wd.location
    WHERE wd.maxtemp IS NOT NULL OR wd.mintemp IS NOT NULL
    GROUP BY ws.name
    ORDER BY station_count DESC
    LIMIT 5
    """
    region_results = pyhtml.get_results_from_query("s4106882/Database/climate_final.db", region_query)
    region_labels = [row[0] for row in region_results]
    region_counts = [row[1] for row in region_results]

    # Get top 5 states with most weather stations
    state_query = """
    SELECT s.name, COUNT(DISTINCT ws.site_id) as station_count
    FROM state s
    JOIN weather_station ws ON s.id = ws.state_id
    JOIN weather_data wd ON ws.site_id = wd.location
    WHERE wd.maxtemp IS NOT NULL OR wd.mintemp IS NOT NULL
    GROUP BY s.name
    ORDER BY station_count DESC
    LIMIT 5
    """
    state_results = pyhtml.get_results_from_query("s4106882/Database/climate_final.db", state_query)
    state_labels = [row[0] for row in state_results]
    state_counts = [row[1] for row in state_results]

    # Format temperature values with proper handling of NULL/None values
    def format_temp(temp):
        try:
            if temp is None or temp == 0 or temp == '':
                return "N/A"
            temp_float = float(temp)
            if temp_float <= 0:
                return "N/A"
            return f"{round(temp_float, 1)}&deg;C"
        except (ValueError, TypeError):
            return "N/A"

    page_html="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="/s4106882/css/style.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="/s4106882/js/page_one.js" defer></script>
        <title>Home Page</title>
        <style>
            .counter {
                font-size: 72px;
                font-weight: bold;
                color: #333;
                text-align: center;
                margin: 20px 0;
            }
            .counter-label {
                font-size: 24px;
                color: #666;
                text-align: center;
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
                <i class="glyphicon glyphicon-star"></i><a href="/page4">Page 4</a>
                <i class="glyphicon glyphicon-heart"></i><a href="/page5">Page 5</a>
                <i class="glyphicon glyphicon-cog"></i><a href="/page6">Page 6</a>
            </nav>
        </header>
        <main style="margin-top: -200px;">
            <section aria-label="Climate Facts">
                <div class="graph-container" data-graph-container>
                    <button class="graph-button prev" data-graph-button="prev"><i class="glyphicon glyphicon-chevron-left"></i></button>
                    <button class="graph-button next" data-graph-button="next"><i class="glyphicon glyphicon-chevron-right"></i></button>
                    <ul data-slides>
                        <li class="slide" data-active>
                            <p style="margin-top: -80px;">The """ + highest_temp_labels[0] + """ recorded the highest temperature of """ + format_temp(highest_temp_values[0]) + """ in our dataset.</p>
                            <div style="width: 25%; height: 200px; margin: 20px auto;">
                                <canvas id="highestTempChart"></canvas>
                            </div>
                        </li>
                        <li class="slide" data-next>
                            <p style="margin-top: -80px;">1970: Average High """ + format_temp(temp_comparison[0]) + """, Average Low """ + format_temp(temp_comparison[1]) + """<br>
                               2020: Average High """ + format_temp(temp_comparison[2]) + """, Average Low """ + format_temp(temp_comparison[3]) + """</p>
                            <div style="width: 25%; height: 200px; margin: 20px auto;">
                                <canvas id="tempComparisonChart"></canvas>
                            </div>
                        </li>
                        <li class="slide" data-prev>
                            <p style="margin-top: -80px;">""" + ("All regions have no more than one weather station." if all(count == 1 for count in region_counts) else region_labels[0] + " has the most weather stations with " + str(region_counts[0]) + " stations.") + """</p>
                            <div class="counter">""" + str(region_counts[0]) + """</div>
                            <div class="counter-label">Weather Stations</div>
                        </li>
                        <li class="slide">
                            <p style="margin-top: -80px;">""" + ("All states have no more than one weather station." if all(count == 1 for count in state_counts) else state_labels[0] + " has the most weather stations with " + str(state_counts[0]) + " stations.") + """</p>
                            <div style="width: 45%; height: 200px; margin: 20px auto;">
                                <canvas id="stateChart"></canvas>
                            </div>
                        </li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: -110px;">
                    <h2 style="margin-bottom: 10px;">About</h2>
                    <p style="max-width: 600px; margin: 0 auto; line-height: 1.4;">This website provides comprehensive insights into Australian climate data, focusing on key aspects of weather patterns and meteorological infrastructure. Our analysis covers temperature extremes, climate change analysis, weather station distribution, and regional climate patterns.</p>
                </div>
            </section>
        </main>
        <script>
            // Highest Temperature Chart
            new Chart(document.getElementById('highestTempChart'), {
                type: 'bar',
                data: {
                    labels: """ + str(highest_temp_labels) + """,
                    datasets: [{
                        data: """ + str(highest_temp_values) + """,
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderColor: 'rgb(255, 99, 132)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return Math.round(context.raw * 10) / 10;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: false
                            },
                            ticks: {
                                display: false
                            }
                        },
                        x: {
                            title: {
                                display: false
                            },
                            ticks: {
                                display: false
                            }
                        }
                    }
                }
            });

            // Temperature Comparison Chart
            new Chart(document.getElementById('tempComparisonChart'), {
                type: 'bar',
                data: {
                    labels: ['1970', '2020'],
                    datasets: [{
                        label: 'High',
                        data: [""" + str(temp_comparison[0]) + """, """ + str(temp_comparison[2]) + """],
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderColor: 'rgb(255, 99, 132)',
                        borderWidth: 1
                    }, {
                        label: 'Low',
                        data: [""" + str(temp_comparison[1]) + """, """ + str(temp_comparison[3]) + """],
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgb(54, 162, 235)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': ' + Math.round(context.raw * 10) / 10;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: false
                            },
                            ticks: {
                                display: false
                            }
                        },
                        x: {
                            title: {
                                display: false
                            },
                            ticks: {
                                display: false
                            }
                        }
                    }
                }
            });

            // Region Chart
            new Chart(document.getElementById('regionChart'), {
                type: 'pie',
                data: {
                    labels: """ + str(region_labels) + """,
                    datasets: [{
                        data: """ + str(region_counts) + """,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.5)',
                            'rgba(54, 162, 235, 0.5)',
                            'rgba(255, 206, 86, 0.5)',
                            'rgba(75, 192, 192, 0.5)',
                            'rgba(153, 102, 255, 0.5)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.label + ': ' + context.raw + ' stations';
                                }
                            }
                        }
                    }
                }
            });

            // State Chart
            new Chart(document.getElementById('stateChart'), {
                type: 'pie',
                data: {
                    labels: """ + str(state_labels) + """,
                    datasets: [{
                        data: """ + str(state_counts) + """,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.5)',
                            'rgba(54, 162, 235, 0.5)',
                            'rgba(255, 206, 86, 0.5)',
                            'rgba(75, 192, 192, 0.5)',
                            'rgba(153, 102, 255, 0.5)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.label + ': ' + context.raw + ' stations';
                                }
                            }
                        }
                    }
                }
            });
        </script>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </body>
    </html>
    """
    return page_html