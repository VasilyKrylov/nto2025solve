import TuyAPI from "tuyapi";

const CODES = {
  ...
  107: "VERSION_INFORMATION",
  118: "SYSTEM_COMMANDS",
  ...
};

function translate(dps) {
  const translated = {};
  for (const [key, value] of Object.entries(dps)) {
    translated[CODES[key]] = value;
  }
  return translated;
}

const device = new TuyAPI({
  id: "DEVICE_IDENTIFICATOR",
  key: "LOCAL_KEY",
});

device.find({ timeout: 20 }).then(() => {
  console.log("Found device:", device.device);
  device.connect();
});

device.on("connected", () => {
  console.log("Connected to device!");

  const f = () => {
    device
     .set({
      dps: CODE,
      set: 'VALUE',
      shouldWaitForResponse: false,
     });
  };
  setTimeout(f, 1000);
});

device.on("disconnected", () => {
  console.log("Disconnected from device.");
});

device.on("error", (error) => {
  console.log("Error!", error);
});

device.on("data", (data, commandByte, sequenceN) => {
  console.log("Data:", translate(data.dps));
});

device.on("dp-refresh", (data, commandByte, sequenceN) => {
  console.log("Refresh:", translate(data.dps));
});

setTimeout(() => {
  device.disconnect();
}, 300_000);
