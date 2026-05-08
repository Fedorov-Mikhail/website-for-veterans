// FAQ toggle
document.addEventListener("DOMContentLoaded", function () {
  const faqItems = document.querySelectorAll(".faq-question");

  faqItems.forEach((item) => {
    item.addEventListener("click", () => {
      const answer = item.nextElementSibling;
      answer.classList.toggle("active");
    });
  });

  // Инициализация карты
  const mapDiv = document.getElementById("map");
  if (mapDiv && mapDiv.dataset.coordinates && typeof ymaps !== "undefined") {
    const coords = mapDiv.dataset.coordinates.split(",").map(Number);
    const zoom = parseInt(mapDiv.dataset.zoom);
    const address = mapDiv.dataset.address;

    ymaps.ready(function () {
      var map = new ymaps.Map("map", {
        center: coords,
        zoom: zoom,
      });

      var placemark = new ymaps.Placemark(coords, {
        balloonContent: address,
      });

      map.geoObjects.add(placemark);
    });
  }
});
