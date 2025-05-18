# footer.py
import streamlit as st
from streamlit.components.v1 import html

def show_footer():
    footer_html = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #6c757d;
            text-align: center;
            padding: 1rem 0;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
        }
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }
        .footer-links {
            display: flex;
            gap: 1.5rem;
        }
        .footer-links a {
            color: #6c757d;
            text-decoration: none;
            transition: color 0.3s;
        }
        .footer-links a:hover {
            color: #4F46E5;
        }
        .footer-copyright {
            font-size: 0.9rem;
        }
        @media (max-width: 768px) {
            .footer-content {
                flex-direction: column;
                gap: 1rem;
                padding: 1rem;
            }
            .footer-links {
                flex-wrap: wrap;
                justify-content: center;
            }
        }
    </style>

    <footer class="footer">
        <div class="footer-content">
            <div class="footer-copyright">
                © 2023 JobGenie Pro. All rights reserved.
            </div>
            <div class="footer-links">
                <a href="/privacy" onclick="handleNavClick(event)">Privacy Policy</a>
                <a href="/terms" onclick="handleNavClick(event)">Terms of Service</a>
                <a href="/contact" onclick="handleNavClick(event)">Contact Us</a>
                <a href="/help" onclick="handleNavClick(event)">Help Center</a>
            </div>
        </div>
    </footer>

    <script>
    function handleNavClick(event) {
        event.preventDefault();
        const path = event.currentTarget.getAttribute('href');
        window.parent.postMessage({
            type: 'streamlit:navigate',
            path: path
        }, '*');
    }
    </script>
    """
    
    html(footer_html, height=80)