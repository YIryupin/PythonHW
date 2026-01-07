-- =====================================================================================================
-- ==========================Создание таблицы пользователей TelegramUsers===============================
-- =====================================================================================================
CREATE TABLE IF NOT EXISTS TelegramUsers (
    TelegamId BIGINT NOT NULL, -- Идентификатор пользователя в Telegram
    UserName VARCHAR(100), --Имя пользователя в Telegram
    GameId VARCHAR(20), --Идентификатор игры
    GameSessionId UUID, --Идентификатор игровой сессии
    RegDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, --Дата и время регистрации пользователя
    CONSTRAINT pk_telegramusers PRIMARY KEY (TelegamId)
);

-- Создание уникального индекса для TelegramUsers
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes 
        WHERE tablename = 'telegramusers' 
        AND indexname = 'idx_telegramusers_telegamid'
    ) THEN
        CREATE UNIQUE INDEX idx_telegramusers_telegamid 
        ON TelegramUsers(TelegamId);
    END IF;
END $$;

-- Создание или обновление процедуры CreateOrUpdateUser
-- Создание или обновление пользователя Telegram
CREATE OR REPLACE FUNCTION CreateOrUpdateUser(
    p_TelegramId BIGINT,
    p_UserName VARCHAR(100)
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    -- Используем UPSERT (INSERT ... ON CONFLICT ... DO UPDATE)
    INSERT INTO TelegramUsers (TelegamId, UserName)
    VALUES (p_TelegramId, p_UserName)
    ON CONFLICT (TelegamId) 
    DO UPDATE SET 
        UserName = EXCLUDED.UserName,
        RegDateTime = CASE 
            WHEN TelegramUsers.UserName IS NULL THEN CURRENT_TIMESTAMP
            ELSE TelegramUsers.RegDateTime 
        END;
END;
$$;

-- Создание или обновление процедуры ChangeUserGame
-- Изменение выбранной игры пользователя. Завершает текущую игру если есть и обновляет GameId
CREATE OR REPLACE FUNCTION ChangeUserGame(
    p_TelegramId BIGINT,
    p_GameId VARCHAR(20)
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    v_CurrentGameSessionId UUID;
    v_CurrentGameId VARCHAR(20);
    v_UserExists BOOLEAN;
BEGIN
    -- 1. Запрашиваем текущую запись пользователя
    SELECT GameSessionId, GameId 
    INTO v_CurrentGameSessionId, v_CurrentGameId
    FROM TelegramUsers
    WHERE TelegamId = p_TelegramId;
    
    v_UserExists := FOUND;
    
    -- Если пользователь существует и у него есть активная игра
    IF v_UserExists AND v_CurrentGameSessionId IS NOT NULL AND v_CurrentGameId IS NOT NULL THEN
        -- Вызываем процедуру завершения текущей игры как "Nobody"
        PERFORM UserPlayLogs_GameFinish(p_TelegramId, 'Nobody');
    END IF;
    
    -- 2. Обновляем запись пользователя в TelegramUsers
    IF v_UserExists THEN
        -- Обновляем GameId и очищаем GameSessionId
        UPDATE TelegramUsers 
        SET GameId = p_GameId,
            GameSessionId = NULL
        WHERE TelegamId = p_TelegramId;
    END IF;
END;
$$;

-- Создание или обновление процедуры GetCurrentGame
-- возвращает идентификатор выбранной пользователем игры. 
CREATE OR REPLACE FUNCTION GetCurrentGame(
    p_TelegramId BIGINT
)
RETURNS VARCHAR(20)
LANGUAGE plpgsql
AS $$
DECLARE
    v_GameId VARCHAR(20);
BEGIN
    -- Запрашиваем запись пользователя и получаем GameId
    SELECT GameId INTO v_GameId
    FROM TelegramUsers
    WHERE TelegamId = p_TelegramId;
    
    -- Если запись найдена, возвращаем GameId, иначе NULL
    RETURN v_GameId;
END;
$$;

-- =====================================================================================================
-- =======================================Создание таблицы UserPlayLogs=================================
-- =====================================================================================================
CREATE TABLE IF NOT EXISTS UserPlayLogs (
    TelegamId BIGINT NOT NULL, --Идентификатор пользователя в Telegram
    GameId VARCHAR(20) NOT NULL, --Идентификатор игры
    GameSessionId UUID NOT NULL, --Идентификатор игровой сессии
    GameStatus VARCHAR(9) NOT NULL, --Статус игры, допустимые значения: 'GameStart', 'WinPlayer', 'WinBot', 'Nobody'
    OperDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, --Дата и время операции
    CONSTRAINT pk_userplaylogs PRIMARY KEY (TelegamId, GameSessionId, GameStatus, OperDateTime)
);

-- Создание индекса для UserPlayLogs
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes 
        WHERE tablename = 'userplaylogs' 
        AND indexname = 'idx_userplaylogs_telegamid_gameid'
    ) THEN
        CREATE INDEX idx_userplaylogs_telegamid_gameid 
        ON UserPlayLogs(TelegamId, GameId);
    END IF;
END $$;

-- Создание или обновление процедуры UserPlayLogs_GameStart
-- Начало новой игры. Создает GameSessionId, завершает предыдущую игру если есть, логирует старт, обновляет TelegramUsers
CREATE OR REPLACE FUNCTION UserPlayLogs_GameStart(
    p_TelegramId BIGINT
)
RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_GameSessionId UUID;
    v_CurrentGameSessionId UUID;
    v_CurrentGameId VARCHAR(20);
    v_UserExists BOOLEAN;
BEGIN
    -- 1. Генерируем новый GUID для GameSessionId
    v_GameSessionId := gen_random_uuid();
    
    -- 2. Проверяем существование пользователя и активной игры
    SELECT GameSessionId, GameId 
    INTO v_CurrentGameSessionId, v_CurrentGameId
    FROM TelegramUsers
    WHERE TelegamId = p_TelegramId;
    
    v_UserExists := FOUND;
    
    -- Если пользователь существует и у него есть активная игра
    IF v_UserExists AND v_CurrentGameSessionId IS NOT NULL AND v_CurrentGameId IS NOT NULL THEN
        -- Вызываем процедуру завершения предыдущей игры как "Nobody"
        PERFORM UserPlayLogs_GameFinish(p_TelegramId, 'Nobody');
    END IF;
    
    -- 3. Создаем запись о начале новой игры в UserPlayLogs
    INSERT INTO UserPlayLogs (TelegamId, GameId, GameSessionId, GameStatus)
    VALUES (p_TelegramId, v_CurrentGameId, v_GameSessionId, 'GameStart');
    
    -- 4. Обновляем информацию в таблице TelegramUsers
    IF v_UserExists THEN
        -- Обновляем существующего пользователя
        UPDATE TelegramUsers 
        SET GameSessionId = v_GameSessionId
        WHERE TelegamId = p_TelegramId;
    END IF;
    
    -- Возвращаем созданный GameSessionId
--    RETURN v_GameSessionId;
END;
$$;

-- Создание или обновление процедуры UserPlayLogs_GameFinish
-- Завершение текущей игры пользователя. Логирует результат и очищает информацию об игре в TelegramUsers
CREATE OR REPLACE FUNCTION UserPlayLogs_GameFinish(
    p_TelegramId BIGINT,
    p_GameStatus VARCHAR(9)
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    v_CurrentGameSessionId UUID;
    v_CurrentGameId VARCHAR(20);
BEGIN
    -- Проверяем допустимость статуса
    IF p_GameStatus NOT IN ('WinPlayer', 'WinBot', 'Nobody') THEN
        RAISE EXCEPTION 'Invalid GameStatus. Allowed values: WinPlayer, WinBot, Nobody';
    END IF;
    
    -- 1. Запрашиваем текущую запись пользователя
    SELECT GameSessionId, GameId 
    INTO v_CurrentGameSessionId, v_CurrentGameId
    FROM TelegramUsers
    WHERE TelegamId = p_TelegramId;
    
    -- Если пользователь найден и у него есть активная игра
    IF FOUND AND v_CurrentGameSessionId IS NOT NULL AND v_CurrentGameId IS NOT NULL THEN
        -- Создаем запись о завершении игры в UserPlayLogs
        INSERT INTO UserPlayLogs (TelegamId, GameId, GameSessionId, GameStatus)
        VALUES (p_TelegramId, v_CurrentGameId, v_CurrentGameSessionId, p_GameStatus);
        
        -- 2. Очищаем поля GameId и GameSessionId в TelegramUsers
        UPDATE TelegramUsers 
        SET --GameId = NULL,
            GameSessionId = NULL
        WHERE TelegamId = p_TelegramId;
    END IF;
    -- Если пользователь не найден или нет активной игры - ничего не делаем
END;
$$;

-- Создание или обновление процедуры UserPlayLogs_PlayerStat
-- Получение статистики игрока за указанное количество дней
CREATE OR REPLACE FUNCTION UserPlayLogs_PlayerStats(
    p_TelegramId BIGINT,
    p_DaysCount INT DEFAULT 30
)
RETURNS TABLE (
    Wins INT,
    Losses INT,
    Nobody INT,
    TotalGames INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH game_stats AS (
        SELECT 
            COUNT(CASE WHEN GameStatus = 'WinPlayer' THEN 1 END) AS wins,
            COUNT(CASE WHEN GameStatus = 'WinBot' THEN 1 END) AS losses,
            COUNT(CASE WHEN GameStatus = 'Nobody' THEN 1 END) AS Nobody,
            COUNT(*) AS total_games
        FROM UserPlayLogs
        WHERE TelegamId = p_TelegramId
          AND GameStatus IN ('WinPlayer', 'WinBot', 'Nobody')
          AND OperDateTime >= CURRENT_DATE - (p_DaysCount || ' days')::INTERVAL
    )
    SELECT 
        COALESCE(wins, 0)::INT,
        COALESCE(losses, 0)::INT,
        COALESCE(Nobody, 0)::INT,
        COALESCE(total_games, 0)::INT
    FROM game_stats;
END;
$$;

-- =====================================================================================================
-- =======================================Создание таблицы G21Matches===================================
-- =====================================================================================================
CREATE TABLE IF NOT EXISTS G21Matches (
    TelegamId BIGINT NOT NULL, --Идентификатор пользователя в Telegram
    MatchCounter INT NOT NULL DEFAULT 21, --Текущее количество спичек
    CONSTRAINT pk_g21matches PRIMARY KEY (TelegamId)
);

-- Создание уникального индекса для G21Matches
-- Получение текущего значения счётчика спичек для игры 21 спичка
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes 
        WHERE tablename = 'g21matches' 
        AND indexname = 'idx_g21matches_telegamid_gamesessionid'
    ) THEN
        CREATE UNIQUE INDEX idx_g21matches_telegamid_gamesessionid 
        ON G21Matches(TelegamId);
    END IF;
END $$;
-- Создание или обновление процедуры G21Matches_GetCounter
CREATE OR REPLACE FUNCTION G21Matches_GetCounter(
    p_TelegramId BIGINT
)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE 
	v_MatchCounter INT;
BEGIN
    -- Пытаемся получить существующее значение
    SELECT MatchCounter INTO v_MatchCounter
    FROM G21Matches
    WHERE TelegamId = p_TelegramId;
    
    -- Если запись не найдена
    IF NOT FOUND THEN
        -- Создаем новую запись со значением 21
        INSERT INTO G21Matches (TelegamId, MatchCounter)
        VALUES (p_TelegramId, 21)
        RETURNING MatchCounter INTO v_MatchCounter;
    END IF;
    
    RETURN v_MatchCounter;
END;
$$;

-- Создание или обновление процедуры G21Matches_SetCounter
-- Установка значения счётчика спичек для игры 21 спичка
CREATE OR REPLACE FUNCTION G21Matches_SetCounter(
    p_TelegramId BIGINT,
    p_MatchCounter INT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    -- Проверяем существование записи
    IF EXISTS (
        SELECT 1 FROM G21Matches 
        WHERE TelegamId = p_TelegramId 
    ) THEN
        -- Обновляем существующую запись
        UPDATE G21Matches 
        SET MatchCounter = p_MatchCounter
        WHERE TelegamId = p_TelegramId;
    ELSE
        -- Создаем новую запись
        INSERT INTO G21Matches (TelegamId, MatchCounter)
        VALUES (p_TelegramId, p_MatchCounter);
    END IF;
END;
$$;

