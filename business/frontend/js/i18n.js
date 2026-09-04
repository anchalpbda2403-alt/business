/* GramBiz AI - Bilingual Translation Dictionary (English | हिन्दी) */

const i18n = {
  currentLang: localStorage.getItem('grambiz_lang') || 'en',
  
  translations: {
    en: {
      "app_title": "GramBiz AI",
      "app_subtitle": "Your AI Business Partner for Rural India",
      "nav_dashboard": "Dashboard",
      "nav_advisor": "AI Advisor",
      "nav_hyperlocal": "Hyperlocal Insights",
      "nav_finance": "Financial Planner",
      "nav_expenses": "Expenses",
      "nav_revenue": "Revenue",
      "nav_business_plan": "Business Plan",
      "nav_funding": "Funding Assistant",
      "nav_notifications": "Notifications",
      "nav_profile": "Profile",
      "nav_settings": "Settings",
      "nav_logout": "Logout",
      "greeting_morning": "Good Morning,",
      "greeting_afternoon": "Good Afternoon,",
      "greeting_evening": "Good Evening,",
      "health_score": "Business Health Score",
      "monthly_revenue": "Monthly Revenue",
      "monthly_expenses": "Monthly Expenses",
      "estimated_profit": "Estimated Profit",
      "available_cash": "Available Cash",
      "funding_requirement": "Funding Need",
      "ai_recommendations": "AI Business Recommendations",
      "revenue_vs_expenses": "Revenue vs Expenses",
      "monthly_profit_trend": "Monthly Profit Trend",
      "quick_actions": "Quick Actions",
      "ask_advisor_placeholder": "Ask AI advisor (e.g. Which business is suitable for my village?)...",
      "btn_send": "Send",
      "btn_calculate": "Calculate",
      "btn_download_plan": "Download Business Plan",
      "btn_get_started": "Get Started",
      "btn_explore_features": "Explore Features",
      "analyze_area": "Analyze My Area",
      "disclaimer_text": "Funding suggestions & scores are informational AI indicators, not official credit approvals."
    },
    hi: {
      "app_title": "ग्रामबिज़ AI",
      "app_subtitle": "ग्रामीण भारत के लिए आपका AI बिजनेस साथी",
      "nav_dashboard": "डैशबोर्ड",
      "nav_advisor": "AI सलाहकारी (एडवाइजर)",
      "nav_hyperlocal": "स्थानीय बाजार अंतर्दृष्टि",
      "nav_finance": "वित्तीय योजनाकार",
      "nav_expenses": "खर्चे (Expenses)",
      "nav_revenue": "कमाई (Revenue)",
      "nav_business_plan": "बिजनेस प्लान बनाएं",
      "nav_funding": "फंडिंग सहायक",
      "nav_notifications": "सूचनाएं (Notifications)",
      "nav_profile": "प्रोफ़ाइल",
      "nav_settings": "सेटिंग्स",
      "nav_logout": "लॉग आउट",
      "greeting_morning": "सुप्रभात,",
      "greeting_afternoon": "नमस्कार,",
      "greeting_evening": "शुभ संध्या,",
      "health_score": "बिजनेस हेल्थ स्कोर",
      "monthly_revenue": "मासिक कमाई (राजस्व)",
      "monthly_expenses": "मासिक खर्च",
      "estimated_profit": "अनुमानित लाभ (मुनाफा)",
      "available_cash": "उपलब्ध नकद राशि",
      "funding_requirement": "फंडिंग की आवश्यकता",
      "ai_recommendations": "AI बिजनेस सुझाव",
      "revenue_vs_expenses": "कमाई बनाम खर्च",
      "monthly_profit_trend": "मासिक लाभ रुझान",
      "quick_actions": "त्वरित क्रियाएँ",
      "ask_advisor_placeholder": "AI से पूछें (उदा. मेरे गाँव के लिए कौन सा व्यवसाय उपयुक्त है?)...",
      "btn_send": "भेजें",
      "btn_calculate": "गणना करें",
      "btn_download_plan": "बिजनेस प्लान डाउनलोड करें",
      "btn_get_started": "शुरू करें",
      "btn_explore_features": "विशेषताएं देखें",
      "analyze_area": "अपने क्षेत्र का विश्लेषण करें",
      "disclaimer_text": "फंडिंग सुझाव और स्कोर सूचनात्मक AI संकेतक हैं, आधिकारिक ऋण स्वीकृति नहीं।"
    }
  },

  setLanguage(lang) {
    this.currentLang = lang;
    localStorage.setItem('grambiz_lang', lang);
    this.applyTranslations();

    // Toggle active state on buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
      if (btn.dataset.lang === lang) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  },

  applyTranslations() {
    const dict = this.translations[this.currentLang] || this.translations['en'];
    document.querySelectorAll('[data-i18n]').forEach(elem => {
      const key = elem.getAttribute('data-i18n');
      if (dict[key]) {
        if (elem.tagName === 'INPUT' || elem.tagName === 'TEXTAREA') {
          elem.placeholder = dict[key];
        } else {
          elem.textContent = dict[key];
        }
      }
    });
  },

  t(key) {
    const dict = this.translations[this.currentLang] || this.translations['en'];
    return dict[key] || key;
  }
};

document.addEventListener('DOMContentLoaded', () => {
  i18n.applyTranslations();
});
