-- Create CuentaUsuario table
CREATE TABLE CuentaUsuario (
    Numero VARCHAR(50) PRIMARY KEY,
    Saldo NUMERIC NOT NULL,
    NumerosContacto TEXT[] -- Array of strings
);

-- Create Operacion table
CREATE TABLE Operacion (
    ID SERIAL PRIMARY KEY, -- Adding an ID for uniqueness
    Origen VARCHAR(50) REFERENCES CuentaUsuario(Numero) ON DELETE CASCADE,
    Destino VARCHAR(50) REFERENCES CuentaUsuario(Numero) ON DELETE CASCADE,
    Valor NUMERIC NOT NULL,
    Fecha TIMESTAMP NOT NULL
);

-- Example functions to handle operations

-- Function to transfer money from one account to another
CREATE OR REPLACE FUNCTION transferir(origen_numero VARCHAR, destino_numero VARCHAR, valor NUMERIC) RETURNS BOOLEAN AS $$
DECLARE
    origen_saldo NUMERIC;
BEGIN
    -- Check if the origin account has enough balance
    SELECT Saldo INTO origen_saldo FROM CuentaUsuario WHERE Numero = origen_numero;
    IF origen_saldo < valor THEN
        RETURN FALSE; -- Not enough balance
    END IF;

    -- Deduct the amount from the origin account
    UPDATE CuentaUsuario
    SET Saldo = Saldo - valor
    WHERE Numero = origen_numero;

    -- Add the amount to the destination account
    UPDATE CuentaUsuario
    SET Saldo = Saldo + valor
    WHERE Numero = destino_numero;

    -- Insert the operation record
    INSERT INTO Operacion (Origen, Destino, Valor, Fecha)
    VALUES (origen_numero, destino_numero, valor, NOW());

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION historialOperaciones(account_numero VARCHAR) RETURNS TABLE (
    Origen VARCHAR,
    Destino VARCHAR,
    Valor NUMERIC,
    Fecha TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT op.Origen, op.Destino, op.Valor, op.Fecha
    FROM Operacion op
    WHERE op.Origen = account_numero OR op.Destino = account_numero
    ORDER BY op.Fecha DESC;
END;
$$ LANGUAGE plpgsql;

