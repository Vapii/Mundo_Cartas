document.addEventListener("DOMContentLoaded", function () {
    const scannerContainer = document.getElementById("scanner");
    const inputCodigo = document.getElementById("codigo_barras");
    const botonEscanear = document.getElementById("btn-escanear");

    if (botonEscanear && scannerContainer && inputCodigo) {
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
                    return;
                }
                Quagga.start();
            });

            Quagga.onDetected(function (result) {
                const codigo = result.codeResult.code;
                inputCodigo.value = codigo;
                Quagga.stop();
                scannerContainer.style.display = "none";
                alert("Código escaneado: " + codigo);
            });
        });
    }
});

