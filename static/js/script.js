/* ============================================================================
   DISEASE PROGRESSION PREDICTION - JAVASCRIPT UTILITIES
   ============================================================================ */

// API Base URL
const API_BASE = '/api';

/**
 * Make a GET request to the API
 */
function apiGet(endpoint) {
    return fetch(`${API_BASE}${endpoint}`)
        .then(response => response.json());
}

/**
 * Make a POST request to the API
 */
function apiPost(endpoint, data) {
    return fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json());
}

/**
 * Format a number as percentage
 */
function formatPercent(value, decimals = 1) {
    return (value * 100).toFixed(decimals) + '%';
}

/**
 * Format bytes to human-readable size
 */
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Format date to readable string
 */
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toLocaleString();
}

/**
 * Show a toast notification
 */
function showToast(message, type = 'info', duration = 3000) {
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast toast-${type}">
            <i class="fas fa-${getToastIcon(type)}"></i> ${message}
            <button class="toast-close" onclick="$('#${toastId}').fadeOut(200, function() { $(this).remove(); });">&times;</button>
        </div>
    `;
    
    if ($('#toast-container').length === 0) {
        $('body').append('<div id="toast-container"></div>');
    }
    
    $('#toast-container').append(toastHtml);
    
    setTimeout(() => {
        $(`#${toastId}`).fadeOut(200, function() { $(this).remove(); });
    }, duration);
}

/**
 * Get icon class for toast type
 */
function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'times-circle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Debounce function for API calls
 */
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

/**
 * Create a chart with Chart.js
 */
function createChart(canvasId, type, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            ...options
        }
    });
}

/**
 * Download file from server
 */
function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Load and display training logs in real-time
 */
function streamLogs(endpoint, containerSelector, interval = 1000) {
    const logStream = setInterval(() => {
        apiGet(endpoint)
            .then(data => {
                let html = '';
                if (data.logs && data.logs.length > 0) {
                    data.logs.forEach(log => {
                        html += `<p>${escapeHtml(log)}</p>`;
                    });
                } else {
                    html = '<p>No logs yet...</p>';
                }
                $(containerSelector).html(html);
                $(containerSelector).scrollTop($(containerSelector)[0].scrollHeight);
            })
            .catch(error => console.error('Error loading logs:', error));
    }, interval);
    
    return logStream;
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Chart.js plugin for gradient backgrounds
 */
const gradientBgPlugin = {
    id: 'gradientBg',
    beforeDraw(chart) {
        if (!chart.options.gradientBg) return;
        
        const { ctx, chartArea: { left, top, width, height } } = chart;
        const gradient = ctx.createLinearGradient(0, top, 0, top + height);
        gradient.addColorStop(0, 'rgba(0, 123, 255, 0.3)');
        gradient.addColorStop(1, 'rgba(0, 123, 255, 0)');
        
        chart.data.datasets.forEach(dataset => {
            dataset.backgroundColor = gradient;
        });
    }
};

// Register plugin
if (typeof Chart !== 'undefined' && Chart.register) {
    Chart.register(gradientBgPlugin);
}

/**
 * Initialize tooltips and popovers
 */
$(document).ready(function() {
    // Add toast container styles
    if ($('#toast-styles').length === 0) {
        $('head').append(`
            <style id="toast-styles">
                #toast-container {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 9999;
                    max-width: 400px;
                }
                
                .toast {
                    background: white;
                    border-radius: 8px;
                    padding: 15px 20px;
                    margin-bottom: 10px;
                    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    animation: slideIn 0.3s ease;
                    border-left: 4px solid #007bff;
                }
                
                .toast-success {
                    border-left-color: #28a745;
                }
                
                .toast-success i {
                    color: #28a745;
                }
                
                .toast-error {
                    border-left-color: #dc3545;
                }
                
                .toast-error i {
                    color: #dc3545;
                }
                
                .toast-warning {
                    border-left-color: #ffc107;
                }
                
                .toast-warning i {
                    color: #ffc107;
                }
                
                .toast i {
                    font-size: 1.2rem;
                }
                
                .toast-close {
                    background: none;
                    border: none;
                    color: #999;
                    cursor: pointer;
                    font-size: 1.3rem;
                    margin-left: auto;
                    padding: 0;
                }
                
                .toast-close:hover {
                    color: #333;
                }
                
                @keyframes slideIn {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                
                @media (max-width: 600px) {
                    #toast-container {
                        left: 10px;
                        right: 10px;
                        max-width: none;
                    }
                }
            </style>
        `);
    }
});

export {
    apiGet,
    apiPost, createChart, debounce, downloadFile, escapeHtml, formatBytes,
    formatDate, formatPercent, showToast, streamLogs
};

