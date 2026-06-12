document.addEventListener('DOMContentLoaded', function () {

    const menuButton = document.getElementById('admin-sidebar');

    if (!menuButton) {
        return;
    }

    menuButton.addEventListener('click', function () {

        document.documentElement.classList.toggle(
            'sidebar-collapsed'
        );

    });

});
