document.addEventListener("DOMContentLoaded", () => {
    // Los datos ya son JSON válidos enviados por Django
    const todosClientes = {{ todos_clientes|safe }};
    const clientesAdeudados = {{ clientes_adeudados|safe }};
    const clientesPagados = {{ clientes_pagados|safe }};

    console.log("Todos los clientes:", todosClientes);
    console.log("Clientes adeudados:", clientesAdeudados);
    console.log("Clientes pagados:", clientesPagados);

    // Renderiza la lista inicial de clientes
    const clientesContainer = document.querySelector("#clientes");
    clientesContainer.innerHTML = ""; // Limpia contenido inicial

    todosClientes.forEach((cliente) => {
        const li = document.createElement("li");
        li.textContent = cliente;
        clientesContainer.appendChild(li);
    });
});
