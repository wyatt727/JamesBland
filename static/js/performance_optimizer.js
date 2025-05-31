/**
 * JAMES BLAND: ACME EDITION - PERFORMANCE OPTIMIZER
 * Asset loading optimization, lazy loading, and memory management
 */

class PerformanceOptimizer {
    constructor() {
        this.assetCache = new Map();
        this.observerOptions = {
            root: null,
            rootMargin: '50px',
            threshold: 0.1
        };
        this.intersectionObserver = null;
        this.memoryThreshold = 100 * 1024 * 1024; // 100MB
        this.performanceMetrics = {};
        
        this.init();
    }
    
    init() {
        this.setupIntersectionObserver();
        this.setupPerformanceMonitoring();
        this.optimizeInitialLoad();
        this.setupMemoryManagement();
    }
    
    /**
     * Set up intersection observer for lazy loading
     */
    setupIntersectionObserver() {
        if ('IntersectionObserver' in window) {
            this.intersectionObserver = new IntersectionObserver(
                this.handleIntersection.bind(this),
                this.observerOptions
            );
        }
    }
    
    /**
     * Handle intersection observer callbacks
     */
    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                
                if (element.dataset.lazySrc) {
                    this.loadLazyImage(element);
                } else if (element.dataset.lazyAudio) {
                    this.loadLazyAudio(element);
                }
                
                this.intersectionObserver.unobserve(element);
            }
        });
    }
    
    /**
     * Load lazy image
     */
    loadLazyImage(img) {
        const src = img.dataset.lazySrc;
        
        if (this.assetCache.has(src)) {
            img.src = this.assetCache.get(src);
            img.classList.add('loaded');
            return Promise.resolve();
        }
        
        return new Promise((resolve, reject) => {
            const image = new Image();
            image.onload = () => {
                this.assetCache.set(src, src);
                img.src = src;
                img.classList.add('loaded');
                resolve();
            };
            image.onerror = reject;
            image.src = src;
        });
    }
    
    /**
     * Load lazy audio
     */
    loadLazyAudio(audio) {
        const src = audio.dataset.lazyAudio;
        
        if (this.assetCache.has(src)) {
            audio.src = this.assetCache.get(src);
            return Promise.resolve();
        }
        
        return new Promise((resolve, reject) => {
            audio.addEventListener('canplaythrough', () => {
                this.assetCache.set(src, src);
                resolve();
            }, { once: true });
            
            audio.addEventListener('error', reject, { once: true });
            audio.src = src;
        });
    }
    
    /**
     * Preload critical assets
     */
    preloadCriticalAssets() {
        const criticalAssets = [
            { type: 'style', href: '/static/css/style.css' },
            { type: 'script', src: '/static/js/app.js' },
            { type: 'audio', src: '/static/audio/sfx/anvil_drop.mp3' }
        ];
        
        return Promise.all(criticalAssets.map(asset => this.preloadAsset(asset)));
    }
    
    /**
     * Preload individual asset
     */
    preloadAsset(asset) {
        return new Promise((resolve, reject) => {
            let element;
            
            switch (asset.type) {
                case 'style':
                    element = document.createElement('link');
                    element.rel = 'preload';
                    element.as = 'style';
                    element.href = asset.href;
                    break;
                    
                case 'script':
                    element = document.createElement('link');
                    element.rel = 'preload';
                    element.as = 'script';
                    element.href = asset.src;
                    break;
                    
                case 'audio':
                    element = document.createElement('audio');
                    element.preload = 'metadata';
                    element.src = asset.src;
                    break;
                    
                case 'image':
                    element = document.createElement('img');
                    element.src = asset.src;
                    break;
                    
                default:
                    resolve();
                    return;
            }
            
            element.onload = () => {
                this.assetCache.set(asset.src || asset.href, element);
                resolve();
            };
            element.onerror = reject;
            
            if (asset.type === 'style' || asset.type === 'script') {
                document.head.appendChild(element);
            }
        });
    }
    
    /**
     * Optimize initial page load
     */
    optimizeInitialLoad() {
        // Defer non-critical scripts
        this.deferNonCriticalScripts();
        
        // Optimize font loading
        this.optimizeFontLoading();
        
        // Setup resource hints
        this.setupResourceHints();
    }
    
    /**
     * Defer non-critical scripts
     */
    deferNonCriticalScripts() {
        const nonCriticalScripts = document.querySelectorAll('script[data-defer]');
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.loadDeferredScripts(nonCriticalScripts);
            });
        } else {
            this.loadDeferredScripts(nonCriticalScripts);
        }
    }
    
    /**
     * Load deferred scripts
     */
    loadDeferredScripts(scripts) {
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            newScript.src = script.src;
            newScript.async = true;
            document.head.appendChild(newScript);
        });
    }
    
    /**
     * Optimize font loading
     */
    optimizeFontLoading() {
        // Add font-display: swap to existing fonts
        const style = document.createElement('style');
        style.textContent = `
            @font-face {
                font-family: 'ACMECartoon';
                src: url('/static/fonts/acme_cartoon.ttf') format('truetype');
                font-weight: bold;
                font-display: swap;
            }
            
            @font-face {
                font-family: 'MonospaceConsole';
                src: url('/static/fonts/monospace_console.ttf') format('truetype');
                font-weight: normal;
                font-display: swap;
            }
        `;
        document.head.appendChild(style);
    }
    
    /**
     * Setup resource hints
     */
    setupResourceHints() {
        const hints = [
            { rel: 'dns-prefetch', href: '//cdnjs.cloudflare.com' },
            { rel: 'preconnect', href: 'https://cdnjs.cloudflare.com', crossorigin: true }
        ];
        
        hints.forEach(hint => {
            const link = document.createElement('link');
            Object.assign(link, hint);
            document.head.appendChild(link);
        });
    }
    
    /**
     * Setup performance monitoring
     */
    setupPerformanceMonitoring() {
        // Monitor Core Web Vitals
        this.monitorCoreWebVitals();
        
        // Monitor memory usage
        this.monitorMemoryUsage();
        
        // Monitor frame rate
        this.monitorFrameRate();
    }
    
    /**
     * Monitor Core Web Vitals
     */
    monitorCoreWebVitals() {
        // Largest Contentful Paint
        if ('PerformanceObserver' in window) {
            new PerformanceObserver(list => {
                for (const entry of list.getEntries()) {
                    if (entry.entryType === 'largest-contentful-paint') {
                        this.performanceMetrics.lcp = entry.startTime;
                    }
                }
            }).observe({ entryTypes: ['largest-contentful-paint'] });
            
            // First Input Delay
            new PerformanceObserver(list => {
                for (const entry of list.getEntries()) {
                    if (entry.entryType === 'first-input') {
                        this.performanceMetrics.fid = entry.processingStart - entry.startTime;
                    }
                }
            }).observe({ entryTypes: ['first-input'] });
            
            // Cumulative Layout Shift
            let clsValue = 0;
            new PerformanceObserver(list => {
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                        this.performanceMetrics.cls = clsValue;
                    }
                }
            }).observe({ entryTypes: ['layout-shift'] });
        }
    }
    
    /**
     * Monitor memory usage
     */
    monitorMemoryUsage() {
        if (performance.memory) {
            setInterval(() => {
                const memory = performance.memory;
                this.performanceMetrics.memoryUsed = memory.usedJSHeapSize;
                this.performanceMetrics.memoryTotal = memory.totalJSHeapSize;
                
                // Trigger garbage collection if memory usage is high
                if (memory.usedJSHeapSize > this.memoryThreshold) {
                    this.triggerMemoryCleanup();
                }
            }, 10000); // Check every 10 seconds
        }
    }
    
    /**
     * Monitor frame rate
     */
    monitorFrameRate() {
        let frameCount = 0;
        let lastTime = performance.now();
        
        const countFrames = (currentTime) => {
            frameCount++;
            
            if (currentTime >= lastTime + 1000) {
                this.performanceMetrics.fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                frameCount = 0;
                lastTime = currentTime;
            }
            
            requestAnimationFrame(countFrames);
        };
        
        requestAnimationFrame(countFrames);
    }
    
    /**
     * Trigger memory cleanup
     */
    triggerMemoryCleanup() {
        // Clear old cache entries
        if (this.assetCache.size > 50) {
            const entries = Array.from(this.assetCache.entries());
            const toDelete = entries.slice(0, Math.floor(entries.length / 2));
            toDelete.forEach(([key]) => this.assetCache.delete(key));
        }
        
        // Remove unused DOM elements
        this.cleanupUnusedElements();
        
        console.log('Performance Optimizer: Memory cleanup triggered');
    }
    
    /**
     * Cleanup unused DOM elements
     */
    cleanupUnusedElements() {
        // Remove old test results that might accumulate
        const oldResults = document.querySelectorAll('.test-result');
        if (oldResults.length > 100) {
            const toRemove = Array.from(oldResults).slice(0, oldResults.length - 50);
            toRemove.forEach(element => element.remove());
        }
        
        // Clear any orphaned event listeners
        this.cleanupEventListeners();
    }
    
    /**
     * Cleanup event listeners
     */
    cleanupEventListeners() {
        // Remove old audio event listeners
        const audioElements = document.querySelectorAll('audio');
        audioElements.forEach(audio => {
            const newAudio = audio.cloneNode(true);
            audio.parentNode.replaceChild(newAudio, audio);
        });
    }
    
    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return {
            ...this.performanceMetrics,
            cacheSize: this.assetCache.size,
            timestamp: Date.now()
        };
    }
    
    /**
     * Optimize images for different screen densities
     */
    optimizeImages() {
        const images = document.querySelectorAll('img[data-optimize]');
        
        images.forEach(img => {
            const pixelRatio = window.devicePixelRatio || 1;
            const width = img.offsetWidth * pixelRatio;
            const height = img.offsetHeight * pixelRatio;
            
            // Create optimized image URL (if using image service)
            const originalSrc = img.src;
            const optimizedSrc = this.createOptimizedImageUrl(originalSrc, width, height);
            
            if (optimizedSrc !== originalSrc) {
                img.src = optimizedSrc;
            }
        });
    }
    
    /**
     * Create optimized image URL
     */
    createOptimizedImageUrl(src, width, height) {
        // This would integrate with an image optimization service
        // For now, return original src
        return src;
    }
    
    /**
     * Setup service worker for caching
     */
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration.scope);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        }
    }
    
    /**
     * Bundle and minify assets (build-time optimization)
     */
    static generateOptimizationReport() {
        return {
            recommendations: [
                'Enable gzip compression on server',
                'Implement image lazy loading',
                'Use WebP format for images where supported',
                'Minimize JavaScript bundle size',
                'Use CSS containment for layout optimization',
                'Implement virtual scrolling for large lists'
            ],
            criticalPath: [
                '/static/css/style.css',
                '/static/js/app.js',
                'Socket.IO CDN'
            ],
            loadingPriority: {
                high: ['HTML', 'Critical CSS', 'Core JS'],
                medium: ['Fonts', 'UI Images'],
                low: ['Audio files', 'Background images']
            }
        };
    }
}

/**
 * Image optimization utilities
 */
class ImageOptimizer {
    static convertToWebP(canvas) {
        return new Promise(resolve => {
            canvas.toBlob(resolve, 'image/webp', 0.8);
        });
    }
    
    static resizeImage(file, maxWidth, maxHeight) {
        return new Promise(resolve => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();
            
            img.onload = () => {
                const ratio = Math.min(maxWidth / img.width, maxHeight / img.height);
                canvas.width = img.width * ratio;
                canvas.height = img.height * ratio;
                
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                resolve(canvas);
            };
            
            img.src = URL.createObjectURL(file);
        });
    }
}

/**
 * Network optimization utilities
 */
class NetworkOptimizer {
    constructor() {
        this.connectionType = this.getConnectionType();
        this.isSlowConnection = this.checkSlowConnection();
    }
    
    getConnectionType() {
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        return connection ? connection.effectiveType : 'unknown';
    }
    
    checkSlowConnection() {
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        if (!connection) return false;
        
        return connection.effectiveType === 'slow-2g' || 
               connection.effectiveType === '2g' ||
               connection.downlink < 1.5;
    }
    
    adaptToConnection() {
        if (this.isSlowConnection) {
            // Reduce quality for slow connections
            this.enableDataSavingMode();
        } else {
            // Enable full quality for fast connections
            this.enableHighQualityMode();
        }
    }
    
    enableDataSavingMode() {
        console.log('NetworkOptimizer: Enabling data saving mode');
        
        // Disable auto-playing audio
        const audioElements = document.querySelectorAll('audio');
        audioElements.forEach(audio => {
            audio.preload = 'none';
        });
        
        // Reduce image quality
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            img.loading = 'lazy';
        });
    }
    
    enableHighQualityMode() {
        console.log('NetworkOptimizer: Enabling high quality mode');
        
        // Enable preloading for better experience
        const audioElements = document.querySelectorAll('audio');
        audioElements.forEach(audio => {
            audio.preload = 'metadata';
        });
    }
}

// Initialize performance optimizer when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.performanceOptimizer = new PerformanceOptimizer();
        window.networkOptimizer = new NetworkOptimizer();
        window.networkOptimizer.adaptToConnection();
    });
} else {
    window.performanceOptimizer = new PerformanceOptimizer();
    window.networkOptimizer = new NetworkOptimizer();
    window.networkOptimizer.adaptToConnection();
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PerformanceOptimizer, ImageOptimizer, NetworkOptimizer };
} 