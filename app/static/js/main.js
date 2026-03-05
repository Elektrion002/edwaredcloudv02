// Simple Navbar Logic
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        if (navLinks.classList.contains('active')) {
            navLinks.style.display = 'flex';
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '100%';
            navLinks.style.left = '0';
            navLinks.style.width = '100%';
            navLinks.style.background = 'var(--primary-navy)';
            navLinks.style.padding = '2rem';
            navLinks.style.borderBottom = '1px solid var(--ui-border)';
        } else {
            navLinks.style.display = 'none';
        }
    });
}

// Basic Entry Animation with GSAP (if available)
if (typeof gsap !== 'undefined') {
    gsap.from("main > *", {
        opacity: 0,
        y: 30,
        duration: 1,
        stagger: 0.2,
        ease: "power2.out"
    });
}
