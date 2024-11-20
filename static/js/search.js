const tabNames = ["users", "posts"];
var current = '';

function switchTabs(tab) {
    if (current == tab.id) return;
    current = tab.id;

    tab.setAttribute("aria-current", true);
    tab.classList.add("active", "bg-light-subtle");
    tab.style = "border-color: var(--bs-border-color-translucent);";
    document.getElementById(`${tab.id}Content`).classList.remove('d-none');

    tabNames.forEach(e => {
        if (e == tab.id) return;
        document.getElementById(e).style = "";
        document.getElementById(e).removeAttribute("aria-current");
        document.getElementById(e).classList.remove("active", "bg-light-subtle");
        document.getElementById(`${e}Content`).classList.add('d-none');
    });

    document.getElementById("card").style.width = tab.id == "users" ? "400px" : "720px";
}


document.addEventListener("DOMContentLoaded", ()=>{
    const urlParams = new URLSearchParams(window.location.search);
    const type = urlParams.get('type');

    if (!type || !tabNames.includes(type)) {
        switchTabs(document.getElementById("users"));
    } else {
        switchTabs(document.getElementById(type));
    }
});
