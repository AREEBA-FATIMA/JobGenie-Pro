import streamlit as st
from streamlit.components.v1 import html
from PIL import Image
import base64
from io import BytesIO
from pathlib import Path

class Navbar:
    def __init__(self, role="job_seeker", is_signed_in=False):
        self.role = role
        self.is_signed_in = is_signed_in
        self.logo_base64 = self._convert_image_to_base64("jobgenie-logo.png")  # ✅ Correct string

    def _convert_image_to_base64(self, image_path: str) -> str:
        """Convert image to base64 for HTML embedding"""
        try:
            img_path = Path(image_path)
            if img_path.exists():
                img = Image.open(img_path)
                img = img.resize((32, 32))  # Resize logo
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                return base64.b64encode(buffered.getvalue()).decode()
            else:
                print(f"Image not found at path: {image_path}")
            return ""
        except Exception as e:
            print("Error loading image:", e)
            return ""

    def _generate_nav_links(self) -> str:
        """Generate navigation links based on user role"""
        if self.role == "job_seeker":
            return """
            <div class='nav-links'>
                <a href="/" onclick="handleNavClick(event)">Home</a>
                <a href="/jobs" onclick="handleNavClick(event)">Browse Jobs</a>
                <a href="/dashboard" onclick="handleNavClick(event)">My Applications</a>
            </div>
            """
        return ""

    def _generate_auth_buttons(self) -> str:
        """Generate authentication buttons based on login status"""
        if not self.is_signed_in:
            return """
            <a href="/become-employer" onclick="handleNavClick(event)" style="font-size: 0.9rem; color: #6B7280;">Become an Employer</a>
            <button class="btn btn-signin" onclick="handleButtonClick('signin')">Sign In</button>
            <button class="btn btn-register" onclick="handleButtonClick('register')">Register</button>
            """
        return """
        <button class="btn btn-signin" onclick="handleButtonClick('signout')">Sign Out</button>
        """

    def _get_css(self) -> str:
        """Return CSS styles for the navbar"""
        return """
        <style>
            .nav-container {
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                padding: 1rem 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: sticky;
                top: 0;
                z-index: 1000;
            }
            .nav-brand {
                font-size: 1.5rem;
                font-weight: bolder;
                color: #4F46E5;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                text-decoration: none;
            }
            .nav-links {
                display: flex;
                gap: 1.5rem;
            }
            .nav-links a {
                color: #374151;
                text-decoration: none;
                font-weight: 500;
            }
            .nav-links a:hover {
                color: #4F46E5;
            }
            .auth-buttons {
                display: flex;
                gap: 1rem;
                align-items: center;
            }
            .btn {
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 0.375rem;
                cursor: pointer;
                font-weight: 500;
            }
            .btn-signin {
                background: none;
                color: #374151;
            }
            .btn-signin:hover {
                color: #4F46E5;
            }
            .btn-register {
                background: #4F46E5;
                color: white;
            }
            .btn-register:hover {
                background: #4338CA;
            }
            .premium-banner {
                position: relative;
                z-index: 10;
                background-color: #1E3A8A;
                color: white;
                text-align: center;
                padding: 0.5rem 1rem;
                font-size: 0.875rem;
            }
            .premium-banner a {
                text-decoration: underline;
                color: white;
            }
            .logo-img {
                height: 32px;
                width: 32px;
                object-fit: contain;
            }
        </style>
        """

    def _get_js(self) -> str:
        """Return JavaScript for navigation handling"""
        return """
        <script>
        function handleNavClick(event) {
            event.preventDefault();
            const path = event.currentTarget.getAttribute('href');
            window.parent.postMessage({
                type: 'streamlit:navigate',
                path: path
            }, '*');
        }
        
        function handleButtonClick(action) {
            window.parent.postMessage({
                type: 'streamlit:buttonClick',
                action: action
            }, '*');
        }
        </script>
        """

    def render(self):
        """Render the navbar component"""
        logo_html = ""
        if self.logo_base64:
            logo_html = f'<img src="data:image/png;base64,{self.logo_base64}" class="logo-img" alt="JobGenie Logo">'

        html_content = f"""
        {self._get_css()}
        <div class="nav-container">
            <a href="/" class="nav-brand" onclick="handleNavClick(event)">
                {logo_html} JobGenie Pro
            </a>
            {self._generate_nav_links()}
            <div class="auth-buttons">
                {self._generate_auth_buttons()}
            </div>
        </div>
        <div class="premium-banner">
            🚀 Premium members get 3x more visibility | <a href="/pages/upgrade.py">Upgrade Now</a>
        </div>
        {self._get_js()}
        """

        html(html_content, height=140)

def main():
    st.set_page_config(page_title="JobGenie", layout="wide")

    # Initialize and render navbar
    navbar = Navbar(role="job_seeker", is_signed_in=False)
    navbar.render()

    # Page content
    st.title("Welcome to JobGenie")
    st.write("This is the main content of your application")

if __name__ == "__main__":
    main()
