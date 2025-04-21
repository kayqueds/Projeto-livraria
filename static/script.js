document.addEventListener("DOMContentLoaded", function() {
    var loadingSpinner = document.getElementById('loading-spinner');
    var content = document.getElementById('conteudo');

    // Simula um tempo de carregamento
    setTimeout(function() {
        loadingSpinner.style.display = 'none';
        content.style.display = 'block';

        // é o meu script de animação
        window.sr = ScrollReveal({ reset: true });

        sr.reveal('.area-1', {
            rotate: {x: 0, y: 80, z: 0},
            duration: 2000
        });
    }, 2000);
});
