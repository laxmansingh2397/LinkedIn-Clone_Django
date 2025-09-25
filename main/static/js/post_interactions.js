document.addEventListener('DOMContentLoaded', function(){
  // toggle reply forms
  document.querySelectorAll('.reply-toggle').forEach(btn => {
    btn.addEventListener('click', function(){
      const id = btn.dataset.commentId;
      const form = document.querySelector('.reply-form[data-parent-id="'+id+'"]');
      if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
    });
  });

  // comment likes via AJAX
  document.querySelectorAll('.comment-like-btn').forEach(btn => {
    btn.addEventListener('click', function(){
      const commentId = btn.dataset.commentId;
      fetch("/comment/toggle-like/", {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({comment_id: commentId})
      }).then(r=>r.json()).then(data=>{
        if(!data.error){
          btn.querySelector('.like-count').textContent = data.count;
          if(data.liked){ btn.classList.add('liked'); } else { btn.classList.remove('liked'); }
        }
      }).catch(err=>console.error(err));
    });
  });

  // post like toggle
  document.querySelectorAll('.post-like-btn').forEach(btn => {
    btn.addEventListener('click', function(){
      const postId = btn.dataset.postId;
      fetch('/post/toggle-like/', {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({post_id: postId})
      }).then(r=>r.json()).then(data=>{
        if(data.ok){
          const countEl = btn.querySelector('.like-count');
          if(countEl) countEl.textContent = data.count;
          if(data.liked){ btn.classList.add('liked'); } else { btn.classList.remove('liked'); }
        } else if(data.error){
          console.error('Like error', data.error);
        }
      }).catch(err=>console.error(err));
    });
  });

  // share modal handling
  let currentSharePostId = null;
  const shareModal = document.getElementById('shareModal');
  const shareModalClose = shareModal ? document.getElementById('shareModalClose') : null;

  // open modal when share button clicked
  document.querySelectorAll('.share-toggle').forEach(btn=>{
    btn.addEventListener('click', function(e){
      currentSharePostId = btn.dataset.postId;
      if(shareModal) shareModal.style.display = 'block';
    });
  });

  // close modal
  if(shareModalClose){
    shareModalClose.addEventListener('click', function(){
      if(shareModal) shareModal.style.display = 'none';
      currentSharePostId = null;
    });
  }

  // when a user in the modal is clicked
  document.querySelectorAll('.modal-share-to-user').forEach(btn=>{
    btn.addEventListener('click', function(){
      const userId = btn.dataset.userId;
      if(!currentSharePostId){
        alert('No post selected');
        return;
      }
      fetch('/post/share/',{
        method:'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({post_id: currentSharePostId, to_user_id: userId})
      }).then(r=>r.json()).then(data=>{
        if(data.ok){
          alert('Shared successfully');
          if(shareModal) shareModal.style.display = 'none';
          currentSharePostId = null;
        } else if(data.error){
          alert('Error: '+data.error);
        }
      }).catch(e=>console.error(e));
    });
  });

  // fallback: keep existing direct share buttons working if present
  document.querySelectorAll('.share-to-user').forEach(btn=>{
    btn.addEventListener('click', function(){
      const postId = btn.dataset.postId;
      const userId = btn.dataset.userId;
      fetch('/post/share/',{
        method:'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({post_id: postId, to_user_id: userId})
      }).then(r=>r.json()).then(data=>{
        if(data.ok){
          alert('Shared successfully');
        } else if(data.error){
          alert('Error: '+data.error);
        }
      }).catch(e=>console.error(e));
    })
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
