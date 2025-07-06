document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  const navbarToggle = document.querySelector('.navbar__toggle');
  const navbarMenu = document.querySelector('.navbar__menu');
  
  if (navbarToggle && navbarMenu) {
    navbarToggle.addEventListener('click', function() {
      navbarMenu.classList.toggle('navbar__menu--active');
      this.classList.toggle('navbar__toggle--active');
    });
  }
  
  // Dropdown functionality
  const dropdownToggles = document.querySelectorAll('.dropdown__toggle');
  
  dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      const dropdown = this.closest('.dropdown');
      dropdown.classList.toggle('dropdown--open');
    });
  });
  
  // Close dropdowns when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.dropdown')) {
      document.querySelectorAll('.dropdown').forEach(dropdown => {
        dropdown.classList.remove('dropdown--open');
      });
    }
  });
});
