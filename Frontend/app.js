var API = "http://localhost:5000";

/* ─────────────────────────────────────────────────────────────
   SESSION
───────────────────────────────────────────────────────────── */

function getSession() {
  return {
    device_id: localStorage.getItem("device_id"),
    name:      localStorage.getItem("name"),
    email:     localStorage.getItem("email"),
  };
}

function saveSession(device_id, name, email) {
  localStorage.setItem("device_id", device_id);
  localStorage.setItem("name",      name);
  localStorage.setItem("email",     email);
}

function clearSession() {
  ["device_id", "name", "email",
   "reg_device_id", "reg_name", "reg_email", "reg_password", "reg_medical"]
    .forEach(function(k) { localStorage.removeItem(k); });
}

function logout() {
  clearSession();
  window.location.href = "Login.html";
}

/* ─────────────────────────────────────────────────────────────
   UI HELPERS
───────────────────────────────────────────────────────────── */

function showMsg(type, text) {
  var el = document.getElementById("msg");
  if (!el) return;
  el.className   = "msg " + type;
  el.textContent = text;
}

function setBtn(id, text, disabled) {
  var btn = document.getElementById(id);
  if (!btn) return;
  btn.textContent = text;
  btn.disabled    = disabled;
}

function chipClass(press) {
  var p = parseInt(press);
  return p === 1 ? "chip-fam" : p === 2 ? "chip-pol" : "chip-med";
}

function chipLabel(press) {
  var p = parseInt(press);
  return p === 1 ? "Family" : p === 2 ? "Police" : "Medical";
}

function timeAgo(iso) {
  var diff = Math.floor((Date.now() - new Date(iso)) / 1000);
  if (diff < 60)    return diff + "s ago";
  if (diff < 3600)  return Math.floor(diff / 60) + "m ago";
  if (diff < 86400) return Math.floor(diff / 3600) + "h ago";
  return new Date(iso).toLocaleDateString("en-GB");
}

/* ─────────────────────────────────────────────────────────────
   PAGE INIT
───────────────────────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", function () {

  /* ── REGISTER FORM — Register.html ───────────────────────── */
  var registerForm = document.getElementById("registerForm");
  if (registerForm) {

    registerForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      setBtn("submitBtn", "Checking...", true);

      var device_id     = document.getElementById("device_id").value.trim();
      var name          = document.getElementById("name").value.trim();
      var email         = document.getElementById("email").value.trim();
      var password      = document.getElementById("password").value;
      var medical_notes = document.getElementById("medical_notes").value.trim();

      if (!device_id || !name || !email || !password) {
        showMsg("err", "Please fill in all required fields.");
        setBtn("submitBtn", "Continue to contacts →", false);
        return;
      }

      try {
        // check device already registered
        var check = await fetch(API + "/user/" + device_id);

        if (check.ok) {
          showMsg("err", "This device is already registered. Please sign in instead.");
          setBtn("submitBtn", "Continue to contacts →", false);
          return;
        }

        if (check.status !== 404) {
          throw new Error("Server error. Please try again.");
        }

        // save temporarily and move to contacts step
        localStorage.setItem("reg_device_id",  device_id);
        localStorage.setItem("reg_name",        name);
        localStorage.setItem("reg_email",       email);
        localStorage.setItem("reg_password",    password);
        localStorage.setItem("reg_medical",     medical_notes);

        window.location.href = "1timeUser.html";

      } catch (err) {
        showMsg("err", err.message || "Could not reach the server. Is it running?");
        setBtn("submitBtn", "Continue to contacts →", false);
      }
    });
  }

  /* ── LOGIN FORM — Login.html ─────────────────────────────── */
  var loginForm = document.getElementById("loginForm");
  if (loginForm) {

    loginForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      setBtn("submitBtn", "Signing in...", true);

      var device_id = document.getElementById("device_id").value.trim();
      var password  = document.getElementById("password").value;

      if (!device_id || !password) {
        showMsg("err", "Please enter your device ID and password.");
        setBtn("submitBtn", "Sign in →", false);
        return;
      }

      try {
        var res  = await fetch(API + "/login", {
          method:  "POST",
          headers: { "Content-Type": "application/json" },
          body:    JSON.stringify({ device_id: device_id, password: password }),
        });

        var data = await res.json();

        if (res.ok) {
          saveSession(data.device_id, data.name, data.email);
          window.location.href = "Dashboard.html";
        } else {
          showMsg("err", data.error || "Sign in failed. Check your device ID and password.");
          setBtn("submitBtn", "Sign in →", false);
        }

      } catch (err) {
        showMsg("err", "Could not reach the server. Make sure server_start.py is running.");
        setBtn("submitBtn", "Sign in →", false);
      }
    });
  }

  /* ── CONTACT SETUP FORM — 1timeUser.html ────────────────── */
  var setupForm = document.getElementById("setupForm");
  if (setupForm) {

    // guard — no pending registration means someone landed here directly
    if (!localStorage.getItem("reg_device_id")) {
      window.location.href = "Register.html";
      return;
    }

    setupForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      setBtn("submitBtn", "Saving...", true);

      var c1name  = document.getElementById("c1_name").value.trim();
      var c1phone = document.getElementById("c1_phone").value.trim();
      var c2name  = document.getElementById("c2_name").value.trim();
      var c2phone = document.getElementById("c2_phone").value.trim();
      var c3name  = document.getElementById("c3_name").value.trim();
      var c3phone = document.getElementById("c3_phone").value.trim();

      if (!c1name || !c1phone || !c2name || !c2phone || !c3name || !c3phone) {
        showMsg("err", "Please fill in all 3 emergency contacts.");
        setBtn("submitBtn", "Save contacts & go to dashboard →", false);
        return;
      }

      var payload = {
        device_id:     localStorage.getItem("reg_device_id"),
        name:          localStorage.getItem("reg_name"),
        email:         localStorage.getItem("reg_email"),
        password:      localStorage.getItem("reg_password"),
        medical_notes: localStorage.getItem("reg_medical"),
        contacts: {
          "1": { name: c1name,  phone: c1phone },
          "2": { name: c2name,  phone: c2phone },
          "3": { name: c3name,  phone: c3phone },
        },
      };

      try {
        var res  = await fetch(API + "/register", {
          method:  "POST",
          headers: { "Content-Type": "application/json" },
          body:    JSON.stringify(payload),
        });

        var data = await res.json();

        if (res.ok) {
          saveSession(payload.device_id, payload.name, payload.email);

          // clear temp reg data
          ["reg_device_id", "reg_name", "reg_email", "reg_password", "reg_medical"]
            .forEach(function (k) { localStorage.removeItem(k); });

          showMsg("ok", "Account created! Taking you to the dashboard...");
          setTimeout(function () { window.location.href = "Dashboard.html"; }, 1200);

        } else {
          showMsg("err", data.error || "Registration failed. Please try again.");
          setBtn("submitBtn", "Save contacts & go to dashboard →", false);
        }

      } catch (err) {
        showMsg("err", "Could not reach the server. Make sure server_start.py is running.");
        setBtn("submitBtn", "Save contacts & go to dashboard →", false);
      }
    });
  }

  /* ── DASHBOARD — Dashboard.html ─────────────────────────── */
  var alertList = document.getElementById("alertList");
  if (alertList) {
    var session = getSession();

    if (!session.device_id) {
      window.location.href = "Login.html";
      return;
    }

    var navUser = document.getElementById("nav-user");
    if (navUser) navUser.textContent = "Hi, " + (session.name || "");

    loadAlerts();
    setInterval(loadAlerts, 10000); // refresh every 10s
  }

});

/* ─────────────────────────────────────────────────────────────
   SEND ALERT  (called by dashboard buttons)
───────────────────────────────────────────────────────────── */

function sendAlert(press_count) {
  var session = getSession();
  if (!session.device_id) {
    window.location.href = "Login.html";
    return;
  }

  if (!navigator.geolocation) {
    alert("Your browser does not support geolocation.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async function (pos) {
      try {
        var res = await fetch(API + "/alert", {
          method:  "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            device_id:   session.device_id,
            press_count: press_count,
            lat:         pos.coords.latitude,
            lon:         pos.coords.longitude,
          }),
        });

        var data = await res.json();

        if (res.ok) {
          loadAlerts();
        } else {
          alert("Error: " + (data.error || "Alert failed."));
        }

      } catch (err) {
        alert("Could not reach the server. Is it running?");
      }
    },
    function () {
      alert("Location access is required. Please allow it in your browser settings.");
    }
  );
}

/* ─────────────────────────────────────────────────────────────
   LOAD ALERT LIST
───────────────────────────────────────────────────────────── */

async function loadAlerts() {
  var list = document.getElementById("alertList");
  if (!list) return;

  var session = getSession();

  try {
    var res  = await fetch(API + "/alerts?per_page=200");
    var data = await res.json();
    var all  = data.alerts || [];

    // only show alerts belonging to this device
    var alerts = all.filter(function (a) {
      return a.device_id === session.device_id;
    });

    if (alerts.length === 0) {
      list.innerHTML = '<div class="empty-state">No alerts sent yet.</div>';
      return;
    }

    list.innerHTML = alerts.map(function (a) {
      return (
        '<div class="alert-item">' +
          '<span class="alert-chip ' + chipClass(a.press_count) + '">' + chipLabel(a.press_count) + '</span>' +
          '<div class="alert-body">' +
            '<strong>' + (a.user_name || "Device") + '</strong>' +
            '<span>Contact: ' + a.contact_name + ' &middot; ' + a.contact_phone + '</span>' +
            '&ensp;<a href="https://maps.google.com/?q=' + a.lat + ',' + a.lon + '" target="_blank">View location &rarr;</a>' +
          '</div>' +
          '<span class="alert-time">' + timeAgo(a.time) + '</span>' +
        '</div>'
      );
    }).join("");

  } catch (err) {
    list.innerHTML = '<div class="empty-state">Could not load alerts. Check your server is running.</div>';
  }
}