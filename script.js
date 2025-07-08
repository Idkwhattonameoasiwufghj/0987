// Garden Trade Hub - JavaScript functionality

// Sample data for demonstration
let trades = [
    {
        id: 1,
        title: "Tomato Seedlings for Herbs",
        category: "Plants",
        offering: "6 healthy tomato seedlings (Roma and Cherry varieties)",
        seeking: "Herb cuttings (basil, oregano, thyme)",
        description: "I have extra tomato seedlings that need good homes. Looking for herb cuttings to start my herb garden.",
        location: "Portland, OR",
        contact_name: "Sarah Johnson",
        contact_email: "sarah.j@email.com",
        contact_phone: "(503) 555-0123",
        created_at: "2025-07-08"
    },
    {
        id: 2,
        title: "Garden Tools Exchange",
        category: "Tools",
        offering: "Rake and small shovel, lightly used",
        seeking: "Pruning shears or watering can",
        description: "Downsizing my tool collection. These are in great condition and ready for a new garden.",
        location: "Seattle, WA",
        contact_name: "Mike Chen",
        contact_email: "mike.chen@email.com",
        contact_phone: "(206) 555-0456",
        created_at: "2025-07-07"
    },
    {
        id: 3,
        title: "Organic Seeds Collection",
        category: "Seeds",
        offering: "Variety pack of organic vegetable seeds",
        seeking: "Flower seeds or bulbs",
        description: "I have extra packets of organic carrot, lettuce, and radish seeds. Looking for flower seeds to beautify my garden.",
        location: "San Francisco, CA",
        contact_name: "Emily Rodriguez",
        contact_email: "emily.r@email.com",
        contact_phone: "",
        created_at: "2025-07-06"
    }
];

// Initialize the application
function initializeApp() {
    setupSearchAndFilter();
    setupFormHandling();
    renderTrades();
    setupSmoothScrolling();
}

// Setup search and filter functionality
function setupSearchAndFilter() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterTrades, 300));
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterTrades);
    }
}

// Filter trades based on search and category
function filterTrades() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const selectedCategory = document.getElementById('categoryFilter').value;
    
    const filteredTrades = trades.filter(trade => {
        const matchesSearch = !searchTerm || 
            trade.title.toLowerCase().includes(searchTerm) ||
            trade.offering.toLowerCase().includes(searchTerm) ||
            trade.seeking.toLowerCase().includes(searchTerm) ||
            trade.description.toLowerCase().includes(searchTerm);
            
        const matchesCategory = selectedCategory === 'all' || trade.category === selectedCategory;
        
        return matchesSearch && matchesCategory;
    });
    
    renderTrades(filteredTrades);
}

// Render trades to the page
function renderTrades(tradesToRender = trades) {
    const container = document.getElementById('tradesContainer');
    
    if (tradesToRender.length === 0) {
        container.innerHTML = `
            <div class="no-results">
                <div style="text-align: center; padding: 3rem; color: var(--gray);">
                    <i data-feather="search" size="64" style="color: var(--primary-color); margin-bottom: 1rem;"></i>
                    <h3 style="color: var(--primary-color); margin-bottom: 1rem;">No trades found</h3>
                    <p style="margin-bottom: 2rem;">Try adjusting your search criteria or browse different categories.</p>
                    <button class="btn btn-secondary" onclick="clearFilters()">
                        <i data-feather="x-circle"></i>
                        Clear Filters
                    </button>
                </div>
            </div>
        `;
        feather.replace();
        return;
    }
    
    container.innerHTML = tradesToRender.map(trade => `
        <div class="trade-card fade-in" data-category="${trade.category}">
            <div class="trade-image">
                <i data-feather="${getCategoryIcon(trade.category)}" size="48"></i>
            </div>
            <div class="trade-content">
                <div class="trade-header">
                    <h3>${trade.title}</h3>
                    <span class="category-badge">${trade.category}</span>
                </div>
                <div class="trade-details">
                    <div class="trade-offer">
                        <strong>Offering:</strong> ${trade.offering}
                    </div>
                    <div class="trade-seeking">
                        <strong>Seeking:</strong> ${trade.seeking}
                    </div>
                </div>
                <p class="trade-description">${truncateText(trade.description, 100)}</p>
                <div class="trade-footer">
                    <div class="trade-location">
                        <i data-feather="map-pin"></i>
                        <span>${trade.location}</span>
                    </div>
                    <button class="btn btn-contact" onclick="showContact(${trade.id})">
                        <i data-feather="user"></i>
                        Contact
                    </button>
                </div>
                <div class="trade-date">Posted: ${trade.created_at}</div>
            </div>
        </div>
    `).join('');
    
    feather.replace();
}

// Get appropriate icon for category
function getCategoryIcon(category) {
    const icons = {
        'Plants': 'leaf',
        'Seeds': 'sun',
        'Tools': 'tool',
        'Supplies': 'package',
        'Other': 'more-horizontal'
    };
    return icons[category] || 'leaf';
}

// Truncate text to specified length
function truncateText(text, length) {
    if (text.length <= length) return text;
    return text.substring(0, length) + '...';
}

// Clear all filters
function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('categoryFilter').value = 'all';
    renderTrades();
}

// Show contact modal
function showContact(tradeId) {
    const trade = trades.find(t => t.id === tradeId);
    if (!trade) return;
    
    const modalBody = document.getElementById('contactModalBody');
    
    modalBody.innerHTML = `
        <div class="contact-info">
            <div class="contact-item">
                <i data-feather="user"></i>
                <div>
                    <strong>Name:</strong> ${trade.contact_name}
                </div>
            </div>
            <div class="contact-item">
                <i data-feather="mail"></i>
                <div>
                    <strong>Email:</strong> <a href="mailto:${trade.contact_email}">${trade.contact_email}</a>
                </div>
            </div>
            ${trade.contact_phone ? `
                <div class="contact-item">
                    <i data-feather="phone"></i>
                    <div>
                        <strong>Phone:</strong> <a href="tel:${trade.contact_phone}">${trade.contact_phone}</a>
                    </div>
                </div>
            ` : ''}
            ${trade.location ? `
                <div class="contact-item">
                    <i data-feather="map-pin"></i>
                    <div>
                        <strong>Location:</strong> ${trade.location}
                    </div>
                </div>
            ` : ''}
            <div style="margin-top: 1.5rem; padding: 1rem; background: var(--light-green); border-radius: var(--border-radius);">
                <strong style="color: var(--primary-color);">Trade:</strong> ${trade.title}
            </div>
        </div>
    `;
    
    feather.replace();
    document.getElementById('contactModal').style.display = 'flex';
}

// Hide contact modal
function hideContactModal() {
    document.getElementById('contactModal').style.display = 'none';
}

// Show add trade form
function showAddTradeForm() {
    document.getElementById('add-trade').style.display = 'block';
    document.getElementById('add-trade').scrollIntoView({ behavior: 'smooth' });
}

// Hide add trade form
function hideAddTradeForm() {
    document.getElementById('add-trade').style.display = 'none';
    document.getElementById('tradeForm').reset();
    document.getElementById('home').scrollIntoView({ behavior: 'smooth' });
}

// Setup form handling
function setupFormHandling() {
    const form = document.getElementById('tradeForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

// Handle form submission
function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const newTrade = {
        id: trades.length + 1,
        title: formData.get('title'),
        category: formData.get('category'),
        offering: formData.get('offering'),
        seeking: formData.get('seeking'),
        description: formData.get('description') || '',
        location: formData.get('location') || '',
        contact_name: formData.get('contact_name'),
        contact_email: formData.get('contact_email'),
        contact_phone: formData.get('contact_phone') || '',
        created_at: new Date().toISOString().split('T')[0]
    };
    
    trades.unshift(newTrade);
    renderTrades();
    hideAddTradeForm();
    showToast('Trade listing added successfully!');
    
    // Clear form
    e.target.reset();
}

// Show toast notification
function showToast(message) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    
    toastMessage.textContent = message;
    toast.style.display = 'block';
    
    setTimeout(() => {
        hideToast();
    }, 3000);
}

// Hide toast notification
function hideToast() {
    document.getElementById('toast').style.display = 'none';
}

// Smooth scrolling
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Scroll to trades section
function scrollToTrades() {
    document.getElementById('trades').scrollIntoView({ behavior: 'smooth' });
}

// Debounce utility function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
    const modal = document.getElementById('contactModal');
    if (e.target === modal) {
        hideContactModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        hideContactModal();
    }
});

// Initialize feather icons when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    feather.replace();
});