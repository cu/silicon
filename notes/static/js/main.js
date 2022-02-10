window.addEventListener("load", function() {
    console.log("I'm in yer function");
    document.querySelector("[data-toggle='nav-top']")
        .addEventListener('click', (event) => {
                const elements = document.querySelectorAll("[data-toggle='nav-shift']");

                elements.forEach(function(element) {
                    element.classList.toggle('shift');
                })
        })
});
