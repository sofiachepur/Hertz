const items = document.querySelectorAll('.photo-wrap');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

items.forEach(item => observer.observe(item));


document.querySelector('.nav-toggle')?.addEventListener('click', () => {
  document.querySelector('.nav-list').classList.toggle('open');
});