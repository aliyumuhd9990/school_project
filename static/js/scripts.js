/*!
* Start Bootstrap - Landing Page v6.0.6 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

const passwordInput = document.getElementById('password');
const passwordHint = document.getElementById('passwordHint');

passwordInput.addEventListener('input', () => {
  const pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
  if (pattern.test(passwordInput.value)) {
    passwordHint.style.display = 'none'; // Hide hint if valid
  } else {
    passwordHint.style.display = 'block'; // Show hint if invalid
  }
});

