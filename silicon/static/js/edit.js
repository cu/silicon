// object for editor state
var editor = {
    changed: false,
    submit_clicked: false,
};

if (silicon_editor === "codemirror") {
    var cm_instance;
}

function usurp_unload(e) {
    e.preventDefault();
    e.returnValue = "";
}

window.addEventListener("load", function () {
    // load CodeMirror instance
    if (silicon_editor === "codemirror") {
        require.config({
            baseUrl: js_modules_root,
        });

        require([
            "lib/codemirror",
            "mode/markdown/markdown",
            "mode/clike/clike",
            "mode/css/css",
            "mode/diff/diff",
            "mode/dockerfile/dockerfile",
            "mode/gfm/gfm",
            "mode/htmlmixed/htmlmixed",
            "mode/jinja2/jinja2",
            "mode/python/python",
            "mode/shell/shell",
            "mode/sql/sql",
            "mode/yaml/yaml",
            "addon/display/fullscreen",
            "addon/display/panel",
        ].map((x) => `codemirror/${x}`), function (CodeMirror) {
            cm_instance = CodeMirror.fromTextArea(
                document.querySelector("#body-text"),
                {
                    mode: {
                        name: "gfm",
                        gitHubSpice: false,
                    },
                    lineSeparator: "\n",
                    lineWrapping: true,
                    extraKeys: {
                        // home/end shouldn't go to the beginning/end of paragraphs
                        Home: "goLineLeft",
                        End: "goLineRight",
                        // do not redefine the browser history navigation keys
                        "Alt-Left": false,
                        "Alt-Right": false,
                    },
                    autofocus: true,
                    // appears to do nothing
                    spellcheck: true,
                    viewportMargin: Infinity,
                }
            );
        });
    }

    // mark the editor as changed if there is an alert shown
    // (implies there was an error saving)
    if (document.querySelector("#alerts") !== null) {
        editor.changed = true;
    }

    // mark the editor as changed if the textarea has changed
    document
        .querySelector("#body-text")
        .addEventListener("input", (event) => (editor.changed = true));

    // don't nag if the Submit button was clicked
    document.querySelector("#page-form").onsubmit = function () {
        editor.submit_clicked = true;
    };

    window.addEventListener("beforeunload", function (e) {
        if (silicon_editor === "codemirror") {
            // alert on changed codemirror
            if (!cm_instance.isClean() && !editor.submit_clicked) {
                usurp_unload(e);
            }
        } else {
            // alert on changed textarea
            if (editor.changed && !editor.submit_clicked) {
                usurp_unload(e);
            }
        }
    });
});
