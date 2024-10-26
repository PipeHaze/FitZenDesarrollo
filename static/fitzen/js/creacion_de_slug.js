document.addEventListener("DOMContentLoaded", function() {
    const tituloField = document.getElementById("id_titulo");
    const slugField = document.getElementById("id_slug");

    tituloField.addEventListener("input", function() {
        const titulo = tituloField.value;
        console.log("Título:", titulo); // Verifica el valor del título

        let slug = titulo
            .toLowerCase()
            .replace(/ /g, '-')
            .replace(/[^\w-]+/g, '')
            .replace(/--+/g, '-')
            .trim();

        const uniqueId = Date.now();
        slugField.value = `${slug}-${uniqueId}`;
        console.log("Slug:", slugField.value); // Verifica el valor del slug
    });
});

