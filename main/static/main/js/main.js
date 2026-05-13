document.addEventListener('DOMContentLoaded', () => {
  initFaq();
  initCarousels();
  initJoinModal();
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

function initJoinModal() {
  const modal = document.querySelector('[data-join-modal]');
  const openButtons = document.querySelectorAll('[data-join-modal-open]');
  if (!modal || openButtons.length === 0) return;

  const closeButtons = modal.querySelectorAll('[data-join-modal-close]');
  const dialog = modal.querySelector('.join-modal-dialog');
  let lastFocusedElement = null;

  function openModal() {
    lastFocusedElement = document.activeElement;
    modal.hidden = false;
    document.body.classList.add('modal-open');
    const closeButton = modal.querySelector('.join-modal-close');
    closeButton?.focus();
  }

  function closeModal() {
    modal.hidden = true;
    document.body.classList.remove('modal-open');
    lastFocusedElement?.focus?.();
  }

  openButtons.forEach((button) => {
    button.addEventListener('click', openModal);
  });

  closeButtons.forEach((button) => {
    button.addEventListener('click', closeModal);
  });

  dialog?.addEventListener('click', (event) => {
    event.stopPropagation();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !modal.hidden) {
      closeModal();
    }
  });
}

function initYandexMap() {
  const mapDiv = document.getElementById('map');
  if (!mapDiv || !mapDiv.dataset.coords || typeof ymaps === 'undefined') return;

  const coords = mapDiv.dataset.coords.split(',').map(Number);
  if (coords.length !== 2 || coords.some(Number.isNaN)) return;
  const zoom = parseInt(mapDiv.dataset.zoom, 10) || 12;

  ymaps.ready(() => {
    const map = new ymaps.Map('map', {
      center: coords,
      zoom,
      controls: ['geolocationControl', 'trafficControl', 'zoomControl', 'fullscreenControl'],
    }, {
      suppressMapOpenBlock: true,
      yandexMapDisablePoiInteractivity: true,
    });
    map.geoObjects.add(new ymaps.Placemark(coords, {}, {
      preset: 'islands#blueDotIcon',
    }));

    map.controls.get('zoomControl')?.options.set('position', { right: 10, top: 140 });
    map.controls.get('geolocationControl')?.options.set('position', { right: 10, bottom: 92 });
    map.controls.get('fullscreenControl')?.options.set('position', { right: 10, top: 10 });
    map.controls.get('trafficControl')?.options.set('position', { right: 58, top: 10 });
  });
}
