document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  // Añade un evento que se activará cuando el formulario sea enviado.
  form.addEventListener("submit", async function (event) {
    // Previene que el formulario se envíe de forma tradicional.
    event.preventDefault();
    let hasErrors = false; // Variable para verificar si hay errores.

    // Obtiene y limpia los valores de los campos de entrada.
    const email = form.email.value.trim();
    const password = form.password.value.trim();
    clearErrors(); // Llama a la función para limpiar mensajes de error anteriores.

    // Verifica si el campo de correo electrónico está vacío.
    if (!email) {
      showError("email", "Por favor, ingresa tu correo electrónico.");
      hasErrors = true; // Marca que hay un error.
    } else if (!validateEmail(email)) {
      // Verifica si el correo electrónico es válido.
      showError("email", "Por favor, ingresa un correo electrónico válido.");
      hasErrors = true; // Marca que hay un error.
    }

    // Verifica si el campo de contraseña está vacío.
    if (!password) {
      showError("password", "Por favor, ingresa tu contraseña.");
      hasErrors = true; // Marca que hay un error.
    }

    // Si hay errores, no continúa con la validación.
    if (hasErrors) return;

    // Intenta hacer una solicitud asíncrona para verificar las credenciales.
    try {
      // Realiza una solicitud POST a la ruta de verificación de credenciales.
      const response = await fetch("/api/check_credentials", {
        method: "POST", // Especifica que el método HTTP es POST.
        headers: {
          "Content-Type": "application/json", // Indica que el contenido es en formato JSON.
        },
        // Envía el correo y la contraseña como un objeto JSON.
        body: JSON.stringify({ email, password }),
      });

      // Convierte la respuesta a formato JSON.
      const result = await response.json();

      // Si la verificación de credenciales no fue exitosa.
      if (!result.success) {
        // Muestra los mensajes de error correspondientes.
        if (result.errors.email) showError("email", result.errors.email);
        if (result.errors.password)
          showError("password", result.errors.password);
      } else {
        // Si la verificación fue exitosa, redirige al usuario a la URL indicada.
        window.location.href = result.redirect_url;
      }
    } catch (error) {
      // Si ocurre un error en la solicitud, lo muestra en la consola.
      console.error("Error:", error);
    }
  });

  // Función para mostrar un mensaje de error para un campo específico.
  function showError(fieldName, message) {
    const field = document.querySelector(`input[name="${fieldName}"]`); // Selecciona el campo correspondiente.
    const errorMessage = document.createElement("p"); // Crea un nuevo elemento de párrafo para el mensaje de error.
    errorMessage.className = "error-message"; // Asigna una clase al mensaje de error.
    errorMessage.innerText = message; // Establece el texto del mensaje de error.
    // Inserta el mensaje de error después del campo correspondiente en el DOM.
    field.parentNode.insertBefore(errorMessage, field.nextSibling);
  }

  // Función para limpiar todos los mensajes de error visibles.
  function clearErrors() {
    const errorMessages = document.querySelectorAll(".error-message"); // Selecciona todos los mensajes de error.
    errorMessages.forEach((message) => message.remove()); // Elimina cada mensaje de error del DOM.
  }

  // Función para validar si el correo electrónico tiene el formato correcto.
  function validateEmail(email) {
    const regex = /[^@]+@[^@]+\.[^@]+/; // Expresión regular para validar el formato del correo electrónico.
    return regex.test(email); // Devuelve verdadero si el correo es válido.
  }
});
