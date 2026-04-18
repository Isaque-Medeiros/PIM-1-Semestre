/**
 * Custom JavaScript for Isaque Medeiros - Hub de Projetos
 * Soft Professional enhancements for MkDocs Material theme
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components and enhancements
    initThemePreferences();
    initSmoothScrolling();
    initCopyCodeButtons();
    initExternalLinkIndicators();
    initProjectCards();
    initTableOfContents();
    
    console.log('Hub de Projetos - Custom JS loaded successfully');
});

/**
 * Theme preferences with localStorage persistence
 */
function initThemePreferences() {
    const themeToggle = document.querySelector('.md-toggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('md-theme');
    if (savedTheme) {
        document.body.setAttribute('data-md-color-scheme', savedTheme);
    }
    
    // Update localStorage when theme changes
    if (themeToggle) {
        themeToggle.addEventListener('change', function() {
            const currentTheme = document.body.getAttribute('data-md-color-scheme');
            localStorage.setItem('md-theme', currentTheme);
        });
    }
    
    // Listen for system theme changes
    prefersDark.addEventListener('change', function(e) {
        if (!localStorage.getItem('md-theme')) {
            document.body.setAttribute('data-md-color-scheme', e.matches ? 'slate' : 'default');
        }
    });
}

/**
 * Smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if it's just "#"
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                
                // Calculate header height for offset
                const headerHeight = document.querySelector('.md-header').offsetHeight || 80;
                
                window.scrollTo({
                    top: target.offsetTop - headerHeight - 20,
                    behavior: 'smooth'
                });
                
                // Update URL without jumping
                history.pushState(null, null, href);
            }
        });
    });
}

/**
 * Add copy buttons to code blocks
 */
function initCopyCodeButtons() {
    document.querySelectorAll('pre > code').forEach(codeBlock => {
        const pre = codeBlock.parentElement;
        
        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'md-button md-button--primary copy-code-button';
        copyButton.innerHTML = '<span class="twemoji">📋</span>';
        copyButton.title = 'Copiar código';
        
        // Position button
        copyButton.style.position = 'absolute';
        copyButton.style.top = '10px';
        copyButton.style.right = '10px';
        copyButton.style.padding = '4px 8px';
        copyButton.style.fontSize = '12px';
        copyButton.style.zIndex = '10';
        
        pre.style.position = 'relative';
        pre.appendChild(copyButton);
        
        // Copy functionality
        copyButton.addEventListener('click', function() {
            const textToCopy = codeBlock.textContent;
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Visual feedback
                const originalHTML = copyButton.innerHTML;
                copyButton.innerHTML = '<span class="twemoji">✅</span>';
                copyButton.style.backgroundColor = '#10b981';
                
                setTimeout(() => {
                    copyButton.innerHTML = originalHTML;
                    copyButton.style.backgroundColor = '';
                }, 2000);
            }).catch(err => {
                console.error('Falha ao copiar: ', err);
                copyButton.innerHTML = '<span class="twemoji">❌</span>';
                copyButton.style.backgroundColor = '#ef4444';
                
                setTimeout(() => {
                    copyButton.innerHTML = '<span class="twemoji">📋</span>';
                    copyButton.style.backgroundColor = '';
                }, 2000);
            });
        });
    });
}

/**
 * Add indicators to external links
 */
function initExternalLinkIndicators() {
    document.querySelectorAll('a[href^="http"]').forEach(link => {
        // Skip internal links and social icons
        if (link.href.includes(window.location.hostname) || 
            link.classList.contains('md-social__link')) {
            return;
        }
        
        // Add external link indicator
        const indicator = document.createElement('span');
        indicator.className = 'external-link-indicator';
        indicator.innerHTML = '↗';
        indicator.style.marginLeft = '4px';
        indicator.style.fontSize = '0.8em';
        indicator.style.opacity = '0.7';
        
        link.appendChild(indicator);
        
        // Add title if missing
        if (!link.getAttribute('title')) {
            link.setAttribute('title', 'Link externo - abre em nova aba');
        }
        
        // Ensure external links open in new tab
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
}

/**
 * Enhance project cards with hover effects
 */
function initProjectCards() {
    document.querySelectorAll('.project-card').forEach(card => {
        // Add clickable area if card contains a link
        const link = card.querySelector('a[href]');
        if (link && !card.classList.contains('clickable')) {
            card.style.cursor = 'pointer';
            card.classList.add('clickable');
            
            card.addEventListener('click', function(e) {
                // Don't trigger if clicking on buttons or links inside
                if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') {
                    return;
                }
                
                link.click();
            });
        }
        
        // Add subtle animation on hover
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });
}

/**
 * Enhance table of contents with active section highlighting
 */
function initTableOfContents() {
    const toc = document.querySelector('.md-sidebar--secondary');
    if (!toc) return;
    
    const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -70% 0px',
        threshold: 0
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            const id = entry.target.getAttribute('id');
            if (!id) return;
            
            const tocLink = toc.querySelector(`a[href="#${id}"]`);
            if (tocLink) {
                if (entry.isIntersecting) {
                    tocLink.classList.add('active');
                } else {
                    tocLink.classList.remove('active');
                }
            }
        });
    }, observerOptions);
    
    // Observe all headings with IDs
    document.querySelectorAll('h1[id], h2[id], h3[id]').forEach(heading => {
        observer.observe(heading);
    });
}

/**
 * Utility: Debounce function for performance
 */
function debounce(func, wait) {
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

/**
 * Handle responsive behavior
 */
window.addEventListener('resize', debounce(function() {
    // Adjust code block copy button positions on resize
    document.querySelectorAll('.copy-code-button').forEach(button => {
        const pre = button.parentElement;
        if (pre.offsetWidth < 300) {
            button.style.display = 'none';
        } else {
            button.style.display = 'block';
        }
    });
}, 250));

/**
 * Add print styles enhancement
 */
window.addEventListener('beforeprint', function() {
    // Hide unnecessary elements when printing
    document.querySelectorAll('.copy-code-button, .external-link-indicator').forEach(el => {
        el.style.display = 'none';
    });
});

window.addEventListener('afterprint', function() {
    // Restore elements after printing
    document.querySelectorAll('.copy-code-button, .external-link-indicator').forEach(el => {
        el.style.display = 'inline-block';
    });
});

/**
 * Progress bar for reading progress
 */
function initReadingProgress() {
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress-bar';
    progressBar.style.position = 'fixed';
    progressBar.style.top = '0';
    progressBar.style.left = '0';
    progressBar.style.height = '3px';
    progressBar.style.backgroundColor = 'var(--md-accent-fg-color)';
    progressBar.style.width = '0%';
    progressBar.style.zIndex = '1000';
    progressBar.style.transition = 'width 0.2s ease';
    
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', debounce(function() {
        const winHeight = window.innerHeight;
        const docHeight = document.documentElement.scrollHeight;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        const scrolled = (scrollTop / (docHeight - winHeight)) * 100;
        progressBar.style.width = scrolled + '%';
    }, 10));
}

// Initialize reading progress on wider screens
if (window.innerWidth > 768) {
    initReadingProgress();
}