var count = 1;

function adicionarPreco() {
    // pegar valor dos inputs
    var money = document.getElementById("precoInput").value;
    var days = document.getElementById("diasInput").value;

    // adiciona option na select
    var hiddenSelect = document.getElementById("hidden-select");
    var newOption = document.createElement("option");
    newOption.value = money + "," + days;
    newOption.innerHTML = money + "," + days;
    newOption.id = "hiddenSelect" + count;
    newOption.setAttribute('selected', true);
    hiddenSelect.appendChild(newOption);

    // adiciona linha na tabela, formatado
    var inputsDaTable = document.getElementById("inputsDaTable");
    var tr = document.createElement("tr");
    var td1 = document.createElement("td");
    var td2 = document.createElement("td");
    var icon = document.createElement("img");

    td1.innerHTML = money + " R$";
    td2.innerHTML = days;
    icon.src = icon_path;
    icon.classList.add('trash');
    icon.id = "ic" + count;
    icon.addEventListener("click", function (e) {
        deletarPreco(e);
    }, false);
    td2.appendChild(icon);

    tr.appendChild(td1);
    tr.appendChild(td2);
    tr.id = "tr" + count;
    inputsDaTable.parentNode.insertBefore(tr, inputsDaTable);

    // limpar inputs
    document.getElementById("precoInput").value = "";
    document.getElementById("diasInput").value = "";

    // incrementa o contador
    count += 1;
}

function deletarPreco(el) {
    var id = el.target.id.replace("ic", "");
    var tr = el.target.parentNode.parentNode;
    var option = document.getElementById("hiddenSelect" + id);
    tr.parentNode.removeChild(tr);
    option.parentNode.removeChild(option);
}