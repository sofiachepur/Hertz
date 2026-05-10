const items = document.querySelectorAll('.photo-wrap');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, {threshold: 0.1});

items.forEach(item => observer.observe(item));


document.querySelector('.nav-toggle')?.addEventListener('click', () => {
  document.querySelector('.nav-list').classList.toggle('open');
});


  document.addEventListener("DOMContentLoaded", function () {

  document.querySelectorAll(".slider").forEach(slider => {

    const slides = slider.querySelectorAll(".slide");
    const prev = slider.querySelector(".prev");
    const next = slider.querySelector(".next");

    let index = 0;

    if (slides.length === 0) return;

    function showSlide(i) {
      slides.forEach(s => s.classList.remove("active"));
      slides[i].classList.add("active");
    }

    prev.addEventListener("click", () => {
      index = (index - 1 + slides.length) % slides.length;
      showSlide(index);
    });

    next.addEventListener("click", () => {
      index = (index + 1) % slides.length;
      showSlide(index);
    });

    showSlide(index);

  });

});
