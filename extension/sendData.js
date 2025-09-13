(function () {
  browser.tabs.query({ currentWindow: true }, getTabData);

  function getTabData(tabs) {
    let activity_data = {};
    tabs.forEach((tab) => {
      let activity_data_tab = {
        isActive: tab.active,
        url: tab.url,
        title: tab.title,
      };

      activity_data[`${tab.id}`] = activity_data_tab;
    });

    fetch("http://127.0.0.1:5000/log-activity", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(activity_data),
    }).catch((error) => console.error("Error sending data to python: ", error));
  }
})();
