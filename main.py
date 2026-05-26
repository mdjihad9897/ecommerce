# ============================================================
# ULTRA MODERN AI POWERED ECOMMERCE PLATFORM
# SINGLE FILE PYTHON APPLICATION
# ============================================================

import os
import json
import time
import asyncio
import secrets
import hashlib
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from passlib.context import CryptContext
import jwt

from rapidfuzz import fuzz

# ============================================================
# APP CONFIGURATION
# ============================================================

APP_NAME = "AI Commerce"
SECRET_KEY = "SUPER_SECRET_ENTERPRISE_KEY"
ALGORITHM = "HS256"

app = FastAPI(
    title="AI Commerce",
    description="Enterprise AI Ecommerce Platform",
    version="1.0"
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = "sqlite:///./ecommerce.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ============================================================
# SECURITY
# ============================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_jwt(data):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# ============================================================
# DATABASE MODELS
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    category = Column(String)
    image = Column(String)
    price = Column(Float)
    rating = Column(Float)
    stock = Column(Integer)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    total = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ============================================================
# DEMO PRODUCTS
# ============================================================

db = SessionLocal()

if db.query(Product).count() == 0:

    sample_products = [

        Product(
            title="Premium Smart Watch",
            description="Modern AI smart wearable",
            category="Electronics",
            image="https://images.unsplash.com/photo-1546868871-7041f2a55e12",
            price=299,
            rating=4.9,
            stock=25
        ),

        Product(
            title="Luxury Sneakers",
            description="Comfortable modern sneakers",
            category="Fashion",
            image="https://images.unsplash.com/photo-1542291026-7eec264c27ff",
            price=180,
            rating=4.8,
            stock=50
        ),

        Product(
            title="Gaming Laptop",
            description="Ultra powerful performance",
            category="Computers",
            image="https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
            price=1999,
            rating=5.0,
            stock=12
        )

    ]

    db.add_all(sample_products)
    db.commit()

# ============================================================
# AI SEARCH ENGINE
# ============================================================

def ai_search(query, products):

    ranked = []

    for product in products:

        title_score = fuzz.ratio(
            query.lower(),
            product.title.lower()
        )

        category_score = fuzz.ratio(
            query.lower(),
            product.category.lower()
        )

        final_score = (title_score * 0.7) + (category_score * 0.3)

        ranked.append((final_score, product))

    ranked.sort(reverse=True, key=lambda x: x[0])

    return [x[1] for x in ranked]

# ============================================================
# SEO GENERATION
# ============================================================

def seo_meta(title, description):

    return f"""
    <title>{title}</title>

    <meta name="description" content="{description}">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">

    <meta name="twitter:card" content="summary_large_image">

    <link rel="canonical" href="http://127.0.0.1:8000">

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Store",
      "name": "AI Commerce"
    }}
    </script>
    """

# ============================================================
# PREMIUM MODERN UI
# ============================================================

def render_page(content, title="AI Commerce"):

    return f"""

<!DOCTYPE html>
<html lang="en">

<head>

{seo_meta(title, "Modern AI Ecommerce Platform")}

<style>

:root {{
    --bg: #0f172a;
    --card: #1e293b;
    --text: #ffffff;
    --soft: #94a3b8;
    --accent: #6366f1;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: Inter, sans-serif;
    background: var(--bg);
    color: var(--text);
}}

.container {{
    width: 95%;
    max-width: 1400px;
    margin: auto;
}}

header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
}}

.logo {{
    font-size: 30px;
    font-weight: bold;
}}

.search-box {{
    width: 100%;
    margin: 30px 0;
}}

.search-box input {{
    width: 100%;
    padding: 18px;
    border-radius: 18px;
    border: none;
    background: #1e293b;
    color: white;
    font-size: 18px;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit,minmax(260px,1fr));
    gap: 25px;
}}

.card {{
    background: var(--card);
    border-radius: 24px;
    overflow: hidden;
    transition: 0.4s;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}}

.card:hover {{
    transform: translateY(-8px);
}}

.card img {{
    width: 100%;
    height: 260px;
    object-fit: cover;
    transition: 0.4s;
}}

.card:hover img {{
    transform: scale(1.05);
}}

.card-body {{
    padding: 20px;
}}

.price {{
    font-size: 24px;
    margin-top: 10px;
    color: #38bdf8;
}}

button {{
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 14px;
    background: var(--accent);
    color: white;
    margin-top: 15px;
    font-size: 16px;
    cursor: pointer;
    transition: 0.3s;
}}

button:hover {{
    opacity: 0.9;
}}

@media(max-width:768px) {{

    .card img {{
        height: 220px;
    }}

}}

.fade {{
    animation: fadeIn 0.8s ease;
}}

@keyframes fadeIn {{

    from {{
        opacity: 0;
        transform: translateY(10px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}

}}

</style>

</head>

<body>

<div class="container">

<header>

<div class="logo">AI Commerce</div>

<div>
🛒 Wishlist | Cart | Account
</div>

</header>

{content}

</div>

<script>

function voiceSearch() {{

    const recognition =
        new webkitSpeechRecognition();

    recognition.onresult = function(event) {{

        document.getElementById("search")
            .value = event.results[0][0].transcript;

        document.getElementById("searchForm")
            .submit();
    }}

    recognition.start();
}}

</script>

</body>
</html>
"""

# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, q: str = ""):

    db = SessionLocal()

    products = db.query(Product).all()

    if q:
        products = ai_search(q, products)

    product_html = ""

    for p in products:

        product_html += f"""

        <div class="card fade">

            <img src="{p.image}">

            <div class="card-body">

                <h2>{p.title}</h2>

                <p>{p.description}</p>

                <div class="price">${p.price}</div>

                <button>Add To Cart</button>

            </div>

        </div>
        """

    content = f"""

    <div class="search-box">

        <form id="searchForm">

            <input
                id="search"
                name="q"
                placeholder="Search products intelligently..."
                value="{q}"
            >

        </form>

        <button onclick="voiceSearch()">
        🎤 Voice Search
        </button>

    </div>

    <div class="grid">
        {product_html}
    </div>
    """

    return render_page(content)

# ============================================================
# AUTHENTICATION
# ============================================================

@app.post("/signup")
async def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = User(
        name=name,
        email=email,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()

    return {"message": "User created"}

@app.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(401)

    if not verify_password(password, user.password):
        raise HTTPException(401)

    token = create_jwt({
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=1)
    })

    return {"token": token}

# ============================================================
# API SYSTEM
# ============================================================

@app.get("/api/products")
async def api_products():

    db = SessionLocal()

    products = db.query(Product).all()

    return [
        {
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "rating": p.rating,
            "stock": p.stock
        }
        for p in products
    ]

# ============================================================
# SITEMAP
# ============================================================

@app.get("/sitemap.xml")
async def sitemap():

    xml = """
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>http://127.0.0.1:8000/</loc>
        </url>
    </urlset>
    """

    return HTMLResponse(xml)

# ============================================================
# ROBOTS
# ============================================================

@app.get("/robots.txt")
async def robots():

    return HTMLResponse("""

User-agent: *
Allow: /

Sitemap: http://127.0.0.1:8000/sitemap.xml

""")

# ============================================================
# AI RECOMMENDATION ENGINE
# ============================================================

def recommend_products(product_id):

    db = SessionLocal()

    current = db.query(Product).filter(
        Product.id == product_id
    ).first()

    products = db.query(Product).filter(
        Product.category == current.category
    ).all()

    return products[:4]

# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():

    db = SessionLocal()

    total_products = db.query(Product).count()
    total_users = db.query(User).count()

    html = f"""

    <h1>Admin Dashboard</h1>

    <br>

    <div class="grid">

        <div class="card">
            <div class="card-body">
                <h2>Total Products</h2>
                <div class="price">
                    {total_products}
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-body">
                <h2>Total Users</h2>
                <div class="price">
                    {total_users}
                </div>
            </div>
        </div>

    </div>
    """

    return render_page(html)

# ============================================================
# MULTILINGUAL
# ============================================================

LANG = {

    "en": {
        "welcome": "Welcome"
    },

    "bn": {
        "welcome": "স্বাগতম"
    }

}

# ============================================================
# LIVE NOTIFICATION SYSTEM
# ============================================================

notifications = []

@app.get("/notifications")
async def get_notifications():
    return notifications

# ============================================================
# AI CHATBOT
# ============================================================

@app.post("/chatbot")
async def chatbot(message: str = Form(...)):

    response = f"""
    AI Assistant Response:
    You asked -> {message}
    """

    return {"response": response}

# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )