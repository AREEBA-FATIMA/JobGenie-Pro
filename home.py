import streamlit as st
from pages.navbar import show_navbar
from dataclasses import dataclass
from typing import List
from PIL import Image
import base64
from io import BytesIO
from pathlib import Path

@dataclass
class Feature:
    emoji: str
    title: str
    description: str

class JobGenieHomePage:
    def __init__(self):
        self.setup_page_config()
        self.load_assets()
        
    def setup_page_config(self):
        # Convert image to base64 for page icon
        img_path = Path("jobgenie-logo.png")  # Replace with your image path
        if img_path.exists():
            img = Image.open(img_path)
            img = img.resize((32, 32))  # Standard icon size
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            page_icon = f"data:image/png;base64,{img_str}"
        else:
            page_icon = "💼"  # Fallback to emoji if image not found

        st.set_page_config(
            page_title="JobGenie - Find Your Dream Job",
            page_icon=page_icon,
            layout="wide"
        )
    
    def load_assets(self):
        self.features = [
            Feature("💼", "Application Tracker", 
                   "Manage all your job applications in one place with real-time status updates."),
            Feature("💰", "Premium Listings", 
                   "Access high-quality jobs from top companies that value talent."),
            Feature("📊", "Smart Analytics", 
                   "Get insights on your application performance and improvement areas.")
        ]
    
    def inject_css(self):
        st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                padding: 0 !important;
                margin: 0 !important;
            }
            [data-testid="stSidebar"] {
                padding: 0 !important;
                margin: 0 !important;
            }

            @keyframes blob {
                0% { transform: translate(0px, 0px) scale(1); }
                33% { transform: translate(30px, -50px) scale(1.1); }
                66% { transform: translate(-20px, 20px) scale(0.9); }
                100% { transform: translate(0px, 0px) scale(1); }
            }
            @keyframes gradient-x {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            .floating-circles {
                position: fixed; top: 0; left: 0;
                width: 100%; height: 100%;
                overflow: hidden; z-index: -1;
            }
            .circle-1, .circle-2, .circle-3 {
                position: absolute; width: 16rem; height: 16rem;
                border-radius: 50%; mix-blend-mode: multiply;
                filter: blur(60px); opacity: 0.3;
                animation: blob 7s infinite;
            }
            .circle-1 { top: 20%; left: 10%; background-color: #C7D2FE; }
            .circle-2 { top: 40%; right: 20%; background-color: #BFDBFE; animation-delay: 2s; }
            .circle-3 { bottom: 20%; left: 50%; background-color: #DDD6FE; animation-delay: 4s; }

            .hero-container {
                text-align: center;
                padding: 5rem 2rem;
            }
            .gradient-text {
                background: linear-gradient(to right, #4F46E5, #2563EB);
                -webkit-background-clip: text;
                color: transparent;
                animation: gradient-x 3s ease infinite;
            }

            .search-bar-container {
                max-width: 42rem; 
                margin: 0 auto 3rem auto;
                padding: 0 1rem;
            }
            .search-bar-wrapper {
                display: flex;
                box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
                border-radius: 0.75rem; 
                overflow: hidden;
            }
            .search-input {
                flex-grow: 1;
                padding: 1rem 1.5rem;
                border: none;
                font-size: 1rem;
                outline: none;
            }
            .search-button {
                background-color: #4F46E5;
                color: white;
                border: none;
                padding: 1rem 1.5rem;
                font-weight: 500;
                cursor: pointer;
            }
            .search-button:hover {
                background-color: #4338CA;
            }

            .features-section {
                margin: 4rem auto;
                max-width: 80rem;
                padding: 0 2rem;
            }

            .feature-card {
                background: white;
                padding: 1.5rem;
                border-radius: 0.75rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                border: 1px solid #E5E7EB;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            }

            .premium-cta {
                background: #EEF2FF;
                padding: 3rem 2rem;
                border-radius: 0.75rem;
                border: 1px solid #C7D2FE;
                text-align: center;
                max-width: 60rem;
                margin: 3rem auto;
            }
            .premium-button {
                background: #4F46E5;
                color: white;
                padding: 0.75rem 1.5rem;
                border-radius: 0.5rem;
                border: none;
                cursor: pointer;
            }
            .premium-button:hover {
                background: #4338CA;
            }
        </style>

        <div class="floating-circles">
            <div class="circle-1"></div>
            <div class="circle-2"></div>
            <div class="circle-3"></div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_hero_section(self):
        st.markdown("""
        <div class="hero-container">
            <h1 style='font-size: 2.5rem; font-weight: 700; margin: 0;'>
                Find Your <span class="gradient-text">Dream Job</span> Faster
            </h1>
            <p style='font-size: 1.25rem; color: #4B5563; margin-top: 1rem;'>
                Track applications, discover premium listings, and get hired with our smart job matching system.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_search_bar(self):
        st.markdown("""
        <div class="search-bar-container">
            <form action="/" method="get">
                <div class="search-bar-wrapper">
                    <input class="search-input" name="search" type="text" placeholder="Job title, company, or keywords" />
                    <button class="search-button" type="submit">Search</button>
                </div>
            </form>
        </div>
        """, unsafe_allow_html=True)
    
    def render_features(self):
        st.markdown('<div class="features-section">', unsafe_allow_html=True)
        
        # Create feature cards
        cols = st.columns(3)
        for i, feature in enumerate(self.features):
            with cols[i]:
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature.emoji}</div>
                    <h3 style='font-weight: 600; margin: 0 0 0.5rem 0;'>{feature.title}</h3>
                    <p style="margin: 0;">{feature.description}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_premium_cta(self):
        st.markdown("""
        <div class="premium-cta">
            <h2 style='font-size: 1.5rem; font-weight: 700; margin: 0 0 1rem 0;'>Upgrade to Premium</h2>
            <p style='max-width: 40rem; margin: auto auto 1.5rem auto;'>Unlock exclusive job listings, priority applications, and personalized career coaching.</p>
            <button class="premium-button">Explore Premium Features</button>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        self.inject_css()
        show_navbar(role="job_seeker", is_signed_in=False)
        self.render_hero_section()
        self.render_search_bar()
        self.render_features()
        self.render_premium_cta()

# Main execution
if __name__ == "__main__":
    app = JobGenieHomePage()
    app.run()