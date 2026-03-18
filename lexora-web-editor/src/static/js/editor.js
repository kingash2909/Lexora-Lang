document.addEventListener("DOMContentLoaded", function() {
    // Initialize CodeMirror
    const codeEditorElement = document.getElementById("code-editor");
    if (!codeEditorElement) return;

    const editor = CodeMirror.fromTextArea(codeEditorElement, {
        mode: "python",
        theme: "material-ocean",
        lineNumbers: true,
        autoCloseBrackets: true,
        indentUnit: 4,
        lineWrapping: true,
        viewportMargin: Infinity,
        extraKeys: {"Ctrl-Enter": executeCode}
    });

    const runButton = document.getElementById("run-button");
    const clearButton = document.getElementById("clear-button");
    const outputArea = document.getElementById("output-area");
    const filenameDisplay = document.getElementById("filename-display");
    
    // File operation buttons
    const uploadButton = document.getElementById("upload-button");
    const downloadButton = document.getElementById("download-button");
    const fileInput = document.getElementById("file-input");
    
    let currentFilename = "main.lx";

    if (runButton) {
        runButton.addEventListener("click", function() {
            executeCode();
        });
    }

    if (clearButton) {
        clearButton.addEventListener("click", function() {
            outputArea.textContent = "";
        });
    }

    // Copy to clipboard functionality
    const copyButton = document.getElementById("copy-button");
    if (copyButton) {
        copyButton.addEventListener("click", function() {
            const text = outputArea.textContent;
            if (text && text !== "Running...") {
                navigator.clipboard.writeText(text).then(() => {
                    const originalHTML = copyButton.innerHTML;
                    copyButton.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => {
                        copyButton.innerHTML = originalHTML;
                    }, 2000);
                });
            }
        });
    }

    // Upload file functionality
    if (uploadButton && fileInput) {
        uploadButton.addEventListener("click", function() {
            fileInput.click();
        });

        fileInput.addEventListener("change", function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const content = e.target.result;
                    editor.setValue(content);
                    currentFilename = file.name;
                    filenameDisplay.textContent = file.name;
                    outputArea.textContent = `✅ File "${file.name}" loaded successfully!`;
                };
                reader.onerror = function() {
                    outputArea.innerHTML = `<span style="color: #ff4d4d;">Error reading file: ${reader.error}</span>`;
                };
                reader.readAsText(file);
            }
            // Reset file input so same file can be selected again
            event.target.value = '';
        });
    }

    // Download file functionality
    if (downloadButton) {
        downloadButton.addEventListener("click", function() {
            const code = editor.getValue();
            if (!code.trim()) {
                alert("No code to save! Please write some code first.");
                return;
            }
            
            const blob = new Blob([code], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = currentFilename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            // Show success message
            outputArea.textContent = `✅ File "${currentFilename}" downloaded successfully!`;
        });
    }

    function executeCode() {
        const code = editor.getValue();
        if (!code.trim()) {
            outputArea.textContent = "Error: No code to execute.";
            return;
        }

        outputArea.innerHTML = '<span class="status-msg">Running...</span>';
        
        fetch("/execute", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === "success") {
                outputArea.textContent = data.output;
            } else {
                outputArea.innerHTML = `<span style="color: #ff4d4d;">Error: ${data.error || "Unknown error occurred"}</span>`;
            }
        })
        .catch(error => {
            outputArea.innerHTML = `<span style="color: #ff4d4d;">Connection Error: ${error.message}</span>`;
        });
    }

    // Simple Resizer Logic
    const resizer = document.querySelector(".resizer");
    const leftPane = document.querySelector(".editor-pane");
    const rightPane = document.querySelector(".output-pane");
    
    if (resizer && leftPane && rightPane) {
        let isResizing = false;

        resizer.addEventListener("mousedown", (e) => {
            isResizing = true;
            document.body.style.cursor = "col-resize";
        });

        document.addEventListener("mousemove", (e) => {
            if (!isResizing) return;
            
            const containerWidth = document.querySelector(".editor-container-main").offsetWidth;
            const leftWidth = (e.clientX / containerWidth) * 100;
            
            if (leftWidth > 20 && leftWidth < 80) {
                leftPane.style.flex = `0 0 ${leftWidth}%`;
                rightPane.style.flex = `0 0 ${100 - leftWidth}%`;
                editor.refresh(); // Crucial to update CodeMirror layout
            }
        });

        document.addEventListener("mouseup", () => {
            isResizing = false;
            document.body.style.cursor = "default";
        });
    }
});
