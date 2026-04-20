<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>LTC6904 Final Fix v6</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #2c3e50; color: #333; display: flex; justify-content: center; padding-top: 50px; }
        .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); width: 350px; text-align: center; }
        input { width: 80%; font-size: 1.5rem; padding: 10px; border: 2px solid #bdc3c7; border-radius: 8px; margin-bottom: 20px; text-align: center; }
        button { width: 100%; background: #d35400; color: white; border: none; padding: 15px; font-size: 1.1rem; font-weight: bold; border-radius: 8px; cursor: pointer; }
        #res { margin-top: 25px; text-align: left; background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #d35400; font-family: monospace; line-height: 1.5; }
        .hex-red { color: #c0392b; font-weight: bold; font-size: 1.2rem; }
    </style>
</head>
<body>
    <div class="card">
        <h2>LTC6904 Master Calc</h2>
        <p>Target Frequency (MHz):</p>
        <input type="text" id="freq" value="12.697">
        <button onclick="calculateNow()">CALCULATE HEX BYTES</button>
        <div id="res">Esperando entrada...</div>
    </div>

    <script>
        function calculateNow() {
            // 1. Limpieza total de entrada (puntos y comas)
            let rawValue = document.getElementById('freq').value.replace(',', '.');
            let fTargetMHz = parseFloat(rawValue);
            
            if (isNaN(fTargetMHz) || fTargetMHz <= 0) {
                alert("Introduce un número válido");
                return;
            }

            // Convertimos a kHz para la fórmula
            let fKhz = fTargetMHz * 1000;
            let oct = 0;

            // 2. BUSCADOR DE OCTAVA (Sin logaritmos para evitar errores de precisión)
            // Rangos basados estrictamente en el Datasheet
            if (fKhz < 2078) oct = 0;
            else if (fKhz < 4156) oct = 1;
            else if (fKhz < 8312) oct = 2;
            else if (fKhz < 16624) oct = 3;
            else if (fKhz < 33248) oct = 4;
            else if (fKhz < 66496) oct = 5;
            else if (fKhz < 132992) oct = 6;
            else if (fKhz < 265984) oct = 7;
            else if (fKhz < 531968) oct = 8;
            else if (fKhz < 1063936) oct = 9;
            else if (fKhz < 2127872) oct = 10;
            else if (fKhz < 4255744) oct = 11;
            else if (fKhz < 8511488) oct = 12; // <--- Los 12 MHz entran AQUÍ
            else if (fKhz < 17022976) oct = 13;
            else if (fKhz < 34045952) oct = 14;
            else oct = 15;

            // 3. CÁLCULO DEL DAC (0-1023)
            // f = 2^oct * (2048 / (2048 - DAC)) * 1.039
            let powerOf2 = Math.pow(2, oct);
            let dac = Math.round(2048 - ((powerOf2 * 2048 * 1.039) / fKhz));

            // Ajuste de seguridad por límites físicos
            if (dac < 0) dac = 0;
            if (dac > 1023) dac = 1023;

            // 4. CONSTRUCCIÓN DE LOS BYTES I2C
            // MSB = [ OCT (4 bits) | DAC High (4 bits) ]
            let msb = (oct << 4) | (dac >> 6);
            // LSB = [ DAC Low (6 bits) | CNF (2 bits) ] -> CNF 01 (Solo Pin 6)
            let lsb = ((dac & 0x3F) << 2) | 1;

            // 5. CÁLCULO DE LA FRECUENCIA REAL RESULTANTE
            let fRealMHz = (powerOf2 * (2048 / (2048 - dac)) * 1.039) / 1000;

            document.getElementById('res').innerHTML = 
                "<b>OCT:</b> " + oct + " | <b>DAC:</b> " + dac + "<br><br>" +
                "HEX MSB: <span class='hex-red'>0x" + msb.toString(16).toUpperCase() + "</span><br>" +
                "HEX LSB: <span class='hex-red'>0x" + lsb.toString(16).toUpperCase() + "</span><br><br>" +
                "<b>Real Freq:</b> " + fRealMHz.toFixed(6) + " MHz";
        }
    </script>
</body>
</html>