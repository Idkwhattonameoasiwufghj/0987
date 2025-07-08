#!/usr/bin/env python3
"""
Garden Trade Hub - Simple Flask Application
A plant and garden supply trading platform
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, redirect, url_for

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'garden-trade-secret-key')

# Simple in-memory storage for trades
trades_data = [
    {
        "id": 1,
        "title": "Tomato Seedlings for Herbs",
        "category": "Plants",
        "offering": "6 healthy tomato seedlings (Roma and Cherry varieties)",
        "seeking": "Herb cuttings (basil, oregano, thyme)",
        "description": "I have extra tomato seedlings that need good homes. Looking for herb cuttings to start my herb garden.",
        "location": "Portland, OR",
        "contact_name": "Sarah Johnson",
        "contact_email": "sarah.j@email.com",
        "contact_phone": "(503) 555-0123",
        "created_at": "2025-07-08"
    },
    {
        "id": 2,
        "title": "Garden Tools Exchange",
        "category": "Tools",
        "offering": "Rake and small shovel, lightly used",
        "seeking": "Pruning shears or watering can",
        "description": "Downsizing my tool collection. These are in great condition and ready for a new garden.",
        "location": "Seattle, WA",
        "contact_name": "Mike Chen",
        "contact_email": "mike.chen@email.com",
        "contact_phone": "(206) 555-0456",
        "created_at": "2025-07-07"
    },
    {
        "id": 3,
        "title": "Organic Seeds Collection",
        "category": "Seeds",
        "offering": "Variety pack of organic vegetable seeds",
        "seeking": "Flower seeds or bulbs",
        "description": "I have extra packets of organic carrot, lettuce, and radish seeds. Looking for flower seeds to beautify my garden.",
        "location": "San Francisco, CA",
        "contact_name": "Emily Rodriguez",
        "contact_email": "emily.r@email.com",
        "contact_phone": "",
        "created_at": "2025-07-06"
    }
]

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Garden Trade Hub - Plant & Garden Supply Trading</title>
    <meta name="description" content="Connect with fellow gardeners to trade plants, seeds, tools, and garden supplies.">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌱</text></svg>">
    <style>
        /* Include all the CSS from style.css here */
        :root {
            --primary-color: #16a34a;
            --primary-dark: #15803d;
            --secondary-color: #059669;
            --accent-color: #22c55e;
            --light-green: #dcfce7;
            --gray: #6b7280;
            --dark-gray: #374151;
            --light-gray: #f8fafc;
            --white: #ffffff;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --border-radius: 8px;
            --transition: all 0.3s ease;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--dark-gray);
            background-color: var(--light-gray);
        }
        
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        
        /* Navigation */
        .navbar {
            background: var(--white);
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 3px solid var(--primary-color);
        }
        
        .navbar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 20px;
        }
        
        .nav-brand {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary-color);
        }
        
        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: var(--gray);
            font-weight: 500;
            transition: var(--transition);
        }
        
        .nav-links a:hover { color: var(--primary-color); }
        
        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, var(--light-green) 0%, #f0fdf4 100%);
            padding: 5rem 0;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 3rem;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 1.2rem;
            color: var(--gray);
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: var(--border-radius);
            font-weight: 500;
            text-decoration: none;
            cursor: pointer;
            transition: var(--transition);
            font-size: 1rem;
            margin: 0.5rem;
        }
        
        .btn-primary {
            background: var(--primary-color);
            color: var(--white);
        }
        
        .btn-primary:hover { background: var(--primary-dark); }
        
        .btn-secondary {
            background: transparent;
            color: var(--primary-color);
            border: 2px solid var(--primary-color);
        }
        
        .btn-secondary:hover {
            background: var(--primary-color);
            color: var(--white);
        }
        
        /* Trade Section */
        .trades-section {
            padding: 3rem 0;
            background: var(--white);
        }
        
        .trades-section h2 {
            text-align: center;
            color: var(--primary-color);
            margin-bottom: 2rem;
        }
        
        .trades-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .trade-card {
            background: var(--white);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: var(--transition);
        }
        
        .trade-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        }
        
        .trade-content { padding: 1.5rem; }
        
        .trade-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .trade-header h3 {
            color: var(--primary-color);
            font-size: 1.2rem;
            margin: 0;
        }
        
        .category-badge {
            background: var(--primary-color);
            color: var(--white);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .trade-details {
            margin-bottom: 1rem;
            padding-left: 1rem;
            border-left: 3px solid var(--primary-color);
        }
        
        .trade-offer, .trade-seeking { margin-bottom: 0.5rem; }
        .trade-offer strong { color: var(--primary-color); }
        .trade-seeking strong { color: var(--secondary-color); }
        
        .trade-description {
            color: var(--gray);
            margin-bottom: 1rem;
            line-height: 1.5;
        }
        
        .trade-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        
        .trade-location {
            color: var(--gray);
            font-size: 0.9rem;
        }
        
        .trade-date {
            color: var(--gray);
            font-size: 0.8rem;
        }
        
        /* Footer */
        .footer {
            background: var(--primary-dark);
            color: var(--white);
            padding: 3rem 0;
            text-align: center;
        }
        
        .footer p {
            color: rgba(255, 255, 255, 0.8);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5rem; }
            .trades-grid { grid-template-columns: 1fr; }
            .nav-links { display: none; }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">
                🌱 Garden Trade Hub
            </div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#trades">Browse Trades</a></li>
                <li><a href="/add">Add Trade</a></li>
            </ul>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="container">
            <h1>Trade Plants & Garden Supplies</h1>
            <p>Connect with fellow gardeners in your community to exchange plants, seeds, tools, and garden supplies.</p>
            <div>
                <a href="/add" class="btn btn-primary">➕ Add Trade</a>
                <a href="#trades" class="btn btn-secondary">🔍 Browse Trades</a>
            </div>
        </div>
    </section>

    <!-- Trades Section -->
    <section id="trades" class="trades-section">
        <div class="container">
            <h2>Browse Trade Listings</h2>
            <div class="trades-grid">
                {% for trade in trades %}
                <div class="trade-card">
                    <div class="trade-content">
                        <div class="trade-header">
                            <h3>{{ trade.title }}</h3>
                            <span class="category-badge">{{ trade.category }}</span>
                        </div>
                        <div class="trade-details">
                            <div class="trade-offer">
                                <strong>Offering:</strong> {{ trade.offering }}
                            </div>
                            <div class="trade-seeking">
                                <strong>Seeking:</strong> {{ trade.seeking }}
                            </div>
                        </div>
                        <p class="trade-description">{{ trade.description }}</p>
                        <div class="trade-footer">
                            <div class="trade-location">📍 {{ trade.location }}</div>
                            <div class="trade-date">Posted: {{ trade.created_at }}</div>
                        </div>
                        <div style="margin-top: 1rem;">
                            <strong>Contact:</strong> {{ trade.contact_name }} ({{ trade.contact_email }})
                            {% if trade.contact_phone %}
                            <br><strong>Phone:</strong> {{ trade.contact_phone }}
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <h4>Garden Trade Hub</h4>
            <p>&copy; 2025 Garden Trade Hub. Built with 🌱 for gardeners.</p>
        </div>
    </footer>
</body>
</html>
"""

ADD_TRADE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Trade - Garden Trade Hub</title>
    <style>
        :root {
            --primary-color: #16a34a;
            --primary-dark: #15803d;
            --light-green: #dcfce7;
            --gray: #6b7280;
            --dark-gray: #374151;
            --light-gray: #f8fafc;
            --white: #ffffff;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --border-radius: 8px;
            --transition: all 0.3s ease;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--dark-gray);
            background-color: var(--light-gray);
        }
        
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        
        .form-container {
            background: var(--white);
            padding: 2rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin-top: 2rem;
        }
        
        h1 {
            color: var(--primary-color);
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        
        input, select, textarea {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid var(--light-green);
            border-radius: var(--border-radius);
            font-size: 1rem;
            transition: var(--transition);
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: var(--primary-color);
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: var(--border-radius);
            font-weight: 500;
            text-decoration: none;
            cursor: pointer;
            transition: var(--transition);
            font-size: 1rem;
            margin: 0.5rem;
        }
        
        .btn-primary {
            background: var(--primary-color);
            color: var(--white);
        }
        
        .btn-primary:hover { background: var(--primary-dark); }
        
        .btn-secondary {
            background: transparent;
            color: var(--primary-color);
            border: 2px solid var(--primary-color);
        }
        
        .btn-secondary:hover {
            background: var(--primary-color);
            color: var(--white);
        }
        
        .form-buttons {
            text-align: center;
            margin-top: 2rem;
        }
        
        .success-message {
            background: var(--light-green);
            color: var(--primary-color);
            padding: 1rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="form-container">
            <h1>🌱 Add New Trade Listing</h1>
            
            {% if success %}
            <div class="success-message">
                ✅ Trade listing added successfully! <a href="/">View all trades</a>
            </div>
            {% endif %}
            
            <form method="POST">
                <div class="form-group">
                    <label for="title">Trade Title *</label>
                    <input type="text" id="title" name="title" required placeholder="e.g., Tomato seedlings for herb cuttings">
                </div>
                
                <div class="form-group">
                    <label for="category">Category *</label>
                    <select id="category" name="category" required>
                        <option value="">Select category</option>
                        <option value="Plants">Plants</option>
                        <option value="Seeds">Seeds</option>
                        <option value="Tools">Tools</option>
                        <option value="Supplies">Supplies</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="offering">What I'm Offering *</label>
                    <textarea id="offering" name="offering" required placeholder="Describe what you're offering to trade"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="seeking">What I'm Seeking *</label>
                    <textarea id="seeking" name="seeking" required placeholder="Describe what you're looking for"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="description">Description</label>
                    <textarea id="description" name="description" placeholder="Additional details about your trade..."></textarea>
                </div>
                
                <div class="form-group">
                    <label for="location">Location</label>
                    <input type="text" id="location" name="location" placeholder="e.g., Portland, OR or ZIP code">
                </div>
                
                <div class="form-group">
                    <label for="contact_name">Your Name *</label>
                    <input type="text" id="contact_name" name="contact_name" required placeholder="Your full name">
                </div>
                
                <div class="form-group">
                    <label for="contact_email">Email Address *</label>
                    <input type="email" id="contact_email" name="contact_email" required placeholder="your.email@example.com">
                </div>
                
                <div class="form-group">
                    <label for="contact_phone">Phone Number</label>
                    <input type="tel" id="contact_phone" name="contact_phone" placeholder="(555) 123-4567">
                </div>
                
                <div class="form-buttons">
                    <a href="/" class="btn btn-secondary">Cancel</a>
                    <button type="submit" class="btn btn-primary">Add Trade Listing</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page displaying all trades"""
    return render_template_string(HTML_TEMPLATE, trades=trades_data)

@app.route('/add', methods=['GET', 'POST'])
def add_trade():
    """Add new trade listing"""
    if request.method == 'POST':
        # Get form data
        new_trade = {
            'id': len(trades_data) + 1,
            'title': request.form.get('title', '').strip(),
            'category': request.form.get('category', '').strip(),
            'offering': request.form.get('offering', '').strip(),
            'seeking': request.form.get('seeking', '').strip(),
            'description': request.form.get('description', '').strip(),
            'location': request.form.get('location', '').strip(),
            'contact_name': request.form.get('contact_name', '').strip(),
            'contact_email': request.form.get('contact_email', '').strip(),
            'contact_phone': request.form.get('contact_phone', '').strip(),
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Simple validation
        if all([new_trade['title'], new_trade['category'], new_trade['offering'], 
                new_trade['seeking'], new_trade['contact_name'], new_trade['contact_email']]):
            trades_data.insert(0, new_trade)  # Add to beginning of list
            return render_template_string(ADD_TRADE_TEMPLATE, success=True)
    
    return render_template_string(ADD_TRADE_TEMPLATE)

@app.route('/api/trades')
def api_trades():
    """API endpoint for trades (for AJAX functionality)"""
    return jsonify(trades_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)