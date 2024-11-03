document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", function (event) {
    let hasErrors = false;

    const email = form.email.value.trim();
    const password = form.password.value.trim();

    clearErrors();

    if (!email) {
      showError("email", "Por favor, ingresa tu correo electrónico.");
      hasErrors = true;
    } else if (!validateEmail(email)) {
      showError("email", "Por favor, ingresa un correo electrónico válido.");
      hasErrors = true;
    }
    if (!password) {
      showError("password", "Por favor, ingresa tu contraseña.");
      hasErrors = true;
    }

    if (hasErrors) {
      event.preventDefault();
    }
  });

  function showError(fieldName, message) {
    const field = document.querySelector(`input[name="${fieldName}"]`);
    const errorMessage = document.createElement("p");
    errorMessage.className = "error-message";
    errorMessage.innerText = message;
    field.parentNode.insertBefore(errorMessage, field.nextSibling);
  }

  function clearErrors() {
    const errorMessages = document.querySelectorAll(".error-message");
    errorMessages.forEach((message) => message.remove());
  }

  function validateEmail(email) {
    const regex = /[^@]+@[^@]+\.[^@]+/;
    return regex.test(email);
  }
});
