// Toggle the notification dropdown on click and close on outside click / ESC
document.addEventListener('DOMContentLoaded', function () {
  const notif = document.querySelector('.notif');
  if (!notif) return;

  const bellAnchor = notif.querySelector('a') || notif.querySelector('.notif-toggle');

  bellAnchor && bellAnchor.addEventListener('click', function (e) {
    // prevent the anchor default so we can toggle dropdown first
    e.preventDefault();
    notif.classList.toggle('open');
  });

  // close when clicking outside
  document.addEventListener('click', function (e) {
    if (!notif.contains(e.target)) {
      notif.classList.remove('open');
    }
  });

  // close on ESC
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') notif.classList.remove('open');
  });
});
