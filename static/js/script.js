// Flask Blog JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    
    // Character count functionality for title field
    const titleInput = document.getElementById('title');
    const bodyInput = document.getElementById('body');
    
    if (titleInput) {
        const titleCount = document.getElementById('title-count');
        
        function updateTitleCount() {
            const count = titleInput.value.length;
            const maxLength = 200;
            titleCount.textContent = count;
            
            // Update styling based on character count
            titleCount.className = '';
            if (count > maxLength * 0.9) {
                titleCount.classList.add('text-warning');
            }
            if (count >= maxLength) {
                titleCount.classList.add('text-danger');
            }
        }
        
        titleInput.addEventListener('input', updateTitleCount);
        updateTitleCount(); // Initialize
    }
    
    if (bodyInput) {
        const bodyCount = document.getElementById('body-count');
        
        function updateBodyCount() {
            const count = bodyInput.value.length;
            bodyCount.textContent = count;
        }
        
        bodyInput.addEventListener('input', updateBodyCount);
        updateBodyCount(); // Initialize
    }
    
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s ease-out';
                alert.style.opacity = '0';
                setTimeout(function() {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000);
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const titleField = form.querySelector('#title');
            const bodyField = form.querySelector('#body');
            
            if (titleField && !titleField.value.trim()) {
                event.preventDefault();
                showAlert('Title is required!', 'danger');
                titleField.focus();
                return false;
            }
            
            if (bodyField && !bodyField.value.trim()) {
                event.preventDefault();
                showAlert('Content is required!', 'danger');
                bodyField.focus();
                return false;
            }
            
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading"></span> Saving...';
                
                // Re-enable button after 5 seconds as fallback
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 5000);
            }
        });
    });
    
    // Confirm before leaving page with unsaved changes
    let formChanged = false;
    const formInputs = document.querySelectorAll('form input, form textarea, form select');
    
    formInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            formChanged = true;
        });
    });
    
    window.addEventListener('beforeunload', function(e) {
        if (formChanged) {
            const confirmationMessage = 'You have unsaved changes. Are you sure you want to leave?';
            (e || window.event).returnValue = confirmationMessage;
            return confirmationMessage;
        }
    });
    
    // Reset form changed flag when form is submitted
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            formChanged = false;
        });
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add copy-to-clipboard functionality for code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(codeBlock) {
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-outline-secondary copy-btn';
        copyButton.innerHTML = '<i class="fas fa-copy"></i> Copy';
        copyButton.style.position = 'absolute';
        copyButton.style.top = '10px';
        copyButton.style.right = '10px';
        
        const pre = codeBlock.parentNode;
        pre.style.position = 'relative';
        pre.appendChild(copyButton);
        
        copyButton.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(function() {
                copyButton.innerHTML = '<i class="fas fa-check"></i> Copied!';
                copyButton.classList.remove('btn-outline-secondary');
                copyButton.classList.add('btn-success');
                
                setTimeout(function() {
                    copyButton.innerHTML = '<i class="fas fa-copy"></i> Copy';
                    copyButton.classList.remove('btn-success');
                    copyButton.classList.add('btn-outline-secondary');
                }, 2000);
            });
        });
    });
    
    // Search functionality (if search input exists)
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const postCards = document.querySelectorAll('.card');
            
            postCards.forEach(function(card) {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const content = card.querySelector('.card-text').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || content.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Word count for blog posts
    if (bodyInput) {
        function updateWordCount() {
            const text = bodyInput.value.trim();
            const words = text.length > 0 ? text.split(/\s+/).length : 0;
            const wordCountElement = document.getElementById('word-count');
            
            if (wordCountElement) {
                wordCountElement.textContent = words + ' words';
            }
        }
        
        bodyInput.addEventListener('input', updateWordCount);
        updateWordCount(); // Initialize
    }
});

// Utility function to show alerts
function showAlert(message, type) {
    const alertContainer = document.querySelector('.flash-messages') || 
                          document.querySelector('main .container');
    
    if (alertContainer) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        if (alertContainer.classList.contains('flash-messages')) {
            alertContainer.appendChild(alert);
        } else {
            alertContainer.insertBefore(alert, alertContainer.firstChild);
        }
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s ease-out';
                alert.style.opacity = '0';
                setTimeout(function() {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000);
    }
}

// Format text to preserve line breaks
function nl2br(str) {
    return str.replace(/\n/g, '<br>');
}

// Utility function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Add loading state to buttons
function addLoadingState(button, loadingText = 'Loading...') {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `<span class="loading"></span> ${loadingText}`;
    
    return function() {
        button.disabled = false;
        button.innerHTML = originalText;
    };
}

// Simple toast notification system
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed`;
    toast.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        opacity: 0;
        transition: opacity 0.3s ease-in-out;
    `;
    toast.innerHTML = message;
    
    document.body.appendChild(toast);
    
    // Fade in
    setTimeout(() => toast.style.opacity = '1', 100);
    
    // Fade out and remove
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, duration);
}
document.addEventListener('DOMContentLoaded', function () {
    const footer = document.querySelector('footer');
    if (footer) {
        footer.style.position = 'fixed';
        footer.style.bottom = '0';
        footer.style.left = '0';
        footer.style.width = '100%';
        footer.style.zIndex = '1030';

        // Prevent content from hiding behind footer
        document.body.style.paddingBottom = footer.offsetHeight + 'px';
    }
});
