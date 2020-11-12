var clicado = false;

function mostrarDropdown() {
    dropdown = document.getElementById("seta");
    dropdownOptions = document.getElementsByClassName("opcao-dropdown");

    if (!clicado) {
        dropdown.classList.add("clicado");
        dropdown.classList.remove("nao-clicado");
        for (let option of dropdownOptions) {
            option.classList.add("clicado");
        }
    }
    else {
        dropdown.classList.remove("clicado");
        dropdown.classList.add("nao-clicado");
        for (let option of dropdownOptions) {
            option.classList.remove("clicado");
        }
    }
    clicado = !clicado;
}