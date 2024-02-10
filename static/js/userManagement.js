var passwordResetId;
var userDeleteId;

function copy(id) {
  // copy to clipboard
  navigator.clipboard.writeText(id);

  // show feedback to user
  const button = document.getElementById(id + "-copy");
  button.innerHTML = "Copied";
  button.classList.remove("btn-light", "border-2");
  button.classList.add("btn-success", "border-0");
  setTimeout(() => {
    button.innerHTML = "Copy";
    button.classList.remove("btn-success", "border-0");
    button.classList.add("btn-light", "border-2");
  }, 700);
}

function setPasswordResetId(id) {
  passwordResetId = id;
}

function handlePasswordReset(password, confirm) {
  const passwordField = document.getElementById("floatingPassword");
  const confirmField = document.getElementById("floatingConfirm");

  const passwordFeedback = document.getElementById("password-feedback");
  const confirmFeedback = document.getElementById("confirm-feedback");

  // clear previous feedback
  passwordField.classList.remove("border-danger");
  confirmField.classList.remove("border-danger");
  passwordFeedback.classList.remove("text-danger");
  confirmFeedback.classList.remove("text-danger");
  passwordFeedback.innerHTML = "";
  confirmFeedback.innerHTML = "";

  if (password !== confirm) {
    passwordField.classList.add("border-danger");
    confirmField.classList.add("border-danger");

    confirmFeedback.classList.add("text-danger");
    confirmFeedback.innerHTML = "Passwords do not match";
    return;
  }

  if (
    password.length < 8 ||
    password.length > 20 ||
    !password.match(/[A-Z]/g) ||
    !password.match(/[a-z]/g) ||
    !password.match(/[0-9]/g) ||
    !password.match(/[@!#$%&? "]/g) /* praying this doesnt break */
  ) {
    passwordField.classList.add("border-danger");
    passwordFeedback.classList.add("text-danger");
    passwordFeedback.innerHTML =
      "Use 8 or more characters with a mix of letters numbers and symbols.";
    return;
  }

  const data = {
    id: passwordResetId,
    password,
  };


  fetch("/api/admin/password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) return alert("Failed to reset password");
      window.location.reload();
    });
}

function handleSearch(search) {
  const isEmail = validateEmail(search);
  const data = {
    search,
    isEmail,
  };

  fetch("/api/admin/search", {

  });

  alert(JSON.stringify(data))
}

const validateEmail = (email) => {
  const str = String(email)
  .toLowerCase()
  .match(
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
  
  return str !== null; /* praying this works also */
};

function setUserDeleteId(id) {
  userDeleteId = id;
}

function handleDelete() {
  fetch("/api/admin/delete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: userDeleteId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) return alert("Failed to delete user");
      window.location = window.location.href;
  })
}

// change event listener for each admin select
(() => {
  const selects = document.getElementsByClassName("admin-select");

  for (const select of selects) {
    select.addEventListener("change", () => {
      const value = select.value;
      const id = select.id.substring(
        0,
        select.id.length - 13 /* 13 is length of '-admin-select'*/
      );

      const data = {
        id,
        role: value === "admin",
      };
      console.log(value);

      fetch("/api/admin/roles", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.success) return alert("Failed to update role");
        });
    });
  }
})();
