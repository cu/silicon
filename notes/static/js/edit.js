// Object for state
var wiki_edit = {};

// Default values
wiki_edit.changed = false;
wiki_edit.submit_clicked = false;

window.onload = function() {
    document.querySelector('#body-text')
        .addEventListener('input', (event) => wiki_edit.changed = true);

    // don't nag if the Submit button was clicked
    document.querySelector('#page-form').onsubmit = function() {
        wiki_edit.submit_clicked = true;
    };

    window.addEventListener('beforeunload', function (e) {
        /* alert on changed codemirror
        if ((! cm_instance.isClean() && ! wiki_edit.submit_clicked)) {
            e.preventDefault();
            e.returnValue = '';
        }
        */
        // alert on changed textarea
        if ((wiki_edit.changed && ! wiki_edit.submit_clicked)) {
            e.preventDefault();
            e.returnValue = '';
        }
    });

};
