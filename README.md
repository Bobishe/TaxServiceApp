# АИС «Налог‑Учёт»

Автоматизированная информационная система учёта налогоплательщиков и налоговых операций ФНС (курсовой проект, СибГУ им. М. Ф. Решетнёва).

---

## ✨ Возможности

* **Полная «карта» налогоплательщика**: данные о физ/юр‑лице, адрес, контакты  
* Поиск по **ИНН** или **ФИО/названию**  
* Учёт **деклараций** с автосозданием **начислений**  
* Регистрация **платежей** с автоматическим обновлением статусов  
* Расчёт **задолженностей и пеней**  
* Журнал **проверок** и доначислений  
* **Отчёты**: поступления по налогам, списки должников (PDF / Excel)  
* Экспорт / импорт данных (CSV, SQL‑дамп)  
* Ролевая модель доступа: `INSPECTOR`, `ADMIN`

---

## 🛠️ Стек

| Слой | Технологии |
|------|------------|
| Ядро сервера | **Python 3.11**, **FastAPI**, **Uvicorn** |
| ORM / БД | **SQLAlchemy 2 (async)** + **MySQL 8.0** |
| Миграции | **Alembic** |
| Отчёты | **WeasyPrint** (PDF), **OpenPyXL** (Excel) |
| Утилиты | **Pandas**, **python‑dotenv** |

---

## Схема БД
/* ──────────────────────────────────────────────────────────────
   Создание базы и выбор схемы
   ────────────────────────────────────────────────────────────── */
CREATE DATABASE IF NOT EXISTS TaxServiceDB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
USE TaxServiceDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Регионы РФ (справочник)
   ────────────────────────────────────────────────────────────── */
CREATE TABLE Region (
    region_code SMALLINT UNSIGNED PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Виды налогов (справочник)
   ────────────────────────────────────────────────────────────── */
CREATE TABLE TaxType (
    tax_type_id VARCHAR(10) PRIMARY KEY,
    tax_name    VARCHAR(100) NOT NULL,
    description TEXT
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Налогоплательщики
   ────────────────────────────────────────────────────────────── */
CREATE TABLE Taxpayer (
    taxpayer_id CHAR(12) PRIMARY KEY,                     -- ИНН (10/12 цифр)
    type        ENUM('F','U') NOT NULL,                   -- F = физлицо, U = юрлицо

    /* Физическое лицо */
    last_name   VARCHAR(50),
    first_name  VARCHAR(50),
    middle_name VARCHAR(50),
    birth_date  DATE,
    passport_no   VARCHAR(20),
    passport_date DATE,

    /* Юридическое лицо */
    company_name VARCHAR(100),
    ogrn         VARCHAR(15),

    /* Адрес и контакты */
    region_code  SMALLINT UNSIGNED,
    city         VARCHAR(50),
    street       VARCHAR(100),
    house        VARCHAR(10),
    apartment    VARCHAR(10),
    phone        VARCHAR(20),
    email        VARCHAR(50),

    FOREIGN KEY (region_code) REFERENCES Region(region_code)
        ON UPDATE RESTRICT ON DELETE RESTRICT,

    CHECK (taxpayer_id REGEXP '^[0-9]{10,12}$')
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Сотрудники ФНС
   ────────────────────────────────────────────────────────────── */
CREATE TABLE Employee (
    employee_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    position   VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    role       ENUM('INSPECTOR','ADMIN') NOT NULL,
    phone      VARCHAR(20),
    email      VARCHAR(50)
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Налоговые декларации
   ────────────────────────────────────────────────────────────── */
CREATE TABLE TaxDeclaration (
    declaration_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    taxpayer_id  CHAR(12)   NOT NULL,
    tax_type_id  VARCHAR(10) NOT NULL,
    period       YEAR        NOT NULL,
    submission_date DATE     NOT NULL,
    declared_tax_amount DECIMAL(15,2) NOT NULL CHECK (declared_tax_amount >= 0),
    status ENUM('принята','на проверке','выявлены ошибки','утверждена') 
           DEFAULT 'принята',

    CONSTRAINT fk_decl_taxpayer FOREIGN KEY (taxpayer_id)
        REFERENCES Taxpayer(taxpayer_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_decl_taxtype  FOREIGN KEY (tax_type_id)
        REFERENCES TaxType(tax_type_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT unq_decl UNIQUE (taxpayer_id, tax_type_id, period)
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Начисления налогов
   ────────────────────────────────────────────────────────────── */
CREATE TABLE Accrual (
    accrual_id  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    taxpayer_id CHAR(12)    NOT NULL,
    tax_type_id VARCHAR(10) NOT NULL,
    period      YEAR        NOT NULL,
    amount      DECIMAL(15,2) NOT NULL CHECK (amount >= 0),
    paid_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00 CHECK (paid_amount >= 0),
    due_date    DATE        NOT NULL,
    declaration_id INT UNSIGNED,
    status ENUM('начислено','оплачено частично','оплачено','просрочено') 
           DEFAULT 'начислено',

    CONSTRAINT fk_accr_taxpayer FOREIGN KEY (taxpayer_id)
        REFERENCES Taxpayer(taxpayer_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_accr_taxtype FOREIGN KEY (tax_type_id)
        REFERENCES TaxType(tax_type_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_accr_decl    FOREIGN KEY (declaration_id)
        REFERENCES TaxDeclaration(declaration_id)
        ON UPDATE RESTRICT ON DELETE SET NULL,

    INDEX idx_accr_taxpayer (taxpayer_id),
    INDEX idx_accr_due      (due_date),
    INDEX idx_accr_taxpayer_period (taxpayer_id, tax_type_id, period)
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Платежи
   ────────────────────────────────────────────────────────────── */
CREATE TABLE Payment (
    payment_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    taxpayer_id CHAR(12) NOT NULL,
    accrual_id  INT UNSIGNED NOT NULL,
    payment_date DATE NOT NULL,
    amount       DECIMAL(15,2) NOT NULL CHECK (amount > 0),

    CONSTRAINT fk_pay_taxpayer FOREIGN KEY (taxpayer_id)
        REFERENCES Taxpayer(taxpayer_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_pay_accr FOREIGN KEY (accrual_id)
        REFERENCES Accrual(accrual_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,

    INDEX idx_pay_taxpayer (taxpayer_id),
    INDEX idx_pay_accr     (accrual_id)
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Долги и пени
   ────────────────────────────────────────────────────────────── */
CREATE TABLE Debt (
    debt_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    accrual_id INT UNSIGNED NOT NULL UNIQUE,
    principal_amount DECIMAL(15,2) NOT NULL CHECK (principal_amount >= 0),
    penalty_amount   DECIMAL(15,2) NOT NULL DEFAULT 0.00 CHECK (penalty_amount >= 0),
    penalty_date     DATE NOT NULL,
    status ENUM('активно','погашено') DEFAULT 'активно',

    CONSTRAINT fk_debt_accr FOREIGN KEY (accrual_id)
        REFERENCES Accrual(accrual_id)
        ON UPDATE RESTRICT ON DELETE CASCADE
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Налоговые проверки
   ────────────────────────────────────────────────────────────── */
CREATE TABLE Inspection (
    inspection_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    taxpayer_id CHAR(12) NOT NULL,
    employee_id INT UNSIGNED NOT NULL,
    type ENUM('камеральная','выездная') NOT NULL,
    start_date DATE NOT NULL,
    end_date   DATE,
    result        TEXT,
    additional_tax DECIMAL(15,2) DEFAULT 0 CHECK (additional_tax >= 0),
    fine_amount    DECIMAL(15,2) DEFAULT 0 CHECK (fine_amount >= 0),

    CONSTRAINT fk_insp_taxpayer FOREIGN KEY (taxpayer_id)
        REFERENCES Taxpayer(taxpayer_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_insp_employee FOREIGN KEY (employee_id)
        REFERENCES Employee(employee_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,

    INDEX idx_insp_taxpayer (taxpayer_id),
    INDEX idx_insp_employee (employee_id)
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Таблица: Журнал аудита
   ────────────────────────────────────────────────────────────── */
CREATE TABLE AuditLog (
    audit_id   BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    event_time TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_name  VARCHAR(100) NOT NULL,
    action_type ENUM('INSERT','UPDATE','DELETE') NOT NULL,
    table_name VARCHAR(64)  NOT NULL,
    record_id  VARCHAR(64)  NOT NULL,
    old_values TEXT,
    new_values TEXT
) ENGINE = InnoDB;

/* ──────────────────────────────────────────────────────────────
   Триггер: автосоздание начисления после подачи декларации
   ────────────────────────────────────────────────────────────── */
DELIMITER //
CREATE TRIGGER trg_taxdecl_after_insert
AFTER INSERT ON TaxDeclaration
FOR EACH ROW
BEGIN
    INSERT INTO Accrual
        (taxpayer_id, tax_type_id, period, amount, due_date, declaration_id, status)
    VALUES
        (NEW.taxpayer_id,
         NEW.tax_type_id,
         NEW.period,
         NEW.declared_tax_amount,
         DATE_ADD(NEW.submission_date, INTERVAL 90 DAY),
         NEW.declaration_id,
         'начислено');
END //
DELIMITER ;

/* ──────────────────────────────────────────────────────────────
   Триггер: запрет переплаты по начислению
   ────────────────────────────────────────────────────────────── */
DELIMITER //
CREATE TRIGGER trg_payment_before_insert
BEFORE INSERT ON Payment
FOR EACH ROW
BEGIN
    DECLARE already_paid DECIMAL(15,2);
    DECLARE accr_amount  DECIMAL(15,2);

    SELECT paid_amount, amount INTO already_paid, accr_amount
    FROM Accrual
    WHERE accrual_id = NEW.accrual_id;

    IF already_paid + NEW.amount > accr_amount THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Сумма платежа превышает сумму начисления';
    END IF;
END //
DELIMITER ;

/* ──────────────────────────────────────────────────────────────
   Триггер: обновление статуса начисления после платежа
   ────────────────────────────────────────────────────────────── */
DELIMITER //
CREATE TRIGGER trg_payment_after_insert
AFTER INSERT ON Payment
FOR EACH ROW
BEGIN
    UPDATE Accrual
    SET paid_amount = paid_amount + NEW.amount,
        status = CASE
                   WHEN paid_amount + NEW.amount = amount THEN 'оплачено'
                   WHEN paid_amount + NEW.amount < amount THEN 'оплачено частично'
                 END
    WHERE accrual_id = NEW.accrual_id;
END //
DELIMITER ;

/* ──────────────────────────────────────────────────────────────
   Триггер: запрет удаления налогоплательщика
   ────────────────────────────────────────────────────────────── */
DELIMITER //
CREATE TRIGGER trg_taxpayer_before_delete
BEFORE DELETE ON Taxpayer
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Удаление налогоплательщика запрещено';
END //
DELIMITER ;

/* ──────────────────────────────────────────────────────────────
   Триггер: аудит изменений таблицы Accrual
   ────────────────────────────────────────────────────────────── */
DELIMITER //
CREATE TRIGGER trg_accrual_after_update
AFTER UPDATE ON Accrual
FOR EACH ROW
BEGIN
    INSERT INTO AuditLog
        (user_name, action_type, table_name, record_id, old_values, new_values)
    VALUES
        (CURRENT_USER(),
         'UPDATE',
         'Accrual',
         OLD.accrual_id,
         CONCAT_WS('|',
                   'amount=',      OLD.amount,
                   ';paid=',       OLD.paid_amount,
                   ';status=',     OLD.status),
         CONCAT_WS('|',
                   'amount=',      NEW.amount,
                   ';paid=',       NEW.paid_amount,
                   ';status=',     NEW.status));
END //
DELIMITER ;

/* ──────────────────────────────────────────────────────────────
   Ежедневное событие: расчёт пеней по просроченным долгам
   ────────────────────────────────────────────────────────────── */
SET GLOBAL event_scheduler = ON;

DELIMITER //
CREATE EVENT ev_calc_penalties
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP + INTERVAL 1 DAY
DO
BEGIN
    /* Фиксированная ставка ЦБ 7.50 % (пример);
       при необходимости хранить актуальную ставку в отдельной таблице. */
    DECLARE ref_rate DECIMAL(5,2) DEFAULT 7.50;

    UPDATE Debt d
    JOIN Accrual a USING (accrual_id)
       SET d.penalty_amount = d.penalty_amount +
                              ROUND(d.principal_amount * ref_rate / 300, 2),
           d.penalty_date   = CURRENT_DATE()
    WHERE a.due_date < CURRENT_DATE()
      AND d.status = 'активно';
END //
DELIMITER ;

/* ──────────────────────────────────────────────────────────────
   Создание ограниченного пользователя приложения
   ────────────────────────────────────────────────────────────── */
CREATE USER IF NOT EXISTS 'tax_app'@'localhost'
  IDENTIFIED BY 'StrongPass123!';
GRANT SELECT, INSERT, UPDATE ON TaxServiceDB.* TO 'tax_app'@'localhost';
FLUSH PRIVILEGES;


## ⚡ Быстрый старт (Windows 10/11)

> Пример для локальной MySQL 8.0 с пользователем `root/rootpass`.

```powershell
# 1. Клонируем репозиторий
cd TaxServiceApp

# 2. Создаём виртуальное окружение
python -m venv venv
.\venv\Scripts\activate

# 3. Устанавливаем зависимости
pip install -r requirements.txt








