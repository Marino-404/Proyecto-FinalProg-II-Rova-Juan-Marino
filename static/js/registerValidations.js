document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", function (event) {
    let hasErrors = false;

    const nombre = form.nombre.value.trim();
    const apellido = form.apellido.value.trim();
    const email = form.email.value.trim();
    const password = form.password.value.trim();
    const confirmPassword = form.confirm_password.value.trim();

    clearErrors();

    if (!nombre) {
      showError("nombre", "Por favor, ingresa tu nombre.");
      hasErrors = true;
    }
    if (!apellido) {
      showError("apellido", "Por favor, ingresa tu apellido.");
      hasErrors = true;
    }
    if (!email) {
      showError("email", "Por favor, ingresa tu correo electrónico.");
      hasErrors = true;
    } else if (!validateEmail(email)) {
      showError("email", "Por favor, ingresa un correo electrónico válido.");
      hasErrors = true;
    }
    if (password.length < 6) {
      showError("password", "La contraseña debe tener al menos 6 caracteres.");
      hasErrors = true;
    }
    if (password !== confirmPassword) {
      showError("confirm_password", "Las contraseñas no coinciden.");
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
