function formatText(command) {
    document.execCommand(command, false, null);
}
function addLink() {
    const url = prompt("Введите URL:");
    if (url) {
        document.execCommand('createLink', false, url);
    }
}

function addImage() {
    const url = prompt("Введите URL изображения:");
    if (url) {
        document.execCommand('insertImage', false, url);
    }
}

function toggleToolbar(show) {
    const toolbar = document.getElementById('toolbar');
    toolbar.style.visibility = show ? 'visible' : 'hidden';
}
