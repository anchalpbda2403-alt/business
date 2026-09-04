/* GramBiz AI - Authentication & Onboarding Handler */

document.addEventListener('DOMContentLoaded', () => {
  // Login Form Submission
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const identifier = document.getElementById('loginIdentifier').value.trim();
      const password = document.getElementById('loginPassword').value;

      if (!identifier || !password) {
        GramBiz.showToast('Please enter both email/mobile and password.', 'warning');
        return;
      }

      const res = await GramBiz.fetch('/login', {
        method: 'POST',
        body: JSON.stringify({ email_or_mobile: identifier, password })
      });

      if (res.success) {
        GramBiz.showToast('Login successful! Redirecting...', 'success');
        setTimeout(() => {
          if (res.data.is_onboarded) {
            window.location.href = '/dashboard.html';
          } else {
            window.location.href = '/onboarding.html';
          }
        }, 1000);
      } else {
        GramBiz.showToast(res.message || 'Login failed.', 'danger');
      }
    });
  }

  // Signup Form Submission
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fullName = document.getElementById('signupFullName').value.trim();
      const mobile = document.getElementById('signupMobile').value.trim();
      const email = document.getElementById('signupEmail').value.trim();
      const password = document.getElementById('signupPassword').value;
      const village = document.getElementById('signupVillage').value.trim();
      const district = document.getElementById('signupDistrict').value.trim();
      const state = document.getElementById('signupState').value.trim();
      const businessType = document.getElementById('signupBusinessType').value;

      if (!fullName || !mobile || !email || !password) {
        GramBiz.showToast('Please fill in all required fields.', 'warning');
        return;
      }

      const res = await GramBiz.fetch('/register', {
        method: 'POST',
        body: JSON.stringify({
          full_name: fullName,
          mobile: mobile,
          email: email,
          password: password,
          village_town: village,
          district: district,
          state: state,
          business_type: businessType
        })
      });

      if (res.success) {
        GramBiz.showToast('Account created successfully! Redirecting to setup...', 'success');
        setTimeout(() => {
          window.location.href = '/onboarding.html';
        }, 1000);
      } else {
        GramBiz.showToast(res.message || 'Signup failed.', 'danger');
      }
    });
  }

  // Onboarding Form Submission
  const onboardingForm = document.getElementById('onboardingForm');
  if (onboardingForm) {
    onboardingForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const goalsChecked = [];
      document.querySelectorAll('input[name="goals"]:checked').forEach(cb => goalsChecked.push(cb.value));

      const payload = {
        name: document.getElementById('obName')?.value,
        village_town: document.getElementById('obVillage')?.value,
        district: document.getElementById('obDistrict')?.value,
        state: document.getElementById('obState')?.value,
        business_type: document.getElementById('obBusinessType')?.value,
        business_status: document.getElementById('obStatus')?.value,
        years_in_business: document.getElementById('obYears')?.value,
        number_of_workers: document.getElementById('obWorkers')?.value,
        initial_investment: document.getElementById('obInvestment')?.value,
        monthly_revenue: document.getElementById('obRevenue')?.value,
        monthly_expenses: document.getElementById('obExpenses')?.value,
        current_savings: document.getElementById('obSavings')?.value,
        existing_loan: document.getElementById('obLoan')?.value,
        goals: goalsChecked
      };

      const res = await GramBiz.fetch('/profile', {
        method: 'POST',
        body: JSON.stringify(payload)
      });

      if (res.success) {
        GramBiz.showToast('Onboarding completed! Welcome to your Dashboard.', 'success');
        setTimeout(() => {
          window.location.href = '/dashboard.html';
        }, 1000);
      } else {
        GramBiz.showToast(res.message || 'Failed to save profile.', 'danger');
      }
    });
  }
});
