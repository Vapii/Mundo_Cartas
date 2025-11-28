document.addEventListener("DOMContentLoaded", function () {
    const scannerContainer = document.getElementById("scanner");
    const inputCodigo = document.getElementById("codigo_barras");
    const inputStock = document.getElementById("stock");
    const botonEscanear = document.getElementById("btn-escanear");

    // Guardar códigos escaneados en esta sesión
    const codigosEscaneados = new Set();

    if (botonEscanear && scannerContainer && inputCodigo && inputStock) {
        botonEscanear.addEventListener("click", function () {
            scannerContainer.style.display = "block";

            Quagga.init({
                inputStream: {
                    name: "Live",
                    type: "LiveStream",
                    target: scannerContainer,
                    constraints: { facingMode: "environment" }
                },
                decoder: {
                    readers: ["ean_reader", "code_128_reader"]
                }
            }, function (err) {
                if (err) {
                    console.error("Error al iniciar Quagga:", err);
                    alert("No se pudo iniciar el escáner. Revisa permisos de cámara.");
                    return;
                }
                Quagga.start();
            });

            Quagga.offDetected();

            Quagga.onDetected(function (result) {
                const codigo = result.codeResult.code;

                // Validar si ya fue escaneado en esta sesión
                if (codigosEscaneados.has(codigo)) {
                    alert("Código ya escaneado: " + codigo);
                    return;
                }

                // Asignar el código si es el primero
                if (!inputCodigo.value) {
                    inputCodigo.value = codigo;
                }

                // Marcar como escaneado
                codigosEscaneados.add(codigo);

                // Aumentar stock en +1
                let currentStock = parseInt(inputStock.value || "0", 10);
                inputStock.value = currentStock + 1;

                alert("Código escaneado: " + codigo + " | Stock actualizado: " + inputStock.value);
            });
        });
    }
});
