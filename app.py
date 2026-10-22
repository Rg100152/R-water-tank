import os
from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
DB_NAME = "r_water_tank_final.db"

# ==========================================
# 1. DATABASE SETUP
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS tanks')
    c.execute('''
        CREATE TABLE tanks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_name TEXT NOT NULL,
            brand TEXT NOT NULL,
            capacity TEXT NOT NULL,
            price REAL NOT NULL,
            layers TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
    ''')
    
    dummy_data = [
        ("Industrial Plastics", "Supremo", "1000 Ltr", 5200.0, "4 Layer", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgeI5zVy39ZDy63N-Krgvg8Ux7FOT_1RXYpZpzU2_gkg&s=10"),
        ("BuildWell Co.", "Waterway", "500 Ltr", 2800.0, "3 Layer", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFq6Lh8Iluq9R2WGhqUyZ0FEdb8uq89YRXGPUJiwlP9A&s"),
        ("VBSPU Metals", "Ganga", "300 Ltr", 1800.0, "2 Layer", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmQRSrqZPK08-s56MsqCXGkJPh9tQBAM2Iyz0X-6NVIg&s=10"),
        ("Metro Hardware", "Shine", "2000 Ltr", 9500.0, "5 Layer", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmwhItRT8xakZWoqtmRezVhj-7mOx0vbn3P5FyAAOEAw&s=10"),
        ("R Tech Suppliers", "Sintex Pro", "750 Ltr", 3900.0, "3 Layer", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRU0E7f3ar_g8vlDX1ulVWnYi-B9_qbMoCMdrtFE7ZDGw&s=10"),
        ("Pioneer Tanks", "Plasto", "5000 Ltr", 22000.0, "6 Layer", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPkg0KJ-I8aJrfVmXcMOxLlzEFBGt6j3x8S_5dH5fLsA&s=10"),
        ("Gautam Tanks", "Penguin", "1500 Ltr", 6800.0, "4 Layer", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4Xqoy9dBLUqy79ErZfUNGAaNFhkcNDcjM0dsrD65xoQ&s=10"),
        ("Aqua Guard", "Ashirvad", "1000 Ltr", 5500.0, "3 Layer", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7uHO3eaVR9xHNtxp2ZtGU4aSvdXiGa0gqaP5bA-7jSQ&s=10")
    ]
    c.executemany('INSERT INTO tanks (seller_name, brand, capacity, price, layers, image_url) VALUES (?, ?, ?, ?, ?, ?)', dummy_data)
    conn.commit()
    conn.close()

# ==========================================
# 2. HTML TEMPLATES
# ==========================================
BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>R Water Tank | Premium Storage Solutions</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Montserrat:wght@500;700;900&display=swap" rel="stylesheet">
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <style>
        :root {
            --primary-blue: #0077b6;
            --light-blue: #90e0ef;
            --navy-blue: #023e8a;
            --accent-red: #d90429;
            --bg-light: #f8f9fa;
        }
        * { box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background-color: var(--bg-light); color: #333; overflow-x: hidden; min-height: 100vh; display: flex; flex-direction: column; margin: 0; }
        h1, h2, h3, .heading-font { font-family: 'Montserrat', sans-serif; }
        
        /* Loader */
        #loader { position: fixed; inset: 0; background: #ffffff; z-index: 9999; display: flex; justify-content: center; align-items: center; flex-direction: column; transition: opacity 0.8s ease, visibility 0.8s; }
        .tank-loader-container { width: 80px; height: 100px; border: 4px solid var(--navy-blue); border-top: 8px solid var(--navy-blue); border-radius: 5px 5px 15px 15px; position: relative; overflow: hidden; }
        .tank-water { position: absolute; bottom: 0; left: 0; right: 0; background: var(--primary-blue); animation: fillTank 1.8s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
        @keyframes fillTank { 0% { height: 0%; } 100% { height: 100%; } }
        .loader-text { margin-top: 20px; font-weight: 800; color: var(--navy-blue); letter-spacing: 2px; text-transform: uppercase; animation: pulse 1s infinite alternate; }
        @keyframes pulse { from { opacity: 0.5; } to { opacity: 1; } }

        /* Bubbles */
        .bubbles-container { position: fixed; inset: 0; z-index: -1; pointer-events: none; overflow: hidden; }
        .bubble { position: absolute; bottom: -50px; background: rgba(0, 119, 182, 0.08); border-radius: 50%; border: 1px solid rgba(0, 119, 182, 0.15); animation: floatUp infinite ease-in; }
        @keyframes floatUp { 0% { transform: translateY(0) scale(1); opacity: 1; } 100% { transform: translateY(-120vh) scale(1.5); opacity: 0; } }

        /* Header */
        .corporate-header { background: #ffffff; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
        .nav-link { color: var(--navy-blue); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; position: relative; transition: color 0.3s; padding-bottom: 5px; }
        .nav-link::after { content: ''; position: absolute; width: 0; height: 3px; bottom: 0; left: 0; background-color: var(--primary-blue); transition: width 0.3s; }
        .nav-link:hover { color: var(--primary-blue); }
        .nav-link:hover::after { width: 100%; }
        
        .btn-primary { background: var(--primary-blue); color: white; transition: 0.3s; box-shadow: 0 4px 15px rgba(0, 119, 182, 0.3); }
        .btn-primary:hover { background: var(--navy-blue); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(2, 62, 138, 0.4); }
        
        /* Product Card */
        .product-card { background: white; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); transition: transform 0.3s, box-shadow 0.3s; overflow: hidden; border: 1px solid #eee; display: flex; flex-direction: column; }
        .product-card:hover { transform: translateY(-8px); box-shadow: 0 15px 40px rgba(0,0,0,0.12); border-color: var(--light-blue); }
        
        /* ✅ FIXED IMAGE STYLES */
        .product-img-wrapper {
            width: 100%;
            height: 220px;
            background: linear-gradient(135deg, #ffffff 0%, #f0f7fb 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
            padding: 12px;
        }
        .product-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
            border-radius: 8px;
            transition: transform 0.5s ease;
        }
        .product-card:hover .product-img { transform: scale(1.06); }
        
        /* Guide card images */
        .guide-img-wrapper {
            width: 100%;
            height: 140px;
            overflow: hidden;
            border-radius: 8px;
            background: #f0f7fb;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .guide-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
            transition: transform 0.4s ease;
        }
        .group:hover .guide-img { transform: scale(1.1); }
        
        /* Hero images */
        .hero-img-main {
            width: 100%;
            height: 380px;
            object-fit: cover;
            object-position: center;
            border-radius: 16px;
        }
        .hero-img-overlay {
            width: 65%;
            height: 200px;
            object-fit: cover;
            object-position: center;
            border-radius: 16px;
        }
        
        .form-input { width: 100%; background: #f8f9fa; border: 1px solid #ddd; padding: 12px; border-radius: 8px; color: #333; transition: 0.3s; }
        .form-input:focus { border-color: var(--primary-blue); outline: none; box-shadow: 0 0 0 3px rgba(0, 119, 182, 0.1); }
    </style>
</head>
<body>
    <div class="bubbles-container" id="bubbles"></div>

    <div id="loader">
        <div class="tank-loader-container"><div class="tank-water"></div></div>
        <div class="loader-text">Loading R Tank Centre...</div>
    </div>

    <nav class="corporate-header sticky top-0 z-50 py-4 px-6 md:px-12 flex flex-wrap justify-between items-center" data-aos="fade-down" data-aos-duration="800">
        <a href="/" class="flex items-center gap-3">
            <div class="w-10 h-10 bg-[#0077b6] rounded-full flex items-center justify-center text-white font-black text-xl">R</div>
            <span class="text-2xl font-black heading-font text-[#023e8a]">Water Tank</span>
        </a>
        <div class="flex gap-6 md:gap-8 mt-4 md:mt-0 text-xs md:text-sm">
            <a href="/" class="nav-link">Home</a>
            <a href="/shop" class="nav-link">Products</a>
            <a href="/seller" class="nav-link text-[#d90429]">Become a Seller</a>
            <a href="/cart" class="nav-link">Bookings</a>
        </div>
    </nav>

    <main class="flex-grow px-4 md:px-12 py-10 relative z-10">
        {{ content | safe }}
    </main>

    <footer class="bg-[#023e8a] text-white text-center py-10 mt-16">
        <h2 class="text-2xl font-black heading-font mb-2">R WATER TANK PLATFORM</h2>
        <p class="text-[#90e0ef] font-medium text-sm mb-6">Reliable and Superior Quality Water Storage Solutions</p>
        <div class="inline-block border-t border-[rgba(255,255,255,0.2)] pt-4 px-10 text-xs font-bold tracking-widest uppercase text-white opacity-80">
            System Developed by Raj Gautam | BCA 5th Sem
        </div>
    </footer>

    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        AOS.init({ once: false, mirror: true, offset: 100 });
        window.addEventListener('load', () => {
            setTimeout(() => {
                document.getElementById('loader').style.opacity = '0';
                setTimeout(() => document.getElementById('loader').style.display = 'none', 800);
            }, 1200);
        });

        const bubblesContainer = document.getElementById('bubbles');
        for (let i = 0; i < 18; i++) {
            let bubble = document.createElement('div');
            bubble.classList.add('bubble');
            let size = Math.random() * 40 + 10;
            bubble.style.width = size + 'px';
            bubble.style.height = size + 'px';
            bubble.style.left = Math.random() * 100 + 'vw';
            bubble.style.animationDuration = Math.random() * 8 + 4 + 's';
            bubble.style.animationDelay = Math.random() * 5 + 's';
            bubblesContainer.appendChild(bubble);
        }

        // ✅ Global image error fallback
        document.querySelectorAll('img').forEach(img => {
            img.addEventListener('error', function() {
                this.src = 'https://via.placeholder.com/400x400/e0f2fe/0077b6?text=Water+Tank';
            });
        });
    </script>
</body>
</html>
"""

HOME_HTML = """
<div class="grid lg:grid-cols-2 gap-12 items-center min-h-[65vh] bg-white rounded-2xl p-8 md:p-12 shadow-sm border border-gray-100" data-aos="fade-up" data-aos-duration="1000">
    <div class="space-y-6">
        <h1 class="text-4xl md:text-6xl font-black heading-font text-[#023e8a] leading-tight">
            Pure Water,<br>
            <span class="text-[#0077b6]">Simple Choice.</span>
        </h1>
        <p class="text-gray-600 text-lg md:text-xl font-medium max-w-lg leading-relaxed">
            Where Simplicity Meets Durability. Explore our range of premium plastic and stainless steel water storage solutions for residential and industrial needs.
        </p>
        <div class="pt-4 flex gap-4">
            <a href="/shop" class="btn-primary px-8 py-3 rounded-full font-bold uppercase tracking-wider text-sm">See Our Products</a>
            <a href="/seller" class="px-8 py-3 rounded-full font-bold uppercase tracking-wider text-sm border-2 border-[#0077b6] text-[#0077b6] hover:bg-[#0077b6] hover:text-white transition">Sell With Us</a>
        </div>
        
        <div class="flex items-center gap-6 pt-6 border-t border-gray-100 mt-6">
            <div class="flex flex-col">
                <span class="text-2xl font-black text-[#023e8a]">100%</span>
                <span class="text-xs text-gray-500 font-bold uppercase">Food Grade</span>
            </div>
            <div class="flex flex-col">
                <span class="text-2xl font-black text-[#023e8a]">UV</span>
                <span class="text-xs text-gray-500 font-bold uppercase">Protected</span>
            </div>
            <div class="flex flex-col">
                <span class="text-2xl font-black text-[#023e8a]">10+</span>
                <span class="text-xs text-gray-500 font-bold uppercase">Top Brands</span>
            </div>
        </div>
    </div>
    
    <div class="relative flex justify-center items-center h-[420px]">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFq6Lh8Iluq9R2WGhqUyZ0FEdb8uq89YRXGPUJiwlP9A&s" 
             alt="Hero Tank" 
             class="hero-img-main shadow-2xl border-4 border-white z-20" 
             data-aos="fade-left" data-aos-delay="200"
             onerror="this.src='https://via.placeholder.com/500x400/e0f2fe/0077b6?text=Water+Tank'">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgeI5zVy39ZDy63N-Krgvg8Ux7FOT_1RXYpZpzU2_gkg&s=10" 
             alt="Hero Tank 2" 
             class="hero-img-overlay absolute -bottom-6 -right-2 shadow-2xl border-4 border-white z-30" 
             data-aos="fade-up" data-aos-delay="400"
             onerror="this.src='https://via.placeholder.com/400x250/e0f2fe/0077b6?text=Water+Tank'">
    </div>
</div>

<div class="mt-24 text-center" data-aos="zoom-in" data-aos-duration="1000">
    <h2 class="text-3xl font-black heading-font text-[#023e8a] mb-2">Types Of Tanks & Guides</h2>
    <div class="h-1 w-20 bg-[#0077b6] mx-auto mb-12"></div>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div class="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-lg transition group" data-aos="fade-up" data-aos-delay="100">
            <div class="guide-img-wrapper mb-4">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFUlFG3VRfAX6jUYAP91YNx20C9Qjg0zx8VPBhL4KDIA&s=10" 
                     class="guide-img" 
                     onerror="this.src='https://via.placeholder.com/300x200/e0f2fe/0077b6?text=Industrial'">
            </div>
            <h3 class="font-bold text-[#023e8a] text-sm">Industrial Base</h3>
        </div>
        <div class="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-lg transition group" data-aos="fade-up" data-aos-delay="200">
            <div class="guide-img-wrapper mb-4">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc4cixVhhCTaLj2fwR2Nb74goLjTSRYuJfuEQWSAPOYw&s=10" 
                     class="guide-img" 
                     onerror="this.src='https://via.placeholder.com/300x200/e0f2fe/0077b6?text=Residential'">
            </div>
            <h3 class="font-bold text-[#023e8a] text-sm">Residential Models</h3>
        </div>
        <div class="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-lg transition group" data-aos="fade-up" data-aos-delay="300">
            <div class="guide-img-wrapper mb-4">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfGy_V4-lwsbjUZnjBXDA7hlsvwGpA-x6kDYVQP8E3GQ&s=10" 
                     class="guide-img" 
                     onerror="this.src='https://via.placeholder.com/300x200/e0f2fe/0077b6?text=Multi-Layer'">
            </div>
            <h3 class="font-bold text-[#023e8a] text-sm">Multi-Layer Guide</h3>
        </div>
        <div class="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-lg transition group" data-aos="fade-up" data-aos-delay="400">
            <div class="guide-img-wrapper mb-4">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTElE9tuAB87_djqD0BMdTGlaoorn292WPWDhkosEIo7g&s=10" 
                     class="guide-img" 
                     onerror="this.src='https://via.placeholder.com/300x200/e0f2fe/0077b6?text=Commercial'">
            </div>
            <h3 class="font-bold text-[#023e8a] text-sm">Commercial Setup</h3>
        </div>
    </div>
</div>
"""

SHOP_HTML = """
<div class="text-center mb-12" data-aos="fade-down">
    <h2 class="text-4xl font-black heading-font text-[#023e8a]">Range of Products</h2>
    <p class="text-gray-500 mt-2 font-medium">Verified Sellers, Genuine Products</p>
</div>

<div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
    {% for tank in tanks %}
    <div class="product-card" data-aos="fade-up" data-aos-delay="{{ loop.index0 * 50 }}">
        <div class="product-img-wrapper">
            <span class="absolute top-3 left-3 bg-[#0077b6] text-white text-[10px] font-bold px-2.5 py-1 rounded-full uppercase z-10">{{ tank[5] }}</span>
            <img src="{{ tank[6] }}" 
                 alt="{{ tank[2] }}" 
                 class="product-img"
                 onerror="this.src='https://via.placeholder.com/400x400/e0f2fe/0077b6?text=Water+Tank'">
        </div>
        <div class="p-5 flex-grow flex flex-col justify-between">
            <div>
                <p class="text-[10px] text-[#0077b6] font-bold uppercase tracking-wider mb-1">{{ tank[1] }}</p>
                <h3 class="text-lg font-bold heading-font text-[#023e8a] mb-2">{{ tank[2] }}</h3>
                <span class="inline-block bg-[#f0f7fb] border border-[#cfe8f3] px-2.5 py-1 rounded-md text-xs text-[#023e8a] font-semibold mb-4">Capacity: {{ tank[3] }}</span>
            </div>
            <div class="flex justify-between items-center pt-3 border-t border-gray-100 mt-2">
                <p class="text-lg font-black text-[#d90429]">₹{{ tank[4] }}</p>
                <a href="/book/{{ tank[0] }}" class="btn-primary px-3 py-2 rounded-lg font-bold text-[11px] uppercase tracking-wide text-center">Book Now</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
"""

SELLER_HTML = """
<div class="max-w-3xl mx-auto" data-aos="zoom-in" data-aos-duration="1000">
    <div class="bg-white p-8 md:p-12 rounded-2xl shadow-lg border border-gray-100 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-2 bg-[#0077b6]"></div>
        
        <div class="text-center mb-8">
            <h2 class="text-3xl font-black heading-font text-[#023e8a]">Partner With Us</h2>
            <p class="text-gray-500 text-sm mt-2">List your high-quality water tanks on the R Platform</p>
        </div>
        
        <form method="POST" action="/seller" class="space-y-6">
            <div class="grid md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-[#023e8a] font-bold text-xs uppercase tracking-wider mb-2">Vendor Name</label>
                    <input type="text" name="seller_name" required class="form-input" placeholder="E.g. Aquacleen Pvt Ltd">
                </div>
                <div>
                    <label class="block text-[#023e8a] font-bold text-xs uppercase tracking-wider mb-2">Product Brand</label>
                    <input type="text" name="brand" required class="form-input" placeholder="E.g. Supremo">
                </div>
            </div>
            
            <div class="grid md:grid-cols-3 gap-6">
                <div>
                    <label class="block text-gray-600 font-bold text-xs uppercase tracking-wider mb-2">Volume</label>
                    <input type="text" name="capacity" required class="form-input" placeholder="E.g. 1000 Ltr">
                </div>
                <div>
                    <label class="block text-gray-600 font-bold text-xs uppercase tracking-wider mb-2">Layer Type</label>
                    <select name="layers" class="form-input cursor-pointer">
                        <option value="2 Layer">2 Layer Standard</option>
                        <option value="3 Layer">3 Layer (Food Grade)</option>
                        <option value="4 Layer">4 Layer (Foam)</option>
                        <option value="6 Layer">6 Layer (Heavy Duty)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-[#d90429] font-bold text-xs uppercase tracking-wider mb-2">Selling Price (₹)</label>
                    <input type="number" name="price" required class="form-input" placeholder="0.00">
                </div>
            </div>

            <div>
                <label class="block text-gray-600 font-bold text-xs uppercase tracking-wider mb-2">Product Image Link</label>
                <input type="text" name="image_url" class="form-input" placeholder="Paste full https://... link here (optional)">
            </div>
            
            <button type="submit" class="w-full btn-primary text-white font-bold text-lg py-4 rounded-xl uppercase tracking-widest mt-6">
                Submit Product Listing
            </button>
        </form>
    </div>
</div>
"""

CART_HTML = """
<div class="max-w-xl mx-auto text-center" data-aos="zoom-in">
    <div class="bg-white p-12 rounded-2xl shadow-xl border border-gray-100">
        <div class="w-20 h-20 mx-auto bg-[#0077b6] rounded-full flex items-center justify-center mb-6 text-white text-3xl shadow-lg" data-aos="zoom-in" data-aos-delay="300">
            ✓
        </div>
        <h2 class="text-3xl font-black heading-font text-[#023e8a] mb-2">Enquiry Submitted</h2>
        <p class="text-gray-600 mb-8">Your product requirement has been forwarded to the supplier. They will contact you for dispatch details.</p>
        
        <div class="bg-[#f8f9fa] p-4 rounded-lg mb-8 border border-gray-200 border-dashed">
            <p class="text-xs text-gray-500 uppercase font-bold tracking-widest mb-1">Enquiry Ref Number</p>
            <p class="font-mono text-xl text-[#023e8a] font-bold">RTK-{{ tid }}</p>
        </div>

        <a href="/shop" class="btn-primary px-8 py-3 rounded-full font-bold uppercase tracking-wider text-sm inline-block">Continue Browsing</a>
    </div>
</div>
"""

# ==========================================
# 3. FLASK BACKEND
# ==========================================
def render_page(content_html, **kwargs):
    rendered_content = render_template_string(content_html, **kwargs)
    return render_template_string(BASE_HTML, content=rendered_content)

@app.route('/')
def home():
    return render_page(HOME_HTML)

@app.route('/shop')
def shop():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM tanks ORDER BY id DESC')
    tanks = c.fetchall()
    conn.close()
    return render_page(SHOP_HTML, tanks=tanks)

@app.route('/seller', methods=['GET', 'POST'])
def seller():
    if request.method == 'POST':
        seller_name = request.form['seller_name']
        brand = request.form['brand']
        capacity = request.form['capacity']
        layers = request.form['layers']
        price = request.form['price']
        image_url = request.form.get('image_url', '').strip()
        
        if not image_url:
            image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgeI5zVy39ZDy63N-Krgvg8Ux7FOT_1RXYpZpzU2_gkg&s=10"
            
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO tanks (seller_name, brand, capacity, price, layers, image_url) VALUES (?, ?, ?, ?, ?, ?)',
                  (seller_name, brand, capacity, float(price), layers, image_url))
        conn.commit()
        conn.close()
        
        print("\n" + "="*50)
        print("🏢 NEW SELLER LISTING ADDED 🏢")
        print("="*50)
        print(f"Vendor : {seller_name}")
        print(f"Product: {brand} | {capacity} | {layers}")
        print(f"Price  : ₹{price}")
        print("="*50 + "\n")
        return redirect(url_for('shop'))
        
    return render_page(SELLER_HTML)

@app.route('/book/<int:tank_id>')
def book(tank_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT brand, seller_name, price FROM tanks WHERE id = ?', (tank_id,))
    tank = c.fetchone()
    conn.close()
    
    transaction_id = f"{random.randint(100000, 999999)}"
    
    if tank:
        print("\n" + "✔️ "*15)
        print("📋 NEW CUSTOMER ENQUIRY LOGGED 📋")
        print("✔️ "*15)
        print(f"Ref ID : RTK-{transaction_id}")
        print(f"Item   : {tank[0]}")
        print(f"Vendor : {tank[1]}")
        print(f"Value  : ₹{tank[2]}")
        print(f"Time   : {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
        print("✔️ "*15 + "\n")
        
    return render_page(CART_HTML, tid=transaction_id)

@app.route('/cart')
def cart():
    return redirect(url_for('shop'))

if __name__ == '__main__':
    init_db()
    print("\n" + "*"*60)
    print("🌍 R WATER TANK (CORPORATE EDITION) IS LIVE 🌍")
    print("🌐 Click here to open: http://127.0.0.1:5000")
    print("*"*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
