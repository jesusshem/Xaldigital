/*  1. ¿Cuál es el nombre aeropuerto que ha tenido mayor movimiento durante el año? */

SELECT TOP(1) A.NOMBRE_AEROPUERTO
              ,COUNT(V.ID_MOVIMIENTO) AS MOVIMIENTOS
FROM Server.[Tabla de vuelos] AS V
LEFT JOIN Server.[Tabla de aeropuertos] AS A
ON V.ID_AEROPUERTO = A.ID_AEROPUERTO
WHERE V.DIA BETWEEN '2021-01-01' AND '2021-12-31'
GROUP BY A.NOMBRE_AEROPUERTO
ORDER BY MOVIMIENTOS DESC;



/*  2. ¿Cuál es el nombre aerolínea que ha realizado mayor número de vuelos durante el año? */

SELECT TOP(1) AE.NOMBRE_AEROLINEA
             ,COUNT(V.ID_MOVIMIENTO) AS VUELOS
FROM Server.[Tabla de vuelos] AS V
LEFT JOIN Server.[Tabla de aerolíneas] AS AE
ON V.ID_AEROLINEA = AE.ID_AEROLINEA
WHERE V.ID_MOVIMIENTO = 1 AND V.DIA BETWEEN '2021-01-01' AND '2021-12-31' ## Acá estoy tomando como vuelos únicamente las salidas
GROUP BY AE.NOMBRE_AEROLINEA
ORDER BY VUELOS DESC;



/*  3. ¿En qué día se han tenido mayor número de vuelos? */

SELECT TOP(1) DIA
             ,COUNT(ID_MOVIMIENTO) AS VUELOS
FROM Server.[Tabla de vuelos]
WHERE ID_MOVIMIENTO = 1 ## Acá estoy tomando como vuelos únicamente las salidas
GROUP BY DIA
ORDER BY VUELOS DESC;



/*  4. ¿Cuáles son las aerolíneas que tienen mas de 2 vuelos por día? */

SELECT T.DIA
      ,T.NOMBRE_AEROLINEA
      ,T.VUELOS
FROM
(
    SELECT V.DIA
          ,AE.NOMBRE_AEROLINEA
          ,COUNT(V.ID_MOVIMIENTO) AS VUELOS
    FROM Server.[Tabla de vuelos] AS V
    LEFT JOIN Server.[Tabla de aerolíneas] AS AE
    ON V.ID_AEROLINEA = AE.ID_AEROLINEA
    WHERE V.ID_MOVIMIENTO = 1 ## Acá estoy tomando como vuelos únicamente las salidas
    GROUP BY AE.NOMBRE_AEROLINEA
    ) AS T
WHERE T.VUELOS >= 2;