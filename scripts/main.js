// Modern JavaScript for Haghmoradi.com - Enhanced Version
class HaghmoradiWebsite {
    constructor() {
        this.isLoading = false;
        this.animations = new Map();
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupHeroAnimations();
        this.setupScrollEffects();
        this.setupCounterAnimations();
        this.setupIntersectionObserver();
        this.setupSmoothScrolling();
        this.setupContactInteractions();
        this.setupPortfolioHovers();
        this.setupParallaxEffects();
        this.setupThemeSystem();
        this.setupPerformanceMonitoring();
    }

    // Enhanced Navigation with Apple-style interactions
    setupNavigation() {
        const navToggle = document.getElementById('nav-toggle');
        const navMenu = document.getElementById('nav-menu');
        const navLinks = document.querySelectorAll('.nav-link');
        const nav = document.querySelector('.nav');

        // Mobile menu toggle with smooth animation
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                navToggle.classList.toggle('active');
                
                // Add ripple effect
                this.createRippleEffect(navToggle);
            });

            // Close menu when clicking on a link
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    navMenu.classList.remove('active');
                    navToggle.classList.remove('active');
                });
            });
        }

        // Enhanced navbar scroll effect with blur
        let lastScrollY = window.scrollY;
        window.addEventListener('scroll', this.throttle(() => {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 100) {
                nav.classList.add('scrolled');
                nav.style.transform = currentScrollY > lastScrollY ? 
                    'translateY(-100%)' : 'translateY(0)';
            } else {
                nav.classList.remove('scrolled');
                nav.style.transform = 'translateY(0)';
            }
            
            lastScrollY = currentScrollY;
        }, 100));

        // Active navigation link with smooth indicator
        this.updateActiveNavLink();
        window.addEventListener('scroll', this.throttle(() => {
            this.updateActiveNavLink();
        }, 100));

        // Add hover sound effect (optional)
        navLinks.forEach(link => {
            link.addEventListener('mouseenter', () => {
                this.playHoverSound();
            });
        });
    }

    updateActiveNavLink() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');
        
        let currentSection = '';
        const scrollPosition = window.scrollY + 150;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }

    // Hero section animations with advanced effects
    setupHeroAnimations() {
        // Animated typing effect for hero title
        this.typewriterEffect();
        
        // Staggered animation for hero elements
        this.animateHeroElements();
        
        // Profile image hover effects
        this.setupProfileImageEffects();
        
        // Scroll indicator animation
        this.setupScrollIndicator();
    }

    typewriterEffect() {
        const titleElement = document.querySelector('.hero-title');
        if (!titleElement) return;

        const text = titleElement.textContent;
        const words = text.split(' ');
        
        titleElement.innerHTML = '';
        
        words.forEach((word, index) => {
            const wordSpan = document.createElement('span');
            wordSpan.style.opacity = '0';
            wordSpan.style.transform = 'translateY(20px)';
            wordSpan.style.transition = `all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) ${index * 0.1}s`;
            
            if (word.includes('Visionary') || word.includes('Minds')) {
                wordSpan.className = 'gradient-text';
            }
            
            wordSpan.textContent = word + ' ';
            titleElement.appendChild(wordSpan);
            
            // Trigger animation
            setTimeout(() => {
                wordSpan.style.opacity = '1';
                wordSpan.style.transform = 'translateY(0)';
            }, 100 + index * 100);
        });
    }

    animateHeroElements() {
        const elements = [
            '.hero-badge',
            '.hero-subtitle',
            '.hero-stats',
            '.hero-cta'
        ];

        elements.forEach((selector, index) => {
            const element = document.querySelector(selector);
            if (element) {
                element.style.opacity = '0';
                element.style.transform = 'translateY(30px)';
                element.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                
                setTimeout(() => {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, 800 + index * 200);
            }
        });
    }

    setupProfileImageEffects() {
        const profileImage = document.querySelector('.profile-image');
        if (!profileImage) return;

        // Mouse move parallax effect
        profileImage.addEventListener('mousemove', (e) => {
            const rect = profileImage.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            
            const photo = profileImage.querySelector('.profile-photo');
            const glow = profileImage.querySelector('.image-glow');
            
            photo.style.transform = `scale(1.05) translate(${x * 10}px, ${y * 10}px)`;
            glow.style.transform = `scale(1.1) translate(${x * 15}px, ${y * 15}px)`;
        });

        profileImage.addEventListener('mouseleave', () => {
            const photo = profileImage.querySelector('.profile-photo');
            const glow = profileImage.querySelector('.image-glow');
            
            photo.style.transform = 'scale(1) translate(0, 0)';
            glow.style.transform = 'scale(1) translate(0, 0)';
        });
    }

    setupScrollIndicator() {
        const scrollIndicator = document.querySelector('.hero-scroll-indicator');
        if (!scrollIndicator) return;

        scrollIndicator.addEventListener('click', () => {
            const aboutSection = document.getElementById('about');
            if (aboutSection) {
                aboutSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });

        // Hide scroll indicator when scrolling
        window.addEventListener('scroll', () => {
            const opacity = Math.max(0, 1 - window.scrollY / 200);
            scrollIndicator.style.opacity = opacity;
        });
    }

    // Advanced scroll effects and parallax
    setupScrollEffects() {
        // Parallax effect for floating shapes
        window.addEventListener('scroll', this.throttle(() => {
            const scrolled = window.pageYOffset;
            const shapes = document.querySelectorAll('.shape');
            
            shapes.forEach((shape, index) => {
                const speed = 0.2 + (index * 0.1);
                const yPos = -(scrolled * speed);
                const rotation = scrolled * 0.05 * (index % 2 === 0 ? 1 : -1);
                
                shape.style.transform = `
                    translateY(${yPos}px) 
                    rotate(${rotation}deg) 
                    scale(${1 + Math.sin(scrolled * 0.01 + index) * 0.1})
                `;
            });

            // Orbit animation speed based on scroll
            const orbits = document.querySelectorAll('.orbit');
            orbits.forEach((orbit, index) => {
                const rotationSpeed = 1 + scrolled * 0.01;
                orbit.style.animationDuration = `${30 + index * 10}s`;
            });
        }, 16));
    }

    // Counter animations with intersection observer
    setupCounterAnimations() {
        const counters = document.querySelectorAll('[data-count]');
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            let hasAnimated = false;
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !hasAnimated) {
                        hasAnimated = true;
                        this.animateCounter(counter, target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });
            
            observer.observe(counter);
        });
    }

    animateCounter(element, target) {
        const duration = 2000;
        const steps = 60;
        const stepValue = target / steps;
        const stepTime = duration / steps;
        let current = 0;
        
        const timer = setInterval(() => {
            current += stepValue;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, stepTime);
    }

    // Intersection Observer for animations
    setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                    
                    // Stagger animations for child elements
                    const children = entry.target.querySelectorAll('.feature-card, .portfolio-item, .insight-card, .project-item');
                    children.forEach((child, index) => {
                        setTimeout(() => {
                            child.classList.add('fade-in-up');
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);

        // Observe elements for animation
        const animateElements = document.querySelectorAll(`
            .section-header,
            .about-grid,
            .portfolio-grid,
            .research-category,
            .insights-grid,
            .contact-content,
            .philosophy-section
        `);
        
        animateElements.forEach(el => observer.observe(el));
    }

    // Enhanced smooth scrolling
    setupSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - 100;
                    
                    // Add loading state
                    this.setLoadingState(true);
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                    
                    // Remove loading state after scroll
                    setTimeout(() => {
                        this.setLoadingState(false);
                    }, 1000);
                }
            });
        });
    }

    // Contact interactions
    setupContactInteractions() {
        const contactMethods = document.querySelectorAll('.contact-method');
        
        contactMethods.forEach(method => {
            method.addEventListener('click', (e) => {
                this.createRippleEffect(method, e);
                this.trackContactClick(method);
            });
            
            method.addEventListener('mouseenter', () => {
                this.playHoverSound();
            });
        });
    }

    // Portfolio hover effects
    setupPortfolioHovers() {
        const portfolioItems = document.querySelectorAll('.portfolio-item');
        
        portfolioItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                this.animatePortfolioItem(item, 'enter');
            });
            
            item.addEventListener('mouseleave', () => {
                this.animatePortfolioItem(item, 'leave');
            });
        });
    }

    animatePortfolioItem(item, action) {
        const image = item.querySelector('.portfolio-image img');
        const overlay = item.querySelector('.portfolio-overlay');
        
        if (action === 'enter') {
            image.style.transform = 'scale(1.1)';
            if (overlay) {
                overlay.style.opacity = '1';
                overlay.style.transform = 'translateY(0)';
            }
        } else {
            image.style.transform = 'scale(1)';
            if (overlay) {
                overlay.style.opacity = '0.8';
                overlay.style.transform = 'translateY(-10px)';
            }
        }
    }

    // Parallax effects
    setupParallaxEffects() {
        window.addEventListener('scroll', this.throttle(() => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            
            // Background parallax for sections
            const parallaxSections = document.querySelectorAll('.research, .portfolio');
            parallaxSections.forEach(section => {
                section.style.transform = `translateY(${rate * 0.1}px)`;
            });
        }, 16));
    }

    // Theme system (dark/light mode support)
    setupThemeSystem() {
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
        
        // Apply initial theme
        this.applyTheme(prefersDarkScheme.matches ? 'dark' : 'light');
        
        // Listen for theme changes
        prefersDarkScheme.addEventListener('change', (e) => {
            this.applyTheme(e.matches ? 'dark' : 'light');
        });
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        
        // Update meta theme-color
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', 
                theme === 'dark' ? '#000000' : '#FFFFFF'
            );
        }
    }

    // Performance monitoring
    setupPerformanceMonitoring() {
        // Monitor scroll performance
        let scrollStart = null;
        window.addEventListener('scroll', () => {
            if (!scrollStart) {
                scrollStart = performance.now();
            }
        });

        // Log performance metrics
        window.addEventListener('load', () => {
            if ('performance' in window) {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log(`Page loaded in ${perfData.loadEventEnd - perfData.loadEventStart}ms`);
                
                // Track largest contentful paint
                new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];
                    console.log('LCP:', lastEntry.startTime);
                }).observe({ entryTypes: ['largest-contentful-paint'] });
            }
        });
    }

    // Utility functions
    createRippleEffect(element, event = null) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        
        let x, y;
        if (event) {
            x = event.clientX - rect.left - size / 2;
            y = event.clientY - rect.top - size / 2;
        } else {
            x = rect.width / 2 - size / 2;
            y = rect.height / 2 - size / 2;
        }
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(0, 122, 255, 0.2);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.8s ease-out;
            pointer-events: none;
            z-index: 1000;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 800);
    }

    playHoverSound() {
        // Optional: Add subtle hover sound effect
        if ('AudioContext' in window) {
            try {
                const audioContext = new AudioContext();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
                gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
                
                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.1);
            } catch (e) {
                // Silently fail if audio context creation fails
            }
        }
    }

    setLoadingState(loading) {
        this.isLoading = loading;
        document.body.classList.toggle('loading', loading);
    }

    trackContactClick(element) {
        // Analytics tracking (replace with your analytics service)
        console.log('Contact method clicked:', element.textContent.trim());
    }

    // Performance optimization utilities
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    debounce(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    }

    // Public API methods
    scrollToSection(sectionId) {
        const element = document.getElementById(sectionId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(newTheme);
    }
}

// Enhanced CSS for additional animations
const enhancedStyles = `
    /* Navigation enhancements */
    .nav.scrolled {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        box-shadow: var(--shadow-lg);
    }
    
    @media (prefers-color-scheme: dark) {
        .nav.scrolled {
            background: rgba(28, 28, 30, 0.95);
        }
    }
    
    /* Mobile navigation */
    @media (max-width: 768px) {
        .nav-menu {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--surface);
            flex-direction: column;
            padding: var(--space-6);
            box-shadow: var(--shadow-xl);
            border-radius: 0 0 var(--radius-xl) var(--radius-xl);
            transform: translateY(-100%);
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            z-index: 1000;
        }
        
        .nav-menu.active {
            transform: translateY(0);
            opacity: 1;
            visibility: visible;
        }
        
        .nav-toggle.active .bar:nth-child(1) {
            transform: rotate(45deg) translate(5px, 5px);
        }
        
        .nav-toggle.active .bar:nth-child(2) {
            opacity: 0;
        }
        
        .nav-toggle.active .bar:nth-child(3) {
            transform: rotate(-45deg) translate(7px, -6px);
        }
    }
    
    /* Ripple animation */
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    /* Loading state */
    .loading {
        cursor: wait;
    }
    
    .loading * {
        pointer-events: none;
    }
    
    /* Enhanced hover effects */
    .portfolio-item {
        transform-origin: center;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .portfolio-item:hover {
        transform: translateY(-8px) scale(1.02);
    }
    
    /* Smooth focus transitions */
    *:focus {
        transition: all 0.2s ease-out;
    }
    
    /* Text selection improvements */
    ::selection {
        background: var(--primary-color);
        color: white;
        text-shadow: none;
    }
    
    /* Scroll indicator enhancement */
    .hero-scroll-indicator {
        cursor: pointer;
        user-select: none;
    }
    
    /* Profile image enhancements */
    .profile-image {
        cursor: pointer;
        user-select: none;
    }
    
    .profile-photo {
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
`;

// Inject enhanced styles
const styleSheet = document.createElement('style');
styleSheet.textContent = enhancedStyles;
document.head.appendChild(styleSheet);

// Initialize website functionality
document.addEventListener('DOMContentLoaded', () => {
    window.haghmoradiSite = new HaghmoradiWebsite();
});

// Handle page visibility changes for performance
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Pause animations when tab is not visible
        document.body.style.animationPlayState = 'paused';
    } else {
        // Resume animations when tab becomes visible
        document.body.style.animationPlayState = 'running';
    }
});

// Service Worker registration for PWA capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HaghmoradiWebsite;
}
