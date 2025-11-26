const initData = window.Telegram.WebApp.initData;

async function authorize() {
    const res = await fetch("https://authsrv.onrender.com/auth/telegram", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ initData })
    });

    const data = await res.json();

    if (data.ok) {
        localStorage.setItem("token", data.token);
        showProfile(data.profile);
    } else {
        document.getElementById("profile").innerText = "Ошибка авторизации";
    }
}

function showProfile(profile) {
    document.getElementById("profile").innerHTML = `
    <p>Email: ${profile.email}</p>
    <img src="${profile.avatar || 'https://via.placeholder.com/100'}" width="100" />
  `;
}

document.getElementById("avatarInput").addEventListener("change", async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("avatar", file);

    await fetch("https://authsrv.onrender.com/user/avatar", {
        method: "POST",
        headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
        },
        body: formData
    });

    alert("Аватар загружен!");
});

authorize();
