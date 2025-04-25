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

// validação de cadastro
function cadastrar(){
    let nome = document.getElementById("nome").value.trim();
    let senha = document.getElementById("senha").value.trim();
    let email = document.getElementById("email").value.trim();

   
    if (nome == "" || senha == "" || email == "") {
        Swal.fire({
            icon: "error",
            title: "Erro!",
            text: "Preencha todos os campos."
        });
    } 
   
    else if (senha.length < 6) {
        Swal.fire({
            icon: "error",
            title: "Erro!",
            text: "A senha deve ter pelo menos 6 caracteres."
        });
        
    }
    else if (!email.includes("@") || !email.includes(".")) {
        Swal.fire({
            icon: "error",
            title: "Erro!",
            text: "Email inválido."
        });
        
    } 
    else {
        Swal.fire({
            icon: "success",
            title: "Sucesso!",
            text: "Cadastro realizado com sucesso."
        });
    }
}

let olho = document.getElementById("olho");
let senha = document.querySelector("#senha");
olho.addEventListener("click", function() {
    if (senha.type === "password") {
        senha.setAttribute("type", "text");
        olho.classList.add("olho-fechado");
        
    } else {
        senha.setAttribute('type', 'password');
        olho.classList.remove("olho-fechado");
    }
});


  

    
