<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}AI Scholarship Finder{% endblock %}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-gradient">
        <div class="container-lg">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-graduation-cap me-2"></i>Scholarship Finder AI
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/dashboard">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/api/health">API Status</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" onclick="openApiDocs()">API Docs</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show m-3" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <!-- Main Content -->
    <main class="py-4">
        <div class="container-lg">
            {% block content %}{% endblock %}
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white mt-5 py-4">
        <div class="container-lg">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <h5>About</h5>
                    <p>AI-powered scholarship finder to help you discover international opportunities.</p>
                </div>
                <div class="col-md-4 mb-3">
                    <h5>Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="/" class="text-decoration-none text-light">Home</a></li>
                        <li><a href="/dashboard" class="text-decoration-none text-light">Dashboard</a></li>
                        <li><a href="#" class="text-decoration-none text-light">API Documentation</a></li>
                    </ul>
                </div>
                <div class="col-md-4 mb-3">
                    <h5>Support</h5>
                    <p><i class="fas fa-envelope"></i> <a href="mailto:support@scholarshipfinder.ai" class="text-decoration-none text-light">support@scholarshipfinder.ai</a></p>
                </div>
            </div>
            <hr class="bg-secondary">
            <div class="text-center">
                <p class="mb-0">&copy; 2024 AI Scholarship Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/1.4.0/axios.min.js"></script>
    <script>
        function openApiDocs() {
            // Open Swagger/OpenAPI documentation
            window.open('/api/docs', '_blank');
        }

        // Global error handler
        function showError(message) {
            const alert = document.createElement('div');
            alert.className = 'alert alert-danger alert-dismissible fade show m-3';
            alert.setAttribute('role', 'alert');
            alert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.body.insertBefore(alert, document.querySelector('main'));
        }

        // Global success handler
        function showSuccess(message) {
            const alert = document.createElement('div');
            alert.className = 'alert alert-success alert-dismissible fade show m-3';
            alert.setAttribute('role', 'alert');
            alert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.body.insertBefore(alert, document.querySelector('main'));
        }
    </script>
    {% block extra_js %}{% endblock %}
</body>
</html>
