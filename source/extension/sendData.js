(function () {
  // const intervalId = setInterval(sendData, 500000); // Every 5 minutes
  const intervalId = setInterval(sendData, 120000); // Every 2 minutes

  function sendData() {
    browser.tabs.query({ currentWindow: true }, getTabData);
  }

  function getTabData(tabs) {
    let activity_data = {};
    tabs.forEach((tab) => {
      let activity_data_tab = {
        id: tab.id,
        title: tab.title,
        url: tab.url,
        isActive: tab.active,
        lastAcess: tab.lastAccessed,
        upTime: 0,
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

  // function cleanUp() {
  //   setTimeout(() => {
  //     clearInterval(intervalId);
  //   }, 10000000);
  // }
})();
