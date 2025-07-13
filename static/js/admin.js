const toggleBtn = document.getElementById("mobile-toggle");
const navLinks = document.getElementById("nav-links");
toggleBtn.addEventListener("click", () => {
  navLinks.classList.toggle("show");
});

// User menu toggle
const userBtn = document.getElementById("user-button");
const userDropdown = document.getElementById("user-dropdown");

userBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  userDropdown.style.display =
    userDropdown.style.display === "flex" ? "none" : "flex";
  userDropdown.style.flexDirection = "column";
});

// Close user menu on clicking outside
window.addEventListener("click", () => {
  userDropdown.style.display = "none";
});
