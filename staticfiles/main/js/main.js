document.addEventListener('DOMContentLoaded', () => {
  initFaq();
  initCarousels();
  initReportForm();
  initYandexMap();
});

function initFaq() {
  document.querySelectorAll('.faq-item').forEach((item) => {
    const question = item.querySelector('.faq-question');
    const toggleBtn = item.querySelector('.faq-toggle');
    if (!question || !toggleBtn) return;

    question.addEventListener('click', () => {
      item.classList.toggle('open');
      const isOpen = item.classList.contains('open');
      toggleBtn.textContent = isOpen ? '−' : '+';
      toggleBtn.setAttribute('aria-label', isOpen ? 'Скрыть ответ' : 'Раскрыть ответ');
    });
  });
}

function initCarousels() {
  document.querySelectorAll('.carousel').forEach((container) => {
    const slidesPerViewDesktop = parseInt(container.dataset.slidesPerView, 10) || 2;
    const track = container.querySelector('.carousel-track');
    const slides = Array.from(container.querySelectorAll('.carousel-slide'));
    const prevBtn = container.querySelector('[data-carousel-prev]');
    const nextBtn = container.querySelector('[data-carousel-next]');
    if (!track || slides.length === 0) return;

    let slidesPerView = slidesPerViewDesktop;
    let currentIndex = 0;
    let animating = false;
    const slideCount = slides.length;
    const loop = slideCount > 1;

    function updatePosition(useTransition = true) {
      if (!useTransition) {
        track.classList.add('no-transition');
      }

      track.style.setProperty('--index', currentIndex);
      track.style.setProperty('--per-view', slidesPerView);
      track.style.transform = `translateX(calc(-1 * ${currentIndex} * (100% / ${slidesPerView})))`;

      if (!useTransition) {
        void track.offsetHeight;
        track.classList.remove('no-transition');
      }
    }

    function updateButtons() {
      if (loop) {
        if (prevBtn) prevBtn.disabled = false;
        if (nextBtn) nextBtn.disabled = false;
        return;
      }

      if (prevBtn) prevBtn.disabled = currentIndex === 0;
      if (nextBtn) nextBtn.disabled = currentIndex >= slideCount - slidesPerView;
    }

    function updateSlidesPerView() {
      const isMobile = window.matchMedia('(max-width: 1200px)').matches;
      slidesPerView = isMobile ? 1 : slidesPerViewDesktop;
      container.style.setProperty('--slides-per-view', slidesPerView);

      const maxIndex = Math.max(0, slideCount - slidesPerView);
      if (currentIndex > maxIndex) currentIndex = maxIndex;

      updatePosition(false);
      updateButtons();
    }

    function shift(direction) {
      if (animating) return;
      if (!loop && direction === -1 && currentIndex === 0) return;
      if (!loop && direction === 1 && currentIndex >= slideCount - slidesPerView) return;

      animating = true;
      let newIndex = currentIndex + direction;

      if (loop) {
        if (newIndex < 0) {
          newIndex = Math.max(0, slideCount - slidesPerView);
        } else if (newIndex >= slideCount) {
          newIndex = 0;
        }
      }

      currentIndex = newIndex;
      updatePosition(true);
      updateButtons();

      const onTransitionEnd = () => {
        track.removeEventListener('transitionend', onTransitionEnd);
        animating = false;
      };
      track.addEventListener('transitionend', onTransitionEnd);
    }

    prevBtn?.addEventListener('click', () => shift(-1));
    nextBtn?.addEventListener('click', () => shift(1));
    window.matchMedia('(max-width: 1200px)').addEventListener('change', updateSlidesPerView);
    window.addEventListener('resize', updateSlidesPerView);

    updateSlidesPerView();
  });
}

function initReportForm() {
  const toggleBtn = document.getElementById('toggleReportForm');
  const form = document.getElementById('reportForm');
  if (!toggleBtn || !form) return;

  toggleBtn.addEventListener('click', () => {
    form.style.display = form.style.display === 'none' ? 'grid' : 'none';
  });

  if (window.location.hash === '#feedback' && document.querySelector('.form-status.error')) {
    form.style.display = 'grid';
  }
}

function initYandexMap() {
  const mapDiv = document.getElementById('map');
  if (!mapDiv || !mapDiv.dataset.coords || typeof ymaps === 'undefined') return;

  const coords = mapDiv.dataset.coords.split(',').map(Number);
  if (coords.length !== 2 || coords.some(Number.isNaN)) return;

  ymaps.ready(() => {
    const map = new ymaps.Map('map', {
      center: coords,
      zoom: parseInt(mapDiv.dataset.zoom, 10) || 12,
    });
    map.geoObjects.add(new ymaps.Placemark(coords));
  });
}
