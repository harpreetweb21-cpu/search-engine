// Configuration - Use relative URL for deployment
const API_BASE_URL = '/api';
let currentPage = 1;
let currentQuery = '';
let totalResults = 0;
const resultsPerPage = 10;

// DOM Elements
const searchInput = document.getElementById('searchInput');
const headerSearchInput = document.getElementById('headerSearchInput');
const clearBtn = document.getElementById('clearBtn');
const mainSearch = document.getElementById('mainSearch');
const header = document.getElementById('header');
const resultsPage = document.getElementById('resultsPage');
const resultsList = document.getElementById('resultsList');
const resultsStats = document.getElementById('resultsStats');
const loading = document.getElementById('loading');
const pagination = document.getElementById('pagination');

// Event Listeners
searchInput.addEventListener('input', handleInputChange);
searchInput.addEventListener('keypress', handleKeyPress);
headerSearchInput.addEventListener('input', handleHeaderInputChange);
headerSearchInput.addEventListener('keypress', handleKeyPress);

function handleInputChange(e) {
    clearBtn.classList.toggle('visible', e.target.value.length > 0);
}

function handleHeaderInputChange(e) {
    // Sync with main input
    searchInput.value = e.target.value;
}

function handleKeyPress(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
}

function clearSearch() {
    searchInput.value = '';
    headerSearchInput.value = '';
    clearBtn.classList.remove('visible');
    searchInput.focus();
}

function goHome() {
    // Reset to main search page
    mainSearch.classList.remove('hidden');
    header.classList.remove('visible');
    resultsPage.classList.remove('visible');
    searchInput.value = '';
    headerSearchInput.value = '';
    currentQuery = '';
    currentPage = 1;
}

async function performSearch(page = 1) {
    const query = searchInput.value.trim() || headerSearchInput.value.trim();
    
    if (!query) {
        alert('Please enter a search term');
        return;
    }

    currentQuery = query;
    currentPage = page;

    // Show loading
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                page: page,
                limit: resultsPerPage
            })
        });

        if (!response.ok) {
            throw new Error('Search failed');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Search error:', error);
        displayError('An error occurred while searching. Please try again.');
    } finally {
        showLoading(false);
    }
}

function displayResults(data) {
    // Hide main search, show header and results
    mainSearch.classList.add('hidden');
    header.classList.add('visible');
    resultsPage.classList.add('visible');

    // Update header search input
    headerSearchInput.value = currentQuery;

    totalResults = data.total || 0;
    const results = data.results || [];
    const searchTime = data.search_time || 0;

    // Display stats
    resultsStats.innerHTML = `About ${totalResults.toLocaleString()} results (${searchTime.toFixed(2)} seconds)`;

    // Display results
    if (results.length === 0) {
        resultsList.innerHTML = `
            <div class="no-results">
                <h2>No results found for "${escapeHtml(currentQuery)}"</h2>
                <p>Try different keywords or check your spelling</p>
            </div>
        `;
        pagination.innerHTML = '';
        return;
    }

    resultsList.innerHTML = results.map(result => `
        <div class="result-item">
            <div class="result-url">
                <cite>${escapeHtml(result.url || result.source || 'Document')}</cite>
            </div>
            <a href="${escapeHtml(result.url || '#')}" class="result-title" target="_blank">
                ${highlightQuery(escapeHtml(result.title), currentQuery)}
            </a>
            <div class="result-snippet">
                ${highlightQuery(escapeHtml(result.snippet || result.content || ''), currentQuery)}
            </div>
        </div>
    `).join('');

    // Display pagination
    displayPagination();
}

function displayPagination() {
    const totalPages = Math.ceil(totalResults / resultsPerPage);
    
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let paginationHtml = '';

    // Previous button
    if (currentPage > 1) {
        paginationHtml += `<button class="page-btn" onclick="performSearch(${currentPage - 1})">← Previous</button>`;
    }

    // Page numbers
    const startPage = Math.max(1, currentPage - 4);
    const endPage = Math.min(totalPages, currentPage + 4);

    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === currentPage ? 'active' : '';
        paginationHtml += `<button class="page-btn ${activeClass}" onclick="performSearch(${i})">${i}</button>`;
    }

    // Next button
    if (currentPage < totalPages) {
        paginationHtml += `<button class="page-btn" onclick="performSearch(${currentPage + 1})">Next →</button>`;
    }

    pagination.innerHTML = paginationHtml;
}

function displayError(message) {
    mainSearch.classList.add('hidden');
    header.classList.add('visible');
    resultsPage.classList.add('visible');
    headerSearchInput.value = currentQuery;

    resultsList.innerHTML = `
        <div class="no-results">
            <h2>Error</h2>
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    pagination.innerHTML = '';
    resultsStats.innerHTML = '';
}

function showLoading(show) {
    loading.classList.toggle('visible', show);
}

function feelingLucky() {
    const query = searchInput.value.trim();
    if (!query) {
        alert('Please enter a search term');
        return;
    }
    
    // Perform search and redirect to first result
    performSearch(1);
}

// Utility functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function highlightQuery(text, query) {
    if (!query || !text) return text;
    
    const words = query.split(/\s+/).filter(word => word.length > 0);
    let result = text;
    
    words.forEach(word => {
        const regex = new RegExp(`(${escapeRegex(word)})`, 'gi');
        result = result.replace(regex, '<em>$1</em>');
    });
    
    return result;
}

function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    searchInput.focus();
});
