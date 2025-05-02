document.addEventListener("DOMContentLoaded", function() {
    var loadingSpinner = document.getElementById('loading-spinner');
    var content = document.getElementById('conteudo');

    setTimeout(function() {
        loadingSpinner.style.display = 'none';
        content.style.display = 'block';

        // animação ScrollReveal
        window.sr = ScrollReveal({ reset: true });
        sr.reveal('.area-1', {
            rotate: {x: 0, y: 80, z: 0},
            duration: 2000
        });
    
    }, 2000);

});
// função para excluir livro
function confirmarExclusao(event) {
    event.preventDefault();
    Swal.fire({
        title: 'Tem certeza?',
        text: "Você não poderá desfazer isso!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sim, excluir!',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                icon: "success",
                title: "Sucesso!",
                text: `Livro excluído com sucesso.`
            });
            window.location.href = event.target.href;
        }
    });
}

// função para editar Livro
function confirmarEdicao(event) {
    event.preventDefault();
    Swal.fire({
        title: 'Tem certeza?',
        text: "Editar livro!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sim, editar!',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                icon: "success",
                title: "Sucesso!",
                text: "Cadastro realizado com sucesso."
            });
            window.location.href = event.target.href;
        }
    });
}

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
   
    else if (senha.length < 3) {
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


// ocultar e mostrar senha
let olho = document.getElementById("olho");
let senha = document.querySelector("#senha");
olho.addEventListener("click", function() {
    if (senha.type === "password") {
        senha.setAttribute("type", "text");
        olho.innerHTML = '<i class="bi bi-eye-fill"></i>'
        
    } else {
        senha.setAttribute('type', 'password');
        olho.innerHTML = '<i class="bi bi-eye-slash"></i>'
    }
});

// adicionar favoritos
function adicionarFavoritos(){
    let btnFavoritar = document.querySelectorAll(".botao-favorito");
    btnFavoritar.forEach(function(btn) {
    btn.classList.toggle("favorito");
    if (btn.classList.contains("favorito")) {
        btn.innerHTML = "Remover dos Favoritos ";
        btn.style.backgroundColor = "#ff0000"; // vermelho
        btn.innerHTML += '<i class="bi bi-trash"></i>';
        Swal.fire({
            icon: "success",
            title: "Sucesso!",
            text: "Adicionado aos favoritos."
        });
    }
    else {
        btn.innerHTML = "Adicionar aos Favoritos ";
        btn.style.backgroundColor = "#007bff"; // azul
        btn.innerHTML += '<i class="bi bi-star"></i>';
       

        Swal.fire({
            icon: "success",
            title: "Sucesso!",
            text: "Removido dos favoritos."
        });
    }
});


}


