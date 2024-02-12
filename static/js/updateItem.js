function handleUpdateDamage(data) {
  const { id, damageDescription, damageDate } = data;
  fetch("/api/admin/items/update/damage", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id,
      description: damageDescription,
      date: new Date(damageDate).getTime(),
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (!data.success)
        return alert(
          "Failed to update damage, you must input at least 1 field."
        );
      window.location.reload();
    });
}

function handleUpdateCurrentRepair(data) {
  console.log("ran");
  const { id, description, startDate, endDate } = data;

  console.log(data);
  fetch("/api/admin/items/update/repair", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id,
      description,
      startDate: new Date(startDate).getTime(),
      endDate: new Date(endDate).getTime(),
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (!data.success)
        return alert(
          "Failed to update repair, you must input at least 1 field."
        );
        window.location.reload();
    });
}

function handleUpdateSubscription(data) {
  const { id, type, startDate, duration } = data;

  console.log(data);
  fetch("/api/admin/items/update/subscription", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id,
      type,
      startDate: new Date(startDate).getTime(),
      duration,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (!data.success)
        return alert(
          "Failed to update subscription, you must input at least 1 field."
        );
        window.location.reload();
    });
}
