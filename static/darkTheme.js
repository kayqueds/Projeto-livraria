
// alterar tema
function alterarTema(){
   
    let tema = document.querySelector('html').getAttribute('data-bs-theme');
    let navbar = document.querySelector('nav.navbar').getAttribute('data-bs-theme');
    
    if(tema == 'dark'){
        document.querySelector('html').setAttribute('data-bs-theme', 'light');
        document.querySelector('nav.navbar').setAttribute('data-bs-theme', 'light');
        document.querySelector('button#alterarTema').innerHTML = `<i class="bi bi-moon"></i>`
    }
    else{
        document.querySelector('html').setAttribute('data-bs-theme', 'dark');
        document.querySelector('nav.navbar').setAttribute('data-bs-theme', 'dark');
        document.querySelector('button#alterarTema').innerHTML = `<i class="bi bi-sun"></i>`;
    }
}
