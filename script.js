document.addEventListener('DOMContentLoaded', function() {
    // Set current year in footer
    document.getElementById('current-year').textContent = new Date().getFullYear();
    
    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Check for saved theme preference or use preferred color scheme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.className = savedTheme;
    } else {
        // Use preferred color scheme if available
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            body.className = 'dark-mode';
        }
    }
    
    // Theme toggle event listener
    themeToggle.addEventListener('click', function() {
        if (body.classList.contains('light-mode')) {
            body.className = 'dark-mode';
            localStorage.setItem('theme', 'dark-mode');
        } else {
            body.className = 'light-mode';
            localStorage.setItem('theme', 'light-mode');
        }
    });
    
    // Mobile menu functionality
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const menu = document.querySelector('.menu');
    
    mobileMenuToggle.addEventListener('click', function() {
        menu.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
        
        // Toggle menu icon
        if (menu.classList.contains('active')) {
            mobileMenuToggle.innerHTML = '<i class="fas fa-times"></i>';
        } else {
            mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
        }
    });
    
    // Close mobile menu when clicking a link
    const menuLinks = document.querySelectorAll('.menu a');
    menuLinks.forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.remove('active');
            mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
        });
    });
    
    // Smooth scroll and active nav highlighting
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.menu a');
    
    // Highlight active nav item on scroll
    function highlightActiveNavItem() {
        let scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + sectionId) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', highlightActiveNavItem);
    
    // Header scroll behavior
    const header = document.querySelector('header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.scrollY;
        
        if (scrollTop > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Form submission
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // In a real implementation, you would send the form data to a server
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';
            
            // Simulate form submission
            setTimeout(() => {
                const formElements = contactForm.elements;
                
                // Reset form
                contactForm.reset();
                
                // Create success message
                const successMsg = document.createElement('div');
                successMsg.className = 'success-message';
                successMsg.textContent = 'Thank you for your message! I will get back to you soon.';
                
                // Style the success message based on theme
                if (body.classList.contains('light-mode')) {
                    successMsg.style.backgroundColor = '#e8f5e9';
                    successMsg.style.color = '#2e7d32';
                } else {
                    successMsg.style.backgroundColor = '#1b5e20';
                    successMsg.style.color = '#e8f5e9';
                }
                
                successMsg.style.padding = '15px';
                successMsg.style.borderRadius = 'var(--border-radius)';
                successMsg.style.marginTop = '20px';
                successMsg.style.textAlign = 'center';
                
                // Add success message after form
                contactForm.parentNode.appendChild(successMsg);
                
                // Reset button
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
                
                // Remove success message after 5 seconds
                setTimeout(() => {
                    successMsg.remove();
                }, 5000);
                
            }, 1500);
        });
    }
    
    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.project-card, .skill-category, .publication, .timeline-item');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight;
            
            if (elementPosition < screenPosition - 100) {
                element.classList.add('visible');
            }
        });
    }
    
    // Add initial CSS for animations
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        .project-card, .skill-category, .publication, .timeline-item {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }
        
        .project-card.visible, .skill-category.visible, .publication.visible, .timeline-item.visible {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(styleElement);
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on page load
});