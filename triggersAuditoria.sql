SELECT * FROM Empleados

SELECT * FROM Auditoria

USE [TIENDAENLINEA]
GO
CREATE ROLE [Administrador] AUTHORIZATION [usuarioana]
GO

USE TIENDAENLINEA; -- Cambia "TuBaseDeDatos" al nombre de tu base de datos
ALTER ROLE db_owner ADD MEMBER [Edgar]; -- Reemplaza "[NombreUsuario]" con el nombre del usuario

USE TIENDAENLINEA;
CREATE ROLE MiRolAdministrador;

GRANT SELECT, INSERT, UPDATE, DELETE TO MiRolAdministrador;

USE TIENDAENLINEA; -- Cambia "TuBaseDeDatos" al nombre de tu base de datos
CREATE ROLE RolProductos;

GRANT SELECT, UPDATE, DELETE ON dbo.Productos TO RolProductos;
GRANT SELECT, UPDATE, DELETE ON dbo.Categorias TO RolProductos;
GRANT SELECT, UPDATE, DELETE ON dbo.SubCategorias TO RolProductos;

USE TIENDAENLINEA; -- Cambia "TuBaseDeDatos" al nombre de tu base de datos
ALTER ROLE RolProductos ADD MEMBER [Mario]; -- Reemplaza "[NombreUsuario]" con el nombre del usuario

CREATE TRIGGER trg_Audit_Facturas -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.Facturas -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones INSERT
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'INSERT', -- Tipo de evento
            'Facturas', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            NULL, -- No hay valor antiguo para INSERT
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted;
    END

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'Facturas', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'Facturas', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO

CREATE TRIGGER trg_Audit_Clientes -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.Clientes -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones INSERT
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'INSERT', -- Tipo de evento
            'Clientes', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            NULL, -- No hay valor antiguo para INSERT
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted;
    END

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'Clientes', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'Clientes', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO

CREATE TRIGGER trg_Audit_Categorias -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.Categorias -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones INSERT
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'INSERT', -- Tipo de evento
            'Categorias', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            NULL, -- No hay valor antiguo para INSERT
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted;
    END

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'Categorias', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'Categorias', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO

CREATE TRIGGER trg_Audit_SubCategorias -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.SubCategorias -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones INSERT
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'INSERT', -- Tipo de evento
            'SubCategorias', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            NULL, -- No hay valor antiguo para INSERT
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted;
    END

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'SubCategorias', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'SubCategorias', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO


CREATE TRIGGER trg_Audit_Productos -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.Productos -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones INSERT
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'INSERT', -- Tipo de evento
            'Productos', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            NULL, -- No hay valor antiguo para INSERT
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted;
    END

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'Productos', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'Productos', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO


CREATE TRIGGER trg_Audit_DetallesVentas -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.DetallesVenta -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'DetallesVenta', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'DetallesVenta', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO


CREATE TRIGGER trg_Audit_DetallesCarrito -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.DetallesCarrito -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'DetallesCarrito', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'DetallesCarrito', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO


CREATE TRIGGER trg_Audit_Pedidos -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.Pedidos -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones INSERT
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'INSERT', -- Tipo de evento
            'Pedidos', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            NULL, -- No hay valor antiguo para INSERT
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted;
    END

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'Pedidos', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'Pedidos', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO

CREATE TRIGGER trg_Audit_Compras -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.Compras -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones INSERT
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'INSERT', -- Tipo de evento
            'Compras', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            NULL, -- No hay valor antiguo para INSERT
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted;
    END

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'Compras', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'Compras', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO

CREATE TRIGGER trg_Audit_Proveedores -- Cambia 'TuTabla' por el nombre de tu tabla
ON dbo.Proveedores -- Cambia 'TuTabla' por el nombre de tu tabla y 'dbo' por tu esquema si es necesario
FOR INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Para operaciones INSERT
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'INSERT', -- Tipo de evento
            'Proveedores', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            NULL, -- No hay valor antiguo para INSERT
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted;
    END

    -- Para operaciones DELETE
    IF EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'DELETE', -- Tipo de evento
            'Proveedoress', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            NULL -- No hay valor nuevo para DELETE
        FROM deleted;
    END

    -- Para operaciones UPDATE
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
    BEGIN
        INSERT INTO dbo.Auditoria (EventType, ObjectName, ObjectSchema, ExecutedBy, OldValue, NewValue)
        SELECT
            'UPDATE', -- Tipo de evento
            'Proveedores', -- Cambia 'TuTabla' por el nombre de tu tabla
            'dbo', -- Cambia 'dbo' por el esquema de tu tabla si es necesario
            SUSER_SNAME(), -- Usuario que ejecutó el cambio
            (SELECT * FROM deleted d FOR JSON PATH), -- Valores antiguos
            (SELECT * FROM inserted i FOR JSON PATH) -- Valores nuevos
        FROM inserted, deleted;
    END
END;
GO

USE TIENDAENLINEA -- Reemplaza con el nombre de tu base de datos
GO

EXEC sys.sp_cdc_enable_db;
GO

EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo', -- Reemplaza con el esquema de tu tabla
    @source_name = N'Empleados', -- Reemplaza con el nombre de tu tabla
    @role_name = NULL;
GO

SELECT * FROM Auditoria
WHERE DATEPART(hour, ExecutionDate) NOT BETWEEN 9 AND 18
  AND DATEPART(dw, ExecutionDate) NOT IN (1, 7); -- 1: Sunday, 7: Saturday

CREATE TRIGGER trg_Audit_OffHours
ON [dbo].[Auditoria]
AFTER INSERT
AS
BEGIN
    DECLARE @subject NVARCHAR(255), @body NVARCHAR(MAX)

    IF EXISTS (
        SELECT 1 FROM inserted
        WHERE DATEPART(hour, ExecutionDate) NOT BETWEEN 9 AND 16
          AND DATEPART(dw, ExecutionDate) NOT IN (1, 7)
    )
    BEGIN
        SET @subject = 'Alerta: Acceso Fuera del Horario Laboral'
        SET @body = 'Se ha detectado un acceso fuera del horario laboral. Revise los detalles en la tabla de auditoría.'

        EXEC dbo.usp_SendAuditAlert @subject, @body
    END
END

CREATE TRIGGER trg_Audit_MassChanges
ON [dbo].[Auditoria]
AFTER INSERT
AS
BEGIN
    DECLARE @subject NVARCHAR(255), @body NVARCHAR(MAX)

    IF EXISTS (
        SELECT ExecutedBy, COUNT(*) AS NumberOfChanges
        FROM Auditoria
        WHERE EventType IN ('UPDATE', 'DELETE')
          AND ExecutionDate >= DATEADD(hour, -1, GETDATE())
        GROUP BY ExecutedBy, ObjectName, ObjectSchema
        HAVING COUNT(*) > 5
    )
    BEGIN
        SET @subject = 'Alerta: Modificaciones Masivas de Datos'
        SET @body = 'Se han detectado modificaciones masivas de datos. Revise los detalles en la tabla de auditoría.'

        EXEC dbo.usp_SendAuditAlert @subject, @body
    END
END


