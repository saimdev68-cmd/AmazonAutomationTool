document.addEventListener("DOMContentLoaded", function () {
    // Target both standard Django password field names 
    const passwordFields = document.querySelectorAll(
        '.profitlens-login-wrapper input[name="password1"], .profitlens-login-wrapper input[name="password2"]'
    );

    passwordFields.forEach(function (inputField) {
        // Create the tactical interactive eye node
        const toggleButton = document.createElement("span");
        toggleButton.className = "password-toggle-trigger";
        
        // Insert node directly behind the target input field inside its paragraph wrapper
        inputField.parentNode.insertBefore(toggleButton, inputField.nextSibling);

        // Core interactive show/hide listener logic
        toggleButton.addEventListener("click", function () {
            if (inputField.type === "password") {
                inputField.type = "text";
                toggleButton.classList.add("is-hidden");
            } else {
                inputField.type = "password";
                toggleButton.classList.remove("is-hidden");
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Target password, password1, and password2 to cover both login and signup forms
    const passwordFields = document.querySelectorAll(
        '.profitlens-login-wrapper input[name="password"], .profitlens-login-wrapper input[name="password1"], .profitlens-login-wrapper input[name="password2"]'
    );

    passwordFields.forEach(function (inputField) {
        // Create the tactical interactive eye node
        const toggleButton = document.createElement("span");
        toggleButton.className = "password-toggle-trigger";
        
        // Insert node directly behind the target input field inside its paragraph wrapper
        inputField.parentNode.insertBefore(toggleButton, inputField.nextSibling);

        // Core interactive show/hide listener logic
        toggleButton.addEventListener("click", function () {
            if (inputField.type === "password") {
                inputField.type = "text";
                toggleButton.classList.add("is-hidden");
            } else {
                inputField.type = "password";
                toggleButton.classList.remove("is-hidden");
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Selectors for all possible password field variations across Django's auth forms
    const passwordSelectors = [
        '.profitlens-login-wrapper input[name="password"]',
        '.profitlens-login-wrapper input[name="password1"]',
        '.profitlens-login-wrapper input[name="password2"]',
        '.profitlens-login-wrapper input[name="new_password1"]',
        '.profitlens-login-wrapper input[name="new_password2"]'
    ].join(', ');

    const passwordFields = document.querySelectorAll(passwordSelectors);

    passwordFields.forEach(function (inputField) {
        // Create the tactical interactive eye node
        const toggleButton = document.createElement("span");
        toggleButton.className = "password-toggle-trigger";
        
        // Insert node directly behind the target input field inside its paragraph wrapper
        inputField.parentNode.insertBefore(toggleButton, inputField.nextSibling);

        // Core interactive show/hide listener logic
        toggleButton.addEventListener("click", function () {
            if (inputField.type === "password") {
                inputField.type = "text";
                toggleButton.classList.add("is-hidden");
            } else {
                inputField.type = "password";
                toggleButton.classList.remove("is-hidden");
            }
        });
    });
});