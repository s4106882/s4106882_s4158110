const buttons = document.querySelectorAll('[data-graph-button]');
let slideInterval;

function updateSlideStates(slides, activeIndex) {
    const totalSlides = slides.children.length;
    
    [...slides.children].forEach(slide => {
        delete slide.dataset.active;
        delete slide.dataset.next;
        delete slide.dataset.prev;
    });
    
    slides.children[activeIndex].dataset.active = true;
    
    const nextIndex = (activeIndex + 1) % totalSlides;
    slides.children[nextIndex].dataset.next = true;
    
    const prevIndex = (activeIndex - 1 + totalSlides) % totalSlides;
    slides.children[prevIndex].dataset.prev = true;
}

function advanceSlide() {
    const container = document.querySelector('[data-graph-container]');
    const slides = container.querySelector('[data-slides]');
    const activeSlide = slides.querySelector('[data-active]');
    let newIndex = [...slides.children].indexOf(activeSlide) + 1;
    if (newIndex >= slides.children.length) newIndex = 0;
    
    updateSlideStates(slides, newIndex);
}

function startSlideTimer() {
    if (slideInterval) {
        clearInterval(slideInterval);
    }
    slideInterval = setInterval(advanceSlide, 5000);
}

startSlideTimer();

buttons.forEach(button => {
    button.addEventListener('click', () => {
        const offset = button.dataset.graphButton === 'next' ? 1 : -1;
        const slides = button.closest('[data-graph-container]').querySelector('[data-slides]');
        const activeSlide = slides.querySelector('[data-active]');
        let newIndex = [...slides.children].indexOf(activeSlide) + offset;
        
        if (newIndex < 0) newIndex = slides.children.length - 1;
        if (newIndex >= slides.children.length) newIndex = 0;
        
        updateSlideStates(slides, newIndex);
        startSlideTimer();
    });
});