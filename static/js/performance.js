// PERFORMANCE OPTIMIZED JAVASCRIPT
// Create this as static/js/performance.js

class PerformanceOptimizer {
    constructor() {
        this.lazyImages = [];
        this.observer = null;
        this.init();
    }
    
    init() {
        // Initialize lazy loading
        this.initLazyLoading();
        
        // Initialize intersection observer for animations
        this.initAnimations();
        
        // Optimize images
        this.optimizeImages();
        
        // Preload critical resources
        this.preloadCriticalResources();
        
        // Initialize service worker
        this.initServiceWorker();
    }
    
    initLazyLoading() {
        // Lazy load images
        this.lazyImages = document.querySelectorAll('[data-lazy]');
        
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.lazy;
                        img.classList.add('loaded');
                        img.removeAttribute('data-lazy');
                        this.observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',  // Load 50px before entering viewport
                threshold: 0.1
            });
            
            this.lazyImages.forEach(img => {
                this.observer.observe(img);
            });
        } else {
            // Fallback for older browsers
            this.lazyImages.forEach(img => {
                img.src = img.dataset.lazy;
                img.classList.add('loaded');
            });
        }
    }
    
    initAnimations() {
        // Animate elements on scroll
        const animateElements = document.querySelectorAll('[data-animate]');
        
        if ('IntersectionObserver' in window) {
            const animationObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const element = entry.target;
                        const animation = element.dataset.animate;
                        element.classList.add(animation);
                        animationObserver.unobserve(element);
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            });
            
            animateElements.forEach(el => {
                animationObserver.observe(el);
            });
        }
    }
    
    optimizeImages() {
        // Convert images to WebP if supported
        const supportsWebP = this.checkWebPSupport();
        
        if (supportsWebP) {
            document.querySelectorAll('img[data-webp]').forEach(img => {
                img.src = img.dataset.webp;
            });
        }
        
        // Lazy load background images
        document.querySelectorAll('[data-bg-lazy]').forEach(el => {
            if (this.observer) {
                this.observer.observe(el);
            }
        });
    }
    
    checkWebPSupport() {
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        return canvas.toDataURL('image/webp').indexOf('webp') > -1;
    }
    
    preloadCriticalResources() {
        // Preload critical CSS
        const criticalCSS = [
            '/static/css/tailwind.min.css',
            '/static/css/main.css'
        ];
        
        criticalCSS.forEach(href => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.href = href;
            document.head.appendChild(link);
        });
        
        // Preload critical fonts
        const criticalFonts = [
            '/static/fonts/inter-var.woff2'
        ];
        
        criticalFonts.forEach(href => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'font';
            link.type = 'font/woff2';
            link.crossOrigin = 'anonymous';
            link.href = href;
            document.head.appendChild(link);
        });
    }
    
    initServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('SW registered:', registration);
                })
                .catch(error => {
                    console.log('SW registration failed:', error);
                });
        }
    }
    
    // Debounced scroll handler
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Performance monitoring
    measurePerformance() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                const navigation = performance.getEntriesByType('navigation')[0];
                const paint = performance.getEntriesByType('paint');
                
                console.log('Page Load Time:', navigation.loadEventEnd - navigation.fetchStart);
                
                paint.forEach(entry => {
                    console.log(entry.name, entry.startTime);
                });
            });
        }
    }
}

// Critical resource loading
document.addEventListener('DOMContentLoaded', () => {
    new PerformanceOptimizer();
});

// Optimize third-party scripts
function loadScript(src, callback) {
    const script = document.createElement('script');
    script.src = src;
    script.async = true;
    script.defer = true;
    
    if (callback) {
        script.onload = callback;
    }
    
    document.head.appendChild(script);
}

// Load non-critical scripts after page load
window.addEventListener('load', () => {
    // Load analytics after page load
    if (typeof gtag !== 'undefined') {
        loadScript('https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID');
    }
});

// Image optimization utilities
class ImageOptimizer {
    static generateSrcSet(baseUrl, sizes = [320, 640, 960, 1280]) {
        return sizes.map(size => 
            `${baseUrl}?w=${size}&f=auto&q=auto ${size}w`
        ).join(', ');
    }
    
    static createResponsiveImage(src, alt, className = '') {
        const img = document.createElement('img');
        img.src = src;
        img.alt = alt;
        img.className = className;
        img.loading = 'lazy';
        img.decoding = 'async';
        
        // Add srcset for responsive images
        img.srcset = this.generateSrcSet(src);
        img.sizes = '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw';
        
        return img;
    }
}