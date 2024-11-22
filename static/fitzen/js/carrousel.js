let currentIndex = 0;
const items = document.querySelectorAll('.carrousel .item_c');
const totalItems = items.length;

function moveSlide(step) {
    currentIndex += step;
    
    if (currentIndex < 0) {
        currentIndex = totalItems - 1;  // Si llegamos al primer elemento, volvemos al último
    } else if (currentIndex >= totalItems) {
        currentIndex = 0;               // Si llegamos al último elemento, volvemos al primero
    }
    
    const newTransformValue = -currentIndex * 100;  // Calculamos el valor de transform en base al índice actual
    document.querySelector('.carrousel').style.transform = `translateX(${newTransformValue}%)`;
}

// Mueve el carrousel automáticamente cada 3 segundos
setInterval(() => {
    moveSlide(1);
}, 3000);