document.addEventListener('DOMContentLoaded', function() {
    // Theme switcher
    const toggleSwitch = document.querySelector('#checkbox');
    const themeLabel = document.querySelector('.theme-label');
    
    // Check for saved theme preference or use system preference
    const currentTheme = localStorage.getItem('theme') || 
                          (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    // Set initial theme
    document.documentElement.setAttribute('data-theme', currentTheme);
    toggleSwitch.checked = currentTheme === 'dark';
    themeLabel.textContent = currentTheme === 'dark' ? 'Dark Mode' : 'Light Mode';
    
    // Toggle theme function
    function switchTheme(e) {
        const theme = e.target.checked ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', theme);
        themeLabel.textContent = theme === 'dark' ? 'Dark Mode' : 'Light Mode';
        localStorage.setItem('theme', theme);
    }
    
    toggleSwitch.addEventListener('change', switchTheme, false);
    
    // Mobile navigation toggle
    const nav = document.querySelector('nav');
    const burger = document.querySelector('.burger');
    const navLinks = document.querySelector('.nav-links');
    const navLinksLi = document.querySelectorAll('.nav-links li');
    
    burger.addEventListener('click', () => {
        // Toggle navigation
        navLinks.classList.toggle('nav-active');
        
        // Animate links
        navLinksLi.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });
        
        // Burger animation
        burger.classList.toggle('toggle');
    });
    
    // Close mobile menu when clicking a nav link
    navLinksLi.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('nav-active');
            burger.classList.remove('toggle');
            
            navLinksLi.forEach(link => {
                link.style.animation = '';
            });
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            nav.classList.add('scrolled-nav');
        } else {
            nav.classList.remove('scrolled-nav');
        }
    });
    
    // Scroll animations
    function animateOnScroll() {
        const animatedElements = document.querySelectorAll('.animate-on-scroll');
        
        animatedElements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.classList.add('fade-in');
            }
        });
    }
    
    // Form submission handling
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;
            
            // Here you would typically send this data to a server
            // For now, just log it to console and show a success message
            console.log('Form submitted:', { name, email, subject, message });
            
            // Show success message (in a real implementation, you'd show this after successful AJAX)
            alert('Thank you for your message! I will get back to you soon.');
            
            // Reset the form
            contactForm.reset();
        });
    }
    
    // Initialize animations on page load
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on page load
});