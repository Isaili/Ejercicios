<?php

$mensaje = "";

if($_SERVER["REQUEST_METHOD"] == "POST"){
    $nombre = $_POST["nombre"];
    $apellido = $_POST['apellido'];
    $edad = $_POST['edad'];
    $direccion = $_POST['direccion'];
  
    $mensaje = "Hola, <strong>$nombre $apellido</strong><br>Su dirección de envío es: <strong>$direccion</strong>.";
}

?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario PHP</title>
    <style>
        
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: rgb(255, 255, 255);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column; 
        }

     
        .banner {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: blueviolet;
            color: white;
            text-align: center;
            padding: 15px;
            font-size: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            z-index: 1000;  
        }
        .banner:hover{
            color:aqua
            
        }

        .hidden {
            display: none;
        }

     
        form {
            background-color: blueviolet;
            width: 300px;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            color: white;
            
        }

        input, button {
            width: 95%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 4px;
            font-size: 16px;
        }

        button {
            height: 40px;
            width: 100%;
            background-color: white;
            color: blueviolet;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover {
            background-color: lightgray;
        }
    </style>
</head>
<body>
    
    <div class="banner <?= empty($mensaje) ? 'hidden' : '' ?>">
        <?= $mensaje ?>
    </div>

   
    <form method="POST">
        <input type="text" name="nombre" placeholder="Nombre" required>
        <input type="text" name="apellido" placeholder="Apellido" required>
        <input type="tel" name="telefono" placeholder="Teléfono" required>
        <input type="number" name="edad" placeholder="Edad" min="18" max="45" required>
        <input type="text" name="direccion" placeholder="Dirección">
        <button type="submit">Enviar</button>
    </form>
</body>
</html>