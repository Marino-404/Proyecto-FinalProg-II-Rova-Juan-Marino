<<<<<<< HEAD

// Esperamos a que todo el contenido de la página esté cargado antes de ejecutar el código
=======
>>>>>>> 20ced4c10f6a049055f1337eb1884ae7e242b51d
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  // Añadimos un evento que se ejecutará cuando el formulario sea enviado
  form.addEventListener("submit", async function (event) {
    // Evitamos que el formulario se envíe de forma tradicional
    event.preventDefault();
    let hasErrors = false; // Variable para rastrear si hay errores en la validación

    // Obtenemos y limpiamos los valores ingresados por el usuario
    const nombre = form.nombre.value.trim();
    const apellido = form.apellido.value.trim();
    const email = form.email.value.trim();
    const password = form.password.value.trim();
    const confirmPassword = form.confirm_password.value.trim();

    // Limpiamos mensajes de error anteriores
    clearErrors();

    // Validamos que se haya ingresado el nombre
    if (!nombre) {
      showError("nombre", "Por favor, ingresa tu nombre."); // Mostramos un mensaje de error
      hasErrors = true; // Marcamos que hay un error
    }
    // Validamos que se haya ingresado el apellido
    if (!apellido) {
      showError("apellido", "Por favor, ingresa tu apellido."); // Mostramos un mensaje de error
      hasErrors = true; // Marcamos que hay un error
    }
    // Validamos que se haya ingresado el correo electrónico
    if (!email) {
      showError("email", "Por favor, ingresa tu correo electrónico."); // Mostramos un mensaje de error
      hasErrors = true; // Marcamos que hay un error
    } else if (!validateEmail(email)) {
      // Validamos que el correo tenga un formato correcto
      showError("email", "Por favor, ingresa un correo electrónico válido."); // Mostramos un mensaje de error
      hasErrors = true; // Marcamos que hay un error
    }
    // Validamos que la contraseña tenga al menos 6 caracteres
    if (password.length < 6) {
      showError("password", "La contraseña debe tener al menos 6 caracteres."); // Mostramos un mensaje de error
      hasErrors = true; // Marcamos que hay un error
    }
    // Validamos que las contraseñas coincidan
    if (password !== confirmPassword) {
      showError("confirm_password", "Las contraseñas no coinciden."); // Mostramos un mensaje de error
      hasErrors = true; // Marcamos que hay un error
    }

    // Si hay errores, no continuamos con el envío del formulario
    if (hasErrors) return;

    // Si no hay errores, verificamos si el correo ya está registrado
    try {
      // Hacemos una petición asíncrona para comprobar el registro
      const response = await fetch("/api/check_register", {
        method: "POST", // Indicamos que es un método POST
        headers: {
          "Content-Type": "application/json", // Especificamos que el contenido es en formato JSON
        },
        body: JSON.stringify({ email }), // Enviamos el correo en el cuerpo de la petición
      });

      const result = await response.json(); // Esperamos la respuesta y la convertimos a JSON

      // Si la verificación falla, mostramos un mensaje de error
      if (!result.success) {
        if (result.errors.email) showError("email", result.errors.email); // Mostramos el error de correo si existe
      } else {
        form.submit(); // Si todo está bien, enviamos el formulario
      }
    } catch (error) {
      console.error("Error:", error); // Si ocurre un error en la petición, lo mostramos en la consola
    }
  });

  // Función para mostrar un mensaje de error junto al campo correspondiente
  function showError(fieldName, message) {
    const field = document.querySelector(`input[name="${fieldName}"]`); // Seleccionamos el campo de entrada correspondiente
    const errorMessage = document.createElement("p"); // Creamos un nuevo párrafo para el mensaje de error
    errorMessage.className = "error-message"; // Asignamos una clase para estilos
    errorMessage.innerText = message; // Establecemos el texto del mensaje de error
    field.parentNode.insertBefore(errorMessage, field.nextSibling); // Insertamos el mensaje de error después del campo
  }

  // Función para limpiar los mensajes de error previos
  function clearErrors() {
    const errorMessages = document.querySelectorAll(".error-message"); // Seleccionamos todos los mensajes de error existentes
    errorMessages.forEach((message) => message.remove()); // Eliminamos cada mensaje de error
  }

  // Función para validar el formato del correo electrónico
  function validateEmail(email) {
    const regex = /[^@]+@[^@]+\.[^@]+/; // Expresión regular para validar el formato del correo
    return regex.test(email); // Devolvemos true si el correo cumple con el formato
  }
});
