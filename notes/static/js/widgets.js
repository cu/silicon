/*
 * Return a widget object.
 *
 * Params:
 * `target`: the id of any element containing a `data-widget-url` attribute
 *
 * Returns an object containing:
 * `element`: the element in the DOM
 * `url`: a URL as specified in the element's `data-widget-url` attribute
 */
function get_widget(target) {
    const widget_element = document.querySelector(target);

    return {
        element: widget_element,
        url: widget_element.getAttribute("data-widget-url")
    };
}

/*
 * Set up relation add button event.
 */
function relation_add_button() {
    document.querySelector("#add-relation-btn")
        .addEventListener("click", (event) => {
            const relative = window.prompt("Related page title");

            if (relative === null) {
                // The user clicked cancel
                return;
            }

            const widget = get_widget("#related-links");
            fetch(widget.url, {
                method: "POST",
                body: new URLSearchParams({relative: relative}),
                headers: new Headers({
                    "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
                })
            })
            .then(response => {
                if (response.ok) {
                    return response.text();
                }
                throw new Error(`Error fetching ${response.url}, got ${response.status}`);
            })
            .then(html => {
                widget.element.innerHTML = html;
                relation_delete_buttons();
            })
            .catch(err => {
                console.error(err);
            });
        });
}

/*
 * Set up relation delete button events.
 */
function relation_delete_buttons() {
    const del_btns = document.querySelectorAll(".del-relation-btn")
    const widget = get_widget("#related-links");

    del_btns.forEach(function(btn) {
        const relative = btn.getAttribute("data-del-relative");
        btn.addEventListener("click", (event) => {
            const answer = window.confirm(`Delete this page's relationship to ${relative}?`);
            if (answer === true) {
                fetch(`${widget.url}/${relative}`, {
                    method: "DELETE",
                }).then(response => {
                    return response.text();
                }).then(html => {
                    widget.element.innerHTML = html;
                    relation_delete_buttons();
                })
            }
        });
    });
}


/*
 * Set up the table of contents update button.
 */
function toc_update_button() {
    if (!document.querySelector("#body-text")) {
        // we're not on the edit page, nothing to do
        return;
    }

    document.querySelector("#update-toc").style.visibility = 'visible';

    document.querySelector("#update-toc-btn")
        .addEventListener("click", (event => {
            const widget = get_widget("#toc");

            fetch(widget.url, {
                method: "POST",
                body: new URLSearchParams(
                    {body: document.querySelector("#body-text").value}
                ),
                headers: new Headers({
                    "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
                })
            })
            .then(response => {
                if (response.ok) {
                    return response.text();
                }
                throw new Error(`Error fetching ${response.url}, got ${response.status}`);
            })
            .then(html => {
                widget.element.innerHTML = html;
            })
            .catch(err => {
                console.error(err);
            });

        }));
}


/*
 * Set up all the page events.
 */
window.addEventListener("load", function() {
    relation_add_button();
    relation_delete_buttons();
    toc_update_button();

    const editor = document.querySelector("#body-text");
    if (editor) {
        editor.focus();
    }
});
