import streamlit as st
from pages.navbar import Navbar
import stripe
import os
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple

@dataclass
class Plan:
    id: str
    name: str
    price: int
    features: List[str]
    highlight: bool = False
    popular: bool = False

@dataclass
class SuccessStory:
    name: str
    title: str
    quote: str
    rating: str
    initial: str

class PremiumUpgradeApp:
    def __init__(self):
        self.init_stripe()
        self.init_session_state()
        self.load_data()
        
    def init_stripe(self):
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        self.stripe_public_key = os.getenv("STRIPE_PUBLIC_KEY")

        
    def init_session_state(self):
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "premium"
        if 'selected_plan' not in st.session_state:
            st.session_state.selected_plan = None
            
    def load_data(self):
        self.plans = [
            Plan(
                id="basic",
                name="Basic",
                price=0,
                features=[
                    "5 Applications/month",
                    "Basic Job Listings",
                    "Application Tracker"
                ]
            ),
            Plan(
                id="premium_monthly",
                name="Premium",
                price=999,
                features=[
                    "Unlimited Applications",
                    "Premium Job Listings",
                    "Priority Applications",
                    "Resume Review"
                ],
                popular=True
            ),
            Plan(
                id="pro_monthly",
                name="Pro",
                price=1999,
                features=[
                    "All Premium Features",
                    "1-on-1 Career Coaching",
                    "Interview Preparation",
                    "LinkedIn Profile Makeover"
                ],
                highlight=True
            )
        ]
        
        self.features = [
            ("🔍 Exclusive Job Listings", "Access unpublished jobs from top companies before they're public"),
            ("⚡ Priority Applications", "Your applications appear first in recruiters' inboxes"),
            ("📈 Advanced Analytics", "Detailed dashboard tracking your application success rates"),
            ("👨‍💼 Career Coaching", "Monthly 1-on-1 sessions with industry experts"),
            ("📝 Smart Resume Builder", "ATS-optimized templates with real-time feedback"),
            ("💬 Direct Recruiter Access", "Message hiring managers directly through our platform")
        ]
        
        self.success_stories = [
            SuccessStory(
                name="Rahul Sharma",
                title="Senior Software Engineer at Microsoft",
                quote="Landing my dream job at Microsoft within 3 weeks of upgrading was unbelievable.",
                rating="★★★★★",
                initial="R"
            ),
            SuccessStory(
                name="Priya Patel",
                title="Marketing Director",
                quote="My application response rate tripled after using the resume review service.",
                rating="★★★★★",
                initial="P"
            ),
            SuccessStory(
                name="Amit Kumar",
                title="Product Manager",
                quote="Negotiation coaching helped me secure a 40% higher salary. Worth every penny!",
                rating="★★★★☆",
                initial="A"
            ),
            SuccessStory(
                name="Sneha Gupta",
                title="UX Designer",
                quote="Recruiters started reaching out to *me*! Priority applications are magical.",
                rating="★★★★★",
                initial="S"
            ),
            SuccessStory(
                name="Vikram Singh",
                title="Data Scientist",
                quote="Found opportunities at unicorn startups through exclusive listings.",
                rating="★★★★★",
                initial="V"
            ),
            SuccessStory(
                name="Neha Joshi",
                title="Financial Analyst",
                quote="From unemployed to 3 offers in 6 weeks. Interview prep changed everything!",
                rating="★★★★★",
                initial="N"
            )
        ]
    
    def run(self):
        self.setup_page()
        Navbar(role="job_seeker", is_signed_in=True)
        self.inject_styles()
        self.handle_routing()
    
    def setup_page(self):
        st.set_page_config(
            page_title="JobGenie - Upgrade to Premium",
            page_icon="💎",
            layout="wide"
        )
    
    def inject_styles(self):
        st.markdown("""
        <style>
            .main-container {
                padding: 0 2rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            .section-spacing { 
                margin: 3rem 0; 
            }
            .pricing-card {
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                background: white;
                transition: all 0.3s ease;
                border: 1px solid #f0f0f0;
            }
            .pricing-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            }
            .premium-feature {
                display: flex;
                align-items: center;
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
            }
            .check-icon {
                color: #4F46E5;
                margin-right: 0.5rem;
                font-size: 1rem;
            }
            .feature-item {
                padding: 1.25rem;
                background: white;
                border-radius: 8px;
                margin-bottom: 1rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                border-left: 4px solid #4F46E5;
                transition: all 0.3s ease;
            }
            .feature-item:hover {
                transform: translateX(5px);
            }
            .story-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 1.5rem;
                justify-content: center;
            }
            .story-card {
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                max-width: 100%;
                flex: 1 1 calc(33.333% - 1.5rem);
                transition: all 0.3s ease;
                position: relative;
            }
            .story-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            }
            .story-header {
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
            }
            .profile-icon {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: #4F46E5;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                font-weight: bold;
                margin-right: 1rem;
            }
            .user-name { 
                font-weight: 600; 
                margin: 0; 
                color: #333; 
            }
            .user-title { 
                font-size: 0.8rem; 
                color: #666; 
                margin: 0.2rem 0 0 0; 
            }
            .story-content {
                font-style: italic;
                color: #444;
                line-height: 1.6;
                margin-bottom: 1rem;
            }
            .rating {
                color: #F59E0B;
                font-size: 0.9rem;
                margin-top: 0.5rem;
            }
            .stButton>button {
                border: none;
                padding: 0.7rem 1.2rem;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                margin-top: 1rem;
                font-size: 0.9rem;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(79, 70, 229, 0.3);
            }
            .stButton>button:disabled {
                background: #E5E7EB !important;
                color: #333 !important;
            }
            .payment-processing {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 2rem;
                text-align: center;
            }
            .payment-button {
                background: #4F46E5;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                font-size: 1rem;
                margin-top: 1rem;
                transition: all 0.3s ease;
                width: 100%;
            }
            .payment-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(79, 70, 229, 0.3);
            }
            .spinner {
                border: 4px solid rgba(0, 0, 0, 0.1);
                width: 36px;
                height: 36px;
                border-radius: 50%;
                border-left-color: #4F46E5;
                animation: spin 1s linear infinite;
                margin-bottom: 1rem;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @media (max-width: 1024px) {
                .story-card {
                    flex: 1 1 calc(50% - 1.5rem);
                }
            }
            @media (max-width: 768px) {
                .story-card {
                    flex: 1 1 100%;
                }
            }
        </style>
        """, unsafe_allow_html=True)
    
    def handle_routing(self):
        if "page" in st.query_params:
            st.session_state.current_page = st.query_params["page"]
            
        if st.session_state.current_page == "premium":
            self.show_premium_page()
        elif st.session_state.current_page == "payment":
            self.show_payment_page()
        elif st.session_state.current_page == "confirmation":
            self.show_confirmation_page()
    
    def navigate_to(self, page: str):
        st.session_state.current_page = page
        st.rerun()
    
    def show_premium_page(self):
        self.render_hero_section()
        self.render_pricing_section()
        self.render_features_section()
        self.render_testimonials_section()
    
    def render_hero_section(self):
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">🚀 Unlock Premium Features</h1>
            <p style="font-size: 1.1rem; color: #666; max-width: 700px; margin: 0 auto;">
                Take your job search to the next level with our exclusive benefits and tools.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_pricing_section(self):
        st.markdown("### Choose Your Plan")
        cols = st.columns(3)
        
        for idx, plan in enumerate(self.plans):
            with cols[idx]:
                self.render_plan_card(plan)
    
    def render_plan_card(self, plan: Plan):
        border_style = ""
        if plan.popular:
            border_style = "border: 2px solid #4F46E5;"
        elif plan.highlight:
            border_style = "border: 1px solid #F59E0B;"
        
        features_html = "\n".join(
            f'<div class="premium-feature"><span class="check-icon">✓</span> {feature}</div>'
            for feature in plan.features
        )
        
        price_display = "Free" if plan.price == 0 else f"Rs. {plan.price}/month"
        description = (
            "Essential job search features" if plan.price == 0 else
            "Best for serious job seekers" if plan.popular else
            "Complete career package"
        )
        
        st.markdown(f"""
        <div class="pricing-card" style="{border_style}">
            <h3>{plan.name}</h3>
            <h2>{price_display}</h2>
            <p style="color: #666;">{description}</p>
            <div>{features_html}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if plan.price == 0:
            st.button("Current Plan", disabled=True)
        else:
            button_text = "Upgrade Now" if not plan.highlight else "Go Pro"
            if st.button(button_text, type="primary", key=f"{plan.id}_upgrade"):
                st.session_state.selected_plan = {
                    "id": plan.id,
                    "name": plan.name,
                    "amount": plan.price
                }
                self.navigate_to("payment")
    
    def render_features_section(self):
        st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
        st.markdown("## ✨ Premium Benefits")
        
        cols = st.columns(2)
        for i, (title, desc) in enumerate(self.features):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="feature-item">
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def render_testimonials_section(self):
        st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
        st.markdown("## 💬 What Our Members Say")
        st.markdown(
            '<div style="text-align: center; margin-bottom: 1.5rem; color: #666;">'
            'Real success stories from JobGenie Premium users</div>',
            unsafe_allow_html=True
        )
        
        st.markdown('<div class="story-grid">', unsafe_allow_html=True)
        for story in self.success_stories:
            st.markdown(f"""
            <div class="story-card">
                <div class="story-header">
                    <div class="profile-icon">{story.initial}</div>
                    <div>
                        <div class="user-name">{story.name}</div>
                        <div class="user-title">{story.title}</div>
                    </div>
                </div>
                <div class="story-content">{story.quote}</div>
                <div class="rating">{story.rating}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def show_payment_page(self):
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">💳 Payment Information</h1>
            <p style="font-size: 1.1rem; color: #666; max-width: 700px; margin: 0 auto;">
                Complete your premium upgrade with secure payment
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.selected_plan:
            st.warning("No plan selected. Redirecting to plans page...")
            self.navigate_to("premium")
            return
            
        st.info(
            f"You're subscribing to: **{st.session_state.selected_plan['name']} Plan** "
            f"(₹{st.session_state.selected_plan['amount']}/month)"
        )
        
        st.markdown("### Secure Payment")
        
        with st.spinner("Preparing secure checkout..."):
            checkout_url = self.create_stripe_session(
                st.session_state.selected_plan['id'],
                st.session_state.selected_plan['name'],
                st.session_state.selected_plan['amount']
            )
            
            if checkout_url:
                st.markdown(f"""
                <div class="payment-processing">
                    <p>You'll be redirected to Stripe's secure payment page</p>
                    <a href="{checkout_url}" target="_self">
                        <button class="payment-button">
                            Complete Payment Now
                        </button>
                    </a>
                    <p style="margin-top: 1rem; color: #666; font-size: 0.9rem;">
                        <i class="fas fa-lock"></i> 256-bit SSL secured payment
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button("← Back to Plans", key="back_to_plans"):
                    self.navigate_to("premium")
    
    def create_stripe_session(self, plan_id: str, plan_name: str, amount: int) -> Optional[str]:
        try:
            current_url = st.query_params.get("_st", {}).get("base_url", "http://localhost:8501")
            
            success_url = (
                f"{current_url}?page=confirmation" 
                if current_url.startswith(('http://', 'https://')) 
                else f"http://localhost:8501?page=confirmation"
            )
            cancel_url = (
                f"{current_url}?page=premium" 
                if current_url.startswith(('http://', 'https://')) 
                else f"http://localhost:8501?page=premium"
            )
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f'JobGenie {plan_name} Plan',
                        },
                        'unit_amount': amount * 100,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "plan_id": plan_id,
                    "plan_name": plan_name
                }
            )
            return session.url
        except stripe.error.StripeError as e:
            st.error(f"Payment Error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"System Error: {str(e)}")
            return None
    
    def show_confirmation_page(self):
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">🎉 Upgrade Successful!</h1>
            <p style="font-size: 1.1rem; color: #666; max-width: 700px; margin: 0 auto;">
                Thank you for upgrading to JobGenie Premium. Your account has been activated.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("""
            <div style="background: #F0F9FF; padding: 1.5rem; border-radius: 12px; margin-top: 2rem;">
                <h3 style="color: #4F46E5; margin-bottom: 1rem;">What's Next?</h3>
                <div style="text-align: left;">
                    <p>✔ Access premium features immediately</p>
                    <p>✔ Check your email for receipt</p>
                    <p>✔ Explore your new dashboard</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Go to Dashboard", type="primary"):
            self.navigate_to("home")

if __name__ == "__main__":
    app = PremiumUpgradeApp()
    app.run()