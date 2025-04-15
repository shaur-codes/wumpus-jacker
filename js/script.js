// ----------------------------------
// SELECTING ELEMENTS
// ----------------------------------
const loginButton = document.querySelector("button");

// -----------------------------------
// ELLIPSIS ANIMATION
// ------------------------------------
function removeEllipsisAnimation() {
  loginButton.innerHTML = "";
  loginButton.textContent = "Log In";
  loginButton.removeAttribute("disabled");
}

function animateEllipsis() {
  loginButton.innerHTML = "";
  loginButton.innerHTML = `<span class="spinner" role="img" aria-label="Loading">
                                    <span class="inner pulsingEllipsis">
                                        <span class="item spinnerItem"></span>
                                        <span class="item spinnerItem"></span>
                                        <span class="item spinnerItem"></span>
                                    </span>
                           </span>`;
  const spinnerItems = document.querySelectorAll(".spinnerItem");
  spinnerItems.forEach((item, index) => {
    item.style.animation = `spinner-pulsing-ellipsis 1.4s infinite ease-in-out ${
      index * 0.2
    }s`;
  });
  loginButton.setAttribute("disabled", "true");

  setTimeout(removeEllipsisAnimation, 3000);
}

// --------------------------------------------------
// ---------- FETCH REQUESTS WITH NGROK HEADER -----
// --------------------------------------------------
async function fetchWithNgrok(url) {
  try {
    const response = await fetch(url, {
      headers: {
        "ngrok-skip-browser-warning": "true",
        "User-Agent": "CustomAgent/1.0",
      },
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch request failed:", error);
    return null;
  }
}

// --------------------------------------------------
// ---------- WANDERING CUBES ANIMATION -------------
// --------------------------------------------------

function generateRandomString() {
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let result = "";
  for (let i = 0; i < 43; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}

function removeQrCodeAnimation() {
  const qrCodeContainer = document.querySelector(".right-section .qr-code");
  qrCodeContainer.innerHTML = "";
  qrCodeContainer.insertAdjacentElement(
    "afterbegin",
    generateQRCode(`https://discord.com/ra/${generateRandomString()}`)
  );
  qrCodeContainer.insertAdjacentHTML(
    "beforeend",
    `<img src="./assets/qrcode-discord-logo.png" alt="Discord Logo">`
  );
  qrCodeContainer.style.background = "white";
}

function simulateQrCodeChange() {
  const qrCodeContainer = document.querySelector(".right-section .qr-code");
  qrCodeContainer.removeChild(qrCodeContainer.querySelector("svg"));
  qrCodeContainer.removeChild(qrCodeContainer.querySelector("img"));
  qrCodeContainer.style.background = "transparent";

  const markup = `<span
  class="spinner qrCode-spinner"
  role="img"
  aria-label="Loading"
  aria-hidden="true"
  >
  <span class="inner wanderingCubes">
    <span class="item"></span>
    <span class="item"></span>
  </span>
</span>`;

  qrCodeContainer.insertAdjacentHTML("afterbegin", markup);

  setTimeout(removeQrCodeAnimation, 3500);
}

setInterval(simulateQrCodeChange, 120 * 1000);

// --------------------------------------------------
// ---------- GENERATING QRCODE ---------------------
// --------------------------------------------------
function generateQRCode(data) {
  try {
    const qr = qrcode(0, "L");
    qr.addData(data);
    qr.make();

    const moduleCount = qr.getModuleCount();
    const svgString = qr.createSvgTag(1, 0);

    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(svgString, "image/svg+xml");
    const svgElement = svgDoc.documentElement;

    svgElement.setAttribute("width", "160");
    svgElement.setAttribute("height", "160");
    svgElement.setAttribute("viewBox", "0 0 37 37");

    const path = svgElement.querySelector("path");
    if (path) {
      path.setAttribute("transform", `scale(${37 / moduleCount})`);
    }

    return svgElement;
  } catch (error) {
    console.error("Error generating QR code:", error);
    return null;
  }
}

// --------------------------
// ATTACHING EVENT LISTENERS
// --------------------------
loginButton.addEventListener("click", animateEllipsis);
document.addEventListener("contextmenu", function (e) {
  e.preventDefault();
});

// ------------------------------
// EXAMPLE USAGE OF NGROK FETCH
// ------------------------------
async function checkQrStatus() {
  const qrData = await fetchWithNgrok("/qr-check?t=" + Date.now());
  if (qrData) {
    console.log("QR Status:", qrData);
  }
}

// Run QR status check every 10 seconds
setInterval(checkQrStatus, 10000);
