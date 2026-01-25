document.addEventListener('DOMContentLoaded', function () {

    // --- Password Visibility Toggle ---
    const toggles = document.querySelectorAll('.toggle-password');
    toggles.forEach(toggle => {
        toggle.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    });

    // --- Password Strength Meter ---
    const newPassInput = document.getElementById('new-password'); // For Reset
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');

    if (newPassInput && strengthBar) {
        newPassInput.addEventListener('input', function () {
            const val = this.value;
            let strength = 0;
            if (val.length > 5) strength += 1;
            if (val.length > 10) strength += 1;
            if (/[A-Z]/.test(val)) strength += 1;
            if (/[0-9]/.test(val)) strength += 1;
            if (/[^A-Za-z0-9]/.test(val)) strength += 1;

            let color = '#ddd';
            let width = '0%';
            let label = 'Weak';

            if (strength <= 1) { width = '20%'; color = '#ef4444'; label = 'Weak'; }
            else if (strength <= 3) { width = '50%'; color = '#eab308'; label = 'Medium'; }
            else { width = '100%'; color = '#22c55e'; label = 'Strong'; }

            strengthBar.style.width = width;
            strengthBar.style.backgroundColor = color;
            strengthText.innerText = label;
            strengthText.style.color = color;
        });
    }

    // --- Resend OTP Timer ---
    const timerDisplay = document.getElementById('timer');
    const resendLink = document.getElementById('resend-link');
    const timerMsg = document.getElementById('timer-msg');

    if (timerDisplay && resendLink) {
        let timeLeft = 30;
        const interval = setInterval(() => {
            if (timeLeft <= 0) {
                clearInterval(interval);
                timerMsg.style.display = 'none';
                resendLink.classList.remove('disabled-link');
                resendLink.style.pointerEvents = 'auto';
                resendLink.style.opacity = '1';
                resendLink.innerText = "Resend OTP Now";
            } else {
                timerDisplay.innerText = timeLeft;
                timeLeft -= 1;
            }
        }, 1000);
    }
});
