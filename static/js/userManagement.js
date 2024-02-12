var passwordResetId;
var userDeleteId;
var billDeleteId;
var itemDeleteId;

function copy(id, ctx) {
  // copy to clipboard
  navigator.clipboard.writeText(id);

  // show feedback to user
  const button = ctx ? ctx : document.getElementById(id + "-copy"); // hack to allow for the correct button to have the feedback, should have just done this for all buttons but too late now
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
    });
}

function setBillDeleteId(id) {
  billDeleteId = id;
}

function handleBillDelete() {
  fetch("/api/admin/bills/delete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: billDeleteId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) return alert("Failed to delete bill");
      window.location = window.location.href;
    });
}

function handleItemCreate(data) {
  Object.keys(data).forEach(function (key) {
    data[key] = data[key].value;
  });

  let {
    ownerId,
    itemDescription,
    address,
    damageDescription,
    damageDate,
    repairDescription,
    repairDate,
    subscriptionType,
    subscriptionStartDate,
    subscriptionDuration,
  } = data;

  damageDate &&= new Date(damageDate).getTime();
  repairDate &&= new Date(repairDate).getTime();
  subscriptionStartDate &&= new Date(subscriptionStartDate).getTime();

  fetch("/api/admin/items/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ownerId,
      itemDescription,
      address,
      damageDescription,
      damageDate,
      repairDescription,
      repairDate,
      subscriptionType,
      subscriptionStartDate,
      subscriptionDuration,
    }),
  })
    .then((response) => response.json())
    .then(handleCreateItemData);
}

const errorToId = {
  NO_ID: {  // should never happen
    ids: ["ownerId"],
  },
  USER_NOT_FOUND: {
    ids: ["ownerId"],
  },
  NO_ITEM_DESCRIPTION: { // should never happen
    ids: ["itemDescription"],
  },
  DAMAGE_INCOMPLETE: {
    ids: ["damageDescription", "damageDate"],
  },
  REPAIR_INCOMPLETE: {
    ids: ["repairDescription", "repairDate"],
  },
  NO_SUBSCRIPTION_TYPE: {
    ids: ["subscriptionType"],
  },
  NO_SUBSCRIPTION_DATE: {
    ids: ["subscriptionStartDate"],
  },
};

const validationIds = [
  "ownerId",
  "itemDescription",
  "damageDescription",
  "damageDate",
  "repairDescription",
  "repairDate",
  "subscriptionType",
  "subscriptionStartDate",
  "subscriptionDuration",
];

function handleCreateItemData(d) {
  // clear validation
  for (const id of validationIds) {
    document.getElementById(id).classList.remove("is-invalid", "is-valid");
  }

  let temp = validationIds;

  const { errors } = d;
  if (errors && errors.length) {
    for (const error of errors) {
      const index = temp.indexOf(error);
      if (index > -1) {
        // only splice array when item is found
        temp.splice(index, 1); // 2nd parameter means remove one item only
      }

      const { feedback, ids } = errorToId[error];
      for (const id of ids) {
        document.getElementById(id).classList.add("is-invalid");
      }
    }

    for (const valid of temp) {
      document.getElementById(valid).classList.add("is-valid")
    }

    return false;
  }

  window.location = window.location.href;
}

function setItemDeleteId(id) {
  itemDeleteId = id;
}

function handleItemDelete() {
  fetch("/api/admin/items/delete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: itemDeleteId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) return alert("Failed to delete item");
      window.location = window.location.href;
    });
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

  const billSelects = document.getElementsByClassName("admin-bill-select");
  for (const select of billSelects) {
    select.addEventListener("change", () => {
      const value = select.value;
      const id = select.id.substring(
        0,
        select.id.length - 18 /* 18 is length of '-admin-bill-select'*/
      );

      const data = {
        id,
        status: value === "paid",
      };
      console.log(data);

      fetch("/api/admin/invoices/status", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.success) return alert("Failed to update invoice status");
        });
    });
  }
})();
