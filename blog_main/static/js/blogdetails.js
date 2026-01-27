document.addEventListener('DOMContentLoaded', function() {
    // Submit main comment form without reload
    const commentForm = document.getElementById('bd-comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);

            fetch("", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": bdGetCSRFToken()
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                }
            });
        });
    }

    // Submit reply forms without reload
    document.addEventListener('submit', function(e) {
        const form = e.target;
        
        if (form.querySelector('input[name="parent_id"]')) {
            e.preventDefault();
            const formData = new FormData(form);

            fetch("", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": bdGetCSRFToken()
                }
            }).then(res => {
                if (res.ok) {
                    location.reload();
                }
            });
        }
    });
});

// Toggle reply form
function bdToggleReplyForm(id) {
    const form = document.getElementById(`bd-reply-form-${id}`);
    if (form) {
        form.classList.toggle('bd-hidden');
    }
}

// Toggle edit form
function bdToggleEditForm(id) {
    const form = document.getElementById(`bd-edit-form-${id}`);
    if (form) {
        form.classList.toggle('bd-hidden');
    }
}

// Submit edit
function bdSubmitEdit(commentId) {
    const textarea = document.getElementById(`bd-edit-text-${commentId}`);
    const newText = textarea.value.trim();

    if (!newText) {
        alert("Comment cannot be empty");
        return;
    }

    fetch(`/edit-comment/${commentId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": bdGetCSRFToken(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `comment=${encodeURIComponent(newText)}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const commentEl = document.querySelector(`#bd-comment-${commentId} .bd-comment-text`);
            if (commentEl) {
                commentEl.innerText = data.comment;
            }
            bdToggleEditForm(commentId);
        } else {
            alert(data.error || "Edit failed");
        }
    })
    .catch(err => {
        console.error('Edit error:', err);
        alert("Failed to edit comment");
    });
}

// Delete comment
function bdDeleteComment(commentId) {
    if (!confirm("Delete this comment?")) return;

    fetch(`/delete-comment/${commentId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": bdGetCSRFToken(),
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const el = document.getElementById(`bd-comment-${commentId}`);
            if (el) el.remove();

            const countEl = document.getElementById("bd-comment-count");
            if (countEl) {
                countEl.innerText = Math.max(0, parseInt(countEl.innerText) - 1);
            }
        } else {
            alert(data.error || "Delete failed");
        }
    })
    .catch(err => {
        console.error('Delete error:', err);
        alert("Failed to delete comment");
    });
}

// Report modal functions
function bdOpenReportModal() {
    const modal = document.getElementById('bd-report-modal');
    if (modal) {
        modal.classList.add('bd-active');
    }
}

function bdCloseReportModal() {
    const modal = document.getElementById('bd-report-modal');
    if (modal) {
        modal.classList.remove('bd-active');
    }
}

// Get CSRF token
function bdGetCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

// Close modal on outside click
document.addEventListener('click', function(e) {
    const modal = document.getElementById('bd-report-modal');
    if (modal && e.target === modal) {
        bdCloseReportModal();
    }
});

// Close modal on ESC key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        bdCloseReportModal();
    }
});