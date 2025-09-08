// Theme Management
class ThemeManager {
    constructor() {
        this.themeToggle = document.getElementById('themeToggle');
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Set initial theme
        this.setTheme(this.currentTheme);
        
        // Add event listener for theme toggle
        this.themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    setTheme(theme) {
        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update toggle button aria-label
        this.themeToggle.setAttribute('aria-label', 
            theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme'
        );
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }
}

// Smooth Scrolling Navigation
class SmoothNavigation {
    constructor() {
        this.navLinks = document.querySelectorAll('.nav-links a[href^="#"]');
        this.sections = document.querySelectorAll('section[id]');
        this.init();
    }

    init() {
        // Add click listeners to navigation links
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetSection = document.getElementById(targetId);
                
                if (targetSection) {
                    this.scrollToSection(targetSection);
                }
            });
        });

        // Add scroll spy functionality
        window.addEventListener('scroll', () => {
            this.updateActiveNavLink();
        });
    }

    scrollToSection(section) {
        const navHeight = document.querySelector('.nav').offsetHeight;
        const targetPosition = section.offsetTop - navHeight - 20;
        
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }

    updateActiveNavLink() {
        const scrollPosition = window.scrollY + 100;
        
        this.sections.forEach((section, index) => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                // Remove active class from all nav links
                this.navLinks.forEach(link => {
                    link.classList.remove('active');
                });
                
                // Add active class to current nav link
                const activeLink = document.querySelector(`.nav-links a[href="#${sectionId}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    }
}

// Intersection Observer for Animations
class AnimationObserver {
    constructor() {
        this.observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        this.init();
    }

    init() {
        // Create intersection observer
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, this.observerOptions);

        // Observe elements for animation
        const animatedElements = document.querySelectorAll(`
            .timeline-item,
            .research-card,
            .skill-category,
            .publication-item,
            .contact-item,
            .stat
        `);

        animatedElements.forEach(el => {
            el.classList.add('animate-on-scroll');
            this.observer.observe(el);
        });
    }
}

// Mobile Navigation
class MobileNavigation {
    constructor() {
        this.nav = document.querySelector('.nav');
        this.navContainer = document.querySelector('.nav-container');
        this.init();
    }

    init() {
        // Create mobile menu button if screen is small
        if (window.innerWidth <= 768) {
            this.createMobileMenu();
        }

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth <= 768 && !this.mobileMenuExists()) {
                this.createMobileMenu();
            } else if (window.innerWidth > 768 && this.mobileMenuExists()) {
                this.removeMobileMenu();
            }
        });
    }

    mobileMenuExists() {
        return document.querySelector('.mobile-menu-btn') !== null;
    }

    createMobileMenu() {
        // Create mobile menu button
        const mobileMenuBtn = document.createElement('button');
        mobileMenuBtn.className = 'mobile-menu-btn';
        mobileMenuBtn.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        mobileMenuBtn.setAttribute('aria-label', 'Toggle navigation menu');

        // Create mobile menu overlay
        const mobileMenu = document.createElement('div');
        mobileMenu.className = 'mobile-menu';
        
        const navLinks = document.querySelector('.nav-links');
        const mobileNavLinks = navLinks.cloneNode(true);
        mobileNavLinks.className = 'mobile-nav-links';
        mobileMenu.appendChild(mobileNavLinks);

        // Add to DOM
        this.navContainer.appendChild(mobileMenuBtn);
        document.body.appendChild(mobileMenu);

        // Add event listeners
        mobileMenuBtn.addEventListener('click', () => {
            this.toggleMobileMenu();
        });

        // Close menu when link is clicked
        mobileNavLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                this.closeMobileMenu();
            });
        });

        // Close menu when clicking outside
        mobileMenu.addEventListener('click', (e) => {
            if (e.target === mobileMenu) {
                this.closeMobileMenu();
            }
        });
    }

    removeMobileMenu() {
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const mobileMenu = document.querySelector('.mobile-menu');
        
        if (mobileMenuBtn) mobileMenuBtn.remove();
        if (mobileMenu) mobileMenu.remove();
    }

    toggleMobileMenu() {
        const mobileMenu = document.querySelector('.mobile-menu');
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        
        mobileMenu.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
        document.body.classList.toggle('menu-open');
    }

    closeMobileMenu() {
        const mobileMenu = document.querySelector('.mobile-menu');
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        
        mobileMenu.classList.remove('active');
        mobileMenuBtn.classList.remove('active');
        document.body.classList.remove('menu-open');
    }
}

// Performance Optimization
class PerformanceOptimizer {
    constructor() {
        this.init();
    }

    init() {
        // Lazy load images when they exist
        this.lazyLoadImages();
        
        // Optimize scroll events with throttling
        this.optimizeScrollEvents();
    }

    lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    optimizeScrollEvents() {
        let ticking = false;

        const updateOnScroll = () => {
            // Update navbar background based on scroll position
            const nav = document.querySelector('.nav');
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
            ticking = false;
        };

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateOnScroll);
                ticking = true;
            }
        });
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all components
    new ThemeManager();
    new SmoothNavigation();
    new AnimationObserver();
    new MobileNavigation();
    new PerformanceOptimizer();

    // Add loading animation end
    document.body.classList.add('loaded');
});

// Add CSS for animations and mobile menu
const additionalStyles = `
<style>
/* Animation styles */
.animate-on-scroll {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.6s ease;
}

.animate-in {
    opacity: 1;
    transform: translateY(0);
}

.loaded {
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Mobile menu styles */
.mobile-menu-btn {
    display: none;
    flex-direction: column;
    justify-content: space-around;
    width: 30px;
    height: 30px;
    background: transparent;
    border: none;
    cursor: pointer;
    z-index: 1001;
}

.mobile-menu-btn span {
    width: 100%;
    height: 3px;
    background: var(--text-primary);
    border-radius: 2px;
    transition: all 0.3s ease;
}

.mobile-menu-btn.active span:nth-child(1) {
    transform: rotate(45deg) translate(8px, 8px);
}

.mobile-menu-btn.active span:nth-child(2) {
    opacity: 0;
}

.mobile-menu-btn.active span:nth-child(3) {
    transform: rotate(-45deg) translate(8px, -8px);
}

.mobile-menu {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
}

.mobile-menu.active {
    opacity: 1;
    visibility: visible;
}

.mobile-nav-links {
    display: flex;
    flex-direction: column;
    gap: 32px;
    text-align: center;
}

.mobile-nav-links a {
    color: white;
    font-size: 1.5rem;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.3s ease;
}

.mobile-nav-links a:hover {
    color: var(--accent-primary);
}

.menu-open {
    overflow: hidden;
}

/* Navbar scroll effect */
.nav.scrolled {
    background: var(--glass-bg);
    box-shadow: 0 2px 20px var(--shadow-light);
}

/* Active nav link style */
.nav-links a.active {
    color: var(--accent-primary);
}

.nav-links a.active::after {
    width: 100%;
}

@media (max-width: 768px) {
    .mobile-menu-btn {
        display: flex;
    }
}
</style>
`;

// Inject additional styles
document.head.insertAdjacentHTML('beforeend', additionalStyles);