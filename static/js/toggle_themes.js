// Adapted from https://albertoroura.com/building-a-theme-switcher-for-bootstrap/

// These lines are to prevent the flash/flicker from the delay of DOMContentLoaded and also the flash that would happen if auto is dark.
const currentMode = localStorage.getItem('bs-theme');
if (currentMode) {
    document.documentElement.setAttribute('data-bs-theme', currentMode);
} else {
    document.documentElement.setAttribute('data-bs-theme', window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
}

document.addEventListener("DOMContentLoaded", ()=>{
    function setTheme (mode = 'auto') {
        const userMode = localStorage.getItem('bs-theme');
        const sysMode = window.matchMedia('(prefers-color-scheme: light)').matches;
        const useSystem = mode === 'system' || (!userMode && mode === 'auto');
        const modeChosen = useSystem ? 'system' : mode === 'dark' || mode === 'light' ? mode : userMode;

        if (useSystem) {
          localStorage.removeItem('bs-theme');
        } else {
          localStorage.setItem('bs-theme', modeChosen);
        }

        document.documentElement.setAttribute('data-bs-theme', useSystem ? (sysMode ? 'light' : 'dark') : modeChosen);
        document.querySelectorAll('.mode-switch .btn').forEach(e => e.classList.remove('active', 'fw-semibold'));
        Array.from(document.getElementsByClassName('themeCheck')).forEach(e => e.remove());

        const modeChosenButton = document.getElementById(modeChosen);
        modeChosenButton.classList.add('active', 'fw-semibold');
        modeChosenButton.innerHTML += '<i class="bi bi-check2 themeCheck ms-3"></i>';
        document.getElementById('themeButton').getElementsByTagName('i')[0].classList = modeChosenButton.getElementsByTagName('i')[0].classList;
    }

    setTheme();
    document.querySelectorAll('.mode-switch .btn').forEach(e => e.addEventListener('click', () => setTheme(e.id)));
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => setTheme());
});
