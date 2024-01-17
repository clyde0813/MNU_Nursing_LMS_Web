window.onload = function () {
    const deadlineSelectableButton = document.getElementsByClassName("deadline-selectable-button")[0];
    const deadlineDateInput = document.getElementById("deadline-date");

    deadlineSelectableButton.addEventListener('click', (e) => {
        if (deadlineDateInput.hidden) {
            deadlineDateInput.hidden = false;
            deadlineSelectableButton.children[1].src = "/static/img/icon/minus-button.png"
        } else {
            deadlineDateInput.hidden = true;
            deadlineDateInput.value = null;
            deadlineSelectableButton.children[1].src = "/static/img/icon/plus-button.png"
        }
    })
}