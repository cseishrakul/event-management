document.addEventListener("DOMContentLoaded", () => {
  const menu = document.querySelector("#menu-bars");
  const navbar = document.querySelector(".navbar");
  const themeToggler = document.querySelector(".theme-toggler");
  const toggleBtn = document.querySelector(".toggle-btn");

  console.log("menu:", menu);
  console.log("navbar:", navbar);

  if (menu && navbar) {
    menu.onclick = () => {
      menu.classList.toggle("fa-times");
      navbar.classList.toggle("active");
    };
  } else {
    console.warn("Menu or navbar element not found");
  }

  if (toggleBtn && themeToggler) {
    toggleBtn.onclick = () => {
      themeToggler.classList.toggle("active");
    };
  } else {
    console.warn("Toggle button or theme toggler not found");
  }

  window.onscroll = () => {
    if (menu) menu.classList.remove("fa-times");
    if (navbar) navbar.classList.remove("active");
    if (themeToggler) themeToggler.classList.remove("active");
  };

  document.querySelectorAll(".theme-toggler .theme-btn").forEach((btn) => {
    btn.onclick = () => {
      let color = getComputedStyle(btn).backgroundColor;
      document.documentElement.style.setProperty("--main-color", color);
    };
  });

  // Initialize Swiper sliders only if Swiper is loaded and elements exist
  if (typeof Swiper !== "undefined") {
    if (document.querySelector(".home-slider")) {
      new Swiper(".home-slider", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        coverflowEffect: {
          rotate: 0,
          stretch: 0,
          depth: 100,
          modifier: 2,
          slideShadows: true,
        },
        loop: true,
        autoplay: {
          delay: 3000,
          disableOnInteraction: false,
        },
      });
    }

    if (document.querySelector(".review-slider")) {
      new Swiper(".review-slider", {
        slidesPerView: 1,
        grabCursor: true,
        loop: true,
        spaceBetween: 10,
        breakpoints: {
          0: { slidesPerView: 1 },
          700: { slidesPerView: 2 },
          1050: { slidesPerView: 3 },
        },
        autoplay: {
          delay: 5000,
          disableOnInteraction: false,
        },
      });
    }
  } else {
    console.warn("Swiper is not loaded");
  }
});
