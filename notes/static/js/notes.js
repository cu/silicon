$(document).ready(function() {
    $("[data-toggle='nav-top']").click(function() {
        console.log("click!");
        $("[data-toggle='nav-shift']").toggleClass("shift");
        $("[data-toggle='nav-bottom']").toggleClass("shift");
    })
});
