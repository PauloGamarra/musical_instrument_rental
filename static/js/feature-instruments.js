function move(add, ElementOriginId, ElementTargetId) {
    if (!add || InstrumentsInBox(ElementTargetId) + SelectedInstrumentsInBox(ElementOriginId) <= 10) {
        elements = document.querySelectorAll('#' + ElementOriginId + ' option:checked');
        targetElement = document.getElementById(ElementTargetId);
    
        for (let element of elements) {
            element.parentNode.removeChild(element);
            targetElement.appendChild(element);
        }
    }
    else {
        alert("numero máximo de instrumentos em destaque é 10");
    }
}

function InstrumentsInBox(ElementTargetId) {
    elements = document.querySelectorAll('#' + ElementTargetId + ' option');
    return elements.length;
}

function SelectedInstrumentsInBox(ElementTargetId) {
    elements = document.querySelectorAll('#' + ElementTargetId + ' option:checked');
    return elements.length;
}

function selecionarTodos10(ElementTargetId) {
    options = document.querySelectorAll('#' + ElementTargetId + ' option');
    if (options.length !== 10) {
        alert("você deve selecionar exatamente 10 instrumentos!");
        return false;
    }

    console.log(options);

    for (let option of options) {
        option.setAttribute('selected', true);
        option.setAttribute('checked', true);
        option.selected = true;
    }

    return true;
}