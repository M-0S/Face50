const deleteModal = document.getElementById('deleteModal');

deleteModal.addEventListener('show.bs.modal', event => {

    // Button that triggered the modal
    const button = event.relatedTarget;

    // Extract info from data-bs-* attributes
    const postId = button.getAttribute('data-bs-id');

    document.getElementById('hiddenInput').setAttribute('value', postId)
});
