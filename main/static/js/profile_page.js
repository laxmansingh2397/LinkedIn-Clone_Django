
document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('editProfileBtn');
    const modal = document.getElementById('editProfileModal');
    const close = document.getElementById('editProfileClose');
    const cancel = document.getElementById('editCancel');
    if (btn && modal) {
        btn.addEventListener('click', () => modal.style.display = 'block');
    }
    if (close) { close.addEventListener('click', () => modal.style.display = 'none'); }
    if (cancel) { cancel.addEventListener('click', () => modal.style.display = 'none'); }
});
// wire up card edit buttons to open modals and prefill values when data- attributes present
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.card-edit').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            var target = btn.getAttribute('data-target');
            if (!target) return;
            var modal = document.querySelector(target);
            if (!modal) return;

            // prefill for experience
            if (target === '#experienceModal') {
                var id = btn.dataset.id || '';
                modal.querySelector('input[name="title"]').value = btn.dataset.title || '';
                modal.querySelector('input[name="company"]').value = btn.dataset.company || '';
                modal.querySelector('input[name="start_date"]').value = btn.dataset.start_date || '';
                modal.querySelector('input[name="end_date"]').value = btn.dataset.end_date || '';
                modal.querySelector('input[name="location"]').value = btn.dataset.location || '';
                // ensure hidden id field exists
                var idField = modal.querySelector('input[name="id"]');
                if (!idField) {
                    idField = document.createElement('input');
                    idField.type = 'hidden';
                    idField.name = 'id';
                    modal.querySelector('form').appendChild(idField);
                }
                idField.value = id;
            }

            // prefill for education
            if (target === '#educationModal') {
                var id = btn.dataset.id || '';
                modal.querySelector('input[name="school"]').value = btn.dataset.school || '';
                modal.querySelector('input[name="degree"]').value = btn.dataset.degree || '';
                modal.querySelector('input[name="start_year"]').value = btn.dataset.start_year || '';
                modal.querySelector('input[name="end_year"]').value = btn.dataset.end_year || '';
                var idField = modal.querySelector('input[name="id"]');
                if (!idField) {
                    idField = document.createElement('input');
                    idField.type = 'hidden';
                    idField.name = 'id';
                    modal.querySelector('form').appendChild(idField);
                }
                idField.value = id;
            }

            modal.style.display = 'block';
        });
    });

    // close buttons for generated modals handled by modal.js already; add simple close when clicking outside
    document.querySelectorAll('.modal').forEach(function (m) {
        m.addEventListener('click', function (e) {
            if (e.target === m) m.style.display = 'none';
        });
    });
});