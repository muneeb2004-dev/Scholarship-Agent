{% extends "base.html" %}

{% block content %}
<div class="row mb-5">
    <div class="col-lg-8 mx-auto text-center">
        <h1 class="display-4 mb-3 fw-bold text-gradient">
            <i class="fas fa-graduation-cap me-2"></i>AI Scholarship Finder
        </h1>
        <p class="lead text-muted">Discover international scholarship opportunities tailored to your profile</p>
    </div>
</div>

<div class="row">
    <div class="col-lg-3">
        <!-- Search Form -->
        <div class="card shadow-sm sticky-top">
            <div class="card-body">
                <h5 class="card-title mb-4">
                    <i class="fas fa-search me-2"></i>Your Profile
                </h5>
                
                <form id="searchForm">
                    <div class="mb-3">
                        <label class="form-label">Degree Level *</label>
                        <select class="form-select" id="degreeLevel" name="degree_level" required>
                            <option value="">Select degree...</option>
                            {% for degree in degrees %}
                            <option value="{{ degree }}">{{ degree }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Field of Study *</label>
                        <select class="form-select" id="fieldOfStudy" name="field_of_study" required>
                            <option value="">Select field...</option>
                            {% for field in fields %}
                            <option value="{{ field }}">{{ field }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Nationality *</label>
                        <select class="form-select" id="nationality" name="nationality" required>
                            <option value="">Select nationality...</option>
                            {% for nat in nationalities %}
                            <option value="{{ nat }}">{{ nat }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">CGPA / GPA</label>
                        <div class="d-flex align-items-center">
                            <input type="range" class="form-range" id="cgpa" name="cgpa" min="0" max="4" step="0.1" value="3.0">
                            <span class="ms-2 badge bg-primary" id="cgpaValue">3.0</span>
                        </div>
                        <small class="text-muted">0.0 - 4.0 scale</small>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Desired Country *</label>
                        <select class="form-select" id="country" name="country" required>
                            <option value="">Select country...</option>
                            {% for country in countries %}
                            <option value="{{ country }}">{{ country }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Work Experience (Years)</label>
                        <input type="number" class="form-control" id="workExperience" name="work_experience_years" min="0" max="50" value="0">
                    </div>

                    <button type="submit" class="btn btn-primary w-100 btn-lg" id="searchBtn">
                        <i class="fas fa-search me-2"></i>Search Scholarships
                    </button>
                </form>

                <hr class="my-4">

                <div class="alert alert-info small">
                    <strong>How it works:</strong>
                    <ol class="mb-0">
                        <li>Fill in your profile</li>
                        <li>Click "Search"</li>
                        <li>Get AI-matched scholarships</li>
                        <li>Export to Excel</li>
                    </ol>
                </div>
            </div>
        </div>
    </div>

    <div class="col-lg-9">
        <!-- Results Area -->
        <div id="welcomeSection">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <div class="card text-center h-100 shadow-sm">
                        <div class="card-body">
                            <i class="fas fa-globe fa-3x text-primary mb-3"></i>
                            <h5 class="card-title">Real-time Scraping</h5>
                            <p class="card-text">Data from official sources (DAAD, HEC, Fulbright, and more)</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card text-center h-100 shadow-sm">
                        <div class="card-body">
                            <i class="fas fa-brain fa-3x text-success mb-3"></i>
                            <h5 class="card-title">AI Matching</h5>
                            <p class="card-text">Smart algorithms to find your perfect scholarship match</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card text-center h-100 shadow-sm">
                        <div class="card-body">
                            <i class="fas fa-file-excel fa-3x text-danger mb-3"></i>
                            <h5 class="card-title">Easy Export</h5>
                            <p class="card-text">Download results to Excel for easy management</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="resultsSection" style="display: none;">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h3 id="resultsTitle">
                    <i class="fas fa-book me-2"></i>Found Scholarships
                </h3>
                <div>
                    <button class="btn btn-outline-secondary btn-sm me-2" id="filterBtn">
                        <i class="fas fa-filter me-1"></i>Filter
                    </button>
                    <button class="btn btn-success btn-sm" id="exportBtn">
                        <i class="fas fa-download me-1"></i>Export to Excel
                    </button>
                </div>
            </div>

            <div id="scholarshipsList"></div>
        </div>

        <!-- Loading Spinner -->
        <div id="loadingSpinner" style="display: none; text-align: center; padding: 40px;">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Searching scholarships...</p>
        </div>
    </div>
</div>

<!-- Filter Modal -->
<div class="modal fade" id="filterModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Filter Results</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="mb-3">
                    <label class="form-label">Minimum Funding Amount</label>
                    <input type="number" class="form-control" id="minFunding" placeholder="e.g., 10000" min="0">
                </div>
                <div class="mb-3">
                    <label class="form-label">Deadline Within (Days)</label>
                    <input type="number" class="form-control" id="maxDeadlineDays" placeholder="e.g., 90" min="0" max="365">
                </div>
                <div class="mb-3">
                    <label class="form-label">Keywords (comma-separated)</label>
                    <input type="text" class="form-control" id="keywords" placeholder="e.g., AI, ML, Research">
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" id="applyFilterBtn">Apply Filters</button>
            </div>
        </div>
    </div>
</div>

{% endblock %}

{% block extra_js %}
<script>
    let allScholarships = [];
    let currentSearchId = null;

    // CGPA slider update
    document.getElementById('cgpa').addEventListener('input', (e) => {
        document.getElementById('cgpaValue').textContent = e.target.value;
    });

    // Search form submission
    document.getElementById('searchForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const profile = {
            degree_level: document.getElementById('degreeLevel').value,
            field_of_study: document.getElementById('fieldOfStudy').value,
            nationality: document.getElementById('nationality').value,
            cgpa: parseFloat(document.getElementById('cgpa').value),
            country: document.getElementById('country').value,
            work_experience_years: parseInt(document.getElementById('workExperience').value) || 0
        };

        // Validate
        if (!profile.degree_level || !profile.field_of_study || !profile.nationality || !profile.country) {
            showError('Please fill in all required fields');
            return;
        }

        // Show loading
        document.getElementById('welcomeSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('loadingSpinner').style.display = 'block';
        document.getElementById('searchBtn').disabled = true;

        try {
            const response = await axios.post('/api/search', profile);

            if (response.data.success) {
                allScholarships = response.data.scholarships;
                currentSearchId = response.data.search_id;
                displayResults(allScholarships, response.data.count);
                showSuccess(`Found ${response.data.count} matching scholarships!`);
            } else {
                showError(response.data.message || 'Search failed');
            }
        } catch (error) {
            showError(error.response?.data?.message || 'Error performing search');
        } finally {
            document.getElementById('loadingSpinner').style.display = 'none';
            document.getElementById('searchBtn').disabled = false;
        }
    });

    // Consolidate duplicate scholarships with multiple platforms
    function consolidateScholarships(scholarships) {
        const consolidated = {};
        
        scholarships.forEach(sch => {
            // Normalize the title to group similar scholarships
            const baseTitle = normalizeScholarshipTitle(sch.title);
            
            if (!consolidated[baseTitle]) {
                consolidated[baseTitle] = {
                    ...sch,
                    title: sch.title, // Keep the best (first) title
                    platforms: [{
                        name: extractPlatform(sch.title, sch.url),
                        url: sch.url
                    }]
                };
                // Include alternate_urls from backend dedup
                if (sch.alternate_urls) {
                    sch.alternate_urls.forEach(altUrl => {
                        if (altUrl !== sch.url) {
                            consolidated[baseTitle].platforms.push({
                                name: extractPlatform('', altUrl),
                                url: altUrl
                            });
                        }
                    });
                }
            } else {
                // Add as alternate platform link
                const platform = extractPlatform(sch.title, sch.url);
                if (!consolidated[baseTitle].platforms.some(p => p.url === sch.url)) {
                    consolidated[baseTitle].platforms.push({
                        name: platform,
                        url: sch.url
                    });
                }
                // Keep the longer/more detailed title
                if (sch.title.length > consolidated[baseTitle].title.length) {
                    consolidated[baseTitle].title = sch.title;
                }
            }
        });
        
        return Object.values(consolidated);
    }
    
    function normalizeScholarshipTitle(title) {
        let t = title.toLowerCase().trim();
        // Remove platform suffixes like "on Facebook", "(on Instagram)", "- X"
        t = t.replace(/\s*\(on\s+\w+\)/i, '');
        t = t.replace(/\s+on\s+(facebook|instagram|twitter|linkedin|x|youtube)\s*$/i, '');
        t = t.replace(/\s*-\s*(facebook|instagram|twitter|linkedin|x|youtube)\s*$/i, '');
        // Remove parenthetical details for grouping
        t = t.replace(/\s*\([^)]*\)\s*/g, ' ');
        // Remove common noise words
        t = t.replace(/\b(scholarship|scholarships|program|programme|the|and|for|in|of)\b/g, ' ');
        // Normalize Erasmus variants
        t = t.replace(/erasmus\s*\+?\s*(mundus)?/gi, 'erasmus');
        // Collapse whitespace
        t = t.replace(/\s+/g, ' ').trim();
        // Take first 4 significant words for grouping
        const words = t.split(' ').filter(w => w.length > 1).slice(0, 4);
        return words.join(' ');
    }
    
    function extractPlatform(title, url) {
        if (url) {
            if (url.includes('facebook.com')) return 'Facebook';
            if (url.includes('instagram.com')) return 'Instagram';
            if (url.includes('twitter.com') || url.includes('x.com')) return 'X/Twitter';
            if (url.includes('linkedin.com')) return 'LinkedIn';
            if (url.includes('youtube.com')) return 'YouTube';
            if (url.includes('daad.de')) return 'DAAD Official';
            if (url.includes('hec.gov.pk')) return 'HEC Official';
            if (url.includes('chevening.org')) return 'Chevening Official';
            if (url.includes('fulbright')) return 'Fulbright Official';
            if (url.includes('erasmus') || url.includes('eacea.ec.europa.eu')) return 'Erasmus+ Official';
            if (url.includes('cscuk.fcdo.gov.uk')) return 'Commonwealth Official';
            if (url.includes('scholars4dev')) return 'Scholars4Dev';
            if (url.includes('opportunitiescorners')) return 'Opportunities Corners';
            if (url.includes('youthopportunities')) return 'Youth Opportunities';
            try {
                const domain = new URL(url).hostname.replace('www.', '');
                return domain.split('.')[0].charAt(0).toUpperCase() + domain.split('.')[0].slice(1);
            } catch(e) {}
        }
        return 'Official Website';
    }

    // Display results
    function displayResults(scholarships, count) {
        const consolidated = consolidateScholarships(scholarships);
        document.getElementById('resultsTitle').textContent = `Found ${consolidated.length} Scholarships (${count} sources)`;
        
        const listHtml = consolidated.map((sch, idx) => `
            <div class="card mb-3 scholarship-card shadow-sm">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title mb-0">${idx + 1}. ${sch.title}</h5>
                        <span class="badge bg-primary">Match: ${Math.round(sch.match_score || 0)}%</span>
                    </div>
                    <div class="row text-small mt-3">
                        <div class="col-md-6">
                            <p class="mb-1"><strong>Country:</strong> ${sch.country || 'N/A'}</p>
                            <p class="mb-1"><strong>Degree:</strong> ${sch.degree || 'N/A'}</p>
                            <p class="mb-1"><strong>Field:</strong> ${sch.field || 'N/A'}</p>
                        </div>
                        <div class="col-md-6">
                            <p class="mb-1"><strong>Funding:</strong> ${sch.funding || 'N/A'}</p>
                            <p class="mb-1"><strong>Deadline:</strong> ${sch.deadline || 'N/A'}</p>
                            <p class="mb-1"><strong>Duration:</strong> ${sch.duration || 'N/A'}</p>
                        </div>
                    </div>
                    <div class="mt-3">
                        ${sch.platforms.length > 1 ? `
                            <span class="text-muted small d-block mb-2">Available on:</span>
                            <div class="btn-group" role="group">
                                ${sch.platforms.map(p => `
                                    <a href="${p.url}" target="_blank" class="btn btn-sm btn-outline-primary">
                                        <i class="fas fa-link me-1"></i>${p.name}
                                    </a>
                                `).join('')}
                            </div>
                        ` : `
                            <a href="${sch.platforms[0]?.url || '#'}" target="_blank" class="btn btn-sm btn-outline-primary">
                                <i class="fas fa-link me-1"></i>View Details
                            </a>
                        `}
                    </div>
                </div>
            </div>
        `).join('');

        document.getElementById('scholarshipsList').innerHTML = listHtml;
        document.getElementById('resultsSection').style.display = 'block';
    }

    // Export to Excel
    document.getElementById('exportBtn').addEventListener('click', async () => {
        if (allScholarships.length === 0) {
            showError('No scholarships to export');
            return;
        }

        try {
            const response = await axios.post('/api/export', {
                scholarships: allScholarships,
                filename: 'my_scholarships'
            }, {
                responseType: 'blob'
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'scholarships.xlsx');
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
            window.URL.revokeObjectURL(url);
            
            showSuccess('Excel file downloaded successfully!');
        } catch (error) {
            showError('Error exporting to Excel');
        }
    });

    // Filter button
    document.getElementById('filterBtn').addEventListener('click', () => {
        new bootstrap.Modal(document.getElementById('filterModal')).show();
    });

    // Apply filters
    document.getElementById('applyFilterBtn').addEventListener('click', async () => {
        const filters = {
            min_funding: parseInt(document.getElementById('minFunding').value) || null,
            max_deadline_days: parseInt(document.getElementById('maxDeadlineDays').value) || null,
            keywords: document.getElementById('keywords').value.split(',').map(k => k.trim()).filter(k => k)
        };

        try {
            const response = await axios.post('/api/filter', {
                scholarships: allScholarships,
                filters: filters
            });

            if (response.data.success) {
                allScholarships = response.data.scholarships;
                displayResults(allScholarships, response.data.count);
                bootstrap.Modal.getInstance(document.getElementById('filterModal')).hide();
                showSuccess(`Filtered to ${response.data.count} scholarships`);
            }
        } catch (error) {
            showError('Error applying filters');
        }
    });
</script>
{% endblock %}
