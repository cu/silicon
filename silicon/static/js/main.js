window.addEventListener("load", function () {
    /* Toggle nav sidebar in "mobile" mode */
    document
        .querySelector("[data-toggle='nav-top']")
        .addEventListener("click", (event) => {
            const elements = document.querySelectorAll(
                "[data-toggle='nav-shift']"
            );

            elements.forEach(function (element) {
                element.classList.toggle("shift");
            });
        });
});
