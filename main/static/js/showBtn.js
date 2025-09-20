document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.querySelector('.password-toggle');
    const input = document.getElementById('password');
    if (toggle && input) {
        toggle.addEventListener('click', function () {
            if (input.type === 'password') {
                input.type = 'text';
                toggle.textContent = 'Hide';
            } else {
                input.type = 'password';
                toggle.textContent = 'Show';
            }
        });
    }
});