document.addEventListener('DOMContentLoaded', () => {
  // Mobile Menu Toggle
  const mobileBtn = document.querySelector('.mobile-menu-btn');
  const nav = document.querySelector('.nav');

  mobileBtn.addEventListener('click', () => {
    nav.classList.toggle('active');

    // Animate burger button
    const spans = mobileBtn.querySelectorAll('span');
    if (nav.classList.contains('active')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans[0].style.transform = 'none';
      spans[1].style.opacity = '1';
      spans[2].style.transform = 'none';
    }
  });

  // Product Filtering
  const filterBtns = document.querySelectorAll('.filter-btn');
  const productCards = document.querySelectorAll('.product-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Remove active class from all btns
      filterBtns.forEach(b => b.classList.remove('active'));
      // Add active class to clicked btn
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      productCards.forEach(card => {
        if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {
          card.style.display = 'block';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
          }, 50);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'scale(0.8)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 300);
        }
      });
    });
  });

  // Scroll Animations
  const observerOptions = {
    threshold: 0,
    rootMargin: "0px 0px -50px 0px"
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.section, .product-card').forEach(el => {
    el.classList.add('animate-on-scroll');
    observer.observe(el);
  });

  // Dynamically add "Order via WhatsApp" button to each product
  document.querySelectorAll('.product-card').forEach(card => {
    const titleElement = card.querySelector('.product-title');
    const overlay = card.querySelector('.product-hover-overlay');

    if (titleElement && overlay) {
      const title = titleElement.innerText;
      const message = `Hi Sri Shasti Mart, I am interested in buying the *${title}*. Could you share the price and details?`;

      const orderBtn = document.createElement('a');
      orderBtn.href = `https://wa.me/917603986646?text=${encodeURIComponent(message)}`;
      orderBtn.target = '_blank';
      orderBtn.className = 'btn btn-product-order';
      orderBtn.innerHTML = '🛒 Order via WhatsApp';

      overlay.appendChild(orderBtn);
    }
  });
});
