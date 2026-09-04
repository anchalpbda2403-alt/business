/* GramBiz AI - Core Application Utility Module */

const GramBiz = {
  apiBase: '/api',

  isPublicPage() {
    const page = window.location.pathname.split('/').pop().toLowerCase();
    return !page || page === 'index.html' || page === 'login.html' || page === 'signup.html';
  },

  async fetch(url, options = {}) {
    const defaultHeaders = {
      'Content-Type': 'application/json'
    };
    options.headers = { ...defaultHeaders, ...options.headers };
    options.credentials = 'same-origin';

    try {
      const res = await fetch(this.apiBase + url, options);
      const data = await res.json();
      if (!res.ok && res.status === 401) {
        // Only redirect if on a protected internal dashboard page
        if (!this.isPublicPage() && !url.includes('/check-auth') && !url.includes('/login')) {
          window.location.href = '/login.html';
        }
      }
      return data;
    } catch (err) {
      console.error(`[API Error] ${url}:`, err);
      return { success: false, message: 'Network error or backend unavailable.' };
    }
  },

  showToast(message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'danger') icon = 'fa-exclamation-triangle';
    if (type === 'warning') icon = 'fa-exclamation-circle';

    toast.innerHTML = `<i class="fas ${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  },

  formatINR(amount) {
    const val = parseFloat(amount || 0);
    return '₹' + val.toLocaleString('en-IN', { maximumFractionDigits: 2 });
  },

  highlightActiveNav() {
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.sidebar-link, .bottom-nav-item').forEach(link => {
      const href = link.getAttribute('href');
      if (href && (href === currentPath || (currentPath === '' && href === 'index.html'))) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  },

  async loadNotifications() {
    if (this.isPublicPage()) return; // Don't load notifications on landing, login or signup pages
    const res = await this.fetch('/notifications');
    if (res.success && res.data) {
      const badge = document.querySelector('.notif-badge');
      if (badge) {
        if (res.data.unread_count > 0) {
          badge.style.display = 'block';
        } else {
          badge.style.display = 'none';
        }
      }
    }
  },

  setupSidebarToggle() {
    const toggleBtn = document.getElementById('mobileMenuToggle');
    const sidebar = document.querySelector('.sidebar');
    if (toggleBtn && sidebar) {
      toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
      });
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  GramBiz.highlightActiveNav();
  GramBiz.setupSidebarToggle();
  GramBiz.loadNotifications();

  // Handle Logout buttons
  document.querySelectorAll('.logout-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      await GramBiz.fetch('/logout', { method: 'POST' });
      GramBiz.showToast('Logged out successfully', 'success');
      setTimeout(() => window.location.href = '/login.html', 800);
    });
  });
});
