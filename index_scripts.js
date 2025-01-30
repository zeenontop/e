// Get the elements
const downloadButton = document.querySelector('.download-button');
const heroVideo = document.querySelector('.hero video');


heroVideo.style.filter = 'blur(4px)';


// Add event listeners for mouseenter and mouseleave
downloadButton.addEventListener('mouseenter', () => {
    heroVideo.style.filter = 'blur(10px)';
});

downloadButton.addEventListener('mouseleave', () => {
    heroVideo.style.filter = 'blur(4px)';
});
