{% extends "base.html" %}

{% block content %}
<div class="row mb-4">
    <div class="col-lg-12">
        <h2 class="mb-4">
            <i class="fas fa-chart-bar me-2"></i>Dashboard & Statistics
        </h2>
    </div>
</div>

<!-- Key Metrics -->
<div class="row mb-4">
    <div class="col-md-3 mb-3">
        <div class="card text-center shadow-sm">
            <div class="card-body">
                <i class="fas fa-search fa-2x text-primary mb-3"></i>
                <h3 class="card-title">{{ stats.total_searches }}</h3>
                <p class="card-text text-muted">Total Searches</p>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card text-center shadow-sm">
            <div class="card-body">
                <i class="fas fa-graduation-cap fa-2x text-success mb-3"></i>
                <h3 class="card-title">{{ stats.total_scholarships_found }}</h3>
                <p class="card-text text-muted">Scholarships Found</p>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card text-center shadow-sm">
            <div class="card-body">
                <i class="fas fa-chart-line fa-2x text-warning mb-3"></i>
                <h3 class="card-title">{{ stats.average_per_search }}</h3>
                <p class="card-text text-muted">Average Per Search</p>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card text-center shadow-sm">
            <div class="card-body">
                <i class="fas fa-clock fa-2x text-info mb-3"></i>
                <h3 class="card-title">{{ stats.last_search or 'N/A' }}</h3>
                <p class="card-text text-muted">Last Search</p>
            </div>
        </div>
    </div>
</div>

<!-- Charts Row -->
<div class="row mb-4">
    <div class="col-lg-6 mb-3">
        <div class="card shadow-sm">
            <div class="card-header">
                <h5 class="mb-0">Top Countries Searched</h5>
            </div>
            <div class="card-body">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Country</th>
                            <th>Searches</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in stats.top_countries %}
                        <tr>
                            <td>{{ item.country }}</td>
                            <td><span class="badge bg-primary">{{ item.count }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="col-lg-6 mb-3">
        <div class="card shadow-sm">
            <div class="card-header">
                <h5 class="mb-0">Top Fields Searched</h5>
            </div>
            <div class="card-body">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Field</th>
                            <th>Searches</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in stats.top_fields %}
                        <tr>
                            <td>{{ item.field }}</td>
                            <td><span class="badge bg-success">{{ item.count }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<!-- API Information -->
<div class="row">
    <div class="col-lg-12">
        <div class="card shadow-sm">
            <div class="card-header">
                <h5 class="mb-0">API Endpoints</h5>
            </div>
            <div class="card-body">
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>Endpoint</th>
                            <th>Method</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>/api/search</code></td>
                            <td><span class="badge bg-success">POST</span></td>
                            <td>Search scholarships by profile</td>
                        </tr>
                        <tr>
                            <td><code>/api/filter</code></td>
                            <td><span class="badge bg-success">POST</span></td>
                            <td>Filter scholarships by criteria</td>
                        </tr>
                        <tr>
                            <td><code>/api/export</code></td>
                            <td><span class="badge bg-success">POST</span></td>
                            <td>Export scholarships to Excel</td>
                        </tr>
                        <tr>
                            <td><code>/api/recommendations</code></td>
                            <td><span class="badge bg-success">POST</span></td>
                            <td>Get AI recommendations</td>
                        </tr>
                        <tr>
                            <td><code>/api/countries</code></td>
                            <td><span class="badge bg-info">GET</span></td>
                            <td>List available countries</td>
                        </tr>
                        <tr>
                            <td><code>/api/history</code></td>
                            <td><span class="badge bg-info">GET</span></td>
                            <td>Get search history</td>
                        </tr>
                        <tr>
                            <td><code>/api/stats</code></td>
                            <td><span class="badge bg-info">GET</span></td>
                            <td>Get statistics</td>
                        </tr>
                        <tr>
                            <td><code>/api/health</code></td>
                            <td><span class="badge bg-info">GET</span></td>
                            <td>Health check</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

{% endblock %}
