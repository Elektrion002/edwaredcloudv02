// Project Velocity: Main JS
// Stack: GSAP + ScrollTrigger + Lenis

document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Initialize Lenis (Smooth Scroll)
    const lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        direction: 'vertical',
        gestureDirection: 'vertical',
        smooth: true,
        mouseMultiplier: 1,
        smoothTouch: false,
        touchMultiplier: 2,
    })

    function raf(time) {
        lenis.raf(time)
        requestAnimationFrame(raf)
    }

    requestAnimationFrame(raf)

    // Integrate Lenis with GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);
    
    // 2. Preloader
    const loader = document.querySelector('.loader');
    
    window.onload = () => {
        gsap.to(loader, {
            opacity: 0,
            duration: 1,
            ease: "power2.inOut",
            onComplete: () => {
                loader.style.display = 'none';
                initAnimations();
            }
        });
    }
    
    // Fallback if onload hangs
    setTimeout(() => {
        if(loader.style.display !== 'none'){
            gsap.to(loader, { opacity: 0, duration: 1, onComplete: () => { loader.style.display = 'none'; initAnimations(); }});
        }
    }, 3000);

    // 3. Main Animations
    function initAnimations() {
        
        // Hero Section: Parallax & Text Reveal
        const heroTl = gsap.timeline();
        
        heroTl.to('.hero-title', { 
            y: 0, 
            opacity: 1, 
            duration: 1, 
            ease: "power3.out" 
        })
        .to('.hero-subtitle', { 
            y: 0, 
            opacity: 1, 
            duration: 1, 
            ease: "power3.out" 
        }, "-=0.6")
        .to('.hero-cta', { 
            y: 0, 
            opacity: 1, 
            duration: 1, 
            ease: "power3.out" 
        }, "-=0.6");

        // Parallax Effect for Hero Background
        gsap.to(".hero-bg", {
            yPercent: 50,
            ease: "none",
            scrollTrigger: {
                trigger: "#hero",
                start: "top top",
                end: "bottom top",
                scrub: true
            }, 
        });

        // About Section: Image Mask Reveal
        gsap.from(".image-mask", {
            scrollTrigger: {
                trigger: "#about",
                start: "top 70%",
            },
            width: "0%",
            duration: 1.5,
            ease: "power2.inOut"
        });

        // Stats Counter Animation
        gsap.utils.toArray(".stat-number").forEach(stat => {
            gsap.from(stat, {
                innerText: 0,
                duration: 2,
                snap: { innerText: 1 },
                scrollTrigger: {
                    trigger: stat,
                    start: "top 85%"
                }
            });
        });

        // Skills: Progress Bar Animation
        gsap.utils.toArray(".progress-fill").forEach(bar => {
            gsap.to(bar, {
                width: bar.getAttribute("data-width"),
                duration: 1.5,
                ease: "power2.out",
                scrollTrigger: {
                    trigger: bar,
                    start: "top 85%"
                }
            });
        });

        // Timeline Animation
        gsap.utils.toArray(".timeline-item").forEach(item => {
            gsap.from(item, {
                y: 30,
                duration: 0.8,
                scrollTrigger: {
                    trigger: item,
                    start: "top 90%"
                }
            });
        });

        // Portfolio: Card Reveal
        gsap.utils.toArray(".project-item").forEach(item => {
            gsap.from(item, {
                scrollTrigger: {
                    trigger: item,
                    start: "top 85%"
                },
                y: 50,
                opacity: 0,
                duration: 1,
                ease: "power3.out"
            });
        });

    }

    // Interactive Magnet Effect for Buttons (Optional Polish)
    // Code would go here for custom cursor interactions

    // 4. Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking a link
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }

});
